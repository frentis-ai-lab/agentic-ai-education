# 09_a2a_dual_agents – 학습 노트

## 학습 목표
- 서로 다른 프레임워크(CrewAI, LangGraph)로 작성된 에이전트를 A2A 프로토콜로 연동하는 방법 이해
- HTTP 기반 `POST /a2a/message` 계약을 설계하고 다중 서비스(두 에이전트 서버 + UI 오케스트레이터)를 조합하는 연습
- 단일 UI에서 단계별 응답 흐름(user → crew → writer)을 시각화

## 시스템 구성
1. **Crew Agent Server (`crew_agent_server/server.py`)**
   - FastAPI 앱 + CrewAI 컴비네이션
   - 요청을 받아 전략 개요를 bullet 리스트로 반환
   - MCP와 달리 HTTP JSON API로 노출 (`/health`, `/metadata`, `/a2a/message`)
2. **LangGraph Agent Server (`langgraph_agent_server/server.py`)**
   - LangGraph `StateGraph`로 이메일 작성
   - Crew 응답을 히스토리에 포함시켜 맞춤형 이메일 작성
3. **Orchestrator UI (`orchestrator_ui/server.py`)**
   - 간단한 FastAPI 프론트엔드 + 템플릿
   - `/api/start` → 세션 생성, `/api/step` → Crew 호출 → 히스토리 업데이트 → LangGraph 호출 → 결과 반환

## 실행 & 관찰 포인트
- 세 서버를 각각 다른 터미널에서 실행 후 브라우저(`http://localhost:8000`)로 접근
- 네트워크 탭/콘솔 로그에서 `conversation_id`, `history`가 어떻게 전달되는지 확인
- UI에 뜨는 메시지 순서를 통해 오케스트레이션이 의도대로 동작하는지 점검

## 심화 질문
- A2A 프로젝트의 `a2a-sdk`를 도입해 표준화된 요청/응답 객체를 사용하려면 어떤 변경이 필요할까?
- 에이전트 수를 늘리거나 병렬 호출을 지원하려면 UI와 서버 설계를 어떻게 바꿔야 할까?
- 인증/권한(예: API 키, JWT)을 추가해야 하는 경우 어떤 지점에서 검증 로직을 넣을지 고민해보기
