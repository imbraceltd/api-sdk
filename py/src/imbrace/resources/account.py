from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport
from ..types.common import ApiResponse
from ..types.platform import User


class AccountResource:
    """Account domain — Sync.

    @param base - platform service base URL (gateway/platform)
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    def get(self) -> User:
        """Lấy thông tin tài khoản hiện tại."""
        res = self._http.request("GET", f"{self._v1}/account").json()
        # Nếu server trả về ApiResponse bọc ngoài, ta lấy data. 
        # Giả định server trả về trực tiếp dict của User hoặc ApiResponse[User]
        if "data" in res and "success" in res:
            return User(**res["data"])
        return User(**res)

    def update(self, body: Dict[str, Any]) -> User:
        """Cập nhật thông tin tài khoản."""
        res = self._http.request("PUT", f"{self._v1}/account", json=body).json()
        if "data" in res and "success" in res:
            return User(**res["data"])
        return User(**res)


class AsyncAccountResource:
    """Account domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    async def get(self) -> User:
        """Lấy thông tin tài khoản hiện tại (bất đồng bộ)."""
        res = await self._http.request("GET", f"{self._v1}/account")
        data = res.json()
        if "data" in data and "success" in data:
            return User(**data["data"])
        return User(**data)

    async def update(self, body: Dict[str, Any]) -> User:
        """Cập nhật thông tin tài khoản (bất đồng bộ)."""
        res = await self._http.request("PUT", f"{self._v1}/account", json=body)
        data = res.json()
        if "data" in data and "success" in data:
            return User(**data["data"])
        return User(**data)
