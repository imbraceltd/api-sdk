from typing import Optional
import os
from .auth.token_manager import TokenManager
from .http import HttpTransport
from .resources.auth import AuthResource
from .resources.account import AccountResource
from .resources.organizations import OrganizationsResource
from .resources.agent import AgentResource
from .resources.channel import ChannelResource
from .resources.conversations import ConversationsResource
from .resources.messages import MessagesResource
from .resources.contacts import ContactsResource
from .resources.teams import TeamsResource
from .resources.workflows import WorkflowsResource
from .resources.boards import BoardsResource
from .resources.settings import SettingsResource
from .resources.ai import AiResource
from .resources.marketplace import MarketplaceResource
from .resources.platform import PlatformResource
from .resources.ips import IpsResource
from .resources.health import HealthResource
from .resources.sessions import SessionsResource
from .resources.categories import CategoriesResource
from .resources.schedule import ScheduleResource

# Auto-load .env nếu có python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class ImbraceClient:
    """Synchronous Imbrace SDK Client.

    Usage:
        client = ImbraceClient()  # tự động đọc IMBRACE_API_KEY từ .env
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
        self.token_manager = TokenManager(access_token)
        self.http = HttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=resolved_key,
        )
        self.auth = AuthResource(self.http, self.base_url)
        self.account = AccountResource(self.http, self.base_url)
        self.organizations = OrganizationsResource(self.http, self.base_url)
        self.agent = AgentResource(self.http, self.base_url)
        self.channel = ChannelResource(self.http, self.base_url)
        self.conversations = ConversationsResource(self.http, self.base_url)
        self.messages = MessagesResource(self.http, self.base_url)
        self.contacts = ContactsResource(self.http, self.base_url)
        self.teams = TeamsResource(self.http, self.base_url)
        self.workflows = WorkflowsResource(self.http, self.base_url)
        self.boards = BoardsResource(self.http, self.base_url)
        self.settings = SettingsResource(self.http, self.base_url)
        self.ai = AiResource(self.http, self.base_url)
        self.marketplace = MarketplaceResource(self.http, self.base_url)
        self.platform = PlatformResource(self.http, self.base_url)
        self.ips = IpsResource(self.http, self.base_url)
        self.sessions = SessionsResource(self.http, self.base_url)
        self.health = HealthResource(self.http, self.base_url)
        self.categories = CategoriesResource(self.http, self.base_url)
        self.schedule = ScheduleResource(self.http, self.base_url)

        if check_health:
            self.init()

    def set_access_token(self, token: str) -> None:
        self.token_manager.set_token(token)

    def clear_access_token(self) -> None:
        self.token_manager.clear()

    def init(self) -> None:
        self.health.check()

    def close(self) -> None:
        self.http.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
