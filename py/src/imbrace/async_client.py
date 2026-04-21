from __future__ import annotations
from typing import Optional, Union
import warnings

from .auth.token_manager import TokenManager
from .http import AsyncHttpTransport
from .environments import EnvironmentPreset, ServiceHosts, ENVIRONMENTS
from .service_registry import resolve_service_urls
from .resources.auth import AsyncAuthResource, SignInResponse, OtpSignInResponse
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
from .resources.campaigns import AsyncCampaignsResource
from .resources.data_files import AsyncDataFilesResource
from .resources.folders import AsyncFoldersResource
from .resources.outbounds import AsyncOutboundsResource
from .resources.touchpoints import AsyncTouchpointsResource
from .resources.chat_ai import AsyncChatAiResource
from .resources.file_service import AsyncFileServiceResource
from .resources.activepieces import AsyncActivePiecesResource


class AsyncImbraceClient:
    """Asynchronous Imbrace SDK Client.

    When check_health=True, use as an async context manager so the health
    check can run:

        async with AsyncImbraceClient(api_key="...", check_health=True) as client:
            ...

    Using check_health=True without 'async with' has no effect unless
    you manually call await client.init().

    Usage:
        async with AsyncImbraceClient(env="develop", access_token="...") as client:
            account = await client.account.get()
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
        # Legacy compat
        base_url: Optional[str] = None,
    ):
        resolved_key = api_key
        resolved_env = env or "stable"
        resolved_gateway = base_url or gateway
        merged_services = services or {}

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

        if not resolved_key and not access_token:
            warnings.warn(
                "AsyncImbraceClient: no credentials provided. "
                "Pass access_token= (user login) or api_key= (server-to-server).",
                UserWarning,
                stacklevel=2,
            )

        self._check_health = check_health
        self.token_manager = TokenManager(access_token)
        self.http = AsyncHttpTransport(
            token_manager=self.token_manager,
            timeout=timeout,
            api_key=resolved_key,
            organization_id=organization_id,
        )

        self.auth          = AsyncAuthResource(self.http, urls.platform, urls.gateway)
        self.account       = AsyncAccountResource(self.http, urls.platform)
        self.platform      = AsyncPlatformResource(self.http, urls.platform, urls.backend)
        self.organizations = AsyncOrganizationsResource(self.http, urls.platform)
        self.teams         = AsyncTeamsResource(self.http, urls.platform, urls.backend)
        self.settings      = AsyncSettingsResource(self.http, urls.channel_service, urls.platform)

        self.channel       = AsyncChannelResource(self.http, urls.channel_service)
        self.contacts      = AsyncContactsResource(self.http, urls.channel_service)
        self.conversations = AsyncConversationsResource(self.http, urls.channel_service)
        self.messages      = AsyncMessagesResource(self.http, urls.channel_service, urls.backend)
        self.categories    = AsyncCategoriesResource(self.http, urls.channel_service)
        self.workflows     = AsyncWorkflowsResource(self.http, urls.channel_service, urls.platform)

        self.boards        = AsyncBoardsResource(self.http, urls.data_board, urls.backend)
        self.ips           = AsyncIpsResource(self.http, urls.ips)
        self.ai            = AsyncAiResource(self.http, urls.ai)
        self.marketplace   = AsyncMarketplaceResource(self.http, urls.marketplaces)
        self.agent         = AsyncAgentResource(self.http, urls.marketplaces, urls.gateway)

        self.health        = AsyncHealthResource(self.http, urls.gateway)
        self.sessions      = AsyncSessionsResource(self.http, urls.gateway)
        self.schedule      = AsyncScheduleResource(self.http, urls.ips)
        self.campaigns     = AsyncCampaignsResource(self.http, urls.channel_service)
        self.data_files    = AsyncDataFilesResource(self.http, urls.data_board)
        self.folders       = AsyncFoldersResource(self.http, urls.data_board)
        self.outbounds     = AsyncOutboundsResource(self.http, urls.channel_service)
        self.touchpoints   = AsyncTouchpointsResource(self.http, urls.channel_service)

        # New services
        self.chat_ai       = AsyncChatAiResource(self.http, f"{urls.ai}/v3")
        self.file_service  = AsyncFileServiceResource(self.http, urls.file_service)    
        self.activepieces  = AsyncActivePiecesResource(self.http, urls.activepieces)
        # —— Convenience auth

    async def login(self, email: str, password: str) -> dict:
        """Sign in with email and password. Stores the returned access token on the client."""
        res = await self.auth.sign_in(email, password)
        token = res.get("accessToken") or res.get("token") or res.get("access_token")
        if token:
            self.set_access_token(token)
        return res

    async def login_with_otp(self, email: str, otp: str) -> dict:
        """Sign in with an OTP code (call request_otp() first). Stores the returned access token."""
        res = await self.auth.signin_with_email(email, otp)
        token = res.get("accessToken") or res.get("token") or res.get("access_token")
        if token:
            self.set_access_token(token)
        return res

    async def request_otp(self, email: str) -> None:
        """Send a one-time password to the given email address."""
        await self.auth.signin_email_request(email)

    def set_access_token(self, token: str) -> None:
        self.token_manager.set_token(token)
        self.http.clear_api_key()

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
