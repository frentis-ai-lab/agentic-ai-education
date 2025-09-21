# 02_fastmcp_package – 학습 노트

## 학습 목표
- FastMCP 서버를 Python 패키지로 배포하는 기본 절차 이해
- `fastmcp.json` 설정 파일로 MCP 클라이언트에 서버를 등록하는 방법 학습
- console script 엔트리포인트(`hello-mcp-server`) 구조 파악

## 아키텍처 개요
1. **패키지 구조**
   - `hello_mcp/` 모듈이 실제 서버 구현(`server.py`)을 포함
   - `pyproject.toml`에 `project.scripts` 설정 → `uv run hello-mcp-server`가 `hello_mcp.server:main` 호출
2. **fastmcp.json**
   - MCP 호환 클라이언트가 읽을 수 있는 설정 파일
   - `type=stdio`, `command=hello-mcp-server` → 설치된 패키지에서 서버를 실행
3. **테스트 스크립트**
   - `demo_client.py`가 `FastMCP.as_proxy(app)` 패턴으로 로컬 테스트

## 실행 & 관찰 포인트
- `uv build` → wheel 생성 과정을 확인 (패키징 흐름 체험)
- `uv pip install --editable .` → 개발 모드 설치 후 `uv run hello-mcp-server`
- `fastmcp.json`을 실제 클라이언트 설정에 복사해 활용

## 심화 질문
- 복수의 MCP 서버를 패키지에 담으려면 `project.scripts`를 어떻게 확장할까?
- `fastmcp.json`에 환경 변수/의존성을 선언할 수 있는가? (`environment.dependencies` 참고)
- 배포 후 버전 업그레이드는 어떤 식으로 진행할지(semantic versioning, changelog 등) 생각해보기
