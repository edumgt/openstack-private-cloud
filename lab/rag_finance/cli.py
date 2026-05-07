"""금융공학 RAG Lab CLI."""

from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import FinanceRAGPipeline

DEFAULT_DATASET = (
    Path(__file__).resolve().parent / "data" / "sample_finance_docs.jsonl"
)


def positive_int(value: str) -> int:
    """1 이상의 정수만 허용한다."""
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("--top-k must be >= 1")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    """CLI 파서 생성."""
    parser = argparse.ArgumentParser(
        description="Python 금융공학 RAG Lab 질의 실행 도구"
    )
    parser.add_argument("--query", required=True, help="질의 문장")
    parser.add_argument(
        "--top-k",
        type=positive_int,
        default=3,
        help="반환할 근거 문서 개수 (기본값: 3)",
    )
    parser.add_argument(
        "--dataset",
        default=str(DEFAULT_DATASET),
        help="JSONL 데이터셋 경로",
    )
    return parser


def main() -> None:
    """CLI 엔트리포인트."""
    parser = build_parser()
    args = parser.parse_args()

    pipeline = FinanceRAGPipeline(dataset_path=args.dataset)
    print(pipeline.draft_answer(query=args.query, top_k=args.top_k))


if __name__ == "__main__":
    main()
