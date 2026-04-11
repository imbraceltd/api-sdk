from typing import Any, Dict
from ...core.http import HttpTransport, AsyncHttpTransport


class AgentResource:
    """AI Agent Templates — App Gateway. /v2/backend/templates"""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/v2/backend/templates"

    def list(self) -> Dict[str, Any]:
        return self._http.request("GET", self._base).json()

    def get(self, template_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/{template_id}").json()

    def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/custom", json=body).json()

    def update(self, template_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._base}/{template_id}/custom", json=body).json()

    def delete(self, template_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/{template_id}").json()


class AsyncAgentResource:
    """AI Agent Templates — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/v2/backend/templates"

    async def list(self) -> Dict[str, Any]:
        res = await self._http.request("GET", self._base)
        return res.json()

    async def get(self, template_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/{template_id}")
        return res.json()

    async def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/custom", json=body)
        return res.json()

    async def update(self, template_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._base}/{template_id}/custom", json=body)
        return res.json()

    async def delete(self, template_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/{template_id}")
        return res.json()
