"""Store and search personal facts with mem0."""

from __future__ import annotations

import os
from typing import Any

from mem0 import MemoryClient

USER_ID = "lecture-student"


def pretty_print(title: str, payload: Any) -> None:
    print(f"\n[{title}]\n{payload}\n")


def main() -> None:
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        raise RuntimeError("MEM0_API_KEY 환경 변수를 설정해 주세요 (https://docs.mem0.ai).")

    client = MemoryClient(api_key=api_key)

    seed_facts = [
        "저는 서울에서 일하고, 매주 수요일 오전에 사내 세션을 진행합니다.",
        "좋아하는 커피는 라떼이고, 오후 3시 이후에는 카페인을 피하려고 합니다.",
        "팀 목표는 6월까지 Agentic 교육 과정을 3개 이상 출시하는 것입니다.",
    ]

    for fact in seed_facts:
        response = client.add(
            messages=[{"role": "user", "content": fact}],
            user_id=USER_ID,
        )
        pretty_print("저장 결과", response)

    results = client.search(
        "카페인 관련 습관은?",
        user_id=USER_ID,
        top_k=2,
    )
    pretty_print("검색 결과", results)

    summary = client.get_summary(filters={"user_id": USER_ID})
    pretty_print("요약", summary)


if __name__ == "__main__":
    main()
