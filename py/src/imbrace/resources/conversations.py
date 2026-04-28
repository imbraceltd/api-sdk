from typing import Any, Dict, List, Optional, Union
from ..http import HttpTransport, AsyncHttpTransport
from ..types.conversation import (
    Conversation, ConversationActionResponse, JoinConversationInput,
    LeaveConversationInput, UpdateStatusInput, UpdateNameInput,
    InitVideoCallInput, AssignTeamMemberInput, RemoveTeamMemberInput,
    InvitableUser, CreateConversationInput, JoinRequestInput
)
from ..types.common import PagedResponse

class ConversationsResource:
    """Conversations domain — Sync.

    @param base - channel-service base URL (gateway/channel-service)
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2"

    def list(self, type: Optional[str] = None, q: Optional[str] = None,
             limit: Optional[int] = None, skip: Optional[int] = None,
             sort: Optional[str] = None) -> PagedResponse[Conversation]:
        """List team conversations (V2)."""
        params: Dict[str, Any] = {}
        if type: params["type"] = type
        if q: params["q"] = q
        if limit: params["limit"] = limit
        if skip is not None: params["skip"] = skip
        if sort: params["sort"] = sort

        return self._http.request("GET", f"{self._v2}/team_conversations", params=params).json()

    def get(self, conv_id: str) -> Conversation:
        return self._http.request("GET", f"{self._v1}/team_conversations/{conv_id}").json()

    def get_by_conversation_id(self, conversation_id: str) -> Conversation:
        params = {"type": "conversation_id", "q": conversation_id}
        return self._http.request("GET", f"{self._v1}/team_conversations", params=params).json()

    def search(self, business_unit_id: str, q: str,
               limit: Optional[int] = None, skip: Optional[int] = None) -> PagedResponse[Conversation]:
        params = {
            "business_unit_id": business_unit_id,
            "type": "text",
            "q": q,
        }
        if limit: params["limit"] = limit
        if skip is not None: params["skip"] = skip
        return self._http.request("GET", f"{self._v1}/team_conversations/_search", params=params).json()

    def get_views_count(self, type: Optional[str] = None, q: Optional[str] = None) -> Dict[str, int]:
        params = {}
        if type: params["type"] = type
        if q: params["q"] = q
        return self._http.request("GET", f"{self._v2}/team_conversations/_views_count", params=params).json()

    def get_outstanding(self, business_unit_id: str,
                        limit: Optional[int] = None, skip: Optional[int] = None) -> PagedResponse[Conversation]:
        params = {"type": "business_unit_id", "q": business_unit_id}
        if limit: params["limit"] = limit
        if skip is not None: params["skip"] = skip
        return self._http.request("GET", f"{self._v1}/team_conversations/_outstanding", params=params).json()

    def join(self, body: JoinConversationInput) -> ConversationActionResponse:
        return self._http.request("POST", f"{self._v1}/team_conversations/_join", json=body).json()

    def leave(self, body: LeaveConversationInput) -> ConversationActionResponse:
        return self._http.request("POST", f"{self._v1}/team_conversations/_leave", json=body).json()

    def update_status(self, body: UpdateStatusInput) -> ConversationActionResponse:
        return self._http.request("POST", f"{self._v1}/team_conversations/_update_status", json=body).json()

    def update_name(self, body: UpdateNameInput) -> ConversationActionResponse:
        return self._http.request("POST", f"{self._v1}/team_conversations/_update_name", json=body).json()

    def init_video_call(self, body: InitVideoCallInput) -> ConversationActionResponse:
        return self._http.request("POST", f"{self._v1}/team_conversations/_init_jaas_conference", json=body).json()

    def assign_team_member(self, body: AssignTeamMemberInput) -> ConversationActionResponse:
        return self._http.request("POST", f"{self._v1}/team_conversations/assign_team_member", json=body).json()

    def remove_team_member(self, body: RemoveTeamMemberInput) -> ConversationActionResponse:
        return self._http.request("POST", f"{self._v1}/team_conversations/remove_team_member", json=body).json()

    def get_invitable_users(self, team_conv_id: str) -> List[InvitableUser]:
        return self._http.request("GET", f"{self._v1}/team_conversations/{team_conv_id}/users").json()

    def get_conversation(self, conversation_id: str) -> Conversation:
        """Get base conversation details."""
        return self._http.request("GET", f"{self._v1}/conversations/{conversation_id}").json()

    def create(self, body: Optional[CreateConversationInput] = None) -> Conversation:
        return self._http.request("POST", f"{self._v1}/conversations", json=body or {}).json()

    def join_request(self, body: JoinRequestInput) -> ConversationActionResponse:
        return self._http.request("POST", f"{self._v1}/team_conversations/_join_request", json=body).json()


class AsyncConversationsResource:
    """Conversations domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2"

    async def list(self, type: Optional[str] = None, q: Optional[str] = None,
                   limit: Optional[int] = None, skip: Optional[int] = None,
                   sort: Optional[str] = None) -> PagedResponse[Conversation]:
        params: Dict[str, Any] = {}
        if type: params["type"] = type
        if q: params["q"] = q
        if limit: params["limit"] = limit
        if skip is not None: params["skip"] = skip
        if sort: params["sort"] = sort

        res = await self._http.request("GET", f"{self._v2}/team_conversations", params=params)
        return res.json()

    async def get(self, conv_id: str) -> Conversation:
        res = await self._http.request("GET", f"{self._v1}/team_conversations/{conv_id}")
        return res.json()

    async def get_by_conversation_id(self, conversation_id: str) -> Conversation:
        params = {"type": "conversation_id", "q": conversation_id}
        res = await self._http.request("GET", f"{self._v1}/team_conversations", params=params)
        return res.json()

    async def search(self, business_unit_id: str, q: str,
                     limit: Optional[int] = None, skip: Optional[int] = None) -> PagedResponse[Conversation]:
        params = {
            "business_unit_id": business_unit_id,
            "type": "text",
            "q": q,
        }
        if limit: params["limit"] = limit
        if skip is not None: params["skip"] = skip
        res = await self._http.request("GET", f"{self._v1}/team_conversations/_search", params=params)
        return res.json()

    async def get_views_count(self, type: Optional[str] = None, q: Optional[str] = None) -> Dict[str, int]:
        params = {}
        if type: params["type"] = type
        if q: params["q"] = q
        res = await self._http.request("GET", f"{self._v2}/team_conversations/_views_count", params=params)
        return res.json()

    async def get_outstanding(self, business_unit_id: str,
                              limit: Optional[int] = None, skip: Optional[int] = None) -> PagedResponse[Conversation]:
        params = {"type": "business_unit_id", "q": business_unit_id}
        if limit: params["limit"] = limit
        if skip is not None: params["skip"] = skip
        res = await self._http.request("GET", f"{self._v1}/team_conversations/_outstanding", params=params)
        return res.json()

    async def join(self, body: JoinConversationInput) -> ConversationActionResponse:
        res = await self._http.request("POST", f"{self._v1}/team_conversations/_join", json=body)
        return res.json()

    async def leave(self, body: LeaveConversationInput) -> ConversationActionResponse:
        res = await self._http.request("POST", f"{self._v1}/team_conversations/_leave", json=body)
        return res.json()

    async def update_status(self, body: UpdateStatusInput) -> ConversationActionResponse:
        res = await self._http.request("POST", f"{self._v1}/team_conversations/_update_status", json=body)
        return res.json()

    async def update_name(self, body: UpdateNameInput) -> ConversationActionResponse:
        res = await self._http.request("POST", f"{self._v1}/team_conversations/_update_name", json=body)
        return res.json()

    async def init_video_call(self, body: InitVideoCallInput) -> ConversationActionResponse:
        res = await self._http.request("POST", f"{self._v1}/team_conversations/_init_jaas_conference", json=body)
        return res.json()

    async def assign_team_member(self, body: AssignTeamMemberInput) -> ConversationActionResponse:
        res = await self._http.request("POST", f"{self._v1}/team_conversations/assign_team_member", json=body)
        return res.json()

    async def remove_team_member(self, body: RemoveTeamMemberInput) -> ConversationActionResponse:
        res = await self._http.request("POST", f"{self._v1}/team_conversations/remove_team_member", json=body)
        return res.json()

    async def get_invitable_users(self, team_conv_id: str) -> List[InvitableUser]:
        res = await self._http.request("GET", f"{self._v1}/team_conversations/{team_conv_id}/users")
        return res.json()

    async def get_conversation(self, conversation_id: str) -> Conversation:
        res = await self._http.request("GET", f"{self._v1}/conversations/{conversation_id}")
        return res.json()

    async def create(self, body: Optional[CreateConversationInput] = None) -> Conversation:
        res = await self._http.request("POST", f"{self._v1}/conversations", json=body or {})
        return res.json()

    async def join_request(self, body: JoinRequestInput) -> ConversationActionResponse:
        res = await self._http.request("POST", f"{self._v1}/team_conversations/_join_request", json=body)
        return res.json()
