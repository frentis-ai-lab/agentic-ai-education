"""CLI chat demo using mem0 long-term memory."""

from __future__ import annotations

import os
from typing import List

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from mem0 import MemoryClient

from memory_utils import Mem0Memory

SESSION_USER_ID = os.getenv("MEM0_CLI_USER_ID", "cli-demo-user")
MEMORY_TOP_K = 3

SYSTEM_PROMPT = (
    "너는 mem0에 저장된 기억과 사용자의 현재 질문을 참고하는 한국어 비서야.\n"
    "- memories 목록에 있는 사실을 우선 활용해 답변하고, 근거가 없으면 솔직히 모른다고 말해.\n"
    "- memories 항목을 인용할 때는 자연스럽게 언급해."
)


def main() -> None:
    load_dotenv()

    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        raise RuntimeError("MEM0_API_KEY 환경 변수를 설정해 주세요.")

    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.3)
    memory_client = Mem0Memory(MemoryClient(api_key=api_key), SESSION_USER_ID)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    "memories 목록:\n{memories_text}\n\n"
                    "원본 memories(JSON): {memories_json}\n\n"
                    "위 기억을 참고하여 사용자 메시지에 답변하세요.\n"
                    "사용자: {user_message}"
                )
            ),
        ]
    )

    print("mem0 CLI 어시스턴트입니다. 'exit' / 'quit' / 'q' 를 입력하면 종료됩니다.")
    print(f"세션 user_id: {SESSION_USER_ID}\n")

    conversation: List[dict[str, str]] = []

    while True:
        user_input = input("You > ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("세션을 종료합니다. 고생하셨습니다!")
            break
        if not user_input:
            continue

        conversation.append({"role": "user", "content": user_input})
        memory_client.add(user_input)

        try:
            search_results = memory_client.search(user_input, top_k=MEMORY_TOP_K)
        except Exception as exc:
            print(f"\n[경고] 검색 중 오류 발생: {exc}")
            search_results = []

        if not search_results:
            search_results = memory_client.recent(top_k=MEMORY_TOP_K)

        if search_results:
            print("\n[검색된 기억]")
            for idx, item in enumerate(search_results, start=1):
                memory_text = item.get("memory", "(내용 없음)")
                score = item.get("score")
                score_text = f" (score {score:.2f})" if score is not None else ""
                print(f" {idx}. {memory_text}{score_text}")
        else:
            print("\n[검색된 기억] 관련 항목이 없습니다.")

        memories_text = (
            "\n".join(f"- {item.get('memory', '')}" for item in search_results)
            if search_results
            else "(관련 기억 없음)"
        )

        chain = prompt | llm
        response = chain.invoke({
            "memories_text": memories_text,
            "memories_json": str(search_results),
            "user_message": user_input,
        })

        reply = response.content.strip()
        conversation.append({"role": "assistant", "content": reply})
        print(f"Assistant > {reply}\n")


if __name__ == "__main__":
    main()
