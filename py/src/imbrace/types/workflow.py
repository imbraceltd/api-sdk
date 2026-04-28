from typing import List, Optional, Union
from typing_extensions import TypedDict

class N8nWorkflow(TypedDict, total=False):
    id: str
    name: Optional[str]
    active: Optional[bool]

class N8nCredential(TypedDict, total=False):
    id: str
    name: Optional[str]
    type: Optional[str]
