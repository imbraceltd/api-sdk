from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict
from ..http import HttpTransport, AsyncHttpTransport


class SignInResponse(TypedDict):
    accessToken: str
    token: Optional[str]
    userId: Optional[str]
    email: Optional[str]


class SignUpInput(TypedDict, total=False):
    email: str
    password: str
    name: str
    organizationName: str


class SignUpResponse(TypedDict):
    userId: str
    email: str


class ForgotPasswordResponse(TypedDict):
    message: str


class LoginProvider(TypedDict):
    name: str
    type: str
    url: Optional[str]


class LoginProvidersResponse(TypedDict):
    providers: List[LoginProvider]


class OtpSignInResponse(TypedDict):
    token: str
    email: str
    expired_at: str


class ExchangeTokenResponse(TypedDict):
    access_token: str


class VerifySignUpResponse(TypedDict):
    verified: bool
    email: str


class AzureGroup(TypedDict):
    id: str
    displayName: str


class AzureGroupsResponse(TypedDict):
    groups: List[AzureGroup]


class OidcRoleMapping(TypedDict):
    _id: str
    role: str
    claim: str
    value: str


class OidcRoleMappingInput(TypedDict):
    role: str
    claim: str
    value: str


class GoogleAuthResponse(TypedDict):
    accessToken: str
    userId: str
    email: Optional[str]


class AwsMarketplaceResponse(TypedDict):
    customerId: str
    productCode: str


class AuthResource:
    """Auth domain — Sync. Login / token / SSO / OIDC."""

    def __init__(self, http: HttpTransport, base: str, gateway: str):
        self._http = http
        self._base = base.rstrip("/")
        self._gateway = gateway.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    # --- Third-party token (API Key generation) ---
    def get_third_party_token(self, expiration_days: int = 10) -> Dict[str, Any]:
        # Path typo is in the backend and intentionally preserved.
        return self._http.request(
            "POST",
            f"{self._gateway}/private/backend/v1/thrid_party_token",
            json={"expirationDays": expiration_days},
        ).json()

    # --- Login ---
    def signin_email_request(self, email: str) -> None:
        self._http.request("POST", f"{self._v1}/login/_signin_email_request", json={"email": email})

    def signin_with_email(self, email: str, otp: str) -> OtpSignInResponse:
        return self._http.request(
            "POST", f"{self._v1}/login/_signin_with_email",
            json={"email": email, "otp": otp},
        ).json()

    def sign_in(self, email: str, password: str) -> SignInResponse:
        return self._http.request(
            "POST", f"{self._v1}/login/sign_in",
            json={"email": email, "password": password},
        ).json()

    def sign_up(self, body: SignUpInput) -> SignUpResponse:
        return self._http.request("POST", f"{self._v1}/login/sign_up", json=body).json()

    def forgot_password(self, email: str) -> ForgotPasswordResponse:
        return self._http.request("GET", f"{self._v1}/login/forget", params={"email": email}).json()

    def reset_password(self, token: str, password: str) -> ForgotPasswordResponse:
        return self._http.request(
            "POST", f"{self._v1}/login/forget/reset",
            json={"token": token, "password": password},
        ).json()

    def get_login_providers(self) -> LoginProvidersResponse:
        return self._http.request("GET", f"{self._v1}/login/providers").json()

    def signin_sso(self, body: Dict[str, Any]) -> SignInResponse:
        return self._http.request("POST", f"{self._v1}/sso/login-success", json=body).json()

    # --- Access token ---
    def exchange_access_token(self, token: str, organization_id: str) -> ExchangeTokenResponse:
        return self._http.request(
            "POST", f"{self._v1}/access/_exchange_access_token",
            json={"token": token, "organization_id": organization_id},
        ).json()

    def exchange_access_token_with_token(self, body: Dict[str, Any]) -> ExchangeTokenResponse:
        return self._http.request(
            "POST", f"{self._v1}/access/_exchange_access_token_with_access_token",
            json=body,
        ).json()

    def signin_with_identity(self, body: Dict[str, Any]) -> SignInResponse:
        return self._http.request("POST", f"{self._v1}/access/_signin_with_identity", json=body).json()

    # --- Sign-up verification ---
    def verify_sign_up_check(self, email: str) -> VerifySignUpResponse:
        return self._http.request("GET", f"{self._v1}/login/sign_up/verify/check", params={"email": email}).json()

    def resend_verification_email(self, email: str) -> ForgotPasswordResponse:
        return self._http.request("GET", f"{self._v1}/login/sign_up/verify/resend", params={"email": email}).json()

    def upload_sign_up_photo(self, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/login/sign_in/file_up_load", files=files).json()

    # --- SSO / Azure AD ---
    def get_azure_groups(self) -> AzureGroupsResponse:
        return self._http.request("GET", f"{self._v1}/sso/azure_ad/groups/all").json()

    # --- OIDC Role Mappings ---
    def list_oidc_role_mappings(self) -> List[OidcRoleMapping]:
        return self._http.request("GET", f"{self._v1}/oidc_role_mappings").json()

    def create_oidc_role_mapping(self, body: OidcRoleMappingInput) -> OidcRoleMapping:
        return self._http.request("POST", f"{self._v1}/oidc_role_mappings", json=body).json()

    def bulk_update_oidc_role_mappings(self, body: Dict[str, Any]) -> List[OidcRoleMapping]:
        return self._http.request("PUT", f"{self._v1}/oidc_role_mappings/bulk", json=body).json()

    # --- Identity ---
    def signup_with_google(self, body: Dict[str, Any]) -> GoogleAuthResponse:
        return self._http.request("POST", f"{self._v1}/identity/_signup_google", json=body).json()

    def signin_with_google(self, body: Dict[str, Any]) -> GoogleAuthResponse:
        return self._http.request("POST", f"{self._v1}/identity_access/_signin_google", json=body).json()

    def signup_with_email(self, body: Dict[str, Any]) -> SignUpResponse:
        return self._http.request("POST", f"{self._v1}/identity/_signup_email", json=body).json()

    def signin_with_email_identity(self, body: Dict[str, Any]) -> SignInResponse:
        return self._http.request("POST", f"{self._v1}/identity_access/_signin_email", json=body).json()

    # --- AWS Marketplace ---
    def resolve_aws_marketplace_customer(self, body: Dict[str, Any]) -> AwsMarketplaceResponse:
        return self._http.request("POST", f"{self._v1}/aws_marketplace/resolve-customer", json=body).json()


class AsyncAuthResource:
    """Auth domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str, gateway: str):
        self._http = http
        self._base = base.rstrip("/")
        self._gateway = gateway.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    async def get_third_party_token(self, expiration_days: int = 10) -> Dict[str, Any]:
        # Path typo is in the backend and intentionally preserved.
        res = await self._http.request(
            "POST",
            f"{self._gateway}/private/backend/v1/thrid_party_token",
            json={"expirationDays": expiration_days},
        )
        return res.json()

    async def signin_email_request(self, email: str) -> None:
        await self._http.request("POST", f"{self._v1}/login/_signin_email_request", json={"email": email})

    async def signin_with_email(self, email: str, otp: str) -> OtpSignInResponse:
        res = await self._http.request(
            "POST", f"{self._v1}/login/_signin_with_email",
            json={"email": email, "otp": otp},
        )
        return res.json()

    async def sign_in(self, email: str, password: str) -> SignInResponse:
        res = await self._http.request("POST", f"{self._v1}/login/sign_in", json={"email": email, "password": password})
        return res.json()

    async def sign_up(self, body: SignUpInput) -> SignUpResponse:
        res = await self._http.request("POST", f"{self._v1}/login/sign_up", json=body)
        return res.json()

    async def forgot_password(self, email: str) -> ForgotPasswordResponse:
        res = await self._http.request("GET", f"{self._v1}/login/forget", params={"email": email})
        return res.json()

    async def reset_password(self, token: str, password: str) -> ForgotPasswordResponse:
        res = await self._http.request("POST", f"{self._v1}/login/forget/reset", json={"token": token, "password": password})
        return res.json()

    async def get_login_providers(self) -> LoginProvidersResponse:
        res = await self._http.request("GET", f"{self._v1}/login/providers")
        return res.json()

    async def signin_sso(self, body: Dict[str, Any]) -> SignInResponse:
        res = await self._http.request("POST", f"{self._v1}/sso/login-success", json=body)
        return res.json()

    async def exchange_access_token(self, token: str, organization_id: str) -> ExchangeTokenResponse:
        res = await self._http.request(
            "POST", f"{self._v1}/access/_exchange_access_token",
            json={"token": token, "organization_id": organization_id},
        )
        return res.json()

    async def exchange_access_token_with_token(self, body: Dict[str, Any]) -> ExchangeTokenResponse:
        res = await self._http.request("POST", f"{self._v1}/access/_exchange_access_token_with_access_token", json=body)
        return res.json()

    async def signin_with_identity(self, body: Dict[str, Any]) -> SignInResponse:
        res = await self._http.request("POST", f"{self._v1}/access/_signin_with_identity", json=body)
        return res.json()

    async def verify_sign_up_check(self, email: str) -> VerifySignUpResponse:
        res = await self._http.request("GET", f"{self._v1}/login/sign_up/verify/check", params={"email": email})
        return res.json()

    async def resend_verification_email(self, email: str) -> ForgotPasswordResponse:
        res = await self._http.request("GET", f"{self._v1}/login/sign_up/verify/resend", params={"email": email})
        return res.json()

    async def upload_sign_up_photo(self, files: Any) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/login/sign_in/file_up_load", files=files)
        return res.json()

    async def get_azure_groups(self) -> AzureGroupsResponse:
        res = await self._http.request("GET", f"{self._v1}/sso/azure_ad/groups/all")
        return res.json()

    async def list_oidc_role_mappings(self) -> List[OidcRoleMapping]:
        res = await self._http.request("GET", f"{self._v1}/oidc_role_mappings")
        return res.json()

    async def create_oidc_role_mapping(self, body: OidcRoleMappingInput) -> OidcRoleMapping:
        res = await self._http.request("POST", f"{self._v1}/oidc_role_mappings", json=body)
        return res.json()

    async def bulk_update_oidc_role_mappings(self, body: Dict[str, Any]) -> List[OidcRoleMapping]:
        res = await self._http.request("PUT", f"{self._v1}/oidc_role_mappings/bulk", json=body)
        return res.json()

    async def signup_with_google(self, body: Dict[str, Any]) -> GoogleAuthResponse:
        res = await self._http.request("POST", f"{self._v1}/identity/_signup_google", json=body)
        return res.json()

    async def signin_with_google(self, body: Dict[str, Any]) -> GoogleAuthResponse:
        res = await self._http.request("POST", f"{self._v1}/identity_access/_signin_google", json=body)
        return res.json()

    async def signup_with_email(self, body: Dict[str, Any]) -> SignUpResponse:
        res = await self._http.request("POST", f"{self._v1}/identity/_signup_email", json=body)
        return res.json()

    async def signin_with_email_identity(self, body: Dict[str, Any]) -> SignInResponse:
        res = await self._http.request("POST", f"{self._v1}/identity_access/_signin_email", json=body)
        return res.json()

    async def resolve_aws_marketplace_customer(self, body: Dict[str, Any]) -> AwsMarketplaceResponse:
        res = await self._http.request("POST", f"{self._v1}/aws_marketplace/resolve-customer", json=body)
        return res.json()
