from typing import Any, Dict, List, Optional
from ..http import HttpTransport, AsyncHttpTransport


class ContactsResource:
    """Contacts domain — Sync."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/v1/backend"

    def list(self, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/contacts",
                                  params={"limit": limit, "skip": skip}).json()

    def search(self, query: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/contacts/_search",
                                  params={"q": query}).json()

    def update(self, contact_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/contacts/{contact_id}", json=body).json()

    def get_conversations(self, contact_id: str, channel_types: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if channel_types:
            params["channel_types"] = channel_types
        return self._http.request("GET", f"{self._base}/contacts/{contact_id}/conversations",
                                  params=params).json()

    def list_notifications(self, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/notifications",
                                  params={"limit": limit, "skip": skip}).json()

    def dismiss_notification(self, notification_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/notifications/dismiss",
                                  json={"notification_id": notification_id}).json()

    def dismiss_all_notifications(self) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/notifications/dismiss/all").json()


class AsyncContactsResource:
    """Contacts domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/v1/backend"

    async def list(self, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/contacts",
                                       params={"limit": limit, "skip": skip})
        return res.json()

    async def search(self, query: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/contacts/_search", params={"q": query})
        return res.json()

    async def update(self, contact_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._base}/contacts/{contact_id}", json=body)
        return res.json()

    async def dismiss_notification(self, notification_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/notifications/dismiss",
                                       json={"notification_id": notification_id})
        return res.json()

    async def dismiss_all_notifications(self) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/notifications/dismiss/all")
        return res.json()
