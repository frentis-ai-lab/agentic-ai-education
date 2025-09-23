# 03_fastmcp_package – 학습 노트

## 학습 목표
- FastMCP 서버를 Python 패키지로 배포하고 PyPI(TestPyPI)를 통해 배포하는 절차 이해
- `fastmcp.json` 설정 파일로 MCP 클라이언트에 서버를 등록하는 방법 학습
- console script 엔트리포인트(`hello-mcp-server`) 구조 파악

## 아키텍처 개요
1. **패키지 구조**
   - `hello_mcp/` 모듈이 실제 서버 구현(`server.py`)을 포함
   - `pyproject.toml`의 배포명은 `agentic-hello-mcp`, `project.scripts`에 `hello-mcp-server` 콘솔 엔트리 등록
2. **배포 흐름**
   - `uv build`로 wheel 생성 → `uvx twine upload --repository testpypi dist/*`
   - 소비자는 `pip install --extra-index-url https://test.pypi.org/simple agentic-hello-mcp` 또는 `pipx run --spec agentic-hello-mcp hello-mcp-server`로 실행
- 설치 또는 1회 실행 후에는 `hello-mcp-server` 콘솔 스크립트로 MCP 클라이언트가 호출 가능
3. **fastmcp.json**
   - MCP 호환 클라이언트가 읽을 수 있는 설정 파일
   - `type=stdio`, `command=hello-mcp-server` → 설치된 패키지에서 서버를 실행
4. **테스트 스크립트**
   - `demo_client.py`가 `FastMCP.as_proxy(app)` 패턴으로 로컬 테스트

## 실행 & 관찰 포인트
- `uv build` → wheel 생성 과정을 확인 (패키징 흐름 체험)
- `uv pip install --editable .` → 개발 모드 설치 후 `uv run hello-mcp-server`
- TestPyPI에 업로드 후 `pip install --extra-index-url … agentic-hello-mcp` 또는 `pipx run --spec agentic-hello-mcp hello-mcp-server` 흐름 검증
- `fastmcp.json`을 실제 클라이언트 설정에 복사해 활용
- PATH가 적용되지 않는 환경에서는 `which hello-mcp-server`로 절대 경로를 구해 `command`에 직접 넣어 동작 확인

## 심화 질문
- PyPI에 올린 패키지를 여러 환경(Windows/macOS/Linux)에서 테스트할 때 주의할 점은?
- 복수의 MCP 서버를 패키지에 담으려면 `project.scripts`를 어떻게 확장할까?
- `fastmcp.json`에 환경 변수/의존성을 선언할 수 있는가? (`environment.dependencies` 참고)
- 배포 후 버전 업그레이드는 어떤 식으로 진행할지(semantic versioning, changelog 등) 생각해보기
