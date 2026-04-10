import asyncio
import os
from dotenv import load_dotenv
from imbrace import AsyncImbraceClient, AuthError, NetworkError

load_dotenv()

async def main():
    async with AsyncImbraceClient(
        base_url=os.getenv("IMBRACE_BASE_URL", "http://localhost:4096"),
        api_key=os.getenv("IMBRACE_API_KEY", ""),
        check_health=True,
    ) as client:
        try:
            session = await client.sessions.create(directory=os.getcwd())
            session_id = session["id"]
            print(f"Created session: {session_id}")

            response = await client.messages.send(
                session_id,
                parts=[{"type": "text", "text": "Explain asyncio in Python"}],
            )
            print("Response:", response)

            # Dynamic token update (e.g. after OAuth refresh)
            client.set_access_token("refreshed-token-here")

        except AuthError as e:
            print(f"Authentication failed: {e}")
        except NetworkError as e:
            print(f"Network error: {e}")

asyncio.run(main())
