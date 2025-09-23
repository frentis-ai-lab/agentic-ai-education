"""간단한 ReAct 에이전트 예시 - LangGraph 사용"""

import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()


@tool
def calculator(expression: str) -> str:
    """수학 계산을 합니다. 예: 2+2*3"""
    try:
        result = eval(expression)
        return f"계산 결과: {result}"
    except:
        return "계산할 수 없습니다."


@tool
def weather_info(city: str) -> str:
    """도시 이름을 받아 날씨를 알려줍니다."""
    weather_data = {
        "서울": "맑음, 23도",
        "부산": "흐림, 20도",
        "대구": "비, 18도"
    }
    return weather_data.get(city, "날씨 정보가 없습니다.")


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY를 설정해주세요.")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [calculator, weather_info]

    agent = create_react_agent(llm, tools)

    # 사용자 입력 받기
    user_input = input("질문을 입력하세요: ")

    for message in agent.stream({"messages": [("user", user_input)]}):
        if "agent" in message:
            print(message["agent"]["messages"][0].content)
        elif "tools" in message:
            print(f"도구 사용: {message}")


if __name__ == "__main__":
    main()