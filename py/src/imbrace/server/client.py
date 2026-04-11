from typing import Optional
from ..core.http import HttpTransport, AsyncHttpTransport
from ..core.auth.token_manager import TokenManager
from .resources.boards import BoardsResource, AsyncBoardsResource
from .resources.ai_agent import AiAgentResource, AsyncAiAgentResource
from .resources.categories import CategoriesResource, AsyncCategoriesResource
from .resources.schedule import ScheduleResource, AsyncScheduleResource
from .resources.marketplace import MarketplaceResource, AsyncMarketplaceResource
from .resources.channel import ChannelServerResource, AsyncChannelServerResource
from .resources.conversation import ConversationServerResource, AsyncConversationServerResource


class ServerGatewayClient:
    """Server Gateway Client — Private APIs for server-to-server integration.

    Auth: API Key via x-access-token header
    Base path: /3rd/

    Usage:
        client = ServerGatewayClient(
            api_key="api_xxx",
            base_url="https://app-gateway.imbrace.co",
        )
        results = client.boards.search("brd_xxx", q="keyword")
        client.boards.create_items("brd_xxx", items=[{"fields": [...]}])
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.token_manager = TokenManager()
        self._http = HttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=api_key,
            token_header="x-access-token",
        )
        self.boards = BoardsResource(self._http, self.base_url)
        self.ai_agent = AiAgentResource(self._http, self.base_url)
        self.categories = CategoriesResource(self._http, self.base_url)
        self.schedule = ScheduleResource(self._http, self.base_url)
        self.marketplace = MarketplaceResource(self._http, self.base_url)
        self.channel = ChannelServerResource(self._http, self.base_url)
        self.conversation = ConversationServerResource(self._http, self.base_url)

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncServerGatewayClient:
    """Async Server Gateway Client."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.token_manager = TokenManager()
        self._http = AsyncHttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=api_key,
            token_header="x-access-token",
        )
        self.boards = AsyncBoardsResource(self._http, self.base_url)
        self.ai_agent = AsyncAiAgentResource(self._http, self.base_url)
        self.categories = AsyncCategoriesResource(self._http, self.base_url)
        self.schedule = AsyncScheduleResource(self._http, self.base_url)
        self.marketplace = AsyncMarketplaceResource(self._http, self.base_url)
        self.channel = AsyncChannelServerResource(self._http, self.base_url)
        self.conversation = AsyncConversationServerResource(self._http, self.base_url)

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
