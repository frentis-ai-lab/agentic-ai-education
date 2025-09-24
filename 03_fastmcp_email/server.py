"""Email MCP server with HTTP transport, OpenAI composition and Gmail SMTP."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from fastmcp import FastMCP
from openai import OpenAI

load_dotenv()

app = FastMCP(
    name="email-mcp-server",
    instructions="Email composition and sending tools with OpenAI and Gmail SMTP.",
)


@app.tool
def compose_email(topic: str, tone: str = "professional", recipient_name: str = "") -> str:
    """OpenAI로 이메일 초안을 작성합니다.

    Args:
        topic: 이메일 주제나 내용
        tone: 어조 (professional, friendly, formal, casual)
        recipient_name: 받는 사람 이름 (선택사항)
    """
    if not os.getenv("OPENAI_API_KEY"):
        return "❌ OPENAI_API_KEY가 설정되지 않았습니다."

    try:
        client = OpenAI()

        greeting = f"안녕하세요 {recipient_name}님," if recipient_name else "안녕하세요,"

        prompt = f"""
다음 조건으로 이메일을 작성해주세요:
- 주제: {topic}
- 어조: {tone}
- 인사말: {greeting}
- 한국어로 작성
- 적절한 이메일 형식과 마무리 인사 포함
"""

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ 이메일 작성 중 오류: {str(e)}"


@app.tool
def send_email(to: str, subject: str, body: str) -> str:
    """Gmail SMTP를 통해 이메일을 발송합니다.

    Args:
        to: 받는 사람 이메일 주소
        subject: 제목
        body: 본문
    """
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_password:
        return "❌ Gmail 설정이 누락되었습니다. GMAIL_USER와 GMAIL_APP_PASSWORD를 확인해주세요."

    try:
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)

        return f"✅ 이메일이 성공적으로 발송되었습니다: {to}"

    except Exception as e:
        return f"❌ 이메일 발송 실패: {str(e)}"


@app.tool
def improve_email(original_email: str, improvement_request: str = "문법과 어조 개선") -> str:
    """기존 이메일을 OpenAI로 개선합니다.

    Args:
        original_email: 원본 이메일 내용
        improvement_request: 개선 요청사항
    """
    if not os.getenv("OPENAI_API_KEY"):
        return "❌ OPENAI_API_KEY가 설정되지 않았습니다."

    try:
        client = OpenAI()

        prompt = f"""
다음 이메일을 개선해주세요:

원본 이메일:
{original_email}

개선 요청사항: {improvement_request}

한국어로 자연스럽고 전문적인 이메일로 다시 작성해주세요.
"""

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=600
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ 이메일 개선 중 오류: {str(e)}"


if __name__ == "__main__":
    print("🚀 Email MCP Server 시작")
    print("📧 사용 가능한 도구:")
    print("  - compose_email: OpenAI로 이메일 작성")
    print("  - send_email: Gmail SMTP로 발송")
    print("  - improve_email: 기존 이메일 개선")
    print()
    print("🌐 HTTP Transport 사용 - http://localhost:8000/mcp/")
    print("⚠️  환경변수 확인: OPENAI_API_KEY, GMAIL_USER, GMAIL_APP_PASSWORD")
    print()

    app.run(transport="http", host="127.0.0.1", port=8000)