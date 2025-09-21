# 09_a2a_mem0_profile – 학습 노트

## 학습 목표
- AutoGen 에이전트에 외부 기억(mem0) 조회 툴을 연결하는 방법 이해
- 사용자 프로필 정보를 기반으로 맞춤형 응답을 생성하는 A2A 패턴 학습
- `register_for_llm` + `register_for_execution` 데코레이터의 역할 파악

## 아키텍처 개요
1. **mem0 시드 데이터**
  - `ensure_memories`에서 사용자 정보(장소, 직함, 목표, 취미 등)를 초기화
  - `USER_ID`를 고정하여 같은 사용자 맥락 재사용
2. **에이전트 구성**
  - `controller`: UserProxyAgent (자동 진행)
  - `profile`: AssistantAgent (mem0 검색 툴 사용)
  - `campaign`: AssistantAgent (profile 정보 기반 이메일 개요 작성)
3. **툴 등록**
  - `@controller.register_for_execution()` → UI/다른 에이전트가 호출 가능
  - `@profile_agent.register_for_llm(...)` → LLM이 툴을 선택해 호출
  - 결과는 JSON 문자열로 반환해 다른 에이전트가 쉽게 파싱

## 실행 & 관찰 포인트
- 로그를 통해 `search_profile` 툴이 호출되는 순서를 확인
- mem0 검색 결과(JSON)에 어떤 필드가 포함되는지 살펴보고, 필요한 정보만 추려 이메일에 반영하는지 점검
- `ensure_memories`에 새로운 사실을 추가해 응답 품질이 어떻게 바뀌는지 실험

## 심화 질문
- `search_profile` 외에 메모리 저장/업데이트 툴을 추가할 때 고려할 점은?
- 동일 세션에서 mem0 정보를 다뤘을 때, 개인정보 보호를 위해 어떤 필터링/마스킹이 필요할까?
- AutoGen 에이전트 간 협업에 mem0 외 다른 데이터베이스(예: 벡터DB)를 추가하려면 어떤 패턴을 사용할까?
