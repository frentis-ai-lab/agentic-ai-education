# 사용자 매뉴얼

이 문서는 `Agentic AI Education Playground` 리포지터리를 사용하는 학습자를 위한 안내서입니다. 각 단계별 실습을 수행하는 방법, 자격증명 설정, 자주 발생하는 문제 해결 방법을 제공합니다.

## 1. 전체 개요
- **구성**: 8개의 단계별 폴더 + 공통 루트 README + 보조 문서
- **목적**: FastMCP, LangChain, CrewAI, mem0, AutoGen(a2a) ⽣태계의 핵심 개념을 단계적으로 체험
- **형식**: 모든 예제는 `uv` 패키지 관리자를 사용하며 최소한의 의존성만 포함

## 2. 사전 준비
| 항목 | 설명 |
| --- | --- |
| Python | 3.11 이상 권장 (로컬 또는 pyenv/conda 환경)
| uv | `curl -LsSf https://astral.sh/uv/install.sh | sh` 또는 Homebrew 등으로 설치
| API Key | OpenAI, mem0 등 필요한 키를 `.env` 또는 셸 환경 변수로 설정
| 터미널 | macOS/Linux 권장, Windows의 경우 WSL 또는 PowerShell 사용 가능

환경 변수를 한 번에 지정하려면 아래 예시를 참고하세요.
```bash
export OPENAI_API_KEY=sk-...
export MEM0_API_KEY=mem0_...
export OPENAI_MODEL=gpt-4o-mini  # (선택)
```

## 3. 공통 실행 흐름
각 단계 폴더에 진입한 뒤 아래 순서로 진행합니다.
```bash
cd 01_fastmcp_tool  # 예시
uv sync             # 의존성 설치
uv run python server.py
uv run python client.py
```
> `uv sync`는 최초 1회만 수행하면 됩니다. `uv run ...`으로 스크립트를 실행하면 자동으로 가상환경이 활성화됩니다.

## 4. 단계별 요약 및 사용법
| 단계 | 주제 | 핵심 명령 | 비고 |
| --- | --- | --- | --- |
| 01_fastmcp_tool | FastMCP 툴/클라이언트 기초 | `uv run python server.py` / `uv run python client.py` | 단일 프로세스 테스트 포함 |
| 02_fastmcp_package | FastMCP 서버 패키징 & PyPI 배포 | `uv build`, `uvx twine upload`, `pip install` / `pipx run agentic-hello-mcp` | `fastmcp.json` 예시 제공 |
| 03_langchain_react | LangChain ReAct 패턴 | `uv run python react_agent.py` | OpenAI API 키 필요 |
| 04_crewai_team | CrewAI 협업 플로우 | `uv run python crew_run.py` | 영업 담당자 입력을 콘솔에서 직접 제공 |
| 05_mem0_basics | mem0 메모리 CRUD | `uv run python memory_demo.py` | MEM0 API 키 필요 |
| 06_a2a_basics | AutoGen a2a 기본 | `uv run python basic_chat.py` | GroupChatManager 로깅 관찰 |
| 07_a2a_mem0_profile | mem0 + a2a | `uv run python personal_agents.py` | `search_profile` 툴 호출 흐름 확인 |
| 08_a2a_dual_agents | CrewAI & LangGraph A2A 서버 + UI | 각 하위 폴더에서 `uv run uvicorn ...` | 세 개의 프로세스를 띄워 브라우저로 테스트 |

각 단계의 README는 추가 설정값과 로그 예시를 포함하므로, 실습 전 반드시 읽어 주세요.

## 5. 문제 해결 가이드
- **모델/LLM 호출 실패**: `OPENAI_API_KEY`가 올바른지, 요청 모델이 계정에서 활성화돼 있는지 확인하세요.
- **mem0 인증 오류**: `MEM0_API_KEY`가 유효한지와 `user_id`가 중복되지 않았는지 확인하세요.
- **패키지 설치 문제**: `uv pip cache purge`로 캐시를 제거하고 다시 `uv sync`를 수행합니다.
- **MCP 실행 오류**: FastMCP 서버 스크립트가 `app.run()`을 호출하는지, `command` 이름이 정확한지 검토하세요.
- **AutoGen에서 무한 루프**: `max_round` 값을 조정하거나, UserProxyAgent에 직접 개입(`human_input_mode="ALWAYS"`)할 수 있습니다.

## 6. 학습 팁
- 각 단계의 로그를 그대로 복사해 강의 자료(슬라이드/노션)에 붙여 넣으면 데모 재현이 쉽습니다.
- `uv run`으로 실행한 스크립트는 `--` 이하에 추가 인자를 전달할 수 있습니다. 예) `uv run python crew_run.py -- --model gpt-4.1-mini`.
- 실습 중 생성된 결과물(`outbox.jsonl`, mem0 저장 내용 등)은 반복 실습 전에 삭제하거나 초기화하는 것이 좋습니다.

## 7. 참고 링크
- FastMCP 문서: https://gofastmcp.com/docs
- LangChain ReAct 소개: https://python.langchain.com/docs/modules/agents/how_to/react
- CrewAI 가이드: https://docs.crewai.com/
- mem0 문서: https://docs.mem0.ai
- AutoGen 프로젝트: https://github.com/microsoft/autogen
- 단계별 심화 노트: `docs/lesson_notes/` 폴더 참조

궁금한 점이 있다면 `docs/TEACHING_GUIDE.md`의 Q&A/토론 질문을 참고하거나 Slack/슬랙 채널 등 커뮤니티에서 공유해 주세요.
