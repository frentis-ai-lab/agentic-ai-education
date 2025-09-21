# 07_a2a_basics – 학습 노트

## 학습 목표
- AutoGen의 Agent-to-Agent(GroupChat) 기본 구조 이해
- 서로 다른 역할을 가진 에이전트(planner, writer, reviewer)를 구성하여 협업 흐름 체험
- `UserProxyAgent`의 `human_input_mode` 옵션 차이를 이해하고 자동/수동 제어 가능성 탐색

## 아키텍처 개요
1. **LLM 설정**
   - `build_llm_config()`에서 모델/키 지정 → 모든 에이전트가 공유
2. **에이전트 역할**
   - `AssistantAgent`: planner, writer (LLM 기반)
   - `UserProxyAgent`: reviewer (기본 자동 승인 메시지)
3. **GroupChat & Manager**
   - `GroupChat(agents=[...], max_round=6)`
   - `GroupChatManager`가 라운드를 관리하며 메시지 라우팅
   - `reviewer.initiate_chat(...)`로 대화 시작

## 실행 & 관찰 포인트
- 콘솔 로그에서 각 라운드의 메시지를 확인 → planner가 구조 제안 → writer가 본문 작성 → reviewer가 요약
- `max_round`를 줄이거나 늘려 결과 품질 비교
- `reviewer`의 `human_input_mode`를 `ALWAYS`로 변경해 직접 개입 실습

## 심화 질문
- 에이전트가 외부 툴(예: 웹 검색)에 액세스하도록 확장하려면 어떤 단계를 추가해야 할까?
- AutoGen과 CrewAI의 가장 큰 차이는 무엇이며, 어떤 상황에서 각각을 쓰면 좋을까?
- 실패한 호출(예: LLM Rate Limit)이 발생하면 어떻게 재시도/에러 처리할까?
