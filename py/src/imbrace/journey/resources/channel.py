from typing import Any, Dict, Optional
from ...core.http import HttpTransport, AsyncHttpTransport


class JourneyChannelResource:
    """Channel — Journey API.

    Endpoints:
        POST   /journeys/v1/channels
        PUT    /journeys/v1/channels/{channel_id}
        DELETE /journeys/v1/channels/{channel_id}
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/journeys/v1/channels"

    def create(
        self,
        business_unit_id: str,
        name: str,
        icon_url: str = "",
        primary_color: str = "#000000",
        secondary_color: str = "#FFFFFF",
        description: str = "",
        welcome_message: str = "",
        fallback_url: str = "",
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "business_unit_id": business_unit_id,
            "name": name,
            "icon_url": icon_url,
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "description": description,
            "welcome_message": welcome_message,
            "fallback_url": fallback_url,
        }
        return self._http.request("POST", self._base, json=body).json()

    def update(self, channel_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/{channel_id}", json=body).json()

    def delete(self, channel_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/{channel_id}").json()


class AsyncJourneyChannelResource:
    """Channel — Journey API. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/journeys/v1/channels"

    async def create(
        self,
        business_unit_id: str,
        name: str,
        icon_url: str = "",
        primary_color: str = "#000000",
        secondary_color: str = "#FFFFFF",
        description: str = "",
        welcome_message: str = "",
        fallback_url: str = "",
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "business_unit_id": business_unit_id,
            "name": name,
            "icon_url": icon_url,
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "description": description,
            "welcome_message": welcome_message,
            "fallback_url": fallback_url,
        }
        res = await self._http.request("POST", self._base, json=body)
        return res.json()

    async def update(self, channel_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/{channel_id}", json=body)
        return res.json()

    async def delete(self, channel_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/{channel_id}")
        return res.json()
