from typing import Any, Dict
from ...core.http import HttpTransport, AsyncHttpTransport


class ChannelServerResource:
    """Channel — Server Gateway.

    Endpoints:
        GET /3rd/channels/{channel_id}
        GET /3rd/organization/{organization_id}/channels/{channel_id}
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def get(self, channel_id: str) -> Dict[str, Any]:
        return self._http.request(
            "GET", f"{self._base}/3rd/channels/{channel_id}"
        ).json()

    def get_by_org(self, organization_id: str, channel_id: str) -> Dict[str, Any]:
        return self._http.request(
            "GET", f"{self._base}/3rd/organization/{organization_id}/channels/{channel_id}"
        ).json()


class AsyncChannelServerResource:
    """Channel — Server Gateway. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def get(self, channel_id: str) -> Dict[str, Any]:
        res = await self._http.request(
            "GET", f"{self._base}/3rd/channels/{channel_id}"
        )
        return res.json()

    async def get_by_org(self, organization_id: str, channel_id: str) -> Dict[str, Any]:
        res = await self._http.request(
            "GET", f"{self._base}/3rd/organization/{organization_id}/channels/{channel_id}"
        )
        return res.json()
