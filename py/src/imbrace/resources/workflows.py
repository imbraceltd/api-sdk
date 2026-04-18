from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


class WorkflowsResource:
    """Workflows domain — Sync.

    @param channel_base - channel-service base URL (gateway/channel-service)
    @param platform_base - platform service base URL (gateway/platform)
    """

    def __init__(self, http: HttpTransport, channel_base: str, platform_base: str):
        self._http = http
        self._ch = channel_base.rstrip("/")
        self._pl = platform_base.rstrip("/")

    @property
    def _ch_v1(self) -> str:
        return f"{self._ch}/v1"

    @property
    def _pl_v1(self) -> str:
        return f"{self._pl}/v1"

    # ─── Channel-service workflows ───────────────────────────────────────────────

    def list(self, tag: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if tag:
            params["tag"] = tag
        return self._http.request("GET", f"{self._ch_v1}/automations", params=params).json()

    def list_channel_automation(self, channel_type: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if channel_type:
            params["channelType"] = channel_type
        return self._http.request("GET", f"{self._ch_v1}/automations/channel_automation",
                                  params=params).json()

    def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._ch_v1}/automations", json=body).json()

    def update(self, workflow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._ch_v1}/automations/{workflow_id}", json=body).json()

    # ─── Platform n8n workflows ──────────────────────────────────────────────────

    def list_n8n(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._pl_v1}/workflows").json()

    def get_n8n(self, id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._pl_v1}/n8n/workflows/{id}").json()

    def create_n8n(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._pl_v1}/n8n/workflows", json=body).json()

    def update_n8n(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._pl_v1}/n8n/workflows/{id}", json=body).json()

    def delete_n8n(self, id: str) -> None:
        self._http.request("DELETE", f"{self._pl_v1}/n8n/workflows/{id}")


class AsyncWorkflowsResource:
    """Workflows domain — Async."""

    def __init__(self, http: AsyncHttpTransport, channel_base: str, platform_base: str):
        self._http = http
        self._ch = channel_base.rstrip("/")
        self._pl = platform_base.rstrip("/")

    @property
    def _ch_v1(self) -> str:
        return f"{self._ch}/v1"

    @property
    def _pl_v1(self) -> str:
        return f"{self._pl}/v1"

    async def list(self, tag: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if tag:
            params["tag"] = tag
        res = await self._http.request("GET", f"{self._ch_v1}/automations", params=params)
        return res.json()

    async def list_channel_automation(self, channel_type: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if channel_type:
            params["channelType"] = channel_type
        res = await self._http.request("GET", f"{self._ch_v1}/automations/channel_automation",
                                       params=params)
        return res.json()

    async def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._ch_v1}/automations", json=body)
        return res.json()

    async def update(self, workflow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._ch_v1}/automations/{workflow_id}", json=body)
        return res.json()

    async def list_n8n(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._pl_v1}/workflows")
        return res.json()

    async def get_n8n(self, id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._pl_v1}/n8n/workflows/{id}")
        return res.json()

    async def create_n8n(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._pl_v1}/n8n/workflows", json=body)
        return res.json()
