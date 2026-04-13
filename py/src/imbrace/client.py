import os
from typing import Optional

from .app.client import AppGatewayClient, AsyncAppGatewayClient
from .server.client import ServerGatewayClient, AsyncServerGatewayClient

# Auto-load .env nếu có python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

_DEFAULT_BASE_URL = "https://app-gateway.imbrace.co"


class ImbraceClient:
    """Unified Imbrace SDK Client.

    Cung cấp truy cập đến App Gateway và Server Gateway.

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
        # Shared
        timeout: int = 30,
    ):
        resolved_app_url = (app_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_server_url = (server_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_server_key = server_api_key or os.environ.get("IMBRACE_API_KEY") or ""

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

    def close(self) -> None:
        self.app.close()
        self.server.close()

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
        timeout: int = 30,
    ):
        resolved_app_url = (app_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_server_url = (server_base_url or os.environ.get("IMBRACE_BASE_URL") or _DEFAULT_BASE_URL)
        resolved_server_key = server_api_key or os.environ.get("IMBRACE_API_KEY") or ""

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

    async def close(self) -> None:
        await self.app.close()
        await self.server.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
