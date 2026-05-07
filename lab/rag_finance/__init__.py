"""Python 금융공학 RAG Lab 패키지."""

# 패키지 외부에서 바로 사용할 핵심 파이프라인 클래스를 가져온다.
from .pipeline import FinanceRAGPipeline

# `from lab.rag_finance import *` 사용 시 공개할 심볼 목록을 명시한다.
__all__ = ["FinanceRAGPipeline"]
