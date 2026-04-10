from typing import Any, Dict
from ..http import HttpTransport, AsyncHttpTransport


class AccountResource:
    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def get(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/v1/backend/account").json()


class AsyncAccountResource:
    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def get(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/v1/backend/account")
        return res.json()
