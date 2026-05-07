"""금융공학 RAG 실습 파이프라인."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .data_loader import FinanceDocument, load_finance_documents
from .retriever import TfidfRetriever


@dataclass(frozen=True)
class RetrievedEvidence:
    """검색 결과 단위."""

    doc: FinanceDocument
    score: float


class FinanceRAGPipeline:
    """검색 증거 기반 답변 초안 생성 파이프라인."""

    def __init__(self, dataset_path: str | Path) -> None:
        documents = load_finance_documents(dataset_path)
        self._retriever = TfidfRetriever(documents)

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedEvidence]:
        """질의와 관련된 근거 문서를 조회한다."""
        return [
            RetrievedEvidence(doc=result[0], score=result[1])
            for result in self._retriever.search(query, top_k=top_k)
        ]

    def draft_answer(self, query: str, top_k: int = 3) -> str:
        """질의에 대한 근거 기반 답변 초안을 생성한다."""
        evidences = self.retrieve(query, top_k=top_k)
        if not evidences:
            return (
                "관련 문서를 찾지 못했습니다. 질의를 더 구체화하거나 "
                "데이터셋에 금융 문서를 추가해 주세요."
            )

        lines = [
            f"[질문] {query}",
            "",
            "[핵심 답변 초안]",
            "아래 근거 문서를 기준으로 리스크 요인과 대응 전략을 검토해야 합니다.",
            "",
            "[근거 문서]",
        ]
        for index, evidence in enumerate(evidences, start=1):
            doc = evidence.doc
            lines.append(
                (
                    f"{index}. ({evidence.score:.3f}) {doc.title} "
                    f"[{doc.category}] - tags={','.join(doc.tags)}"
                )
            )
            lines.append(f"   요약: {doc.content}")

        lines.append("")
        lines.append(
            "[주의] 본 초안은 학습용 결과이며, 실제 투자/헤지 의사결정 전 "
            "전문가 검토가 필요합니다."
        )
        return "\n".join(lines)
