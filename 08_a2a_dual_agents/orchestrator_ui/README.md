# Orchestrator UI Server

간단한 FastAPI + Jinja UI를 통해 CrewAI 에이전트 서버와 LangGraph 에이전트 서버를 연결합니다. 사용자는 웹 페이지에서 메시지를 입력하고, 두 에이전트가 순차적으로 응답하는 흐름을 확인할 수 있습니다.

## 실행 방법
1. Crew 에이전트 서버(8001), LangGraph 에이전트 서버(8002)를 먼저 실행합니다.
2. 아래 명령으로 UI 서버를 실행합니다.
```bash
uv sync
uv run uvicorn server:app --reload --port 8000
```

## 환경 변수
- `CREW_AGENT_URL` (기본: `http://localhost:8001`)
- `LANGGRAPH_AGENT_URL` (기본: `http://localhost:8002`)

## 주요 엔드포인트
- `GET /` : 대화 UI 렌더링
- `POST /api/start` : 새 대화 세션 시작
- `POST /api/step` : 사용자의 입력을 받아 Crew → LangGraph 순으로 호출하고 결과 반환

세션별 대화 내용은 메모리(dict)로만 저장되며, 학습용 데모에 적합합니다.
