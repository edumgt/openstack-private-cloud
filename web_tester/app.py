from __future__ import annotations

import importlib.util
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from lab.rag_finance.pipeline import FinanceRAGPipeline
from scripts import mock_openstack_api

APP_ROOT = Path(__file__).resolve().parent
REPO_ROOT = APP_ROOT.parent
STATIC_DIR = APP_ROOT / "static"
INDEX_HTML = STATIC_DIR / "index.html"
DEFAULT_RAG_DATASET = (
    REPO_ROOT / "lab" / "rag_finance" / "data" / "sample_finance_docs.jsonl"
)
RAG_DATASET_MAP = {"sample_finance_docs": DEFAULT_RAG_DATASET}
MAX_PIPELINE_CACHE_SIZE = 8

PY_SOURCE_FILES = [
    "lab/rag_finance/__init__.py",
    "lab/rag_finance/cli.py",
    "lab/rag_finance/data_loader.py",
    "lab/rag_finance/pipeline.py",
    "lab/rag_finance/retriever.py",
    "scripts/mock_openstack_api.py",
    "ansible/files/docker_bench_to_html.py",
    "archive/legacy/scripts/render_captures.py",
]
PY_SOURCE_MAP = {source: REPO_ROOT / source for source in PY_SOURCE_FILES}

app = FastAPI(
    title="openstack-private-cloud python web tester",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class SmokeTestRequest(BaseModel):
    targets: list[str] | None = Field(
        default=None,
        description="상대 경로 목록. 미지정 시 전체 Python 소스 검사",
    )


class RagQueryRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1)
    dataset: str | None = Field(
        default="sample_finance_docs",
        description="허용된 데이터셋 키 (기본값: sample_finance_docs)",
    )


def _load_module(path: Path) -> tuple[bool, str | None]:
    spec = importlib.util.spec_from_file_location(
        f"web_tester_dynamic_{path.stem}", str(path)
    )
    if spec is None or spec.loader is None:
        return False, "spec loader 생성 실패"
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001
        return False, f"{path.name}: {type(exc).__name__}"
    return True, None


def _resolve_dataset_path(dataset_key: str | None) -> Path:
    selected_key = dataset_key or "sample_finance_docs"
    if selected_key not in RAG_DATASET_MAP:
        raise HTTPException(status_code=400, detail="지원하지 않는 dataset 키입니다.")
    resolved = RAG_DATASET_MAP[selected_key].resolve()
    if not resolved.exists():
        raise HTTPException(status_code=404, detail="dataset 파일이 존재하지 않습니다.")
    return resolved


@lru_cache(maxsize=MAX_PIPELINE_CACHE_SIZE)
def _get_pipeline(dataset_path: str) -> FinanceRAGPipeline:
    """동일 데이터셋 요청에 대해 파이프라인 재생성을 줄이기 위한 캐시."""
    return FinanceRAGPipeline(dataset_path=dataset_path)


def _token_doc() -> dict[str, Any]:
    return mock_openstack_api.token_doc(
        host="127.0.0.1", keystone_port=5000, nova_port=8774
    )


@app.get("/", response_class=FileResponse)
def index() -> FileResponse:
    return FileResponse(str(INDEX_HTML))


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/python/sources")
def list_python_sources() -> dict[str, Any]:
    return {"count": len(PY_SOURCE_FILES), "items": PY_SOURCE_FILES}


@app.post("/api/python/smoke-test")
def smoke_test(request: SmokeTestRequest) -> dict[str, Any]:
    targets = request.targets or PY_SOURCE_FILES
    unknown_targets = sorted(set(targets) - set(PY_SOURCE_MAP))
    if unknown_targets:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 target: {', '.join(unknown_targets)}",
        )

    results: list[dict[str, Any]] = []
    for target in targets:
        full_path = PY_SOURCE_MAP[target]
        if not full_path.exists():
            results.append(
                {
                    "path": target,
                    "ok": False,
                    "error": "파일이 존재하지 않습니다.",
                }
            )
            continue

        ok, error = _load_module(full_path)
        results.append({"path": target, "ok": ok, "error": error})

    success_count = len([result for result in results if result["ok"]])
    return {
        "total": len(results),
        "success": success_count,
        "failed": len(results) - success_count,
        "results": results,
    }


@app.post("/api/rag/query")
def rag_query(request: RagQueryRequest) -> dict[str, Any]:
    dataset_path = _resolve_dataset_path(request.dataset)
    pipeline = _get_pipeline(str(dataset_path))
    evidence = pipeline.retrieve(query=request.query, top_k=request.top_k)
    return {
        "query": request.query,
        "top_k": request.top_k,
        "dataset": str(dataset_path),
        "draft_answer": pipeline.draft_answer(
            query=request.query, top_k=request.top_k
        ),
        "evidence": [
            {
                "score": item.score,
                "doc_id": item.doc.doc_id,
                "title": item.doc.title,
                "category": item.doc.category,
                "tags": item.doc.tags,
            }
            for item in evidence
        ],
    }


@app.get("/api/mock-openstack/overview")
def mock_openstack_overview() -> dict[str, Any]:
    return {
        "keystone_version": mock_openstack_api.keystone_version_doc("127.0.0.1", 5000),
        "nova_services": mock_openstack_api.nova_services_doc(),
        "servers": mock_openstack_api.nova_servers_doc(),
        "networks": mock_openstack_api.neutron_networks_doc(),
        "subnets": mock_openstack_api.neutron_subnets_doc(),
        "volumes": mock_openstack_api.cinder_volumes_doc(),
    }


@app.get("/api/mock-openstack/dashboard-html")
def mock_openstack_dashboard_html() -> dict[str, str]:
    return {"html": mock_openstack_api.dashboard_html()}


@app.get("/api/mock-openstack/token-doc")
def mock_openstack_token_doc() -> dict[str, Any]:
    return _token_doc()


@app.get("/api/mock-openstack/pretty-token-doc")
def mock_openstack_pretty_token_doc() -> dict[str, str]:
    return {
        "token_doc_json": json.dumps(
            _token_doc(),
            ensure_ascii=False,
            indent=2,
        )
    }
