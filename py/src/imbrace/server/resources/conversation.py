from typing import Any, Dict, Optional
from ...core.http import HttpTransport, AsyncHttpTransport


class ConversationServerResource:
    """Conversation — Server Gateway.

    Endpoints:
        GET /3rd/conversations/{conversation_id}/messages
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def list_messages(
        self,
        conversation_id: str,
        limit: int = 10,
        skip: int = 0,
    ) -> Dict[str, Any]:
        return self._http.request(
            "GET",
            f"{self._base}/3rd/conversations/{conversation_id}/messages",
            params={"limit": limit, "skip": skip},
        ).json()


class AsyncConversationServerResource:
    """Conversation — Server Gateway. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def list_messages(
        self,
        conversation_id: str,
        limit: int = 10,
        skip: int = 0,
    ) -> Dict[str, Any]:
        res = await self._http.request(
            "GET",
            f"{self._base}/3rd/conversations/{conversation_id}/messages",
            params={"limit": limit, "skip": skip},
        )
        return res.json()
