"""금융공학 RAG 실습 파이프라인."""

# 최신 타입 힌트 문법을 안정적으로 사용하기 위한 선언이다.
from __future__ import annotations

# 검색 결과 단위를 불변 데이터 클래스로 정의하기 위해 사용한다.
from dataclasses import dataclass
# 문자열 경로와 Path 입력을 모두 허용하기 위해 사용한다.
from pathlib import Path

# 데이터 로딩 함수와 문서 타입을 가져온다.
from .data_loader import FinanceDocument, load_finance_documents
# TF-IDF 검색기 구현을 가져온다.
from .retriever import TfidfRetriever


# 검색 결과를 명확하게 표현하는 불변 구조체다.
@dataclass(frozen=True)
class RetrievedEvidence:
    """검색 결과 단위."""

    # 검색으로 선택된 원본 문서다.
    doc: FinanceDocument
    # 질의와 문서의 유사도 점수다.
    score: float


class FinanceRAGPipeline:
    """검색 증거 기반 답변 초안 생성 파이프라인."""

    def __init__(self, dataset_path: str | Path) -> None:
        # 지정된 데이터셋 경로에서 문서 목록을 불러온다.
        documents = load_finance_documents(dataset_path)
        # 로드된 문서들로 검색 인덱스를 초기화한다.
        self._retriever = TfidfRetriever(documents)

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedEvidence]:
        """질의와 관련된 근거 문서를 조회한다."""
        # 검색 결과를 파이프라인 전용 결과 타입으로 변환해 반환한다.
        return [
            RetrievedEvidence(doc=result[0], score=result[1])
            for result in self._retriever.search(query, top_k=top_k)
        ]

    def draft_answer(self, query: str, top_k: int = 3) -> str:
        """질의에 대한 근거 기반 답변 초안을 생성한다."""
        # 먼저 질의와 관련된 근거 문서를 조회한다.
        evidences = self.retrieve(query, top_k=top_k)
        # 근거가 없으면 사용자에게 재질의/데이터 보강을 안내한다.
        if not evidences:
            return (
                "관련 문서를 찾지 못했습니다. 질의를 더 구체화하거나 "
                "데이터셋에 금융 문서를 추가해 주세요."
            )

        # 출력 본문을 줄 단위로 누적하기 위한 버퍼를 초기화한다.
        lines = [
            f"[질문] {query}",
            "",
            "[핵심 답변 초안]",
            "아래 근거 문서를 기준으로 리스크 요인과 대응 전략을 검토해야 합니다.",
            "",
            "[근거 문서]",
        ]
        # 근거 문서를 순서대로 렌더링한다.
        for index, evidence in enumerate(evidences, start=1):
            # 가독성을 위해 지역 변수로 문서를 꺼낸다.
            doc = evidence.doc
            # 문서 메타데이터와 점수를 한 줄로 정리해 추가한다.
            lines.append(
                (
                    f"{index}. ({evidence.score:.3f}) {doc.title} "
                    f"[{doc.category}] - tags={','.join(doc.tags)}"
                )
            )
            # 문서 핵심 내용을 요약 라인으로 추가한다.
            lines.append(f"   요약: {doc.content}")

        # 문단 구분을 위해 빈 줄을 추가한다.
        lines.append("")
        # 학습용 결과라는 면책 문구를 마지막에 덧붙인다.
        lines.append(
            "[주의] 본 초안은 학습용 결과이며, 실제 투자/헤지 의사결정 전 "
            "전문가 검토가 필요합니다."
        )
        # 누적한 줄을 개행으로 합쳐 최종 문자열로 반환한다.
        return "\n".join(lines)
