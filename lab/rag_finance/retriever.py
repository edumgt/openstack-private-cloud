"""TF-IDF 기반 금융 문서 검색기."""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

from .data_loader import FinanceDocument, iter_document_texts

TOKEN_PATTERN = re.compile(r"[0-9A-Za-z가-힣]+")


def tokenize(text: str) -> list[str]:
    """영문/숫자/한글 토큰으로 분리한다."""
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


class TfidfRetriever:
    """간단한 TF-IDF 검색기."""

    def __init__(self, documents: list[FinanceDocument]) -> None:
        self._documents = {doc.doc_id: doc for doc in documents}
        self._vocabulary: set[str] = set()
        self._doc_term_counts: dict[str, Counter[str]] = {}
        self._idf: dict[str, float] = {}
        self._vectors: dict[str, dict[str, float]] = {}
        self._doc_norm: dict[str, float] = {}
        self._build_index()

    def _build_index(self) -> None:
        doc_frequency: defaultdict[str, int] = defaultdict(int)

        for doc_id, text in iter_document_texts(self._documents.values()):
            tokens = tokenize(text)
            term_counts = Counter(tokens)
            self._doc_term_counts[doc_id] = term_counts
            for term in term_counts:
                doc_frequency[term] += 1
                self._vocabulary.add(term)

        doc_count = max(len(self._documents), 1)
        self._idf = {
            term: math.log((doc_count + 1) / (frequency + 1)) + 1.0
            for term, frequency in doc_frequency.items()
        }

        for doc_id, term_counts in self._doc_term_counts.items():
            vector: dict[str, float] = {}
            max_tf = max(term_counts.values(), default=1)
            for term, count in term_counts.items():
                tf = count / max_tf
                vector[term] = tf * self._idf.get(term, 0.0)
            self._vectors[doc_id] = vector
            self._doc_norm[doc_id] = math.sqrt(sum(weight**2 for weight in vector.values()))

    def search(self, query: str, top_k: int = 3) -> list[tuple[FinanceDocument, float]]:
        """질의와 가장 유사한 문서를 반환한다."""
        query_terms = Counter(tokenize(query))
        if not query_terms:
            return []

        max_tf = max(query_terms.values())
        query_vector = {
            term: (count / max_tf) * self._idf.get(term, 0.0)
            for term, count in query_terms.items()
            if term in self._vocabulary
        }
        query_norm = math.sqrt(sum(weight**2 for weight in query_vector.values()))
        if query_norm == 0:
            return []

        scored: list[tuple[FinanceDocument, float]] = []
        for doc_id, vector in self._vectors.items():
            numerator = sum(
                query_vector.get(term, 0.0) * vector.get(term, 0.0)
                for term in query_vector
            )
            denominator = query_norm * self._doc_norm.get(doc_id, 0.0)
            if denominator == 0:
                continue
            score = numerator / denominator
            if score > 0:
                scored.append((self._documents[doc_id], score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[: max(top_k, 1)]
