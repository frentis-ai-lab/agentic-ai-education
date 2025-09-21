# Agentic AI Education Playground

이 리포지터리는 Python 기반 Agentic AI 교육용 예제를 단계별(step-by-step)로 정리한 자료입니다. 각 폴더는 uv 패키지 관리자를 활용하여 독립적으로 실행할 수 있는 최소 예제를 담고 있습니다.

## 준비 사항
- Python 3.11 이상
- [uv](https://github.com/astral-sh/uv) 0.8 이상
- (필요 시) OpenAI API Key, Anthropic API Key 등 LLM 공급자 자격증명

처음 사용할 때 루트 디렉터리에 있는 `.env.example`을 복사해 API 키를 채워 두면 편리합니다.

```bash
cp .env.example .env  # 값 편집 후 `source .env`
```

각 단계로 이동한 뒤 아래 명령으로 의존성을 설치하고 예제를 실행하세요.

```bash
uv sync
uv run python <script.py>
```

## 단계 요약
1. **01_fastmcp_tool** – FastMCP로 간단한 MCP 서버/툴 만들기와 클라이언트 테스트
2. **02_fastmcp_package** – FastMCP 서버를 패키징하고 PyPI를 통해 배포/등록해 보기
3. **03_langchain_react** – LangChain ReAct 패턴으로 도구 사용 테스트
4. **04_crewai_team** – CrewAI로 마케터 → 영업 담당(휴먼) → 메일러 협업 크루 구성
5. **05_mem0_basics** – mem0로 개인화 메모리를 저장/조회하는 기초
6. **06_a2a_basics** – AutoGen a2a 스타일로 두 에이전트가 대화하도록 구성
7. **07_a2a_mem0_profile** – mem0를 활용해 개인정보를 가진 에이전트 구성 및 상호작용
8. **08_a2a_dual_agents** – CrewAI/ LangGraph 에이전트를 개별 서버로 띄우고 UI에서 A2A 오케스트레이션

각 폴더의 README를 참고하여 실습을 진행하고, 필요 시 API 키나 MCP 서버 설정을 개별적으로 구성하세요.

## 추가 자료
- `docs/USER_MANUAL.md` – 수강생을 위한 실행 가이드 및 FAQ
- `docs/TEACHING_GUIDE.md` – 강의자용 커리큘럼, 토론 질문, 평가 아이디어
