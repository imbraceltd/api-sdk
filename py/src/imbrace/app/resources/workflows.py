from typing import Any, Dict, Optional
from ...core.http import HttpTransport, AsyncHttpTransport


class WorkflowsResource:
    """Workflows domain — Sync."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def list(self, tag: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if tag:
            params["tag"] = tag
        return self._http.request("GET", f"{self._base}/v1/backend/workflows", params=params).json()

    def list_channel_automation(self, channel_type: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if channel_type:
            params["channelType"] = channel_type
        return self._http.request("GET", f"{self._base}/v1/backend/workflows/channel_automation",
                                  params=params).json()

    def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/v1/backend/workflow", json=body).json()

    def update(self, workflow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._base}/v1/backend/workflow/{workflow_id}", json=body).json()

    def list_n8n(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/v1/backend/n8n/workflows").json()

    def get_n8n(self, id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/v1/backend/n8n/workflows/{id}").json()

    def create_n8n(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/v1/backend/n8n/workflows", json=body).json()


class AsyncWorkflowsResource:
    """Workflows domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def list(self, tag: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if tag:
            params["tag"] = tag
        res = await self._http.request("GET", f"{self._base}/v1/backend/workflows", params=params)
        return res.json()

    async def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/v1/backend/workflow", json=body)
        return res.json()

    async def update(self, workflow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._base}/v1/backend/workflow/{workflow_id}", json=body)
        return res.json()
