# 01_langchain_react – 학습 노트

## 학습 목표
- LangChain의 ReAct(Reasoning + Acting) 에이전트 패턴 이해
- 텍스트 기반 함수 툴을 정의하고 에이전트에게 연결하는 방법 학습
- Thought → Action → Observation 로그를 통해 모델의 의사결정 과정을 해석하는 연습

## 아키텍처 개요
1. **로컬 툴 함수**
   - `get_product_snapshot`, `get_segment_tip`, `last_campaign_result`
   - `Tool` 객체로 래핑해 모델에게 설명 및 함수 시그니처 제공
2. **LLM 구성**
   - `ChatOpenAI` (`OPENAI_MODEL`, 기본 `gpt-4o-mini`)
   - `temperature=0.2`로 안정적 응답 유도
3. **에이전트 초기화**
   - `initialize_agent(..., agent=AgentType.REACT_DESCRIPTION)`
   - `handle_parsing_errors=True`로 모델 출력이 어긋날 때 graceful fallback

## 실행 & 관찰 포인트
- 로그에서 `Thought`, `Action`, `Observation` 패턴을 직접 확인
- 툴 설명을 바꿔 결과에 어떤 영향을 주는지 실험
- 모델 이름을 변경(`OPENAI_MODEL`)하여 호출 비용/성능 차이를 비교

## 심화 질문
- 다단계 추론이 필요한 시나리오(예: 복수 제품 비교)를 어떻게 설정할까?
- ReAct 대신 함수 호출(Function Calling) 기반 에이전트를 선택해야 하는 상황은?
- LangChain 에이전트를 MCP 툴 호출과 결합하려면 어떤 구조가 필요할까?
