"""금융공학 RAG 실습용 문서 로더."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class FinanceDocument:
    """RAG 검색 대상 문서."""

    doc_id: str
    title: str
    category: str
    content: str
    tags: list[str]


def load_finance_documents(dataset_path: str | Path) -> list[FinanceDocument]:
    """JSONL 파일에서 금융 문서를 로딩한다."""
    path = Path(dataset_path)
    documents: list[FinanceDocument] = []

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            payload = json.loads(line)
            documents.append(
                FinanceDocument(
                    doc_id=str(payload["doc_id"]),
                    title=str(payload["title"]),
                    category=str(payload["category"]),
                    content=str(payload["content"]),
                    tags=list(payload.get("tags", [])),
                )
            )
    return documents


def iter_document_texts(
    documents: Iterable[FinanceDocument],
) -> Iterable[tuple[str, str]]:
    """문서별 결합 텍스트를 생성한다."""
    for doc in documents:
        combined = " ".join([doc.title, doc.category, doc.content, " ".join(doc.tags)])
        yield doc.doc_id, combined
