from typing import Optional
from ..core.http import HttpTransport, AsyncHttpTransport
from ..core.auth.token_manager import TokenManager
from .resources.auth import AuthResource, AsyncAuthResource
from .resources.account import AccountResource, AsyncAccountResource
from .resources.organizations import OrganizationsResource, AsyncOrganizationsResource
from .resources.agent import AgentResource, AsyncAgentResource
from .resources.channel import ChannelResource, AsyncChannelResource
from .resources.conversations import ConversationsResource, AsyncConversationsResource
from .resources.messages import MessagesResource, AsyncMessagesResource
from .resources.contacts import ContactsResource, AsyncContactsResource
from .resources.teams import TeamsResource, AsyncTeamsResource
from .resources.workflows import WorkflowsResource, AsyncWorkflowsResource
from .resources.boards import BoardsResource, AsyncBoardsResource
from .resources.settings import SettingsResource, AsyncSettingsResource
from .resources.ai import AiResource, AsyncAiResource
from .resources.health import HealthResource, AsyncHealthResource
from .resources.sessions import SessionsResource, AsyncSessionsResource


class AppGatewayClient:
    """App Gateway Client — Public APIs for client applications.

    Auth: OTP-based (email → OTP → access_token)
    Base path: /v1/backend/, /v2/backend/, /v3/backend/

    Usage:
        client = AppGatewayClient(base_url="https://app-gateway.imbrace.co")
        # Step 1: request OTP
        client.auth.signin_email_request("user@example.com")
        # Step 2: verify OTP
        result = client.auth.signin_with_email("user@example.com", "123456")
        # Step 3: exchange token
        token = client.auth.exchange_access_token(result["token"], org_id)
        client.set_access_token(token["access_token"])
        # Now use other resources
        boards = client.boards.list()
    """

    def __init__(
        self,
        base_url: str,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.token_manager = TokenManager(access_token)
        self._http = HttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=api_key,
            token_header="x-access-token",
        )
        self.auth = AuthResource(self._http, self.base_url)
        self.account = AccountResource(self._http, self.base_url)
        self.organizations = OrganizationsResource(self._http, self.base_url)
        self.agent = AgentResource(self._http, self.base_url)
        self.channel = ChannelResource(self._http, self.base_url)
        self.conversations = ConversationsResource(self._http, self.base_url)
        self.messages = MessagesResource(self._http, self.base_url)
        self.contacts = ContactsResource(self._http, self.base_url)
        self.teams = TeamsResource(self._http, self.base_url)
        self.workflows = WorkflowsResource(self._http, self.base_url)
        self.boards = BoardsResource(self._http, self.base_url)
        self.settings = SettingsResource(self._http, self.base_url)
        self.ai = AiResource(self._http, self.base_url)
        self.health = HealthResource(self._http, self.base_url)
        self.sessions = SessionsResource(self._http, self.base_url)

    def set_access_token(self, token: str) -> None:
        self.token_manager.set_token(token)

    def clear_access_token(self) -> None:
        self.token_manager.clear()

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncAppGatewayClient:
    """Async App Gateway Client."""

    def __init__(
        self,
        base_url: str,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.token_manager = TokenManager(access_token)
        self._http = AsyncHttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=api_key,
            token_header="x-access-token",
        )
        self.auth = AsyncAuthResource(self._http, self.base_url)
        self.account = AsyncAccountResource(self._http, self.base_url)
        self.organizations = AsyncOrganizationsResource(self._http, self.base_url)
        self.agent = AsyncAgentResource(self._http, self.base_url)
        self.channel = AsyncChannelResource(self._http, self.base_url)
        self.conversations = AsyncConversationsResource(self._http, self.base_url)
        self.messages = AsyncMessagesResource(self._http, self.base_url)
        self.contacts = AsyncContactsResource(self._http, self.base_url)
        self.teams = AsyncTeamsResource(self._http, self.base_url)
        self.workflows = AsyncWorkflowsResource(self._http, self.base_url)
        self.boards = AsyncBoardsResource(self._http, self.base_url)
        self.settings = AsyncSettingsResource(self._http, self.base_url)
        self.ai = AsyncAiResource(self._http, self.base_url)
        self.health = AsyncHealthResource(self._http, self.base_url)
        self.sessions = AsyncSessionsResource(self._http, self.base_url)

    def set_access_token(self, token: str) -> None:
        self.token_manager.set_token(token)

    def clear_access_token(self) -> None:
        self.token_manager.clear()

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
