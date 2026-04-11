from typing import Any, Dict
from ...core.http import HttpTransport, AsyncHttpTransport


class OrganizationsResource:
    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def list(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        return self._http.request(
            "GET", f"{self._base}/v2/backend/organizations",
            params={"limit": limit, "skip": skip},
        ).json()


class AsyncOrganizationsResource:
    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def list(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request(
            "GET", f"{self._base}/v2/backend/organizations",
            params={"limit": limit, "skip": skip},
        )
        return res.json()
