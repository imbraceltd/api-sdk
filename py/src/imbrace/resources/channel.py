from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


class ChannelResource:
    """Channel domain — Sync."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/v1/backend/channels"
        self._base_v3 = f"{base}/v3/backend/channels"

    def list(self, type: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if type:
            params["type"] = type
        return self._http.request("GET", self._base, params=params).json()

    def get_count(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/_count").json()

    def get(self, channel_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/{channel_id}").json()

    def create_web(self, name: str) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base_v3}/_web", json={"name": name}).json()

    def update(self, channel_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/{channel_id}", json=body).json()

    def delete(self, channel_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/{channel_id}").json()

    def get_conv_count(self, view: Optional[str] = None, team_id: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if view:
            params["view"] = view
        if team_id:
            params["team_id"] = team_id
        return self._http.request("GET", f"{self._base}/_conv_count", params=params).json()


class AsyncChannelResource:
    """Channel domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/v1/backend/channels"
        self._base_v3 = f"{base}/v3/backend/channels"

    async def list(self, type: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if type:
            params["type"] = type
        res = await self._http.request("GET", self._base, params=params)
        return res.json()

    async def get_count(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/_count")
        return res.json()

    async def get(self, channel_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/{channel_id}")
        return res.json()

    async def create_web(self, name: str) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base_v3}/_web", json={"name": name})
        return res.json()

    async def update(self, channel_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/{channel_id}", json=body)
        return res.json()

    async def delete(self, channel_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/{channel_id}")
        return res.json()

    async def get_conv_count(self, view: Optional[str] = None, team_id: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if view:
            params["view"] = view
        if team_id:
            params["team_id"] = team_id
        res = await self._http.request("GET", f"{self._base}/_conv_count", params=params)
        return res.json()
