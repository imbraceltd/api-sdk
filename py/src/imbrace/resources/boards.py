from typing import Any, Dict, List, Optional
from ..http import HttpTransport, AsyncHttpTransport
from ..types.board import Board, BoardItem


class BoardsResource:
    """Boards / Knowledge Hub / External Drive — Sync.
    
    @param http     - HTTP transport
    @param base     - data-board base URL (`{gateway}/data-board`) — KnowledgeHub folders/files/drive
    @param backend  - backend base URL (`{gateway}/v1/backend` or `v2/backend`) — board CRUD, items, fields, search
    """

    def __init__(self, http: HttpTransport, base: str, backend: str):
        self._http = http
        self._base = base.rstrip("/")
        self._backend = backend.rstrip("/")

    # --- Boards ---
    def list(self, limit: int = 20, skip: int = 0) -> List[Board]:
        return self._http.request("GET", f"{self._backend}/board", params={"limit": limit, "skip": skip}).json()

    def get(self, board_id: str) -> Board:
        return self._http.request("GET", f"{self._backend}/board/{board_id}").json()

    def create(self, name: str, description: Optional[str] = None) -> Board:
        body: Dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        return self._http.request("POST", f"{self._backend}/board", json=body).json()

    def update(self, board_id: str, body: Dict[str, Any]) -> Board:
        return self._http.request("PUT", f"{self._backend}/board/{board_id}", json=body).json()

    def delete(self, board_id: str) -> None:
        self._http.request("DELETE", f"{self._backend}/board/{board_id}")

    def reorder(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/_order", json=body).json()

    def export_csv(self, board_id: str, params: Optional[Dict[str, str]] = None) -> str:
        return self._http.request("GET", f"{self._backend}/board/{board_id}/export_csv", params=params or {}).text

    def import_csv(self, board_id: str, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/{board_id}/import_csv", files=files).json()

    def import_excel(self, board_id: str, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/{board_id}/import_excel", files=files).json()

    def get_import_progress(self, board_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._backend}/board/{board_id}/import_progress").json()

    def upload_board_file(self, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/_fileupload", files=files).json()

    def upload_board_file_v2(self, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/upload", files=files).json()

    def get_linked_board_items(self, contact_board_id: str, board_item_id: str, item_type: str) -> Dict[str, Any]:
        """Get linked board items (Opportunities/Tasks)."""
        params = {"related_board_item_id": board_item_id, "type": item_type}
        return self._http.request("GET", f"{self._backend}/board/{contact_board_id}/board_items/_related_board_item", params=params).json()

    # --- Fields ---
    def create_field(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/{board_id}/board_fields", json=body).json()

    def update_field(self, board_id: str, field_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._backend}/board/{board_id}/board_fields/{field_id}", json=body).json()

    def delete_field(self, board_id: str, field_id: str) -> None:
        self._http.request("DELETE", f"{self._backend}/board/{board_id}/board_fields/{field_id}")

    def reorder_fields(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/{board_id}/board_fields/_order", json=body).json()

    def bulk_update_fields(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._backend}/board/{board_id}/multiple_board_fields", json=body).json()

    # --- Items ---
    def list_items(self, board_id: str, limit: int = 20, skip: int = 0) -> List[BoardItem]:
        return self._http.request("GET", f"{self._backend}/board/{board_id}/board_items",
                                  params={"limit": limit, "skip": skip}).json()

    def get_item(self, board_id: str, item_id: str) -> BoardItem:
        return self._http.request("GET", f"{self._backend}/board/{board_id}/board_items/{item_id}").json()

    def create_item(self, board_id: str, body: Dict[str, Any]) -> BoardItem:
        return self._http.request("POST", f"{self._backend}/board/{board_id}/board_items", json=body).json()

    def update_item(self, board_id: str, item_id: str, body: Dict[str, Any]) -> BoardItem:
        return self._http.request("PUT", f"{self._backend}/board/{board_id}/board_items/{item_id}", json=body).json()

    def delete_item(self, board_id: str, item_id: str) -> None:
        self._http.request("DELETE", f"{self._backend}/board/{board_id}/board_items/{item_id}")

    def bulk_delete_items(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/delete/{board_id}/board_items", json=body).json()

    def check_conflict(self, board_id: str, item_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/{board_id}/board_items/{item_id}/_is_conflicted", json=body).json()

    def get_related_items(self, board_id: str, item_id: str, related_board_id: str) -> Dict[str, Any]:
        """Get items from a specific related board for a board item."""
        return self._http.request("GET", f"{self._backend}/board/{board_id}/board_items/{item_id}/related_boards/{related_board_id}/board_items").json()

    def get_related_boards(self, board_id: str, item_id: str) -> List[Dict[str, Any]]:
        """Get all boards related to a specific board item."""
        return self._http.request("GET", f"{self._backend}/board/{board_id}/board_items/{item_id}/related_boards").json()

    def link_items(self, board_id: str, item_id: str, related_board_id: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._backend}/board/{board_id}/board_items/{item_id}/related_boards/{related_board_id}/link", json=body or {}).json()

    def unlink_items(self, board_id: str, item_id: str, related_board_id: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._backend}/board/{board_id}/board_items/{item_id}/related_boards/{related_board_id}/unlink", json=body or {}).json()

    # --- Search ---
    def search(self, board_id: str, q: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        body: Dict[str, Any] = {"limit": limit, "offset": offset}
        if q:
            body["q"] = q
        return self._http.request("POST", f"{self._backend}/meilisearch/{board_id}/search", json=body).json()

    # --- Segmentation ---
    def list_segments(self, board_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._backend}/board/{board_id}/segmentation").json()

    def create_segment(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/board/{board_id}/segmentation", json=body).json()

    def update_segment(self, board_id: str, segment_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._backend}/board/{board_id}/segmentation/{segment_id}", json=body).json()

    def delete_segment(self, board_id: str, segment_id: str) -> None:
        self._http.request("DELETE", f"{self._backend}/board/{board_id}/segmentation/{segment_id}")

    # --- Folders ---
    # data-board wraps all responses: { success, message, data }
    # get_folder returns { data: { folder, files } } — unwrap to data["folder"]
    # get_folder_contents returns { data: { folder, subfolders, files, ... } }
    # delete_folders body uses { ids: [...] }

    def search_folders(self, organization_id: Optional[str] = None, q: Optional[str] = None) -> list:
        params: Dict[str, str] = {}
        if organization_id:
            params["organization_id"] = organization_id
        if q:
            params["q"] = q
        r = self._http.request("GET", f"{self._base}/folders/search", params=params).json()
        return r.get("data", r)

    def get_folder(self, folder_id: str, recursive: Optional[bool] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if recursive is not None:
            params["recursive"] = str(recursive).lower()
        r = self._http.request("GET", f"{self._base}/folders/{folder_id}", params=params).json()
        data = r.get("data", r)
        return data.get("folder", data) if isinstance(data, dict) else data

    def create_folder(self, body: Dict[str, Any]) -> Dict[str, Any]:
        r = self._http.request("POST", f"{self._base}/folders", json=body).json()
        return r.get("data", r)

    def update_folder(self, folder_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        r = self._http.request("PUT", f"{self._base}/folders/{folder_id}", json=body).json()
        return r.get("data", r)

    def delete_folders(self, ids: list) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/folders/delete", json={"ids": ids}).json()

    def get_folder_contents(self, folder_id: str) -> Dict[str, Any]:
        r = self._http.request("GET", f"{self._base}/folders/{folder_id}/contents").json()
        return r.get("data", r)

    # --- Files ---
    def search_files(self, folder_id: str) -> list:
        r = self._http.request("GET", f"{self._base}/files/search", params={"folder_id": folder_id}).json()
        return r.get("data", r)

    def get_file(self, file_id: str) -> Dict[str, Any]:
        r = self._http.request("GET", f"{self._base}/files/{file_id}").json()
        return r.get("data", r)

    def create_file(self, body: Dict[str, Any]) -> Dict[str, Any]:
        r = self._http.request("POST", f"{self._base}/files", json=body).json()
        return r.get("data", r)

    def upload_file(self, files: Any) -> Dict[str, Any]:
        r = self._http.request("POST", f"{self._base}/files/upload", files=files).json()
        return r.get("data", r)

    def download_file(self, file_id: str) -> Any:
        return self._http.request("GET", f"{self._base}/files/{file_id}/download")

    def update_file(self, file_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        r = self._http.request("PUT", f"{self._base}/files/{file_id}", json=body).json()
        return r.get("data", r)

    def delete_files(self, ids: list) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/files/delete", json={"ids": ids}).json()

    def generate_ai_tags(self, body: Dict[str, Any]) -> Dict[str, Any]:
        r = self._http.request("POST", f"{self._base}/ai/tag-generation", json=body).json()
        return r.get("data", r)

    def get_link_preview(self, url: str) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._backend}/link_preview/getWebsiteInfo", json={"url": url}).json()

    # --- External Drive ---
    def initiate_drive_auth(self, drive_type: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/auth/{drive_type}/initiate").json()

    def list_drive_folders(self, drive_type: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/{drive_type}/folders", params=params or {}).json()

    def list_drive_files(self, drive_type: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/{drive_type}/files", params=params or {}).json()

    def download_drive_file(self, drive_type: str, params: Optional[Dict[str, str]] = None) -> Any:
        return self._http.request("GET", f"{self._base}/{drive_type}/files/download", params=params or {})

    def get_onedrive_session_status(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/auth/onedrive/files/session/status").json()


class AsyncBoardsResource:
    """Boards / Knowledge Hub / External Drive — Async.

    @param http     - HTTP transport
    @param base     - data-board base URL (`{gateway}/data-board`) — KnowledgeHub folders/files/drive
    @param backend  - backend base URL (`{gateway}/v1/backend` or `v2/backend`) — board CRUD, items, fields, search
    """

    def __init__(self, http: AsyncHttpTransport, base: str, backend: str):
        self._http = http
        self._base = base.rstrip("/")
        self._backend = backend.rstrip("/")

    async def list(self, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._backend}/board", params={"limit": limit, "skip": skip})
        return res.json()

    async def get(self, board_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._backend}/board/{board_id}")
        return res.json()

    async def create(self, name: str, description: Optional[str] = None) -> Board:
        body: Dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        res = await self._http.request("POST", f"{self._backend}/board", json=body)
        return res.json()

    async def update(self, board_id: str, body: Dict[str, Any]) -> Board:
        res = await self._http.request("PUT", f"{self._backend}/board/{board_id}", json=body)
        return res.json()

    async def delete(self, board_id: str) -> None:
        await self._http.request("DELETE", f"{self._backend}/board/{board_id}")

    async def reorder(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/_order", json=body)
        return res.json()

    async def export_csv(self, board_id: str, params: Optional[Dict[str, str]] = None) -> str:
        res = await self._http.request("GET", f"{self._backend}/board/{board_id}/export_csv", params=params or {})
        return res.text

    async def import_csv(self, board_id: str, files: Any) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/{board_id}/import_csv", files=files)
        return res.json()

    async def import_excel(self, board_id: str, files: Any) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/{board_id}/import_excel", files=files)
        return res.json()

    async def get_import_progress(self, board_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._backend}/board/{board_id}/import_progress")
        return res.json()

    async def upload_board_file(self, files: Any) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/_fileupload", files=files)
        return res.json()

    async def upload_board_file_v2(self, files: Any) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/upload", files=files)
        return res.json()

    async def get_linked_board_items(self, contact_board_id: str, board_item_id: str, item_type: str) -> Dict[str, Any]:
        params = {"related_board_item_id": board_item_id, "type": item_type}
        res = await self._http.request("GET", f"{self._backend}/board/{contact_board_id}/board_items/_related_board_item", params=params)
        return res.json()

    # --- Fields ---
    async def create_field(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/{board_id}/board_fields", json=body)
        return res.json()

    async def update_field(self, board_id: str, field_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._backend}/board/{board_id}/board_fields/{field_id}", json=body)
        return res.json()

    async def delete_field(self, board_id: str, field_id: str) -> None:
        await self._http.request("DELETE", f"{self._backend}/board/{board_id}/board_fields/{field_id}")

    async def reorder_fields(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/{board_id}/board_fields/_order", json=body)
        return res.json()

    async def bulk_update_fields(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._backend}/board/{board_id}/multiple_board_fields", json=body)
        return res.json()

    # --- Items ---
    async def list_items(self, board_id: str, limit: int = 20, skip: int = 0) -> List[BoardItem]:
        res = await self._http.request("GET", f"{self._backend}/board/{board_id}/board_items",
                                       params={"limit": limit, "skip": skip})
        return res.json()

    async def get_item(self, board_id: str, item_id: str) -> BoardItem:
        res = await self._http.request("GET", f"{self._backend}/board/{board_id}/board_items/{item_id}")
        return res.json()

    async def create_item(self, board_id: str, body: Dict[str, Any]) -> BoardItem:
        res = await self._http.request("POST", f"{self._backend}/board/{board_id}/board_items", json=body)
        return res.json()

    async def update_item(self, board_id: str, item_id: str, body: Dict[str, Any]) -> BoardItem:
        res = await self._http.request("PUT", f"{self._backend}/board/{board_id}/board_items/{item_id}", json=body)
        return res.json()

    async def delete_item(self, board_id: str, item_id: str) -> None:
        await self._http.request("DELETE", f"{self._backend}/board/{board_id}/board_items/{item_id}")

    async def bulk_delete_items(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/delete/{board_id}/board_items", json=body)
        return res.json()

    async def check_conflict(self, board_id: str, item_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/{board_id}/board_items/{item_id}/_is_conflicted", json=body)
        return res.json()

    async def get_related_items(self, board_id: str, item_id: str, related_board_id: str) -> Dict[str, Any]:
        """Get items from a specific related board for a board item (async)."""
        res = await self._http.request("GET", f"{self._backend}/board/{board_id}/board_items/{item_id}/related_boards/{related_board_id}/board_items")
        return res.json()

    async def get_related_boards(self, board_id: str, item_id: str) -> List[Dict[str, Any]]:
        """Get all boards related to a specific board item (async)."""
        res = await self._http.request("GET", f"{self._backend}/board/{board_id}/board_items/{item_id}/related_boards")
        return res.json()

    async def link_items(self, board_id: str, item_id: str, related_board_id: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._backend}/board/{board_id}/board_items/{item_id}/related_boards/{related_board_id}/link", json=body or {})
        return res.json()

    async def unlink_items(self, board_id: str, item_id: str, related_board_id: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._backend}/board/{board_id}/board_items/{item_id}/related_boards/{related_board_id}/unlink", json=body or {})
        return res.json()

    # --- Search ---
    async def search(self, board_id: str, q: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        body: Dict[str, Any] = {"limit": limit, "offset": offset}
        if q:
            body["q"] = q
        res = await self._http.request("POST", f"{self._backend}/meilisearch/{board_id}/search", json=body)
        return res.json()

    # --- Segmentation ---
    async def list_segments(self, board_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._backend}/board/{board_id}/segmentation")
        return res.json()

    async def create_segment(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/board/{board_id}/segmentation", json=body)
        return res.json()

    async def update_segment(self, board_id: str, segment_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._backend}/board/{board_id}/segmentation/{segment_id}", json=body)
        return res.json()

    async def delete_segment(self, board_id: str, segment_id: str) -> None:
        await self._http.request("DELETE", f"{self._backend}/board/{board_id}/segmentation/{segment_id}")

    # --- Folders ---
    async def search_folders(self, organization_id: Optional[str] = None, q: Optional[str] = None) -> list:
        params: Dict[str, str] = {}
        if organization_id:
            params["organization_id"] = organization_id
        if q:
            params["q"] = q
        res = await self._http.request("GET", f"{self._base}/folders/search", params=params)
        r = res.json()
        return r.get("data", r)

    async def get_folder(self, folder_id: str, recursive: Optional[bool] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if recursive is not None:
            params["recursive"] = str(recursive).lower()
        res = await self._http.request("GET", f"{self._base}/folders/{folder_id}", params=params)
        r = res.json()
        data = r.get("data", r)
        return data.get("folder", data) if isinstance(data, dict) else data

    async def create_folder(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/folders", json=body)
        r = res.json()
        return r.get("data", r)

    async def update_folder(self, folder_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/folders/{folder_id}", json=body)
        r = res.json()
        return r.get("data", r)

    async def delete_folders(self, ids: list) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/folders/delete", json={"ids": ids})
        return res.json()

    async def get_folder_contents(self, folder_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/folders/{folder_id}/contents")
        r = res.json()
        return r.get("data", r)

    # --- Files ---
    async def search_files(self, folder_id: str) -> list:
        res = await self._http.request("GET", f"{self._base}/files/search", params={"folder_id": folder_id})
        r = res.json()
        return r.get("data", r)

    async def get_file(self, file_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/files/{file_id}")
        r = res.json()
        return r.get("data", r)

    async def create_file(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/files", json=body)
        r = res.json()
        return r.get("data", r)

    async def upload_file(self, files: Any) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/files/upload", files=files)
        r = res.json()
        return r.get("data", r)

    async def download_file(self, file_id: str) -> Any:
        return await self._http.request("GET", f"{self._base}/files/{file_id}/download")

    async def update_file(self, file_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/files/{file_id}", json=body)
        r = res.json()
        return r.get("data", r)

    async def delete_files(self, ids: list) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/files/delete", json={"ids": ids})
        return res.json()

    async def generate_ai_tags(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/ai/tag-generation", json=body)
        r = res.json()
        return r.get("data", r)

    async def get_link_preview(self, url: str) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._backend}/link_preview/getWebsiteInfo", json={"url": url})
        return res.json()

    # --- External Drive ---
    async def initiate_drive_auth(self, drive_type: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/auth/{drive_type}/initiate")
        return res.json()

    async def list_drive_folders(self, drive_type: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/{drive_type}/folders", params=params or {})
        return res.json()

    async def list_drive_files(self, drive_type: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/{drive_type}/files", params=params or {})
        return res.json()

    async def download_drive_file(self, drive_type: str, params: Optional[Dict[str, str]] = None) -> Any:
        return await self._http.request("GET", f"{self._base}/{drive_type}/files/download", params=params or {})

    async def get_onedrive_session_status(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/auth/onedrive/files/session/status")
        return res.json()
