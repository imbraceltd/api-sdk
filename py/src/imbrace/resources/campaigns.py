from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


class CampaignsResource:
    """Campaigns domain — Sync.

    @param base - channel-service base URL (gateway/channel-service)
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base.rstrip('/')}/v1/campaign"

    def list(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._http.request("GET", self._base, params=params or {}).json()

    def get(self, campaign_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/{campaign_id}").json()

    def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", self._base, json=body).json()

    def delete(self, campaign_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/{campaign_id}").json()


class AsyncCampaignsResource:
    """Campaigns domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base.rstrip('/')}/v1/campaign"

    async def list(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        res = await self._http.request("GET", self._base, params=params or {})
        return res.json()

    async def get(self, campaign_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/{campaign_id}")
        return res.json()

    async def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", self._base, json=body)
        return res.json()

    async def delete(self, campaign_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/{campaign_id}")
        return res.json()
