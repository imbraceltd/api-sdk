from typing import List, Optional, Union
from typing_extensions import TypedDict

class Team(TypedDict, total=False):
    id: str
    organization_id: str
    business_unit_id: Optional[str]
    name: str
    mode: Optional[str]
    icon_url: Optional[str]
    description: Optional[str]
    is_default: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]

class TeamMembershipResponse(TypedDict, total=False):
    success: bool

class TeamUserItem(TypedDict, total=False):
    _id: str
    user_id: Optional[str]
    team_id: Optional[str]
    role: Optional[str]

class TeamWorkflowItem(TypedDict, total=False):
    _id: str
    name: Optional[str]
