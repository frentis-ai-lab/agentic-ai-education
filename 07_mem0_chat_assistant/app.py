"""Streamlit chat app showcasing mem0 long-term memory."""

from __future__ import annotations

import json
import os
import uuid
from typing import List

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


def render_sidebar(mem_client: Mem0Memory) -> None:
    st.sidebar.header("세션 정보")
    st.sidebar.write(f"**user_id**: `{mem_client.user_id}`")

    if st.sidebar.button("요약 보기", use_container_width=True):
        summary = mem_client.get_summary()
        st.sidebar.subheader("mem0 Summary")
        st.sidebar.code(json.dumps(summary, ensure_ascii=False, indent=2))

    st.sidebar.write("---")
    st.sidebar.write("검색된 기억은 채팅 아래쪽에 함께 표시됩니다.")


def main() -> None:
    st.title("mem0 장기 기억 챗봇")
    st.caption("mem0에 저장된 사실을 LangChain 에이전트가 재활용하는 예제입니다.")

    ensure_session_state()
    client = get_mem0_client()
    mem = Mem0Memory(client, user_id=st.session_state.session_id)
    render_sidebar(mem)

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
        st.code(json.dumps(st.session_state.last_memories, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
