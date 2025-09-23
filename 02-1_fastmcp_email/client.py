"""Email MCP client for testing HTTP transport functionality."""

import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()


async def test_email_tools():
    """Email MCP 도구들을 테스트합니다."""

    print("🧪 Email MCP Client 테스트 시작")
    print("📡 서버 연결: http://localhost:8000/mcp/")
    print()

    try:
        # FastMCP HTTP client - URL을 직접 전달
        async with Client("http://localhost:8000/mcp/") as client:

            # 1. 도구 목록 확인
            print("📋 사용 가능한 도구 목록:")
            tools = await client.list_tools()
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            print()

            # 2. 이메일 작성 테스트
            print("✍️  이메일 작성 테스트...")
            compose_result = await client.call_tool("compose_email", {
                "topic": "새로운 FastMCP 이메일 도구 소개",
                "tone": "professional",
                "recipient_name": "개발팀"
            })

            if compose_result.content:
                draft_email = compose_result.content[0].text
                print("📝 작성된 이메일:")
                print(draft_email)
                print()

                # 3. 이메일 개선 테스트
                print("🔧 이메일 개선 테스트...")
                improve_result = await client.call_tool("improve_email", {
                    "original_email": draft_email,
                    "improvement_request": "더 친근하고 간결하게 작성"
                })

                if improve_result.content:
                    improved_email = improve_result.content[0].text
                    print("✨ 개선된 이메일:")
                    print(improved_email)
                    print()

                # 4. 이메일 발송 테스트
                print("📤 이메일 발송 테스트...")

                # 실제 발송 여부 확인
                send_real = input("⚠️  정말로 이메일을 발송하시겠습니까? (y/N): ").lower().startswith('y')

                if send_real:
                    print("\n📮 이메일 발송 정보 입력:")
                    to_email = input("📧 받는 사람 이메일: ").strip()
                    if not to_email:
                        print("❌ 받는 사람 이메일이 입력되지 않았습니다.")
                    else:
                        subject = input("📝 이메일 제목: ").strip()
                        if not subject:
                            subject = "FastMCP 이메일 도구 테스트"

                        print(f"\n📤 {to_email}로 이메일 발송 중...")
                        send_result = await client.call_tool("send_email", {
                            "to": to_email,
                            "subject": subject,
                            "body": improved_email
                        })
                        print("📧 발송 결과:", send_result.content[0].text)
                else:
                    print("🔒 테스트 모드: 실제 발송하지 않습니다.")

            else:
                print("❌ 이메일 작성 실패")

    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        print()
        print("🔍 확인사항:")
        print("  1. 서버가 실행 중인지 확인: uv run python server.py")
        print("  2. 환경변수 설정 확인: .env 파일")
        print("  3. 네트워크 연결 상태 확인")


async def interactive_demo():
    """대화형 이메일 도구 데모"""

    print("\n🎯 대화형 이메일 작성 데모")
    print("='=" * 20)

    topic = input("📝 이메일 주제를 입력하세요: ").strip()
    if not topic:
        print("❌ 주제가 입력되지 않았습니다.")
        return

    tone = input("🎭 어조를 선택하세요 (professional/friendly/formal/casual): ").strip()
    if not tone:
        tone = "professional"

    recipient_name = input("👤 받는 사람 이름 (선택사항): ").strip()

    try:
        # FastMCP HTTP client - URL을 직접 전달
        async with Client("http://localhost:8000/mcp/") as client:

            print("\n✍️  이메일 작성 중...")
            result = await client.call_tool("compose_email", {
                "topic": topic,
                "tone": tone,
                "recipient_name": recipient_name
            })

            if result.content:
                print("\n📧 작성된 이메일:")
                print("=" * 50)
                print(result.content[0].text)
                print("=" * 50)

                # 이메일 발송 여부 확인
                send_email = input("\n📤 이 이메일을 발송하시겠습니까? (y/N): ").lower().startswith('y')
                if send_email:
                    print("\n📮 발송 정보 입력:")
                    to_email = input("📧 받는 사람 이메일: ").strip()
                    if not to_email:
                        print("❌ 받는 사람 이메일이 입력되지 않았습니다.")
                    else:
                        subject = input("📝 이메일 제목: ").strip()
                        if not subject:
                            subject = f"Re: {topic}"

                        confirm = input(f"\n⚠️  정말로 {to_email}로 발송하시겠습니까? (y/N): ").lower().startswith('y')
                        if confirm:
                            print(f"\n📤 {to_email}로 이메일 발송 중...")
                            send_result = await client.call_tool("send_email", {
                                "to": to_email,
                                "subject": subject,
                                "body": result.content[0].text
                            })
                            print("📧 발송 결과:", send_result.content[0].text)
                        else:
                            print("🔒 발송이 취소되었습니다.")
                else:
                    print("📝 이메일 작성만 완료되었습니다.")
            else:
                print("❌ 이메일 작성에 실패했습니다.")

    except Exception as e:
        print(f"❌ 오류: {e}")


async def main():
    """메인 함수"""
    print("📧 FastMCP Email Tool Client")
    print("=" * 40)
    print()

    # 모드 선택
    print("🎯 사용 모드를 선택하세요:")
    print("  1. 데모 모드 (자동 테스트)")
    print("  2. 대화형 모드 (직접 입력)")
    print()

    choice = input("선택 (1/2): ").strip()

    if choice == "2":
        await interactive_demo()
    else:
        await test_email_tools()

        # 추가 대화형 모드 제안
        if input("\n🎯 대화형 모드도 실행하시겠습니까? (y/N): ").lower().startswith('y'):
            await interactive_demo()

    print("\n✅ 완료!")


if __name__ == "__main__":
    # 환경변수 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY가 설정되지 않았습니다.")
        print("📄 .env 파일을 확인해주세요.")
        print()

    asyncio.run(main())