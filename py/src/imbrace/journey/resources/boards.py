from typing import Any, Dict, List, Optional
from ...core.http import HttpTransport, AsyncHttpTransport


class BoardsResource:
    """Boards — Journey API.

    Endpoints:
        POST   /journeys/v1/board
        PUT    /journeys/v1/board/{board_id}
        DELETE /journeys/v1/board/{board_id}
        GET    /journeys/v1/board
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/journeys/v1/board"

    def list(self) -> Dict[str, Any]:
        return self._http.request("GET", self._base).json()

    def create(self, name: str, description: str = "",
               workflow_id: Optional[str] = None,
               team_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name, "description": description}
        if workflow_id:
            body["workflow_id"] = workflow_id
        if team_ids:
            body["team_ids"] = team_ids
        return self._http.request("POST", self._base, json=body).json()

    def update(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/{board_id}", json=body).json()

    def delete(self, board_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/{board_id}").json()


class AsyncBoardsResource:
    """Boards — Journey API. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/journeys/v1/board"

    async def list(self) -> Dict[str, Any]:
        res = await self._http.request("GET", self._base)
        return res.json()

    async def create(self, name: str, description: str = "",
                     workflow_id: Optional[str] = None,
                     team_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name, "description": description}
        if workflow_id:
            body["workflow_id"] = workflow_id
        if team_ids:
            body["team_ids"] = team_ids
        res = await self._http.request("POST", self._base, json=body)
        return res.json()

    async def update(self, board_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/{board_id}", json=body)
        return res.json()

    async def delete(self, board_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/{board_id}")
        return res.json()
