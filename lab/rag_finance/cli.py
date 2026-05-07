"""금융공학 RAG Lab CLI."""

# 최신 타입 힌트 문법을 일관되게 사용하기 위한 선언이다.
from __future__ import annotations

# 커맨드라인 인자를 파싱하기 위한 표준 모듈이다.
import argparse
# 기본 데이터셋 경로를 계산하기 위해 Path를 사용한다.
from pathlib import Path

# 질의/검색/답변 생성을 수행하는 핵심 파이프라인을 가져온다.
from .pipeline import FinanceRAGPipeline

# 모듈 파일 기준으로 샘플 데이터셋의 기본 경로를 정의한다.
DEFAULT_DATASET = (
    Path(__file__).resolve().parent / "data" / "sample_finance_docs.jsonl"
)


def positive_int(value: str) -> int:
    """1 이상의 정수만 허용한다."""
    # 문자열 인자를 정수로 변환한다.
    parsed = int(value)
    # 1 미만 값은 사용자 입력 오류로 간주한다.
    if parsed < 1:
        raise argparse.ArgumentTypeError("--top-k must be >= 1")
    # 검증을 통과한 정수를 반환한다.
    return parsed


def build_parser() -> argparse.ArgumentParser:
    """CLI 파서 생성."""
    # 도구 설명 문구를 포함한 ArgumentParser를 초기화한다.
    parser = argparse.ArgumentParser(
        description="Python 금융공학 RAG Lab 질의 실행 도구"
    )
    # 필수 질의 문장 인자를 등록한다.
    parser.add_argument("--query", required=True, help="질의 문장")
    # 검색 근거 문서 개수를 지정하는 옵션을 등록한다.
    parser.add_argument(
        "--top-k",
        type=positive_int,
        default=3,
        help="반환할 근거 문서 개수 (기본값: 3)",
    )
    # 데이터셋 파일 경로를 지정하는 옵션을 등록한다.
    parser.add_argument(
        "--dataset",
        default=str(DEFAULT_DATASET),
        help="JSONL 데이터셋 경로",
    )
    # 완성된 파서를 호출자에게 반환한다.
    return parser


def main() -> None:
    """CLI 엔트리포인트."""
    # CLI 파서를 구성한다.
    parser = build_parser()
    # 실제 커맨드라인 입력값을 파싱한다.
    args = parser.parse_args()

    # 선택된 데이터셋으로 파이프라인을 초기화한다.
    pipeline = FinanceRAGPipeline(dataset_path=args.dataset)
    # 질의 결과 초안을 표준 출력으로 출력한다.
    print(pipeline.draft_answer(query=args.query, top_k=args.top_k))


# 스크립트 직접 실행 시에만 main 함수를 호출한다.
if __name__ == "__main__":
    main()
