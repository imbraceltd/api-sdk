from typing import List, Optional, Dict, Any, Union
from typing_extensions import TypedDict

class ChannelType:
    WEB = "web"
    FACEBOOK = "facebook"
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    WECHAT = "wechat"
    LINE = "line"
    EMAIL = "email"
    WECOM = "wecom"

class Channel(TypedDict, total=False):
    object_name: Optional[str]
    id: str
    name: str
    type: str
    organization_id: str
    business_unit_id: Optional[str]
    is_active: bool
    config: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str

class CreateChannelInput(TypedDict, total=False):
    name: str
    type: Optional[str]
    config: Optional[Dict[str, Any]]

class UpdateChannelInput(TypedDict, total=False):
    active: Optional[bool]
    config: Optional[Dict[str, Any]]

class ConvCountResponse(TypedDict, total=False):
    count: int

class ChannelCredential(TypedDict, total=False):
    _id: str
    type: Optional[str]
    name: Optional[str]

class TeamObserver(TypedDict, total=False):
    _id: str
    user_id: Optional[str]
    team_id: Optional[str]
