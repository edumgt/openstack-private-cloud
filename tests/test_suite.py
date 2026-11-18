from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from lab.rag_finance.data_loader import load_finance_documents
from lab.rag_finance.pipeline import FinanceRAGPipeline
from lab.rag_finance.retriever import HybridRetriever, TfidfRetriever, tokenize
from scripts import mock_openstack_api
from web_tester.app import app

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = REPO_ROOT / "lab" / "rag_finance" / "data" / "sample_finance_docs.jsonl"


def test_load_finance_documents() -> None:
    docs = load_finance_documents(DATASET_PATH)
    assert len(docs) >= 8
    doc_ids = {d.doc_id for d in docs}
    assert {"D001", "D006", "D008"}.issubset(doc_ids)


def test_hybrid_retriever_ranking() -> None:
    docs = load_finance_documents(DATASET_PATH)
    retriever = TfidfRetriever(docs)
    assert isinstance(retriever, HybridRetriever)

    results = retriever.search("금리 상승기 듀레이션 리스크 스왑 헤지", top_k=3)
    assert len(results) >= 1
    assert results[0][0].doc_id == "D001"
    assert results[0][1] > 0.0

    tokens = tokenize("듀레이션과 변동성")
    assert "듀레이션과" in tokens
    assert "_듀레" in tokens


def test_finance_rag_pipeline_draft_answer() -> None:
    pipeline = FinanceRAGPipeline(DATASET_PATH)
    answer = pipeline.draft_answer("Expected Shortfall VaR 바젤3 리스크", top_k=2)
    assert "[질문]" in answer
    assert "[근거 문서]" in answer
    assert "D006" in answer or "Expected Shortfall" in answer


def test_mock_openstack_api_docs() -> None:
    keystone = mock_openstack_api.keystone_version_doc("127.0.0.1", 5000)
    assert keystone["version"]["id"] == "v3.14"

    servers = mock_openstack_api.nova_servers_doc()
    assert len(servers["servers"]) == 2
    assert {s["name"] for s in servers["servers"]} == {"compute1", "compute2"}

    filtered = mock_openstack_api.nova_servers_doc(name="compute1")
    assert len(filtered["servers"]) == 1
    assert filtered["servers"][0]["name"] == "compute1"

    html = mock_openstack_api.dashboard_html()
    assert "OpenStack Horizon Mock" in html
    assert "compute1" in html


def test_web_tester_endpoints() -> None:
    client = TestClient(app)

    health_resp = client.get("/api/health")
    assert health_resp.status_code == 200
    assert health_resp.json() == {"status": "ok"}

    smoke_resp = client.post("/api/python/smoke-test", json={})
    assert smoke_resp.status_code == 200
    smoke_data = smoke_resp.json()
    assert smoke_data["failed"] == 0
    assert smoke_data["success"] == smoke_data["total"]

    rag_resp = client.post(
        "/api/rag/query",
        json={"query": "금리 상승기에 듀레이션 리스크를 어떻게 관리하나요?", "top_k": 3},
    )
    assert rag_resp.status_code == 200
    rag_data = rag_resp.json()
    assert len(rag_data["evidence"]) == 3
    assert rag_data["evidence"][0]["doc_id"] == "D001"

    os_resp = client.get("/api/mock-openstack/overview")
    assert os_resp.status_code == 200
    os_data = os_resp.json()
    assert len(os_data["servers"]["servers"]) == 2

    curr_resp = client.get("/api/curriculum/overview")
    assert curr_resp.status_code == 200
    curr_data = curr_resp.json()
    assert curr_data["total_lectures"] == 24
