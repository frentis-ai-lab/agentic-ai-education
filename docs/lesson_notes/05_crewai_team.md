# 05_crewai_team – 학습 노트

## 학습 목표
- CrewAI의 핵심 구성요소(Agent, Task, Crew)와 sequential 프로세스 이해
- `human_input=True`를 사용해 사람의 피드백을 수집하는 워크플로우 체험
- 다중 역할(마케터 → 영업 → 메일러) 협업 시나리오 설계 연습

## 아키텍처 개요
1. **에이전트 정의 (`build_agents`)**
   - 각 Agent는 역할, 목표, 백스토리를 갖고 동일 LLM을 공유 (`ChatOpenAI`)
   - `allow_delegation` 플래그로 하위 작업 위임 여부 조정
2. **태스크 구성 (`build_tasks`)**
   - Task가 어떤 Agent에 의해 수행되는지와 기대 출력, context(전 단계 결과) 명시
   - 영업 검토 태스크에 `human_input=True` → 콘솔에서 직접 피드백 입력
3. **Crew 실행**
   - `Crew(..., process=Process.sequential)`
   - `kickoff(inputs={...})`로 제품과 대상 세그먼트 전달

## 실행 & 관찰 포인트
- 콘솔에 노출되는 사용자 입력 프롬프트를 통해 사람이 어떻게 개입하는지 확인
- 에이전트 로그(verbose=True 설정된 에이전트)로 내부 reasoning 분석
- 다른 역할(예: Legal Reviewer)을 추가하고 context 체인을 확장해 보기

## 심화 질문
- 병렬 처리(`Process.hierarchical` 등)를 적용하면 어떤 장단점이 있을까?
- CrewAI에 MCP 툴이나 LangChain 툴을 붙이려면 어떤 추상화가 필요할까?
- 사람의 입력 값을 저장하고 재사용하려면 어떤 저장소/프로토콜을 사용할지 고민해보기
