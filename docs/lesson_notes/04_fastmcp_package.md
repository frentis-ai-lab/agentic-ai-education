# 04. FastMCP Package 작성 도구

## 목표
FastMCP를 사용해 Python 패키지 형태로 배포 가능한 MCP 도구를 작성합니다.

## 핵심 개념
- **PyPI 업로드**: `uv build` + `uv publish`
- **Entry Point**: `pyproject.toml`의 스크립트 정의
- **패키지 구조**: `src/` 레이아웃 사용

## 실습 단계
1. 패키지 프로젝트 구조 설정
2. `pyproject.toml` 패키지 메타데이터 작성
3. Entry point 스크립트 정의
4. 로컬 설치 테스트: `uv pip install -e .`
5. 빌드 및 배포: `uv build` → `uv publish`

## 주요 학습 포인트
- Python 패키지 배포 플로우 이해
- FastMCP 도구의 재사용성 확보
- PyPI를 통한 도구 공유 방법

## 다음 단계
LangChain에서 MCP 도구를 사용하는 방법을 학습합니다.