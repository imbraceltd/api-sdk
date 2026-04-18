from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


class BoardsResource:
    """Boards / Knowledge Hub / External Drive — Sync. Routes via gateway/data-board."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    # --- Boards ---
    def list(self, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/boards", params={"limit": limit, "skip": skip}).json()

    def get(self, board_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/boards/{board_id}").json()

    def get_by_contact(self, contact_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/boards/by-contact/{contact_id}").json()

    def create(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        return self._http.request("POST", f"{self._base}/boards", json=body).json()

    def update(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/boards/{board_id}", json=body).json()

    def delete(self, board_id: str) -> None:
        self._http.request("DELETE", f"{self._base}/boards/{board_id}")

    def reorder(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/_order", json=body).json()

    def export_csv(self, board_id: str, params: Optional[Dict[str, str]] = None) -> str:
        return self._http.request("GET", f"{self._base}/boards/{board_id}/export_csv", params=params or {}).text

    def import_csv(self, board_id: str, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/{board_id}/import_csv", files=files).json()

    def import_excel(self, board_id: str, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/{board_id}/import_excel", files=files).json()

    def get_import_progress(self, board_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/boards/{board_id}/import_progress").json()

    def upload_board_file(self, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/_fileupload", files=files).json()

    # --- Fields ---
    def create_field(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/{board_id}/fields", json=body).json()

    def update_field(self, board_id: str, field_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/boards/{board_id}/fields/{field_id}", json=body).json()

    def delete_field(self, board_id: str, field_id: str) -> None:
        self._http.request("DELETE", f"{self._base}/boards/{board_id}/fields/{field_id}")

    def reorder_fields(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/{board_id}/fields/reorder", json=body).json()

    def bulk_update_fields(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/boards/{board_id}/fields/bulk", json=body).json()

    # --- Items ---
    def list_items(self, board_id: str, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/boards/{board_id}/items",
                                  params={"limit": limit, "skip": skip}).json()

    def get_item(self, board_id: str, item_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/boards/{board_id}/items/{item_id}").json()

    def create_item(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/{board_id}/items", json=body).json()

    def update_item(self, board_id: str, item_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/boards/{board_id}/items/{item_id}", json=body).json()

    def delete_item(self, board_id: str, item_id: str) -> None:
        self._http.request("DELETE", f"{self._base}/boards/{board_id}/items/{item_id}")

    def bulk_delete_items(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/boards/{board_id}/items/bulk-delete", json=body).json()

    def check_conflict(self, board_id: str, item_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/{board_id}/items/{item_id}/_is_conflicted", json=body).json()

    def get_related_items(self, board_id: str, item_id: str, related_board_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/boards/{board_id}/items/{item_id}/related/{related_board_id}").json()

    def link_items(self, board_id: str, item_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/{board_id}/items/{item_id}/related", json=body).json()

    def unlink_items(self, board_id: str, item_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/boards/{board_id}/items/{item_id}/related", json=body).json()

    # --- Search ---
    def search(self, board_id: str, q: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        body: Dict[str, Any] = {"limit": limit, "offset": offset}
        if q:
            body["q"] = q
        return self._http.request("POST", f"{self._base}/search/{board_id}", json=body).json()

    # --- Segmentation ---
    def list_segments(self, board_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/boards/{board_id}/segmentation").json()

    def create_segment(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/boards/{board_id}/segmentation", json=body).json()

    def update_segment(self, board_id: str, segment_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/boards/{board_id}/segmentation/{segment_id}", json=body).json()

    def delete_segment(self, board_id: str, segment_id: str) -> None:
        self._http.request("DELETE", f"{self._base}/boards/{board_id}/segmentation/{segment_id}")

    # --- Folders ---
    def search_folders(self, organization_id: str, q: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {"organization_id": organization_id}
        if q:
            params["q"] = q
        return self._http.request("GET", f"{self._base}/folders/search", params=params).json()

    def get_folder(self, folder_id: str, recursive: Optional[bool] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if recursive is not None:
            params["recursive"] = str(recursive).lower()
        return self._http.request("GET", f"{self._base}/folders/{folder_id}", params=params).json()

    def create_folder(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/folders", json=body).json()

    def update_folder(self, folder_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/folders/{folder_id}", json=body).json()

    def delete_folders(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/folders/delete", json=body).json()

    def get_folder_contents(self, folder_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/folders/{folder_id}/contents").json()

    # --- Files ---
    def search_files(self, folder_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/files/search", params={"folder_id": folder_id}).json()

    def get_file(self, file_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/files/{file_id}").json()

    def create_file(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/files", json=body).json()

    def upload_file(self, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/files/upload", files=files).json()

    def download_file(self, file_id: str) -> Any:
        return self._http.request("GET", f"{self._base}/files/{file_id}/download")

    def update_file(self, file_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/files/{file_id}", json=body).json()

    def delete_files(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/files/delete", json=body).json()

    def generate_ai_tags(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/ai/tag-generation", json=body).json()

    def get_link_preview(self, url: str) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/link_preview/getWebsiteInfo", json={"url": url}).json()

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
    """Boards / Knowledge Hub / External Drive — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    async def list(self, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/boards", params={"limit": limit, "skip": skip})
        return res.json()

    async def get(self, board_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/boards/{board_id}")
        return res.json()

    async def create(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        res = await self._http.request("POST", f"{self._base}/boards", json=body)
        return res.json()

    async def update(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/boards/{board_id}", json=body)
        return res.json()

    async def delete(self, board_id: str) -> None:
        await self._http.request("DELETE", f"{self._base}/boards/{board_id}")

    async def list_items(self, board_id: str, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/boards/{board_id}/items",
                                       params={"limit": limit, "skip": skip})
        return res.json()

    async def get_item(self, board_id: str, item_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/boards/{board_id}/items/{item_id}")
        return res.json()

    async def create_item(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/boards/{board_id}/items", json=body)
        return res.json()

    async def update_item(self, board_id: str, item_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/boards/{board_id}/items/{item_id}", json=body)
        return res.json()

    async def delete_item(self, board_id: str, item_id: str) -> None:
        await self._http.request("DELETE", f"{self._base}/boards/{board_id}/items/{item_id}")

    async def search(self, board_id: str, q: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        body: Dict[str, Any] = {"limit": limit, "offset": offset}
        if q:
            body["q"] = q
        res = await self._http.request("POST", f"{self._base}/search/{board_id}", json=body)
        return res.json()

    async def export_csv(self, board_id: str) -> str:
        res = await self._http.request("GET", f"{self._base}/boards/{board_id}/export_csv")
        return res.text

    async def upload_file(self, files: Any) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/files/upload", files=files)
        return res.json()

    async def get_folder(self, folder_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/folders/{folder_id}")
        return res.json()

    async def search_folders(self, organization_id: str, q: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {"organization_id": organization_id}
        if q:
            params["q"] = q
        res = await self._http.request("GET", f"{self._base}/folders/search", params=params)
        return res.json()
