from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


class BoardsResource:
    """Boards domain — Sync."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/v1/backend/board"
        self._search_base = f"{base}/v1/backend/meilisearch"

    def list(self, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        return self._http.request("GET", self._base, params={"limit": limit, "skip": skip}).json()

    def get(self, board_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/{board_id}").json()

    def create(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        return self._http.request("POST", self._base, json=body).json()

    def update(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/{board_id}", json=body).json()

    def delete(self, board_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/{board_id}").json()

    def list_items(self, board_id: str, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/{board_id}/board_items",
                                  params={"limit": limit, "skip": skip}).json()

    def get_item(self, board_id: str, item_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/{board_id}/board_items/{item_id}").json()

    def create_item(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/{board_id}/board_items", json=body).json()

    def update_item(self, board_id: str, item_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/{board_id}/board_items/{item_id}", json=body).json()

    def delete_item(self, board_id: str, item_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/{board_id}/board_items/{item_id}").json()

    def search(self, board_id: str, q: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        body: Dict[str, Any] = {"limit": limit}
        if q:
            body["q"] = q
        return self._http.request("POST", f"{self._search_base}/{board_id}/search", json=body).json()

    def export_csv(self, board_id: str) -> str:
        return self._http.request("GET", f"{self._base}/{board_id}/export_csv").text


class AsyncBoardsResource:
    """Boards domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/v1/backend/board"
        self._search_base = f"{base}/v1/backend/meilisearch"

    async def list(self, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request("GET", self._base, params={"limit": limit, "skip": skip})
        return res.json()

    async def get(self, board_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/{board_id}")
        return res.json()

    async def create(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name}
        if description:
            body["description"] = description
        res = await self._http.request("POST", self._base, json=body)
        return res.json()

    async def list_items(self, board_id: str, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/{board_id}/board_items",
                                       params={"limit": limit, "skip": skip})
        return res.json()

    async def create_item(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/{board_id}/board_items", json=body)
        return res.json()
