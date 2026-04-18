"""
Imbrace Python SDK — Async demo (dùng với FastAPI / asyncio)
Chạy: python examples/async_demo.py
"""
import asyncio
from dotenv import load_dotenv
from imbrace import AsyncImbraceClient, AuthError, NetworkError

load_dotenv()


async def main():
    async with AsyncImbraceClient(check_health=True) as client:
        try:
            # ── Platform ──────────────────────────────────────────────────────
            me = await client.platform.get_me()
            print("Me:", me)

            # ── Marketplace ───────────────────────────────────────────────────
            products = await client.marketplace.list_products(limit=5)
            print("Products:", products)

            # ── Channel ───────────────────────────────────────────────────────
            channels = await client.channel.list_channels()
            print("Channels:", channels)

            # ── IPS ───────────────────────────────────────────────────────────
            profile = await client.ips.get_my_profile()
            print("Profile:", profile)

            # ── Agent ─────────────────────────────────────────────────────────
            run = await client.agent.run_agent(
                agent_id="agent_123",
                input={"task": "Analyze sales data for Q1 2025"},
            )
            print("Agent Run:", run)

            # ── AI Streaming ──────────────────────────────────────────────────
            print("AI Streaming:")
            async for chunk in client.ai.stream(
                model="gpt-4o",
                messages=[{"role": "user", "content": "Say hello in 3 languages."}],
            ):
                content = chunk["choices"][0]["delta"].get("content", "")
                print(content, end="", flush=True)
            print()

        except AuthError as e:
            print(f"Auth failed: {e}")
        except NetworkError as e:
            print(f"Network error: {e}")


asyncio.run(main())
