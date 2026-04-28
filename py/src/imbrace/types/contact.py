from typing import List, Optional, Dict, Any, Union
from typing_extensions import TypedDict

class Contact(TypedDict, total=False):
    object_name: Optional[str]
    id: str
    organization_id: str
    display_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    avatar_url: Optional[str]
    created_at: str
    updated_at: str

class UpdateContactInput(TypedDict, total=False):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]

class ContactComment(TypedDict, total=False):
    _id: str
    text: Optional[str]
    created_at: Optional[str]

class ContactFile(TypedDict, total=False):
    _id: str
    name: Optional[str]
    url: Optional[str]
    size: Optional[int]

class ConversationActivity(TypedDict, total=False):
    _id: str
    type: Optional[str]
    created_at: Optional[str]

class Notification(TypedDict, total=False):
    object_name: Optional[str]
    id: str
    organization_id: str
    user_id: str
    type: str
    content: Dict[str, Any]
    is_read: bool
    created_at: str

class NotificationActionResponse(TypedDict, total=False):
    success: bool
