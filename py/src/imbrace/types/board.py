from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict

class Board(TypedDict, total=False):
    id: str
    organization_id: str
    name: str
    description: Optional[str]
    workflow_id: Optional[str]
    hidden: Optional[bool]
    team_ids: Optional[List[str]]
    created_at: str
    updated_at: str

class BoardItem(TypedDict, total=False):
    id: str
    board_id: str
    fields: Dict[str, Any]
    created_at: str
    updated_at: str
