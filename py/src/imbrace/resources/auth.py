from typing import Any, Dict
from ..http import HttpTransport, AsyncHttpTransport


class AuthResource:
    """Auth domain — Sync. Third-party token + OTP login flow."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def get_third_party_token(self, expiration_days: int = 10) -> Dict[str, Any]:
        return self._http.request(
            "POST",
            f"{self._base}/private/backend/v1/thrid_party_token",
            json={"expirationDays": expiration_days},
        ).json()

    def signin_email_request(self, email: str) -> Dict[str, Any]:
        """Bước 1 — Gửi OTP về email."""
        return self._http.request(
            "POST",
            f"{self._base}/v1/backend/login/_signin_email_request",
            json={"email": email},
        ).json()

    def signin_with_email(self, email: str, otp: str) -> Dict[str, Any]:
        """Bước 2 — Xác thực OTP, nhận login token."""
        return self._http.request(
            "POST",
            f"{self._base}/v1/login/_signin_with_email",
            json={"email": email, "otp": otp},
        ).json()

    def exchange_access_token(self, login_token: str, organization_id: str) -> Dict[str, Any]:
        """Bước 3 — Đổi login token lấy access token của org."""
        return self._http.request(
            "POST",
            f"{self._base}/v1/backend/access/_exchange_access_token",
            json={"token": login_token, "organization_id": organization_id},
        ).json()


class AsyncAuthResource:
    """Auth domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def get_third_party_token(self, expiration_days: int = 10) -> Dict[str, Any]:
        res = await self._http.request(
            "POST",
            f"{self._base}/private/backend/v1/thrid_party_token",
            json={"expirationDays": expiration_days},
        )
        return res.json()

    async def signin_email_request(self, email: str) -> Dict[str, Any]:
        res = await self._http.request(
            "POST",
            f"{self._base}/v1/backend/login/_signin_email_request",
            json={"email": email},
        )
        return res.json()

    async def signin_with_email(self, email: str, otp: str) -> Dict[str, Any]:
        res = await self._http.request(
            "POST",
            f"{self._base}/v1/login/_signin_with_email",
            json={"email": email, "otp": otp},
        )
        return res.json()

    async def exchange_access_token(self, login_token: str, organization_id: str) -> Dict[str, Any]:
        res = await self._http.request(
            "POST",
            f"{self._base}/v1/backend/access/_exchange_access_token",
            json={"token": login_token, "organization_id": organization_id},
        )
        return res.json()
