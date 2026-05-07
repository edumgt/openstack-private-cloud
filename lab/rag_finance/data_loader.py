"""금융공학 RAG 실습용 문서 로더."""

# 미래 문법(예: `|` 유니온 타입)을 안정적으로 사용하기 위한 선언이다.
from __future__ import annotations

# JSONL 한 줄씩을 파싱하기 위해 표준 json 모듈을 사용한다.
import json
# 불변 데이터 모델(FinanceDocument)을 선언하기 위해 dataclass를 가져온다.
from dataclasses import dataclass
# 문자열/Path 입력을 모두 다루기 위해 Path 클래스를 사용한다.
from pathlib import Path
# 제너레이터 타입 힌트를 위해 Iterable을 사용한다.
from typing import Iterable


# 문서 객체는 생성 후 값이 변하지 않도록 frozen dataclass로 정의한다.
@dataclass(frozen=True)
class FinanceDocument:
    """RAG 검색 대상 문서."""

    # 문서 고유 식별자다.
    doc_id: str
    # 사람이 읽을 수 있는 문서 제목이다.
    title: str
    # 문서 분류(예: 채권, 리스크 관리)다.
    category: str
    # 문서 본문 내용이다.
    content: str
    # 검색 보조 키워드 목록이다.
    tags: list[str]


def load_finance_documents(dataset_path: str | Path) -> list[FinanceDocument]:
    """JSONL 파일에서 금융 문서를 로딩한다."""
    # 입력 경로를 Path 객체로 표준화한다.
    path = Path(dataset_path)
    # 파싱한 문서 객체를 담을 리스트를 준비한다.
    documents: list[FinanceDocument] = []

    # UTF-8 인코딩으로 JSONL 파일을 읽는다.
    with path.open("r", encoding="utf-8") as handle:
        # JSONL은 줄 단위 레코드 구조이므로 한 줄씩 순회한다.
        for line in handle:
            # 좌우 공백/개행을 제거해 빈 줄 여부를 정확히 판정한다.
            line = line.strip()
            # 빈 줄은 유효한 JSON 레코드가 아니므로 건너뛴다.
            if not line:
                continue
            # 각 줄을 JSON 객체(dict)로 파싱한다.
            payload = json.loads(line)
            # 파싱 결과를 강타입 문서 객체로 변환해 리스트에 추가한다.
            documents.append(
                FinanceDocument(
                    # 식별자는 문자열로 강제 변환해 타입 일관성을 지킨다.
                    doc_id=str(payload["doc_id"]),
                    # 제목 필드를 문자열로 변환해 안전하게 저장한다.
                    title=str(payload["title"]),
                    # 카테고리 필드를 문자열로 변환한다.
                    category=str(payload["category"]),
                    # 본문 필드를 문자열로 변환한다.
                    content=str(payload["content"]),
                    # 태그가 없을 경우 빈 리스트를 기본값으로 사용한다.
                    tags=list(payload.get("tags", [])),
                )
            )
    # 완성된 문서 목록을 호출자에게 반환한다.
    return documents


def iter_document_texts(
    documents: Iterable[FinanceDocument],
) -> Iterable[tuple[str, str]]:
    """문서별 결합 텍스트를 생성한다."""
    # 입력 문서 스트림을 순회하며 검색용 텍스트를 만든다.
    for doc in documents:
        # 제목/카테고리/본문/태그를 하나의 문자열로 합쳐 검색 품질을 높인다.
        combined = " ".join(
            [doc.title, doc.category, doc.content, " ".join(doc.tags)]
        )
        # (문서 ID, 결합 텍스트) 튜플을 순차적으로 내보낸다.
        yield doc.doc_id, combined
