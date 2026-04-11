import os
from typing import Optional

from .app.client import AppGatewayClient, AsyncAppGatewayClient
from .server.client import ServerGatewayClient, AsyncServerGatewayClient
from .journey.client import JourneyClient, AsyncJourneyClient

# Auto-load .env nếu có python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

_DEFAULT_BASE_URL = "https://app-gateway.imbrace.co"


class ImbraceClient:
    """Unified Imbrace SDK Client.

    Cung cấp truy cập đến cả 3 gateway thông qua một entry point duy nhất.

    Usage:
        client = ImbraceClient(
            app_base_url="https://app-gateway.imbrace.co",
            server_api_key="api_xxx",
        )
        # App Gateway — OTP auth
        client.app.auth.signin_email_request("user@example.com")
        client.app.boards.list()

        # Server Gateway — API Key auth
        client.server.boards.search("brd_xxx", q="keyword")
        client.server.boards.create_items("brd_xxx", items=[...])

        # Journey API — temp token auth
        client.journey.workflow.get("12345", org_id="org_xxx")
        client.journey.ai_assistant.list()
    """

    def __init__(
        self,
        # App Gateway
        app_base_url: Optional[str] = None,
        app_access_token: Optional[str] = None,
        app_api_key: Optional[str] = None,
        # Server Gateway
        server_base_url: Optional[str] = None,
        server_api_key: Optional[str] = None,
        # Journey API
        journey_base_url: Optional[str] = None,
        journey_temp_token: Optional[str] = None,
        # Shared
        timeout: int = 30,
    ):
        resolved_app_url = (app_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_server_url = (server_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_journey_url = (journey_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_server_key = server_api_key or os.environ.get("IMBRACE_API_KEY") or ""
        resolved_journey_token = journey_temp_token or os.environ.get("IMBRACE_TEMP_TOKEN") or ""

        self.app = AppGatewayClient(
            base_url=resolved_app_url,
            access_token=app_access_token,
            api_key=app_api_key,
            timeout=timeout,
        )
        self.server = ServerGatewayClient(
            api_key=resolved_server_key,
            base_url=resolved_server_url,
            timeout=timeout,
        )
        self.journey = JourneyClient(
            temp_token=resolved_journey_token,
            base_url=resolved_journey_url,
            timeout=timeout,
        )

    def close(self) -> None:
        self.app.close()
        self.server.close()
        self.journey.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncImbraceClient:
    """Async Unified Imbrace SDK Client."""

    def __init__(
        self,
        app_base_url: Optional[str] = None,
        app_access_token: Optional[str] = None,
        app_api_key: Optional[str] = None,
        server_base_url: Optional[str] = None,
        server_api_key: Optional[str] = None,
        journey_base_url: Optional[str] = None,
        journey_temp_token: Optional[str] = None,
        timeout: int = 30,
    ):
        resolved_app_url = (app_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_server_url = (server_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_journey_url = (journey_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_server_key = server_api_key or os.environ.get("IMBRACE_API_KEY") or ""
        resolved_journey_token = journey_temp_token or os.environ.get("IMBRACE_TEMP_TOKEN") or ""

        self.app = AsyncAppGatewayClient(
            base_url=resolved_app_url,
            access_token=app_access_token,
            api_key=app_api_key,
            timeout=timeout,
        )
        self.server = AsyncServerGatewayClient(
            api_key=resolved_server_key,
            base_url=resolved_server_url,
            timeout=timeout,
        )
        self.journey = AsyncJourneyClient(
            temp_token=resolved_journey_token,
            base_url=resolved_journey_url,
            timeout=timeout,
        )

    async def close(self) -> None:
        await self.app.close()
        await self.server.close()
        await self.journey.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
