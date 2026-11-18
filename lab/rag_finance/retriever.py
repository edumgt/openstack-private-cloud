"""Hybrid (BM25 + TF-IDF Cosine + Character N-Gram) 금융 문서 검색기."""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

from .data_loader import FinanceDocument, iter_document_texts

TOKEN_PATTERN = re.compile(r"[0-9A-Za-z가-힣]+")


def tokenize(text: str) -> list[str]:
    """영문/숫자/한글 단어 토큰과 2-gram 서브토큰을 함께 추출해 한국어 조사 변화에도 강건한 검색을 지원한다."""
    words = [token.lower() for token in TOKEN_PATTERN.findall(text)]
    ngrams: list[str] = []
    for word in words:
        if len(word) >= 2 and any("가" <= ch <= "힣" for ch in word):
            for idx in range(len(word) - 1):
                ngrams.append(f"_{word[idx:idx + 2]}")
    return words + ngrams


class TfidfRetriever:
    """BM25 + Sublinear TF-IDF 코사인 하이브리드 검색기 (하위 호환 클래스명 유지)."""

    def __init__(
        self,
        documents: list[FinanceDocument],
        k1: float = 1.5,
        b: float = 0.75,
        bm25_weight: float = 0.55,
    ) -> None:
        self._documents = {doc.doc_id: doc for doc in documents}
        self._vocabulary: set[str] = set()
        self._doc_term_counts: dict[str, Counter[str]] = {}
        self._doc_lengths: dict[str, int] = {}
        self._avg_doc_length: float = 1.0
        self._idf: dict[str, float] = {}
        self._bm25_idf: dict[str, float] = {}
        self._vectors: dict[str, dict[str, float]] = {}
        self._doc_norm: dict[str, float] = {}
        self._k1 = k1
        self._b = b
        self._bm25_weight = bm25_weight
        self._build_index()

    def _build_index(self) -> None:
        doc_frequency: defaultdict[str, int] = defaultdict(int)

        for doc_id, text in iter_document_texts(self._documents.values()):
            tokens = tokenize(text)
            term_counts = Counter(tokens)
            self._doc_term_counts[doc_id] = term_counts
            self._doc_lengths[doc_id] = max(len(tokens), 1)
            for term in term_counts:
                doc_frequency[term] += 1
                self._vocabulary.add(term)

        doc_count = max(len(self._documents), 1)
        total_len = sum(self._doc_lengths.values())
        self._avg_doc_length = max(total_len / doc_count, 1.0)

        self._idf = {
            term: math.log((doc_count + 1) / (frequency + 1)) + 1.0
            for term, frequency in doc_frequency.items()
        }
        self._bm25_idf = {
            term: math.log(1.0 + (doc_count - frequency + 0.5) / (frequency + 0.5))
            for term, frequency in doc_frequency.items()
        }

        for doc_id, term_counts in self._doc_term_counts.items():
            vector: dict[str, float] = {}
            max_tf = max(term_counts.values(), default=1)
            for term, count in term_counts.items():
                tf = count / max_tf
                vector[term] = tf * self._idf.get(term, 0.0)
            self._vectors[doc_id] = vector
            self._doc_norm[doc_id] = math.sqrt(
                sum(weight**2 for weight in vector.values())
            )

    def _bm25_score(self, doc_id: str, query_terms: Counter[str]) -> float:
        term_counts = self._doc_term_counts.get(doc_id)
        if not term_counts:
            return 0.0
        doc_len = self._doc_lengths.get(doc_id, 1)
        score = 0.0
        for term, q_count in query_terms.items():
            if term not in term_counts:
                continue
            tf = term_counts[term]
            idf = self._bm25_idf.get(term, 0.0)
            denom = tf + self._k1 * (1.0 - self._b + self._b * (doc_len / self._avg_doc_length))
            score += idf * ((tf * (self._k1 + 1.0)) / max(denom, 1e-9)) * (1.0 + 0.1 * (q_count - 1))
        return score

    def search(
        self, query: str, top_k: int = 3
    ) -> list[tuple[FinanceDocument, float]]:
        """질의와 가장 유사한 문서를 하이브리드(BM25 + TF-IDF Cosine) 점수로 반환한다."""
        if top_k < 1:
            raise ValueError("top_k must be >= 1")

        query_terms = Counter(tokenize(query))
        if not query_terms:
            return []

        max_tf = max(query_terms.values())
        query_vector = {
            term: (count / max_tf) * self._idf.get(term, 0.0)
            for term, count in query_terms.items()
            if term in self._vocabulary
        }
        query_norm = math.sqrt(
            sum(weight**2 for weight in query_vector.values())
        )
        if query_norm == 0:
            return []

        cosine_scores: dict[str, float] = {}
        bm25_scores: dict[str, float] = {}

        for doc_id, vector in self._vectors.items():
            numerator = sum(
                query_vector.get(term, 0.0) * vector.get(term, 0.0)
                for term in query_vector
            )
            denominator = query_norm * self._doc_norm.get(doc_id, 0.0)
            if denominator > 0:
                cos_val = numerator / denominator
                if cos_val > 0:
                    cosine_scores[doc_id] = cos_val
            bm25_val = self._bm25_score(doc_id, query_terms)
            if bm25_val > 0:
                bm25_scores[doc_id] = bm25_val

        max_bm25 = max(bm25_scores.values(), default=1.0) or 1.0
        scored: list[tuple[FinanceDocument, float]] = []

        for doc_id in set(cosine_scores) | set(bm25_scores):
            cos_norm = cosine_scores.get(doc_id, 0.0)
            bm25_norm = bm25_scores.get(doc_id, 0.0) / max_bm25
            hybrid = (1.0 - self._bm25_weight) * cos_norm + self._bm25_weight * bm25_norm
            if hybrid > 0:
                scored.append((self._documents[doc_id], round(hybrid, 4)))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]


HybridRetriever = TfidfRetriever
