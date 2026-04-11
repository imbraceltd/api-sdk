from typing import Any, Dict, Optional
from ...core.http import HttpTransport, AsyncHttpTransport


class AiAssistantResource:
    """AI Assistant — Journey API.

    Endpoints:
        GET    /journeys/v2/ai/assistants
        POST   /journeys/v2/ai/assistants
        PUT    /journeys/v2/ai/assistants/{assistant_id}
        DELETE /journeys/v2/ai/assistants/{assistant_id}
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/journeys/v2/ai/assistants"

    def list(self, limit: Optional[int] = None, sort: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        return self._http.request("GET", self._base, params=params).json()

    def create(self, name: str, description: str = "", instructions: str = "",
               file_ids: Optional[list] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "name": name,
            "description": description,
            "instructions": instructions,
            "file_ids": file_ids or [],
            "metadata": metadata or {},
        }
        return self._http.request("POST", self._base, json=body).json()

    def update(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/{assistant_id}", json=body).json()

    def delete(self, assistant_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/{assistant_id}").json()


class AsyncAiAssistantResource:
    """AI Assistant — Journey API. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/journeys/v2/ai/assistants"

    async def list(self, limit: Optional[int] = None, sort: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        res = await self._http.request("GET", self._base, params=params)
        return res.json()

    async def create(self, name: str, description: str = "", instructions: str = "",
                     file_ids: Optional[list] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "name": name,
            "description": description,
            "instructions": instructions,
            "file_ids": file_ids or [],
            "metadata": metadata or {},
        }
        res = await self._http.request("POST", self._base, json=body)
        return res.json()

    async def update(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/{assistant_id}", json=body)
        return res.json()

    async def delete(self, assistant_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/{assistant_id}")
        return res.json()
