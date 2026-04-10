from typing import Optional
import os
from .auth.token_manager import TokenManager
from .http import AsyncHttpTransport
from .resources.auth import AsyncAuthResource
from .resources.account import AsyncAccountResource
from .resources.organizations import AsyncOrganizationsResource
from .resources.agent import AsyncAgentResource
from .resources.channel import AsyncChannelResource
from .resources.conversations import AsyncConversationsResource
from .resources.messages import AsyncMessagesResource
from .resources.contacts import AsyncContactsResource
from .resources.teams import AsyncTeamsResource
from .resources.workflows import AsyncWorkflowsResource
from .resources.boards import AsyncBoardsResource
from .resources.settings import AsyncSettingsResource
from .resources.ai import AsyncAiResource
from .resources.marketplace import AsyncMarketplaceResource
from .resources.platform import AsyncPlatformResource
from .resources.ips import AsyncIpsResource
from .resources.health import AsyncHealthResource
from .resources.sessions import AsyncSessionsResource
from .resources.categories import AsyncCategoriesResource
from .resources.schedule import AsyncScheduleResource

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class AsyncImbraceClient:
    """Asynchronous Imbrace SDK Client.

    Usage:
        async with AsyncImbraceClient() as client:
            account = await client.account.get()
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30,
        check_health: bool = False,
    ):
        resolved_key = api_key or os.environ.get("IMBRACE_API_KEY")
        resolved_url = (
            base_url
            or os.environ.get("IMBRACE_BASE_URL")
            or "https://app-gatewayv2.imbrace.co"
        )
        self.base_url = resolved_url.rstrip("/")
        self._check_health = check_health
        self.token_manager = TokenManager(access_token)
        self.http = AsyncHttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=resolved_key,
        )
        self.auth = AsyncAuthResource(self.http, self.base_url)
        self.account = AsyncAccountResource(self.http, self.base_url)
        self.organizations = AsyncOrganizationsResource(self.http, self.base_url)
        self.agent = AsyncAgentResource(self.http, self.base_url)
        self.channel = AsyncChannelResource(self.http, self.base_url)
        self.conversations = AsyncConversationsResource(self.http, self.base_url)
        self.messages = AsyncMessagesResource(self.http, self.base_url)
        self.contacts = AsyncContactsResource(self.http, self.base_url)
        self.teams = AsyncTeamsResource(self.http, self.base_url)
        self.workflows = AsyncWorkflowsResource(self.http, self.base_url)
        self.boards = AsyncBoardsResource(self.http, self.base_url)
        self.settings = AsyncSettingsResource(self.http, self.base_url)
        self.ai = AsyncAiResource(self.http, self.base_url)
        self.marketplace = AsyncMarketplaceResource(self.http, self.base_url)
        self.platform = AsyncPlatformResource(self.http, self.base_url)
        self.ips = AsyncIpsResource(self.http, self.base_url)
        self.sessions = AsyncSessionsResource(self.http, self.base_url)
        self.health = AsyncHealthResource(self.http, self.base_url)
        self.categories = AsyncCategoriesResource(self.http, self.base_url)
        self.schedule = AsyncScheduleResource(self.http, self.base_url)

    def set_access_token(self, token: str) -> None:
        self.token_manager.set_token(token)

    def clear_access_token(self) -> None:
        self.token_manager.clear()

    async def init(self) -> None:
        await self.health.check()

    async def close(self) -> None:
        await self.http.close()

    async def __aenter__(self):
        if self._check_health:
            await self.init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
