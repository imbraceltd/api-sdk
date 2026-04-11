from typing import Any, Dict, List, Optional
from ...core.http import HttpTransport, AsyncHttpTransport


class BoardsResource:
    """Boards domain — Server Gateway. /3rd/ bulk operations.

    Endpoints:
        POST /3rd/board_search/{board_id}/search
        POST /3rd/boards/create/{board_id}/board_items
        POST /3rd/boards/delete/{board_id}/board_items
        PUT  /3rd/boards/update/{board_id}/board_items
        GET  /3rd/boards/{board_id}/board_items
        GET  /3rd/boards/{board_id}/export_csv
        POST /3rd/boards/{board_id}/import_csv
        POST /3rd/boards/_fileupload
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/3rd"

    def search(self, board_id: str, q: Optional[str] = None, limit: int = 20,
               offset: int = 0, matching_strategy: str = "last") -> Dict[str, Any]:
        body: Dict[str, Any] = {"limit": limit, "offset": offset, "matchingStrategy": matching_strategy}
        if q:
            body["q"] = q
        return self._http.request(
            "POST", f"{self._base}/board_search/{board_id}/search", json=body
        ).json()

    def list_items(self, board_id: str, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        return self._http.request(
            "GET", f"{self._base}/boards/{board_id}/board_items",
            params={"limit": limit, "skip": skip},
        ).json()

    def create_items(self, board_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk create — POST /3rd/boards/create/{board_id}/board_items"""
        return self._http.request(
            "POST", f"{self._base}/boards/create/{board_id}/board_items",
            json={"items": items},
        ).json()

    def update_items(self, board_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk update — PUT /3rd/boards/update/{board_id}/board_items"""
        return self._http.request(
            "PUT", f"{self._base}/boards/update/{board_id}/board_items",
            json={"items": items},
        ).json()

    def delete_items(self, board_id: str, ids: List[str]) -> Dict[str, Any]:
        """Bulk delete — POST /3rd/boards/delete/{board_id}/board_items"""
        return self._http.request(
            "POST", f"{self._base}/boards/delete/{board_id}/board_items",
            json={"ids": ids},
        ).json()

    def export_csv(self, board_id: str) -> str:
        return self._http.request("GET", f"{self._base}/boards/{board_id}/export_csv").text

    def import_csv(self, board_id: str, file_content: bytes, filename: str = "data.csv") -> Dict[str, Any]:
        return self._http.request(
            "POST", f"{self._base}/boards/{board_id}/import_csv",
            files={"file": (filename, file_content, "text/csv")},
        ).json()

    def upload_file(self, file_content: bytes, filename: str,
                    content_type: str = "application/octet-stream") -> Dict[str, Any]:
        return self._http.request(
            "POST", f"{self._base}/boards/_fileupload",
            files={"file": (filename, file_content, content_type)},
        ).json()


class AsyncBoardsResource:
    """Boards domain — Server Gateway. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/3rd"

    async def search(self, board_id: str, q: Optional[str] = None, limit: int = 20,
                     offset: int = 0, matching_strategy: str = "last") -> Dict[str, Any]:
        body: Dict[str, Any] = {"limit": limit, "offset": offset, "matchingStrategy": matching_strategy}
        if q:
            body["q"] = q
        res = await self._http.request("POST", f"{self._base}/board_search/{board_id}/search", json=body)
        return res.json()

    async def list_items(self, board_id: str, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request(
            "GET", f"{self._base}/boards/{board_id}/board_items",
            params={"limit": limit, "skip": skip},
        )
        return res.json()

    async def create_items(self, board_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        res = await self._http.request(
            "POST", f"{self._base}/boards/create/{board_id}/board_items",
            json={"items": items},
        )
        return res.json()

    async def update_items(self, board_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        res = await self._http.request(
            "PUT", f"{self._base}/boards/update/{board_id}/board_items",
            json={"items": items},
        )
        return res.json()

    async def delete_items(self, board_id: str, ids: List[str]) -> Dict[str, Any]:
        res = await self._http.request(
            "POST", f"{self._base}/boards/delete/{board_id}/board_items",
            json={"ids": ids},
        )
        return res.json()

    async def export_csv(self, board_id: str) -> str:
        res = await self._http.request("GET", f"{self._base}/boards/{board_id}/export_csv")
        return res.text
