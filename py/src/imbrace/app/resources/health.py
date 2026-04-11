from typing import Any
from ...core.http import HttpTransport, AsyncHttpTransport


class HealthResource:
    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def check(self) -> Any:
        return self._http.request("GET", f"{self._base}/global/health").json()


class AsyncHealthResource:
    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def check(self) -> Any:
        res = await self._http.request("GET", f"{self._base}/global/health")
        return res.json()
