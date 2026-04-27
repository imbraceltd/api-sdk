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

    # ── n8n Workflows ──────────────────────────────────────────────────────────

    def list_n8n(self) -> Dict[str, Any]:
        """List all n8n workflows."""
        return self._http.request("GET", f"{self._backend}/n8n/workflows").json()

    def get_n8n(self, workflow_id: str) -> Dict[str, Any]:
        """Get an n8n workflow by ID."""
        return self._http.request("GET", f"{self._backend}/n8n/workflows/{workflow_id}").json()

    def create_n8n(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new n8n workflow."""
        return self._http.request("POST", f"{self._backend}/workflow", json=body).json()

    def update_n8n(self, workflow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing n8n workflow."""
        return self._http.request("PATCH", f"{self._backend}/workflow/{workflow_id}", json=body).json()

    def list_n8n_credentials(self) -> Dict[str, Any]:
        """List all n8n credentials."""
        return self._http.request("GET", f"{self._backend}/n8n/credentials").json()

    def update_n8n_credential(self, credential_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Update an n8n credential."""
        return self._http.request("PATCH", f"{self._backend}/workflow/credentials/{credential_id}", json=body).json()

    def get_processed_credential_types(self) -> Dict[str, Any]:
        """Get all processed credential types (for channel integrations)."""
        return self._http.request("GET", f"{self._backend}/workflow/processed-credential-types").json()


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

    # ── n8n Workflows (Async) ──────────────────────────────────────────────────

    async def list_n8n(self) -> Dict[str, Any]:
        """List all n8n workflows (async)."""
        res = await self._http.request("GET", f"{self._backend}/n8n/workflows")
        return res.json()

    async def get_n8n(self, workflow_id: str) -> Dict[str, Any]:
        """Get an n8n workflow by ID (async)."""
        res = await self._http.request("GET", f"{self._backend}/n8n/workflows/{workflow_id}")
        return res.json()

    async def create_n8n(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new n8n workflow (async)."""
        res = await self._http.request("POST", f"{self._backend}/workflow", json=body)
        return res.json()

    async def update_n8n(self, workflow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing n8n workflow (async)."""
        res = await self._http.request("PATCH", f"{self._backend}/workflow/{workflow_id}", json=body)
        return res.json()

    async def list_n8n_credentials(self) -> Dict[str, Any]:
        """List all n8n credentials (async)."""
        res = await self._http.request("GET", f"{self._backend}/n8n/credentials")
        return res.json()

    async def update_n8n_credential(self, credential_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Update an n8n credential (async)."""
        res = await self._http.request("PATCH", f"{self._backend}/workflow/credentials/{credential_id}", json=body)
        return res.json()

    async def get_processed_credential_types(self) -> Dict[str, Any]:
        """Get all processed credential types (async)."""
        res = await self._http.request("GET", f"{self._backend}/workflow/processed-credential-types")
        return res.json()
