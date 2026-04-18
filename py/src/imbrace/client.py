from __future__ import annotations
from typing import Optional, Union
import os
import warnings

from .auth.token_manager import TokenManager
from .http import HttpTransport
from .environments import EnvironmentPreset, ServiceHosts, ENVIRONMENTS
from .service_registry import resolve_service_urls
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
from .resources.campaigns import CampaignsResource
from .resources.data_files import DataFilesResource
from .resources.folders import FoldersResource
from .resources.outbounds import OutboundsResource
from .resources.touchpoints import TouchpointsResource


class ImbraceClient:
    """Synchronous Imbrace SDK Client.

    Usage:
        # Develop environment
        client = ImbraceClient(env="develop", access_token="...")

        # Stable (default)
        client = ImbraceClient(api_key=os.environ["IMBRACE_API_KEY"])

        # Override a single service (e.g. local dev)
        client = ImbraceClient(env="develop", services={"data_board": "http://localhost:3001/data-board"})
    """

    def __init__(
        self,
        env: Optional[Union[str, EnvironmentPreset]] = None,
        gateway: Optional[str] = None,
        services: Optional[dict] = None,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        organization_id: Optional[str] = None,
        timeout: int = 30,
        check_health: bool = False,
        # Legacy compat — takes precedence over env if set
        base_url: Optional[str] = None,
    ):
        # If access_token is explicitly provided, don't fall back to IMBRACE_API_KEY from env
        # — the caller has chosen access_token mode.
        if api_key is not None:
            resolved_key = api_key
        elif access_token is None:
            resolved_key = os.environ.get("IMBRACE_API_KEY")
        else:
            resolved_key = None
        resolved_env = env or os.environ.get("IMBRACE_ENV") or "stable"
        resolved_gateway = base_url or gateway or os.environ.get("IMBRACE_GATEWAY_URL")

        # 1. Collect overrides from environment variables (e.g. IMBRACE_IPS_URL)
        env_services = {}
        service_keys = ["platform", "channel_service", "ips", "data_board", "ai", "marketplaces"]
        for key in service_keys:
            env_val = os.environ.get(f"IMBRACE_{key.upper()}_URL")
            if env_val:
                env_services[key] = env_val

        # 2. Merge environment overrides with explicitly passed services
        merged_services = {**env_services, **(services or {})}

        # Resolve preset
        if resolved_gateway:
            env_name = resolved_env if isinstance(resolved_env, str) else "stable"
            preset = EnvironmentPreset(
                gateway=resolved_gateway.rstrip("/"),
                service_hosts=ENVIRONMENTS[env_name].service_hosts if env_name in ENVIRONMENTS else ServiceHosts(),
            )
        else:
            preset = resolved_env

        urls = resolve_service_urls(preset, merged_services)

        if not resolved_key and not access_token and not os.environ.get("IMBRACE_ACCESS_TOKEN"):
            warnings.warn(
                "ImbraceClient: no credentials provided. "
                "Pass access_token= (user login) or api_key= (server-to-server).",
                UserWarning,
                stacklevel=2,
            )

        self.token_manager = TokenManager(access_token)
        self.http = HttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=resolved_key,
            organization_id=organization_id,
        )

        # Auth & Account → platform service
        self.auth          = AuthResource(self.http, urls.platform)
        self.account       = AccountResource(self.http, urls.platform)

        # Platform group
        self.platform      = PlatformResource(self.http, urls.platform)
        self.organizations = OrganizationsResource(self.http, urls.platform)
        self.teams         = TeamsResource(self.http, urls.platform)
        self.settings      = SettingsResource(self.http, urls.channel_service, urls.platform)

        # channel-service group
        self.channel       = ChannelResource(self.http, urls.channel_service)
        self.contacts      = ContactsResource(self.http, urls.channel_service)
        self.conversations = ConversationsResource(self.http, urls.channel_service)
        self.messages      = MessagesResource(self.http, urls.channel_service)
        self.categories    = CategoriesResource(self.http, urls.channel_service)

        # Workflows: channel-service (automation) + platform (n8n)
        self.workflows     = WorkflowsResource(self.http, urls.channel_service, urls.platform)

        # Dedicated services
        self.boards        = BoardsResource(self.http, urls.data_board)
        self.ips           = IpsResource(self.http, urls.ips)
        self.ai            = AiResource(self.http, urls.ai)

        # Marketplace: standalone service + platform/v2 sub-paths
        self.marketplace   = MarketplaceResource(self.http, urls.marketplaces, urls.platform)

        # Agent templates + use-cases
        self.agent         = AgentResource(self.http, urls.marketplaces, urls.gateway)

        # Gateway fallback
        self.health        = HealthResource(self.http, urls.gateway)
        self.sessions      = SessionsResource(self.http, urls.gateway)
        self.schedule      = ScheduleResource(self.http, urls.ips)
        self.campaigns     = CampaignsResource(self.http, urls.channel_service)
        self.data_files    = DataFilesResource(self.http, urls.data_board)
        self.folders       = FoldersResource(self.http, urls.data_board)
        self.outbounds     = OutboundsResource(self.http, urls.channel_service)
        self.touchpoints   = TouchpointsResource(self.http, urls.channel_service)

        if check_health:
            self.init()

    # ── Convenience auth ──────────────────────────────────────────────────────

    def login(self, email: str, password: str) -> dict:
        """Login bằng email/password, tự lưu access token vào client."""
        res = self.auth.sign_in(email, password)
        token = res.get("accessToken") or res.get("token") or res.get("access_token")
        if token:
            self.set_access_token(token)
        return res

    def login_with_otp(self, email: str, otp: str) -> dict:
        """Login bằng OTP (sau khi gọi request_otp), tự lưu access token."""
        res = self.auth.signin_with_email(email, otp)
        token = res.get("accessToken") or res.get("token") or res.get("access_token")
        if token:
            self.set_access_token(token)
        return res

    def request_otp(self, email: str) -> None:
        """Gửi OTP về email. Dùng trước login_with_otp()."""
        self.auth.signin_email_request(email)

    def set_access_token(self, token: str) -> None:
        self.token_manager.set_token(token)
        self.http.api_key = None  # Explicit access_token call switches off api_key mode

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
