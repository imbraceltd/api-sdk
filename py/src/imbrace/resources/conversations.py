from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


class ConversationsResource:
    """Conversations domain — Sync."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def get_views_count(self, type: Optional[str] = None, q: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if type:
            params["type"] = type
        if q:
            params["q"] = q
        return self._http.request("GET", f"{self._base}/v2/backend/team_conversations/_views_count",
                                  params=params).json()

    def create(self) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/v1/backend/conversation").json()

    def search(self, organization_id: str, q: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        body: Dict[str, Any] = {"limit": limit}
        if q:
            body["q"] = q
        return self._http.request("POST", f"{self._base}/v1/backend/meilisearch/{organization_id}/search",
                                  json=body).json()

    def fetch(self, organization_id: str, filter: str, limit: int = 10000) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/v1/backend/meilisearch/{organization_id}/fetch",
                                  json={"filter": filter, "limit": limit}).json()


class AsyncConversationsResource:
    """Conversations domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def get_views_count(self, type: Optional[str] = None, q: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if type:
            params["type"] = type
        if q:
            params["q"] = q
        res = await self._http.request("GET", f"{self._base}/v2/backend/team_conversations/_views_count",
                                       params=params)
        return res.json()

    async def create(self) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/v1/backend/conversation")
        return res.json()

    async def search(self, organization_id: str, q: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        body: Dict[str, Any] = {"limit": limit}
        if q:
            body["q"] = q
        res = await self._http.request("POST", f"{self._base}/v1/backend/meilisearch/{organization_id}/search",
                                       json=body)
        return res.json()
