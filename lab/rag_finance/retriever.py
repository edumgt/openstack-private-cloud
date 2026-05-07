"""TF-IDF 기반 금융 문서 검색기."""

# 최신 타입 표기 문법을 일관되게 사용하기 위한 선언이다.
from __future__ import annotations

# 로그/제곱근 계산 등 수학 연산에 사용한다.
import math
# 정규식 기반 토큰 분리를 위해 사용한다.
import re
# 용어 빈도 집계를 위해 Counter/defaultdict를 사용한다.
from collections import Counter, defaultdict

# 문서 구조체와 문서 텍스트 생성 유틸을 가져온다.
from .data_loader import FinanceDocument, iter_document_texts

# 영문/숫자/한글만 토큰으로 취급하기 위한 정규식 패턴이다.
TOKEN_PATTERN = re.compile(r"[0-9A-Za-z가-힣]+")


def tokenize(text: str) -> list[str]:
    """영문/숫자/한글 토큰으로 분리한다."""
    # 추출한 토큰을 모두 소문자로 정규화해 검색 일관성을 높인다.
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


class TfidfRetriever:
    """간단한 TF-IDF 검색기."""

    def __init__(self, documents: list[FinanceDocument]) -> None:
        # 문서 ID를 키로 하는 사전을 구성해 빠른 조회를 지원한다.
        self._documents = {doc.doc_id: doc for doc in documents}
        # 전체 용어 집합(어휘)을 저장한다.
        self._vocabulary: set[str] = set()
        # 문서별 용어 빈도(Counter)를 저장한다.
        self._doc_term_counts: dict[str, Counter[str]] = {}
        # 용어별 IDF 값을 저장한다.
        self._idf: dict[str, float] = {}
        # 문서별 TF-IDF 벡터를 저장한다.
        self._vectors: dict[str, dict[str, float]] = {}
        # 문서 벡터의 L2 노름(정규화 분모)을 저장한다.
        self._doc_norm: dict[str, float] = {}
        # 초기화 시점에 즉시 인덱스를 구축한다.
        self._build_index()

    def _build_index(self) -> None:
        # 용어가 몇 개 문서에 등장했는지(문서 빈도) 집계용 맵이다.
        doc_frequency: defaultdict[str, int] = defaultdict(int)

        # 문서별 결합 텍스트를 순회하며 토큰/빈도를 계산한다.
        for doc_id, text in iter_document_texts(self._documents.values()):
            # 텍스트를 토큰 시퀀스로 변환한다.
            tokens = tokenize(text)
            # 문서 내 용어 출현 횟수를 계산한다.
            term_counts = Counter(tokens)
            # 이후 TF 계산을 위해 문서별 빈도를 저장한다.
            self._doc_term_counts[doc_id] = term_counts
            # 해당 문서에서 등장한 고유 용어를 순회한다.
            for term in term_counts:
                # 용어 문서 빈도를 1 증가시킨다.
                doc_frequency[term] += 1
                # 어휘 집합에 용어를 등록한다.
                self._vocabulary.add(term)

        # 문서가 0개여도 0 나눗셈을 피하도록 최소 1로 보정한다.
        doc_count = max(len(self._documents), 1)
        # 스무딩된 IDF 공식을 사용해 용어별 가중치를 계산한다.
        self._idf = {
            term: math.log((doc_count + 1) / (frequency + 1)) + 1.0
            for term, frequency in doc_frequency.items()
        }

        # 문서별 TF-IDF 벡터와 노름을 계산한다.
        for doc_id, term_counts in self._doc_term_counts.items():
            # 현재 문서 벡터를 담을 딕셔너리다.
            vector: dict[str, float] = {}
            # 서브리니어 대체로 최대 TF 정규화를 사용한다.
            max_tf = max(term_counts.values(), default=1)
            # 문서에 등장한 모든 용어를 순회한다.
            for term, count in term_counts.items():
                # 최대 빈도로 나눠 0~1 범위의 정규화 TF를 만든다.
                tf = count / max_tf
                # TF와 IDF를 곱해 최종 가중치를 저장한다.
                vector[term] = tf * self._idf.get(term, 0.0)
            # 완성된 문서 벡터를 저장한다.
            self._vectors[doc_id] = vector
            # 코사인 유사도 분모 계산을 위해 L2 노름을 저장한다.
            self._doc_norm[doc_id] = math.sqrt(
                sum(weight**2 for weight in vector.values())
            )

    def search(
        self, query: str, top_k: int = 3
    ) -> list[tuple[FinanceDocument, float]]:
        """질의와 가장 유사한 문서를 반환한다."""
        # top_k는 최소 1 이상이어야 하므로 방어적으로 검증한다.
        if top_k < 1:
            raise ValueError("top_k must be >= 1")

        # 질의를 토큰화하고 용어 빈도를 계산한다.
        query_terms = Counter(tokenize(query))
        # 질의 토큰이 없으면 점수 계산 없이 빈 결과를 반환한다.
        if not query_terms:
            return []

        # 질의 TF 정규화를 위한 최대 빈도 값을 구한다.
        max_tf = max(query_terms.values())
        # 인덱스 어휘에 존재하는 용어만 사용해 질의 벡터를 만든다.
        query_vector = {
            term: (count / max_tf) * self._idf.get(term, 0.0)
            for term, count in query_terms.items()
            if term in self._vocabulary
        }
        # 질의 벡터의 L2 노름을 계산한다.
        query_norm = math.sqrt(
            sum(weight**2 for weight in query_vector.values())
        )
        # 질의 벡터가 영벡터면 유사도 계산이 불가능하므로 종료한다.
        if query_norm == 0:
            return []

        # (문서, 점수) 결과를 누적할 리스트다.
        scored: list[tuple[FinanceDocument, float]] = []
        # 인덱스된 모든 문서 벡터를 순회한다.
        for doc_id, vector in self._vectors.items():
            # 질의-문서 내적(코사인 유사도 분자)을 계산한다.
            numerator = sum(
                query_vector.get(term, 0.0) * vector.get(term, 0.0)
                for term in query_vector
            )
            # 질의 노름과 문서 노름 곱으로 분모를 계산한다.
            denominator = query_norm * self._doc_norm.get(doc_id, 0.0)
            # 분모가 0이면 유효 점수를 계산할 수 없어 건너뛴다.
            if denominator == 0:
                continue
            # 코사인 유사도 점수를 계산한다.
            score = numerator / denominator
            # 양의 유사도만 결과에 포함한다.
            if score > 0:
                scored.append((self._documents[doc_id], score))

        # 점수 내림차순으로 정렬해 상위 문서를 우선 배치한다.
        scored.sort(key=lambda item: item[1], reverse=True)
        # 요청한 개수(top_k)만 잘라 반환한다.
        return scored[:top_k]
