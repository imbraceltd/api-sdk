from typing import Any, Dict, List, Optional, Union
from ..http import HttpTransport, AsyncHttpTransport
from ..types.agent import (
    AgentTemplate, CreateAgentInput, UpdateAgentInput, DeleteAgentResponse,
    UseCase, CreateUseCaseInput, UpdateUseCaseInput
)

class AgentResource:
    """Agent / UseCase templates — Sync.

    Manages 2 groups of endpoints:
    - Marketplace templates: {marketplaces}/templates
    - Use-cases (AI): {marketplaces}/templates (aligned with TS)

    @param http       - HTTP transport
    @param base       - marketplaces service base URL (gateway/marketplaces)
    @param gateway    - App Gateway root URL (gateway)
    """

    def __init__(self, http: HttpTransport, base: str, gateway: Optional[str] = None):
        self._http = http
        # Match TS logic: base is marketplaces, we need backendV2 which is parent
        backend_v2 = base.rstrip("/").replace("/marketplaces", "")
        self._templates = f"{backend_v2}/templates"
        self._use_cases = self._templates

    # ── Marketplace Templates  

    def list(self) -> List[AgentTemplate]:
        return self._http.request("GET", self._templates).json()

    def list_agents(self) -> List[AgentTemplate]:
        return self.list()

    def get(self, template_id: str) -> Dict[str, AgentTemplate]:
        return self._http.request("GET", f"{self._templates}/{template_id}").json()

    def get_agent(self, agent_id: str) -> Dict[str, AgentTemplate]:
        return self.get(agent_id)

    def create(self, body: CreateAgentInput) -> AgentTemplate:
        return self._http.request("POST", f"{self._templates}/custom", json=body).json()

    def create_agent(self, body: CreateAgentInput) -> AgentTemplate:
        return self.create(body)

    def update(self, template_id: str, body: UpdateAgentInput) -> AgentTemplate:
        return self._http.request("PATCH", f"{self._templates}/{template_id}/custom", json=body).json()

    def update_agent(self, agent_id: str, body: UpdateAgentInput) -> AgentTemplate:
        return self.update(agent_id, body)

    def delete(self, template_id: str) -> DeleteAgentResponse:
        return self._http.request("DELETE", f"{self._templates}/{template_id}").json()

    def delete_agent(self, agent_id: str) -> DeleteAgentResponse:
        return self.delete(agent_id)

    # ── Use-cases      

    def list_use_cases(self) -> List[UseCase]:
        return self._http.request("GET", self._use_cases).json()

    def get_use_case(self, use_case_id: str) -> UseCase:
        return self._http.request("GET", f"{self._use_cases}/{use_case_id}").json()

    def create_use_case(self, body: CreateUseCaseInput) -> UseCase:
        return self._http.request("POST", f"{self._use_cases}/v2/custom", json=body).json()

    def update_use_case(self, use_case_id: str, body: UpdateUseCaseInput) -> UseCase:
        return self._http.request("PATCH", f"{self._use_cases}/{use_case_id}", json=body).json()

    def delete_use_case(self, use_case_id: str) -> DeleteAgentResponse:
        return self._http.request("DELETE", f"{self._use_cases}/{use_case_id}").json()


class AsyncAgentResource:
    """Agent / UseCase templates — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str, gateway: Optional[str] = None):
        self._http = http
        backend_v2 = base.rstrip("/").replace("/marketplaces", "")
        self._templates = f"{backend_v2}/templates"
        self._use_cases = self._templates

    # ── Marketplace Templates (Async)

    async def list(self) -> List[AgentTemplate]:
        res = await self._http.request("GET", self._templates)
        return res.json()

    async def list_agents(self) -> List[AgentTemplate]:
        return await self.list()

    async def get(self, template_id: str) -> Dict[str, AgentTemplate]:
        res = await self._http.request("GET", f"{self._templates}/{template_id}")
        return res.json()

    async def get_agent(self, agent_id: str) -> Dict[str, AgentTemplate]:
        return await self.get(agent_id)

    async def create(self, body: CreateAgentInput) -> AgentTemplate:
        res = await self._http.request("POST", f"{self._templates}/custom", json=body)
        return res.json()

    async def create_agent(self, body: CreateAgentInput) -> AgentTemplate:
        return await self.create(body)

    async def update(self, template_id: str, body: UpdateAgentInput) -> AgentTemplate:
        res = await self._http.request("PATCH", f"{self._templates}/{template_id}/custom", json=body)
        return res.json()

    async def update_agent(self, agent_id: str, body: UpdateAgentInput) -> AgentTemplate:
        return await self.update(agent_id, body)

    async def delete(self, template_id: str) -> DeleteAgentResponse:
        res = await self._http.request("DELETE", f"{self._templates}/{template_id}")
        return res.json()

    async def delete_agent(self, agent_id: str) -> DeleteAgentResponse:
        return await self.delete(agent_id)

    # ── Use-cases (Async)

    async def list_use_cases(self) -> List[UseCase]:
        res = await self._http.request("GET", self._use_cases)
        return res.json()

    async def get_use_case(self, use_case_id: str) -> UseCase:
        res = await self._http.request("GET", f"{self._use_cases}/{use_case_id}")
        return res.json()

    async def create_use_case(self, body: CreateUseCaseInput) -> UseCase:
        res = await self._http.request("POST", f"{self._use_cases}/v2/custom", json=body)
        return res.json()

    async def update_use_case(self, use_case_id: str, body: UpdateUseCaseInput) -> UseCase:
        res = await self._http.request("PATCH", f"{self._use_cases}/{use_case_id}", json=body)
        return res.json()

    async def delete_use_case(self, use_case_id: str) -> DeleteAgentResponse:
        res = await self._http.request("DELETE", f"{self._use_cases}/{use_case_id}")
        return res.json()
