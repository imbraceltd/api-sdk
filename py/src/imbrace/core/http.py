import time
import asyncio
from typing import Optional
import httpx

from .auth.token_manager import TokenManager
from .exceptions import AuthError, ApiError, NetworkError


class HttpTransport:
    """Synchronous HTTP Transport Layer for Imbrace SDK.

    Lớp vận chuyển HTTP với logic retry và xử lý lỗi.
    """
    def __init__(
        self,
        token_manager: TokenManager,
        timeout: int = 30,
        api_key: Optional[str] = None,
        token_header: str = "x-access-token",
    ):
        self.token_manager = token_manager
        self.timeout = timeout
        self.api_key = api_key
        self.token_header = token_header
        self._client = httpx.Client(timeout=timeout)

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

        headers = kwargs.pop("headers", {})
        if self.api_key:
            headers[self.token_header] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers[self.token_header] = token
        kwargs["headers"] = headers

        while True:
            try:
                res = self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:
                    raise AuthError("Invalid or expired access token.")
                if (res.status_code == 429 or res.status_code >= 500) and retries < max_retries:
                    retries += 1
                    time.sleep(2 ** retries)
                    continue
                raise ApiError(res.status_code, res.text)
            except httpx.RequestError as e:
                if retries < max_retries:
                    retries += 1
                    time.sleep(2 ** retries)
                    continue
                raise NetworkError(f"Network error or timeout: {str(e)}")

    def close(self):
        self._client.close()


class AsyncHttpTransport:
    """Asynchronous HTTP Transport Layer for Imbrace SDK.

    Phiên bản bất đồng bộ của HttpTransport với async/await.
    """
    def __init__(
        self,
        token_manager: TokenManager,
        timeout: int = 30,
        api_key: Optional[str] = None,
        token_header: str = "x-access-token",
    ):
        self.token_manager = token_manager
        self.timeout = timeout
        self.api_key = api_key
        self.token_header = token_header
        self._client = httpx.AsyncClient(timeout=timeout)

    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 0
        max_retries = 2

        headers = kwargs.pop("headers", {})
        if self.api_key:
            headers[self.token_header] = self.api_key
        token = self.token_manager.get_token()
        if token:
            headers[self.token_header] = token
        kwargs["headers"] = headers

        while True:
            try:
                res = await self._client.request(method, url, **kwargs)
                if res.status_code < 400:
                    return res
                if res.status_code in [401, 403]:
                    raise AuthError("Invalid or expired access token.")
                if (res.status_code == 429 or res.status_code >= 500) and retries < max_retries:
                    retries += 1
                    await asyncio.sleep(2 ** retries)
                    continue
                raise ApiError(res.status_code, res.text)
            except httpx.RequestError as e:
                if retries < max_retries:
                    retries += 1
                    await asyncio.sleep(2 ** retries)
                    continue
                raise NetworkError(f"Network error or timeout: {str(e)}")

    async def close(self):
        await self._client.aclose()
