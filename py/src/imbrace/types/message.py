from typing import List, Optional, Dict, Any, Union
from typing_extensions import TypedDict

class MessageContent(TypedDict, total=False):
    text: Optional[str]
    url: Optional[str]
    caption: Optional[str]
    title: Optional[str]
    payload: Optional[str]

class ChannelMessage(TypedDict, total=False):
    object_name: str
    id: str
    organization_id: str
    business_unit_id: str
    conversation_id: str
    from_user: str # 'from' is reserved in Python
    type: str
    content: MessageContent
    created_at: str
    updated_at: str

class MessageComment(TypedDict, total=False):
    _id: str
    text: Optional[str]
    user_id: Optional[str]
    created_at: Optional[str]

class AddCommentInput(TypedDict, total=False):
    text: str

class UpdateCommentInput(TypedDict, total=False):
    text: Optional[str]

class MessageActionResponse(TypedDict, total=False):
    success: bool
    message: Optional[ChannelMessage]
