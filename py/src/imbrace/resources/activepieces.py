from typing import Any, Dict, List, Optional
from ..http import HttpTransport, AsyncHttpTransport


def _json_or_none(res) -> Any:
    if res.status_code == 204 or res.headers.get("content-length") == "0":
        return None
    return res.json()


class ActivePiecesResource:
    """ActivePieces workflow resource — Sync."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self._base}{path}"

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        p = {k: v for k, v in (params or {}).items() if v is not None}
        return self._http.request("GET", self._url(path), params=p).json()

    def _post(self, path: str, body: Any = None) -> Any:
        return _json_or_none(self._http.request("POST", self._url(path), json=body or {}))

    def _delete(self, path: str) -> None:
        _json_or_none(self._http.request("DELETE", self._url(path)))

    # ── Flows ──────────────────────────────────────────────────────────────────

    def list_flows(self, limit: int = 10, cursor: Optional[str] = None,
                   project_id: Optional[str] = None, folder_id: Optional[str] = None,
                   status: Optional[str] = None) -> Dict[str, Any]:
        return self._get("/v1/flows", {"limit": limit, "cursor": cursor,
                                       "projectId": project_id, "folderId": folder_id,
                                       "status": status})

    def get_flow(self, flow_id: str) -> Dict[str, Any]:
        return self._get(f"/v1/flows/{flow_id}")

    def create_flow(self, display_name: str, project_id: str) -> Dict[str, Any]:
        return self._post("/v1/flows", {"displayName": display_name, "projectId": project_id})

    def delete_flow(self, flow_id: str) -> None:
        self._delete(f"/v1/flows/{flow_id}")

    def apply_flow_operation(self, flow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post(f"/v1/flows/{flow_id}", body)

    def trigger_flow(self, flow_id: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        return self._post(f"/v1/webhooks/{flow_id}", payload or {})

    def trigger_flow_sync(self, flow_id: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        return self._post(f"/v1/webhooks/{flow_id}/sync", payload or {})

    # ── Flow Runs ──────────────────────────────────────────────────────────────

    def list_runs(self, limit: int = 10, cursor: Optional[str] = None,
                  flow_id: Optional[str] = None, status: Optional[str] = None,
                  project_id: Optional[str] = None) -> Dict[str, Any]:
        return self._get("/v1/flow-runs", {"limit": limit, "cursor": cursor,
                                           "flowId": flow_id, "status": status,
                                           "projectId": project_id})

    def get_run(self, run_id: str) -> Dict[str, Any]:
        return self._get(f"/v1/flow-runs/{run_id}")

    # ── Folders ────────────────────────────────────────────────────────────────

    def list_folders(self, limit: int = 10, cursor: Optional[str] = None) -> Dict[str, Any]:
        return self._get("/v1/folders", {"limit": limit, "cursor": cursor})

    def get_folder(self, folder_id: str) -> Dict[str, Any]:
        return self._get(f"/v1/folders/{folder_id}")

    def create_folder(self, display_name: str, project_id: str) -> Dict[str, Any]:
        return self._post("/v1/folders", {"displayName": display_name, "projectId": project_id})

    def update_folder(self, folder_id: str, display_name: str) -> Dict[str, Any]:
        return self._post(f"/v1/folders/{folder_id}", {"displayName": display_name})

    def delete_folder(self, folder_id: str) -> None:
        self._delete(f"/v1/folders/{folder_id}")

    # ── App Connections ────────────────────────────────────────────────────────

    def list_connections(self, limit: int = 10, cursor: Optional[str] = None,
                         project_id: Optional[str] = None,
                         piece_name: Optional[str] = None) -> Dict[str, Any]:
        return self._get("/v1/app-connections", {"limit": limit, "cursor": cursor,
                                                  "projectId": project_id,
                                                  "pieceName": piece_name})

    def get_connection(self, connection_id: str) -> Dict[str, Any]:
        return self._get(f"/v1/app-connections/{connection_id}")

    def upsert_connection(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/v1/app-connections", body)

    def delete_connection(self, connection_id: str) -> None:
        self._delete(f"/v1/app-connections/{connection_id}")

    # ── Pieces ─────────────────────────────────────────────────────────────────

    def list_pieces(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._get("/v1/pieces", {"limit": limit})

    # ── Triggers ───────────────────────────────────────────────────────────────

    def get_trigger_run_status(self) -> Dict[str, Any]:
        return self._get("/v1/trigger-runs/status")

    def test_trigger(self, body: Dict[str, Any]) -> Any:
        return self._post("/v1/test-trigger", body)

    # ── Tables & Records ───────────────────────────────────────────────────────

    def list_tables(self, limit: int = 10, cursor: Optional[str] = None) -> Dict[str, Any]:
        return self._get("/v1/tables", {"limit": limit, "cursor": cursor})

    def get_table(self, table_id: str) -> Dict[str, Any]:
        return self._get(f"/v1/tables/{table_id}")

    def list_records(self, table_id: str, limit: int = 10,
                     cursor: Optional[str] = None) -> Dict[str, Any]:
        return self._get("/v1/records", {"tableId": table_id, "limit": limit, "cursor": cursor})

    # ── MCP Servers ────────────────────────────────────────────────────────────

    def list_mcp_servers(self, project_id: str) -> Dict[str, Any]:
        return self._get("/v1/mcp-servers", {"projectId": project_id})

    def get_mcp_server(self, mcp_server_id: str) -> Dict[str, Any]:
        return self._get(f"/v1/mcp-servers/{mcp_server_id}")

    def create_mcp_server(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/v1/mcp-servers", body)

    def delete_mcp_server(self, mcp_server_id: str) -> None:
        self._delete(f"/v1/mcp-servers/{mcp_server_id}")

    def rotate_mcp_token(self, mcp_server_id: str) -> Dict[str, Any]:
        return self._post(f"/v1/mcp-servers/{mcp_server_id}/rotate")

    # ── User Invitations ───────────────────────────────────────────────────────

    def list_invitations(self, type: str, limit: int = 10,
                         cursor: Optional[str] = None,
                         project_id: Optional[str] = None) -> Dict[str, Any]:
        return self._get("/v1/user-invitations", {"type": type, "limit": limit,
                                                   "cursor": cursor, "projectId": project_id})

    def delete_invitation(self, invitation_id: str) -> None:
        self._delete(f"/v1/user-invitations/{invitation_id}")


class AsyncActivePiecesResource:
    """ActivePieces workflow resource — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self._base}{path}"

    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        p = {k: v for k, v in (params or {}).items() if v is not None}
        res = await self._http.request("GET", self._url(path), params=p)
        return res.json()

    async def _post(self, path: str, body: Any = None) -> Any:
        res = await self._http.request("POST", self._url(path), json=body or {})
        return _json_or_none(res)

    async def _delete(self, path: str) -> None:
        res = await self._http.request("DELETE", self._url(path))
        _json_or_none(res)

    # ── Flows ──────────────────────────────────────────────────────────────────

    async def list_flows(self, limit: int = 10, cursor: Optional[str] = None,
                         project_id: Optional[str] = None, folder_id: Optional[str] = None,
                         status: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("/v1/flows", {"limit": limit, "cursor": cursor,
                                              "projectId": project_id, "folderId": folder_id,
                                              "status": status})

    async def get_flow(self, flow_id: str) -> Dict[str, Any]:
        return await self._get(f"/v1/flows/{flow_id}")

    async def create_flow(self, display_name: str, project_id: str) -> Dict[str, Any]:
        return await self._post("/v1/flows", {"displayName": display_name, "projectId": project_id})

    async def delete_flow(self, flow_id: str) -> None:
        await self._delete(f"/v1/flows/{flow_id}")

    async def apply_flow_operation(self, flow_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post(f"/v1/flows/{flow_id}", body)

    async def trigger_flow(self, flow_id: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        return await self._post(f"/v1/webhooks/{flow_id}", payload or {})

    async def trigger_flow_sync(self, flow_id: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        return await self._post(f"/v1/webhooks/{flow_id}/sync", payload or {})

    # ── Flow Runs ──────────────────────────────────────────────────────────────

    async def list_runs(self, limit: int = 10, cursor: Optional[str] = None,
                        flow_id: Optional[str] = None, status: Optional[str] = None,
                        project_id: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("/v1/flow-runs", {"limit": limit, "cursor": cursor,
                                                  "flowId": flow_id, "status": status,
                                                  "projectId": project_id})

    async def get_run(self, run_id: str) -> Dict[str, Any]:
        return await self._get(f"/v1/flow-runs/{run_id}")

    # ── Folders ────────────────────────────────────────────────────────────────

    async def list_folders(self, limit: int = 10, cursor: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("/v1/folders", {"limit": limit, "cursor": cursor})

    async def get_folder(self, folder_id: str) -> Dict[str, Any]:
        return await self._get(f"/v1/folders/{folder_id}")

    async def create_folder(self, display_name: str, project_id: str) -> Dict[str, Any]:
        return await self._post("/v1/folders", {"displayName": display_name, "projectId": project_id})

    async def update_folder(self, folder_id: str, display_name: str) -> Dict[str, Any]:
        return await self._post(f"/v1/folders/{folder_id}", {"displayName": display_name})

    async def delete_folder(self, folder_id: str) -> None:
        await self._delete(f"/v1/folders/{folder_id}")

    # ── App Connections ────────────────────────────────────────────────────────

    async def list_connections(self, limit: int = 10, cursor: Optional[str] = None,
                                project_id: Optional[str] = None,
                                piece_name: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("/v1/app-connections", {"limit": limit, "cursor": cursor,
                                                        "projectId": project_id,
                                                        "pieceName": piece_name})

    async def get_connection(self, connection_id: str) -> Dict[str, Any]:
        return await self._get(f"/v1/app-connections/{connection_id}")

    async def upsert_connection(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/v1/app-connections", body)

    async def delete_connection(self, connection_id: str) -> None:
        await self._delete(f"/v1/app-connections/{connection_id}")

    # ── Pieces ─────────────────────────────────────────────────────────────────

    async def list_pieces(self, limit: int = 10) -> List[Dict[str, Any]]:
        return await self._get("/v1/pieces", {"limit": limit})

    # ── Triggers ───────────────────────────────────────────────────────────────

    async def get_trigger_run_status(self) -> Dict[str, Any]:
        return await self._get("/v1/trigger-runs/status")

    async def test_trigger(self, body: Dict[str, Any]) -> Any:
        return await self._post("/v1/test-trigger", body)

    # ── Tables & Records ───────────────────────────────────────────────────────

    async def list_tables(self, limit: int = 10, cursor: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("/v1/tables", {"limit": limit, "cursor": cursor})

    async def get_table(self, table_id: str) -> Dict[str, Any]:
        return await self._get(f"/v1/tables/{table_id}")

    async def list_records(self, table_id: str, limit: int = 10,
                            cursor: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("/v1/records", {"tableId": table_id, "limit": limit,
                                                "cursor": cursor})

    # ── MCP Servers ────────────────────────────────────────────────────────────

    async def list_mcp_servers(self, project_id: str) -> Dict[str, Any]:
        return await self._get("/v1/mcp-servers", {"projectId": project_id})

    async def get_mcp_server(self, mcp_server_id: str) -> Dict[str, Any]:
        return await self._get(f"/v1/mcp-servers/{mcp_server_id}")

    async def create_mcp_server(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("/v1/mcp-servers", body)

    async def delete_mcp_server(self, mcp_server_id: str) -> None:
        await self._delete(f"/v1/mcp-servers/{mcp_server_id}")

    async def rotate_mcp_token(self, mcp_server_id: str) -> Dict[str, Any]:
        return await self._post(f"/v1/mcp-servers/{mcp_server_id}/rotate")

    # ── User Invitations ───────────────────────────────────────────────────────

    async def list_invitations(self, type: str, limit: int = 10,
                                cursor: Optional[str] = None,
                                project_id: Optional[str] = None) -> Dict[str, Any]:
        return await self._get("/v1/user-invitations", {"type": type, "limit": limit,
                                                         "cursor": cursor,
                                                         "projectId": project_id})

    async def delete_invitation(self, invitation_id: str) -> None:
        await self._delete(f"/v1/user-invitations/{invitation_id}")
