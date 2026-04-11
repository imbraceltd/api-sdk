from typing import Any, Dict, List
from ...core.http import HttpTransport, AsyncHttpTransport


class WorkflowResource:
    """Workflow — Journey API.

    Endpoints:
        GET   /journeys/api/v1/workflows/{workflow_id}
        GET   /journeys/api/v1/workflows/verify  (body: {workflow_ids: [...]})
        PATCH /journeys/v1/workflow/{workflow_id}
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def get(self, workflow_id: str, organization_id: str) -> Dict[str, Any]:
        return self._http.request(
            "GET", f"{self._base}/journeys/api/v1/workflows/{workflow_id}",
            headers={"x-organization-id": organization_id},
        ).json()

    def verify(self, workflow_ids: List[int], organization_id: str) -> Dict[str, Any]:
        return self._http.request(
            "GET", f"{self._base}/journeys/api/v1/workflows/verify",
            json={"workflow_ids": workflow_ids},
            headers={"x-organization-id": organization_id},
        ).json()

    def update(self, workflow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request(
            "PATCH", f"{self._base}/journeys/v1/workflow/{workflow_id}", json=body
        ).json()


class AsyncWorkflowResource:
    """Workflow — Journey API. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def get(self, workflow_id: str, organization_id: str) -> Dict[str, Any]:
        res = await self._http.request(
            "GET", f"{self._base}/journeys/api/v1/workflows/{workflow_id}",
            headers={"x-organization-id": organization_id},
        )
        return res.json()

    async def verify(self, workflow_ids: List[int], organization_id: str) -> Dict[str, Any]:
        res = await self._http.request(
            "GET", f"{self._base}/journeys/api/v1/workflows/verify",
            json={"workflow_ids": workflow_ids},
            headers={"x-organization-id": organization_id},
        )
        return res.json()

    async def update(self, workflow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request(
            "PATCH", f"{self._base}/journeys/v1/workflow/{workflow_id}", json=body
        )
        return res.json()
