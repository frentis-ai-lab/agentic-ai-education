# 04_langchain_mcp – 학습 노트

## 학습 목표
- LangChain ReAct 에이전트가 MCP 툴과 로컬 툴을 동시에 사용하는 패턴 이해
- FastMCP 서버를 임베드하거나 별도 프로세스로 실행하는 두 가지 방식을 비교
- MCP 구조화 응답을 LangChain이 어떻게 해석/활용하는지 확인

## 아키텍처 개요
1. **MCP 서버 (`mcp_server.py`)**
   - `campaign_compass`, `audience_scanner`, `email_blueprint` 툴 제공
   - 서버는 FastMCP 표준(`app.run()`)을 따르며, LangChain 스크립트에서는 `FastMCP.as_proxy`로 임베드합니다.
2. **LangChain 에이전트 (`react_with_mcp.py`)**
   - 로컬 툴: 제품 요약, 내부 KPI 계산
   - MCP 브리징 툴: `_call_mcp` 헬퍼를 통해 `fastmcp.Client`로 원격 툴 호출
   - 프롬프트에서 MCP 툴 활용을 유도하는 지시 포함

## 실행 & 관찰 포인트
- `uv run python react_with_mcp.py` 실행 후 로그에 MCP 툴 호출(Observation)이 찍히는지 확인
- MCP 서버를 별도 터미널에서 실행하면 두 프로세스 간 표준 입출력을 확인 가능
- `_call_mcp`가 반환하는 JSON 문자열이 LangChain agent의 최종 응답에 어떻게 반영되는지 살펴보기

## 심화 질문
- MCP 서버를 HTTP/SSE로 배포하면 LangChain 측 브리징 로직은 어떻게 달라져야 할까?
- MCP 툴 호출 실패나 타임아웃을 처리하기 위해 어떤 예외 처리/재시도 정책이 필요할까?
- 동일한 MCP 서버를 CrewAI나 AutoGen과 공유하려면 어떤 공통 인터페이스를 설계해야 할까?
