from typing import Any, Dict
from ..http import HttpTransport, AsyncHttpTransport


class OrganizationsResource:
    """Organizations domain — Sync.

    @param base - platform service base URL (gateway/platform)
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2"

    def list(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v2}/organizations",
                                  params={"limit": limit, "skip": skip}).json()

    def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/organizations", json=body).json()

    def list_all(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v2}/organizations/_all").json()


class AsyncOrganizationsResource:
    """Organizations domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2"

    async def list(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v2}/organizations",
                                       params={"limit": limit, "skip": skip})
        return res.json()

    async def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/organizations", json=body)
        return res.json()

    async def list_all(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v2}/organizations/_all")
        return res.json()
