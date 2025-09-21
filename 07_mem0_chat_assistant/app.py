"""Streamlit chat app showcasing mem0 long-term memory."""

from __future__ import annotations

import os
import uuid
from typing import Any, List, Sequence

import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from mem0 import MemoryClient

from memory_utils import Mem0Memory

load_dotenv()

st.set_page_config(page_title="mem0 장기 기억 챗봇", layout="wide")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_QUERY = "사용자가 알려준 사실을 기반으로 친근하게 답변하십시오."


@st.cache_resource(show_spinner=False)
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model=OPENAI_MODEL, temperature=0.4)


@st.cache_resource(show_spinner=False)
def get_mem0_client() -> MemoryClient:
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        st.stop()
    return MemoryClient(api_key=api_key)


def ensure_session_state() -> None:
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"streamlit-{uuid.uuid4().hex[:8]}"
    if "conversation" not in st.session_state:
        st.session_state.conversation: List[dict[str, str]] = []
    if "latest_summary" not in st.session_state:
        st.session_state.latest_summary = None


def reset_session_buffers() -> None:
    st.session_state.conversation = []
    st.session_state.pop("last_memories", None)
    st.session_state.latest_summary = None


def render_summary(summary: dict[str, Any] | None, container: st.delta_generator.DeltaGenerator) -> None:
    if not summary:
        container.info("요약이 아직 생성되지 않았습니다.")
        return

    text = summary.get("summary")
    if text:
        container.markdown(f"**요약**\n\n{text}")

    memories = summary.get("memories") or []
    if memories:
        container.markdown("최근 기억:")
        for item in memories:
            memory_text = item.get("memory")
            if memory_text:
                container.markdown(f"- {memory_text}")


def render_memories(results: Sequence[dict[str, Any]]) -> None:
    if not results:
        st.info("저장된 기억이 아직 없습니다.")
        return

    for item in results:
        memory_text = item.get("memory", "(내용 없음)")
        score = item.get("score")
        created_at = item.get("created_at")

        with st.container(border=True):
            st.markdown(f"**{memory_text}**")
            meta_parts = []
            if created_at:
                meta_parts.append(created_at.replace("T", " ")[:19])
            if score is not None:
                meta_parts.append(f"score {score:.2f}")
            if meta_parts:
                st.caption(" · ".join(meta_parts))


def main() -> None:
    st.title("mem0 장기 기억 챗봇")
    st.caption("mem0에 저장된 사실을 LangChain 에이전트가 재활용하는 예제입니다.")

    ensure_session_state()
    client = get_mem0_client()

    st.sidebar.header("세션 정보")
    user_id_input = st.sidebar.text_input(
        "user_id",
        value=st.session_state.session_id,
        help="새 user_id를 입력하면 해당 대화 기록이 초기화됩니다.",
    )
    sanitized_user_id = user_id_input.strip() or st.session_state.session_id
    if sanitized_user_id != st.session_state.session_id:
        st.session_state.session_id = sanitized_user_id
        reset_session_buffers()

    if st.sidebar.button("새 user_id 발급", use_container_width=True):
        st.session_state.session_id = f"streamlit-{uuid.uuid4().hex[:8]}"
        reset_session_buffers()
        st.experimental_rerun()

    mem = Mem0Memory(client, user_id=st.session_state.session_id)

    if st.sidebar.button("요약 보기", use_container_width=True):
        st.session_state.latest_summary = mem.get_summary()

    if st.session_state.latest_summary:
        st.sidebar.subheader("mem0 요약")
        render_summary(st.session_state.latest_summary, st.sidebar)

    st.sidebar.caption("검색된 기억은 채팅 영역 아래 카드에서 확인할 수 있습니다.")

    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=DEFAULT_QUERY),
            HumanMessage(content="Memories: {memories}\n\nUser: {user_message}"),
        ]
    )

    user_input = st.chat_input("메시지를 입력해 주세요")
    if user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})
        mem.add_message(user_input)

        search_results = mem.search(user_input, top_k=3)
        memories_text = json.dumps(search_results, ensure_ascii=False)

        chain = prompt | llm
        response = chain.invoke({"memories": memories_text, "user_message": user_input})
        st.session_state.conversation.append({"role": "assistant", "content": response.content})

        st.session_state.last_memories = search_results

    for msg in st.session_state.conversation:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if "last_memories" in st.session_state:
        st.write("---")
        st.subheader("검색된 기억")
        render_memories(st.session_state.last_memories)


if __name__ == "__main__":
    main()
