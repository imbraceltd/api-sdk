from typing import List, Optional, Union, Dict, Any
from typing_extensions import TypedDict
from .common import PagedResponse

class IpsProfile(TypedDict, total=False):
    id: str
    user_id: str
    display_name: str
    avatar_url: Optional[str]
    bio: Optional[str]
    created_at: str
    updated_at: str

class Identity(TypedDict, total=False):
    id: str
    user_id: str
    provider: str
    provider_user_id: str
    created_at: str

class Scheduler(TypedDict, total=False):
    _id: str
    name: Optional[str]
    type: Optional[str]
    status: Optional[str]

class SchedulerFilterOptions(TypedDict, total=False):
    options: List[Dict[str, Any]]

class IpsWorkflow(TypedDict, total=False):
    _id: str
    name: Optional[str]
    active: Optional[bool]

class ExternalDataSync(TypedDict, total=False):
    _id: str
    name: Optional[str]
    status: Optional[str]

class EnableExternalDataSyncResponse(TypedDict, total=False):
    success: bool
    sync: Optional[ExternalDataSync]
