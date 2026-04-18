from typing import Any, Dict
from ..http import HttpTransport, AsyncHttpTransport


class AgentResource:
    """Agent / UseCase templates — Sync.

    Quản lý 2 nhóm endpoint:
    - Marketplace templates: {marketplaces}/v1/market-places/templates
    - Use-cases (AI): {gateway}/v3/marketplaces/use-cases

    @param http       - HTTP transport
    @param base       - marketplaces service base URL (gateway/marketplaces)
    @param gateway    - App Gateway root URL (gateway)
    """

    def __init__(self, http: HttpTransport, base: str, gateway: str):
        self._http = http
        self._templates = f"{base.rstrip('/')}/v1/market-places/templates"
        self._use_cases = f"{gateway.rstrip('/')}/v3/marketplaces/use-cases"

    # ── Marketplace Templates ──────────────────────────────────────────────────

    def list(self) -> Dict[str, Any]:
        return self._http.request("GET", self._templates).json()

    def list_agents(self) -> Dict[str, Any]:
        return self.list()

    def get(self, template_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._templates}/{template_id}").json()

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        return self.get(agent_id)

    def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._templates}/custom", json=body).json()

    def create_agent(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self.create(body)

    def update(self, template_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._templates}/{template_id}/custom", json=body).json()

    def update_agent(self, agent_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self.update(agent_id, body)

    def delete(self, template_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._templates}/{template_id}").json()

    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        return self.delete(agent_id)

    # ── Use-cases ─────────────────────────────────────────────────────────────

    def list_use_cases(self) -> Dict[str, Any]:
        return self._http.request("GET", self._use_cases).json()

    def get_use_case(self, use_case_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._use_cases}/{use_case_id}").json()

    def create_use_case(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._use_cases}/v2/custom", json=body).json()

    def update_use_case(self, use_case_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._use_cases}/{use_case_id}", json=body).json()

    def delete_use_case(self, use_case_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._use_cases}/{use_case_id}").json()


class AsyncAgentResource:
    """Agent / UseCase templates — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str, gateway: str):
        self._http = http
        self._templates = f"{base.rstrip('/')}/v1/market-places/templates"
        self._use_cases = f"{gateway.rstrip('/')}/v3/marketplaces/use-cases"

    # ── Marketplace Templates ──────────────────────────────────────────────────

    async def list(self) -> Dict[str, Any]:
        res = await self._http.request("GET", self._templates)
        return res.json()

    async def list_agents(self) -> Dict[str, Any]:
        return await self.list()

    async def get(self, template_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._templates}/{template_id}")
        return res.json()

    async def get_agent(self, agent_id: str) -> Dict[str, Any]:
        return await self.get(agent_id)

    async def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._templates}/custom", json=body)
        return res.json()

    async def create_agent(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return await self.create(body)

    async def update(self, template_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._templates}/{template_id}/custom", json=body)
        return res.json()

    async def update_agent(self, agent_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return await self.update(agent_id, body)

    async def delete(self, template_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._templates}/{template_id}")
        return res.json()

    async def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        return await self.delete(agent_id)

    # ── Use-cases ─────────────────────────────────────────────────────────────

    async def list_use_cases(self) -> Dict[str, Any]:
        res = await self._http.request("GET", self._use_cases)
        return res.json()

    async def get_use_case(self, use_case_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._use_cases}/{use_case_id}")
        return res.json()

    async def create_use_case(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._use_cases}/v2/custom", json=body)
        return res.json()

    async def update_use_case(self, use_case_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._use_cases}/{use_case_id}", json=body)
        return res.json()

    async def delete_use_case(self, use_case_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._use_cases}/{use_case_id}")
        return res.json()
