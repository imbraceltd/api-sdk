from typing import Any, Dict, List, Optional, Union
from ..http import HttpTransport, AsyncHttpTransport
from ..types.message import (
    ChannelMessage, MessageContent, MessageComment,
    AddCommentInput, UpdateCommentInput, MessageActionResponse
)
from ..types.common import PagedResponse

class MessagesResource:
    """Messages domain — Sending, Comments, Pinning — Sync.

    @param base         - channel-service base URL (gateway/channel-service)
    @param backend_base - backend base URL (gateway/v1/backend) for file upload
    """

    def __init__(self, http: HttpTransport, base: str, backend_base: Optional[str] = None):
        self._http = http
        self._base = base.rstrip("/")
        self._backend_base = backend_base.rstrip("/") if backend_base else None

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    def list(self, limit: int = 10, skip: int = 0, q: Optional[str] = None, 
             type: Optional[str] = None) -> PagedResponse[ChannelMessage]:
        params = {"limit": limit, "skip": skip}
        if q: params["q"] = q
        if type: params["type"] = type
        return self._http.request("GET", f"{self._v1}/conversation_messages", params=params).json()

    def send(self, type: str, text: Optional[str] = None, url: Optional[str] = None,
             caption: Optional[str] = None, title: Optional[str] = None,
             payload: Optional[str] = None) -> ChannelMessage:
        body: Dict[str, Any] = {"type": type}
        if text: body["text"] = text
        if url: body["url"] = url
        if caption: body["caption"] = caption
        if title: body["title"] = title
        if payload: body["payload"] = payload
        return self._http.request("POST", f"{self._v1}/conversation_messages", json=body).json()

    def upload_file(self, files: Any) -> Dict[str, str]:
        """Upload message file. Returns {'url': '...' }"""
        base = self._backend_base or f"{self._v1.replace('/channel-service/v1', '')}/v1/backend"
        return self._http.request("POST", f"{base}/conversation_messages/_fileupload", files=files).json()

    def add_comment(self, conv_id: str, message_id: str, text: str) -> MessageComment:
        return self._http.request(
            "POST",
            f"{self._v1}/conversations/{conv_id}/conversation_messages/{message_id}/comments",
            json={"text": text},
        ).json()

    def update_comment(self, conv_id: str, comment_id: str, text: str) -> MessageComment:
        return self._http.request(
            "PUT",
            f"{self._v1}/conversations/{conv_id}/comments/{comment_id}",
            json={"text": text},
        ).json()

    def delete_comment(self, conv_id: str, comment_id: str) -> None:
        self._http.request("DELETE", f"{self._v1}/conversations/{conv_id}/comments/{comment_id}")

    def pin(self, conv_id: str, message_id: str) -> MessageActionResponse:
        return self._http.request(
            "GET",
            f"{self._v1}/conversations/{conv_id}/conversation_messages/{message_id}",
            params={"action": "pin"},
        ).json()

    def unpin(self, conv_id: str, message_id: str) -> MessageActionResponse:
        return self._http.request(
            "GET",
            f"{self._v1}/conversations/{conv_id}/conversation_messages/{message_id}",
            params={"action": "unpin"},
        ).json()

    def get_index(self, conv_id: str, message_id: str) -> Dict[str, int]:
        """Returns {'index': N}"""
        return self._http.request(
            "GET",
            f"{self._v1}/conversations/{conv_id}/conversation_messages/{message_id}/_index",
        ).json()


class AsyncMessagesResource:
    """Messages domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str, backend_base: Optional[str] = None):
        self._http = http
        self._base = base.rstrip("/")
        self._backend_base = backend_base.rstrip("/") if backend_base else None

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    async def list(self, limit: int = 10, skip: int = 0, q: Optional[str] = None, 
                 type: Optional[str] = None) -> PagedResponse[ChannelMessage]:
        params = {"limit": limit, "skip": skip}
        if q: params["q"] = q
        if type: params["type"] = type
        res = await self._http.request("GET", f"{self._v1}/conversation_messages", params=params)
        return res.json()

    async def send(self, type: str, text: Optional[str] = None, url: Optional[str] = None,
                   caption: Optional[str] = None, title: Optional[str] = None,
                   payload: Optional[str] = None) -> ChannelMessage:
        body: Dict[str, Any] = {"type": type}
        if text: body["text"] = text
        if url: body["url"] = url
        if caption: body["caption"] = caption
        if title: body["title"] = title
        if payload: body["payload"] = payload
        res = await self._http.request("POST", f"{self._v1}/conversation_messages", json=body)
        return res.json()

    async def upload_file(self, files: Any) -> Dict[str, str]:
        base = self._backend_base or f"{self._v1.replace('/channel-service/v1', '')}/v1/backend"
        res = await self._http.request("POST", f"{base}/conversation_messages/_fileupload", files=files)
        return res.json()

    async def add_comment(self, conv_id: str, message_id: str, text: str) -> MessageComment:
        res = await self._http.request(
            "POST",
            f"{self._v1}/conversations/{conv_id}/conversation_messages/{message_id}/comments",
            json={"text": text},
        )
        return res.json()

    async def update_comment(self, conv_id: str, comment_id: str, text: str) -> MessageComment:
        res = await self._http.request(
            "PUT",
            f"{self._v1}/conversations/{conv_id}/comments/{comment_id}",
            json={"text": text},
        )
        return res.json()

    async def delete_comment(self, conv_id: str, comment_id: str) -> None:
        await self._http.request("DELETE", f"{self._v1}/conversations/{conv_id}/comments/{comment_id}")

    async def pin(self, conv_id: str, message_id: str) -> MessageActionResponse:
        res = await self._http.request(
            "GET",
            f"{self._v1}/conversations/{conv_id}/conversation_messages/{message_id}",
            params={"action": "pin"},
        )
        return res.json()

    async def unpin(self, conv_id: str, message_id: str) -> MessageActionResponse:
        res = await self._http.request(
            "GET",
            f"{self._v1}/conversations/{conv_id}/conversation_messages/{message_id}",
            params={"action": "unpin"},
        )
        return res.json()

    async def get_index(self, conv_id: str, message_id: str) -> Dict[str, int]:
        res = await self._http.request(
            "GET",
            f"{self._v1}/conversations/{conv_id}/conversation_messages/{message_id}/_index",
        )
        return res.json()
