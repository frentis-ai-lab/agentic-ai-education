# 07-1. CrewAI + MCP 뉴스레터 시스템

CrewAI 멀티 에이전트와 MCP(Model Control Protocol) 도구를 결합한 AI 뉴스레터 자동 제작/발송 시스템입니다.

## 🎯 학습 목표

- CrewAI 에이전트들의 협업 워크플로우 이해
- MCP 서버를 통한 도구 통합 경험
- 실제 이메일 발송까지 포함한 완전한 자동화 시스템 구축

## 🏗️ 시스템 구조

### MCP 서버 (newsletter_server.py)
- **이메일 도구**: compose_email, send_email, improve_email (02-1에서 재사용)
- **뉴스 도구**: fetch_tech_news (RSS 피드에서 AI 뉴스 수집)
- **디자인 도구**: create_newsletter_html (HTML 템플릿 생성)

### CrewAI 에이전트 (newsletter_crew.py)
1. **News Researcher**: 최신 AI/Tech 뉴스 수집 및 필터링
2. **Content Editor**: 뉴스 큐레이션 및 인사이트 추가
3. **Newsletter Designer**: HTML 뉴스레터 템플릿 제작
4. **Email Campaign Manager**: 실제 이메일 발송

## 🚀 사용법

### 1. 환경 설정

```bash
# .env 파일 생성 (프로젝트 루트에서)
cp ../.env.example ../.env

# 필수 환경변수 설정
OPENAI_API_KEY=your_openai_api_key
GMAIL_USER=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_app_password
```

### 2. 의존성 설치

```bash
uv sync
```

### 3. 실행

```bash
# 뉴스레터 자동 제작 및 발송
uv run python newsletter_crew.py --email recipient@example.com

# 다른 모델 사용
uv run python newsletter_crew.py --email recipient@example.com --model gpt-4
```

### 4. MCP 서버 단독 실행 (테스트용)

```bash
uv run python newsletter_server.py
# HTTP MCP 서버가 localhost:8000에서 실행됩니다
```

## ⚙️ Gmail 설정

이메일 발송을 위해서는 Gmail 앱 비밀번호가 필요합니다:

1. Google 계정의 2단계 인증 활성화
2. [앱 비밀번호 생성](https://support.google.com/accounts/answer/185833)
3. `.env` 파일에 `GMAIL_APP_PASSWORD` 설정

## 📋 워크플로우

1. **뉴스 수집**: TechCrunch AI RSS 피드에서 최신 뉴스 가져오기
2. **콘텐츠 큐레이션**: AI가 중요한 뉴스 선별 및 요약
3. **뉴스레터 디자인**: HTML 템플릿으로 시각적 구성
4. **이메일 발송**: Gmail SMTP로 실제 발송

## 🔧 주요 MCP 도구

- `fetch_tech_news`: AI/기술 뉴스 RSS 수집
- `compose_email`: OpenAI로 이메일 초안 작성
- `create_newsletter_html`: HTML 뉴스레터 생성
- `send_email`: Gmail SMTP 발송
- `improve_email`: 이메일 품질 개선

## 📝 예시 실행 결과

시스템이 자동으로:
1. 최신 AI 뉴스 5개를 수집
2. 중요도에 따라 3개 선별
3. 독자 친화적으로 큐레이션
4. HTML 뉴스레터 생성
5. 지정된 이메일로 발송

## 🎓 확장 아이디어

- 다양한 RSS 피드 소스 추가
- 개인화된 뉴스 추천 로직
- 구독자 관리 시스템
- A/B 테스트 기능
- 발송 스케줄링