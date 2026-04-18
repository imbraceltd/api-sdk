from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


class MessagesResource:
    """Messages domain — Sync.

    @param base - channel-service base URL (gateway/channel-service)
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base.rstrip('/')}/v1/conversation_messages"

    def list(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        return self._http.request("GET", self._base, params={"limit": limit, "skip": skip}).json()

    def send(self, type: str, text: Optional[str] = None, url: Optional[str] = None,
             caption: Optional[str] = None, title: Optional[str] = None,
             payload: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"type": type}
        if text:
            body["text"] = text
        if url:
            body["url"] = url
        if caption:
            body["caption"] = caption
        if title:
            body["title"] = title
        if payload:
            body["payload"] = payload
        return self._http.request("POST", self._base, json=body).json()


class AsyncMessagesResource:
    """Messages domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base.rstrip('/')}/v1/conversation_messages"

    async def list(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        res = await self._http.request("GET", self._base, params={"limit": limit, "skip": skip})
        return res.json()

    async def send(self, type: str, text: Optional[str] = None, url: Optional[str] = None,
                   caption: Optional[str] = None, title: Optional[str] = None,
                   payload: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"type": type}
        if text:
            body["text"] = text
        if url:
            body["url"] = url
        if caption:
            body["caption"] = caption
        if title:
            body["title"] = title
        if payload:
            body["payload"] = payload
        res = await self._http.request("POST", self._base, json=body)
        return res.json()
