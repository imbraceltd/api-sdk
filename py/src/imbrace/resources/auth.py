from typing import Any, Dict
from ..http import HttpTransport, AsyncHttpTransport


class AuthResource:
    """Auth domain — Sync. Login / token / SSO / OIDC.

    @param base - platform service base URL (gateway/platform)
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    @property
    def _gateway(self) -> str:
        # Derive gateway from platform base: "gateway/platform" → "gateway"
        return self._base.removesuffix("/platform")

    # --- Third-party token (API Key generation) ---
    def get_third_party_token(self, expiration_days: int = 10) -> Dict[str, Any]:
        # Requires active access token. "thrid" is a backend typo — preserved intentionally.
        return self._http.request(
            "POST",
            f"{self._gateway}/private/backend/v1/thrid_party_token",
            json={"expirationDays": expiration_days},
        ).json()

    # --- Login ---
    def signin_email_request(self, email: str) -> None:
        self._http.request("POST", f"{self._v1}/login/_signin_email_request", json={"email": email})

    def signin_with_email(self, email: str, otp: str) -> Dict[str, Any]:
        return self._http.request(
            "POST", f"{self._v1}/login/_signin_with_email",
            json={"email": email, "otp": otp},
        ).json()

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        return self._http.request(
            "POST", f"{self._v1}/login/sign_in",
            json={"email": email, "password": password},
        ).json()

    def sign_up(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/login/sign_up", json=body).json()

    def forgot_password(self, email: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v1}/login/forget", params={"email": email}).json()

    def reset_password(self, token: str, password: str) -> Dict[str, Any]:
        return self._http.request(
            "POST", f"{self._v1}/login/forget/reset",
            json={"token": token, "password": password},
        ).json()

    def get_login_providers(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v1}/login/providers").json()

    def signin_sso(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/sso/login-success", json=body).json()

    # --- Access token ---
    def exchange_access_token(self, token: str, organization_id: str) -> Dict[str, Any]:
        return self._http.request(
            "POST", f"{self._v1}/access/_exchange_access_token",
            json={"token": token, "organization_id": organization_id},
        ).json()

    def exchange_access_token_with_token(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request(
            "POST", f"{self._v1}/access/_exchange_access_token_with_access_token",
            json=body,
        ).json()

    def signin_with_identity(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/access/_signin_with_identity", json=body).json()

    # --- Sign-up verification ---
    def verify_sign_up_check(self, email: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v1}/login/sign_up/verify/check", params={"email": email}).json()

    def resend_verification_email(self, email: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v1}/login/sign_up/verify/resend", params={"email": email}).json()

    def upload_sign_up_photo(self, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/login/sign_in/file_up_load", files=files).json()

    # --- SSO / Azure AD ---
    def get_azure_groups(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v1}/sso/azure_ad/groups/all").json()

    # --- OIDC Role Mappings ---
    def list_oidc_role_mappings(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v1}/oidc_role_mappings").json()

    def create_oidc_role_mapping(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/oidc_role_mappings", json=body).json()

    def bulk_update_oidc_role_mappings(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v1}/oidc_role_mappings/bulk", json=body).json()

    # --- Identity ---
    def signup_with_google(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/identity/_signup_google", json=body).json()

    def signin_with_google(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/identity_access/_signin_google", json=body).json()

    def signup_with_email(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/identity/_signup_email", json=body).json()

    def signin_with_email_identity(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/identity_access/_signin_email", json=body).json()

    # --- AWS Marketplace ---
    def resolve_aws_marketplace_customer(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/aws_marketplace/resolve-customer", json=body).json()


class AsyncAuthResource:
    """Auth domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    @property
    def _gateway(self) -> str:
        return self._base.removesuffix("/platform")

    async def get_third_party_token(self, expiration_days: int = 10) -> Dict[str, Any]:
        # Requires active access token. "thrid" is a backend typo — preserved intentionally.
        res = await self._http.request(
            "POST",
            f"{self._gateway}/private/backend/v1/thrid_party_token",
            json={"expirationDays": expiration_days},
        )
        return res.json()

    async def signin_email_request(self, email: str) -> None:
        await self._http.request("POST", f"{self._v1}/login/_signin_email_request", json={"email": email})

    async def signin_with_email(self, email: str, otp: str) -> Dict[str, Any]:
        res = await self._http.request(
            "POST", f"{self._v1}/login/_signin_with_email",
            json={"email": email, "otp": otp},
        )
        return res.json()

    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/login/sign_in", json={"email": email, "password": password})
        return res.json()

    async def sign_up(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/login/sign_up", json=body)
        return res.json()

    async def forgot_password(self, email: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v1}/login/forget", params={"email": email})
        return res.json()

    async def reset_password(self, token: str, password: str) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/login/forget/reset", json={"token": token, "password": password})
        return res.json()

    async def get_login_providers(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v1}/login/providers")
        return res.json()

    async def signin_sso(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/sso/login-success", json=body)
        return res.json()

    async def exchange_access_token(self, token: str, organization_id: str) -> Dict[str, Any]:
        res = await self._http.request(
            "POST", f"{self._v1}/access/_exchange_access_token",
            json={"token": token, "organization_id": organization_id},
        )
        return res.json()

    async def exchange_access_token_with_token(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/access/_exchange_access_token_with_access_token", json=body)
        return res.json()

    async def signin_with_identity(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/access/_signin_with_identity", json=body)
        return res.json()

    async def verify_sign_up_check(self, email: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v1}/login/sign_up/verify/check", params={"email": email})
        return res.json()

    async def resend_verification_email(self, email: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v1}/login/sign_up/verify/resend", params={"email": email})
        return res.json()

    async def upload_sign_up_photo(self, files: Any) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/login/sign_in/file_up_load", files=files)
        return res.json()

    async def get_azure_groups(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v1}/sso/azure_ad/groups/all")
        return res.json()

    async def list_oidc_role_mappings(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v1}/oidc_role_mappings")
        return res.json()

    async def create_oidc_role_mapping(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/oidc_role_mappings", json=body)
        return res.json()

    async def bulk_update_oidc_role_mappings(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v1}/oidc_role_mappings/bulk", json=body)
        return res.json()

    async def signup_with_google(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/identity/_signup_google", json=body)
        return res.json()

    async def signin_with_google(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/identity_access/_signin_google", json=body)
        return res.json()

    async def signup_with_email(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/identity/_signup_email", json=body)
        return res.json()

    async def signin_with_email_identity(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/identity_access/_signin_email", json=body)
        return res.json()

    async def resolve_aws_marketplace_customer(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/aws_marketplace/resolve-customer", json=body)
        return res.json()
