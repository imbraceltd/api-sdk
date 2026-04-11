from typing import Any, Dict
from ...core.http import HttpTransport, AsyncHttpTransport


class AppsResource:
    """Apps — Journey API. Submit + Settings.

    Endpoints:
        POST /journeys/v2/apps/submit/{app_id}
        PUT  /journeys/v2/apps/settings/{app_id}
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/journeys/v2/apps"

    def submit(self, app_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/submit/{app_id}", json=body).json()

    def update_settings(self, app_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/settings/{app_id}", json=body).json()


class AsyncAppsResource:
    """Apps — Journey API. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/journeys/v2/apps"

    async def submit(self, app_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/submit/{app_id}", json=body)
        return res.json()

    async def update_settings(self, app_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/settings/{app_id}", json=body)
        return res.json()
