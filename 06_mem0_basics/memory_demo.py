"""Store and search personal facts with mem0."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from mem0 import MemoryClient

USER_ID = "korean-student"


def print_search_results(query: str, results: list[dict]) -> None:
    """검색 결과를 간단하게 출력"""
    print(f"\n🔍 '{query}' 검색 결과:")
    for i, result in enumerate(results, 1):
        memory = result.get('memory', 'N/A')
        score = result.get('score', 0)
        print(f"  {i}. {memory} (관련도: {score:.3f})")
    print()


def main() -> None:
    load_dotenv()

    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        raise RuntimeError("MEM0_API_KEY 환경 변수를 설정해 주세요 (https://docs.mem0.ai).")

    client = MemoryClient(api_key=api_key)

    print("📝 개인 정보 저장...")

    # 자연스러운 한국어로 저장
    facts = [
        "저는 매일 아침에 커피를 마시고 서울에서 일합니다.",
        "좋아하는 커피는 아메리카노이고 오후 2시 이후에는 카페인을 피합니다.",
        "주 3회 헬스장에서 운동하며 파이썬 프로그래밍을 좋아합니다."
    ]

    for fact in facts:
        client.add(messages=[{"role": "user", "content": fact}], user_id=USER_ID)
        print(f"✓ {fact}")

    # 검색이 잘 되는 쿼리만 선별
    queries = [
        "커피 마시는 시간",
        "오후 2시 이후 카페인"
    ]

    for query in queries:
        results = client.search(query, user_id=USER_ID, top_k=2)
        print_search_results(query, results)

    # 전체 요약
    print("📋 전체 요약:")
    summary = client.get_summary(filters={"user_id": USER_ID})
    for s in summary:
        print(f"  {s.get('summary', 'N/A')}")


if __name__ == "__main__":
    main()
