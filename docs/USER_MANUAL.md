# 사용자 매뉴얼

이 문서는 `Agentic AI Education Playground` 리포지터리를 사용하는 학습자를 위한 안내서입니다. 각 단계별 실습을 수행하는 방법, 자격증명 설정, 자주 발생하는 문제 해결 방법을 제공합니다.

## 1. 전체 개요
- **구성**: 11개의 단계별 폴더 + 공통 루트 README + 보조 문서
- **목적**: FastMCP, LangChain, CrewAI, mem0, Google A2A SDK 생태계의 핵심 개념을 단계적으로 체험
- **형식**: 모든 예제는 `uv` 패키지 관리자를 사용하며 최소한의 의존성만 포함

## 2. 사전 준비
| 항목 | 설명 |
| --- | --- |
| Python | 3.11 이상 권장 (A2A SDK는 3.13 필요)
| uv | `curl -LsSf https://astral.sh/uv/install.sh | sh` 또는 Homebrew 등으로 설치
| API Key | OpenAI, mem0, Google API 등 필요한 키를 `.env` 또는 셸 환경 변수로 설정
| 터미널 | macOS/Linux 권장, Windows의 경우 WSL 또는 PowerShell 사용 가능

환경 변수를 한 번에 지정하려면 아래 예시를 참고하세요.
```bash
export OPENAI_API_KEY=sk-...
export MEM0_API_KEY=mem0_...
export GOOGLE_API_KEY=...
export GMAIL_USER=your@gmail.com
export GMAIL_APP_PASSWORD=...
export OPENAI_MODEL=gpt-4o-mini  # (선택)
```
> 루트 디렉터리의 `.env.example`을 복사해 `.env`를 만들고 `source .env`로 불러오는 방식이 가장 간편합니다.

## 3. 공통 실행 흐름
각 단계 폴더에 진입한 뒤 아래 순서로 진행합니다.
```bash
cd 02_fastmcp_tool  # 예시
uv sync             # 의존성 설치
uv run python server.py
uv run python client.py
```
> `uv sync`는 최초 1회만 수행하면 됩니다. `uv run ...`으로 스크립트를 실행하면 자동으로 가상환경이 활성화됩니다.

## 4. 단계별 요약 및 사용법
| 단계 | 주제 | 핵심 명령 | 비고 |
| --- | --- | --- | --- |
| 01_langchain_react | LangChain ReAct 패턴 | `uv run python react_agent.py` | OpenAI API 키 필요 |
| 02_fastmcp_tool | FastMCP 툴/클라이언트 기초 | `uv run python server.py` / `uv run python client.py` | 단일 프로세스 테스트 포함 |
| 03_fastmcp_email | FastMCP 이메일 도구 | `uv run python server.py` / `uv run python client.py` | Gmail 앱 비밀번호 설정 필요 |
| 04_fastmcp_package | FastMCP 서버 패키징 & PyPI 배포 | `uv build`, `uvx twine upload`, `pip install` / `pipx run agentic-hello-mcp` | `fastmcp.json` 예시 제공 |
| 05_langchain_mcp | LangChain + MCP 혼합 워크플로우 | `uv run python react_with_mcp.py` | MCP 서버 임베드, 필요 시 별도 실행 |
| 06_mem0_basics | mem0 메모리 CRUD | `uv run python memory_demo.py` | MEM0 API 키 필요 |
| 07_mem0_cli_chat | mem0 장기 기억 CLI | `uv run python chat_cli.py` | Streamlit 없이 터미널에서 기억 활용 체험 |
| 08_crewai_team | CrewAI 협업 플로우 | `uv run python crew_run.py` | 영업 담당자 입력을 콘솔에서 직접 제공 |
| 09_crewai_mcp | CrewAI + MCP 뉴스레터 시스템 | `uv run python newsletter_crew.py --email recipient@example.com` | 뉴스 수집부터 이메일 발송까지 |
| 10_a2a_airbnb | Google A2A 멀티 에이전트 | 각 하위 폴더에서 `uv run .` | Python 3.13, Google API 키 필요 |
| 11_next_project | 미래 기술 탐구 | 개별 프로젝트 진행 | 최신 트렌드 조사 및 프로젝트 기획 |

각 단계의 README는 추가 설정값과 로그 예시를 포함하므로, 실습 전 반드시 읽어 주세요.

## 5. 문제 해결 가이드
- **모델/LLM 호출 실패**: `OPENAI_API_KEY`가 올바른지, 요청 모델이 계정에서 활성화돼 있는지 확인하세요.
- **mem0 인증 오류**: `MEM0_API_KEY`가 유효한지와 `user_id`가 중복되지 않았는지 확인하세요.
- **Gmail 발송 실패**: `GMAIL_APP_PASSWORD`가 올바른지, 2단계 인증이 활성화됐는지 확인하세요.
- **Google A2A 실행 오류**: Python 3.13 환경인지, `GOOGLE_API_KEY` 설정이 올바른지 확인하세요.
- **패키지 설치 문제**: `uv pip cache purge`로 캐시를 제거하고 다시 `uv sync`를 수행합니다.
- **MCP 실행 오류**: FastMCP 서버 스크립트가 `app.run()`을 호출하는지, `command` 이름이 정확한지 검토하세요.
- **`hello-mcp-server`를 찾지 못함(ENOENT)**: `pipx run`/`uv tool run`처럼 직접 실행하거나, `which hello-mcp-server`로 확인한 절대 경로를 `fastmcp.json`의 `command`에 지정합니다.

## 6. 학습 팁
- 각 단계의 로그를 그대로 복사해 강의 자료(슬라이드/노션)에 붙여 넣으면 데모 재현이 쉽습니다.
- `uv run`으로 실행한 스크립트는 `--` 이하에 추가 인자를 전달할 수 있습니다. 예) `uv run python crew_run.py -- --model gpt-4.1-mini`.
- 실습 중 생성된 결과물(`outbox.jsonl`, mem0 저장 내용 등)은 반복 실습 전에 삭제하거나 초기화하는 것이 좋습니다.

## 7. 참고 링크
- FastMCP 문서: https://gofastmcp.com/docs
- LangChain ReAct 소개: https://python.langchain.com/docs/modules/agents/how_to/react
- CrewAI 가이드: https://docs.crewai.com/
- mem0 문서: https://docs.mem0.ai
- Google A2A SDK: https://github.com/google/a2a-python
- Google ADK 문서: https://google.github.io/adk-docs/
- 단계별 심화 노트: `docs/lesson_notes/` 폴더 참조

궁금한 점이 있다면 `docs/TEACHING_GUIDE.md`의 Q&A/토론 질문을 참고하거나 Slack/슬랙 채널 등 커뮤니티에서 공유해 주세요.
