from typing import Any, Dict, List, Optional
from ..http import HttpTransport, AsyncHttpTransport


class WorkflowsResource:
    """Workflows domain (channel automations via Activepieces) — Sync.

    @param backend - backend base URL (`{gateway}/v1/backend`)
    Note: channel automation routes respond on v2/backend.
    """

    def __init__(self, http: HttpTransport, backend: str):
        self._http = http
        self._backend = backend.rstrip("/")

    @property
    def _v2(self) -> str:
        return self._backend.replace("/v1/", "/v2/")

    def list_channel_automation(self, channel_type: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if channel_type:
            params["channelType"] = channel_type
        return self._http.request("GET", f"{self._v2}/workflows/channel_automation", params=params).json()


class AsyncWorkflowsResource:
    """Workflows domain (channel automations via Activepieces) — Async."""

    def __init__(self, http: AsyncHttpTransport, backend: str):
        self._http = http
        self._backend = backend.rstrip("/")

    @property
    def _v2(self) -> str:
        return self._backend.replace("/v1/", "/v2/")

    async def list_channel_automation(self, channel_type: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if channel_type:
            params["channelType"] = channel_type
        res = await self._http.request("GET", f"{self._v2}/workflows/channel_automation", params=params)
        return res.json()
