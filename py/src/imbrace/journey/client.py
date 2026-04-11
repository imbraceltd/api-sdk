from typing import Optional
from ..core.http import HttpTransport, AsyncHttpTransport
from ..core.auth.token_manager import TokenManager
from .resources.workflow import WorkflowResource, AsyncWorkflowResource
from .resources.ai_assistant import AiAssistantResource, AsyncAiAssistantResource
from .resources.apps import AppsResource, AsyncAppsResource
from .resources.boards import BoardsResource, AsyncBoardsResource
from .resources.channel import JourneyChannelResource, AsyncJourneyChannelResource


class JourneyClient:
    """Journey API Client — Developer Portal for building custom apps.

    Auth: x-temp-token header (temp token from Developer Portal)
    Base path: /journeys/api/v1/, /journeys/v1/, /journeys/v2/

    Usage:
        client = JourneyClient(
            temp_token="api_xxx",
            base_url="https://app-gateway.imbrace.co",
        )
        workflow = client.workflow.get("12345", org_id="org_xxx")
        client.ai_assistant.create(name="My Assistant", instructions="...")
    """

    def __init__(
        self,
        temp_token: str,
        base_url: str,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.token_manager = TokenManager()
        self._http = HttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=temp_token,
            token_header="x-temp-token",
        )
        self.workflow = WorkflowResource(self._http, self.base_url)
        self.ai_assistant = AiAssistantResource(self._http, self.base_url)
        self.apps = AppsResource(self._http, self.base_url)
        self.boards = BoardsResource(self._http, self.base_url)
        self.channel = JourneyChannelResource(self._http, self.base_url)

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncJourneyClient:
    """Async Journey API Client."""

    def __init__(
        self,
        temp_token: str,
        base_url: str,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.token_manager = TokenManager()
        self._http = AsyncHttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=temp_token,
            token_header="x-temp-token",
        )
        self.workflow = AsyncWorkflowResource(self._http, self.base_url)
        self.ai_assistant = AsyncAiAssistantResource(self._http, self.base_url)
        self.apps = AsyncAppsResource(self._http, self.base_url)
        self.boards = AsyncBoardsResource(self._http, self.base_url)
        self.channel = AsyncJourneyChannelResource(self._http, self.base_url)

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
