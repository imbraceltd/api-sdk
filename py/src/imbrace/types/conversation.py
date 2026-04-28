from typing import List, Optional, Dict, Any, Union
from typing_extensions import TypedDict

class SimpleUser(TypedDict, total=False):
    object_name: str
    id: str
    display_name: str
    avatar_url: str

class Conversation(TypedDict, total=False):
    object_name: str
    id: str
    organization_id: str
    business_unit_id: str
    channel_id: str
    channel_type: str
    contact_id: str
    status: str
    name: str
    timestamp: str
    users: List[SimpleUser]

class ConversationActionResponse(TypedDict, total=False):
    success: bool
    conversation: Optional[Conversation]

class JoinConversationInput(TypedDict, total=False):
    conversation_id: str

class LeaveConversationInput(TypedDict, total=False):
    conversation_id: str

class UpdateStatusInput(TypedDict, total=False):
    conversation_id: str
    status: str

class UpdateNameInput(TypedDict, total=False):
    conversation_id: str
    name: str

class InitVideoCallInput(TypedDict, total=False):
    conversation_id: str

class AssignTeamMemberInput(TypedDict, total=False):
    conversation_id: str
    user_id: str

class RemoveTeamMemberInput(TypedDict, total=False):
    conversation_id: str
    user_id: str

class InvitableUser(TypedDict, total=False):
    _id: str
    name: Optional[str]
    email: Optional[str]

class CreateConversationInput(TypedDict, total=False):
    channel_id: Optional[str]
    contact_id: Optional[str]

class JoinRequestInput(TypedDict, total=False):
    conversation_id: str
