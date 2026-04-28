from typing import List, Optional, Dict, Any
from typing_extensions import TypedDict

class AgentTemplate(TypedDict, total=False):
    _id: str
    name: Optional[str]
    description: Optional[str]
    # More fields based on usage

class AgentAssistantInput(TypedDict, total=False):
    name: Optional[str]
    description: Optional[str]
    model: Optional[str]
    instructions: Optional[str]

class AgentUseCaseInput(TypedDict, total=False):
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]

class CreateAgentInput(TypedDict, total=False):
    assistant: AgentAssistantInput
    usecase: AgentUseCaseInput

class UpdateAgentInput(TypedDict, total=False):
    assistant: Optional[AgentAssistantInput]
    usecase: Optional[AgentUseCaseInput]

class DeleteAgentResponse(TypedDict, total=False):
    success: bool

class UseCase(TypedDict, total=False):
    _id: str
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]

class CreateUseCaseInput(TypedDict, total=False):
    name: str
    description: Optional[str]
    category: Optional[str]
    assistant_id: Optional[str]

class UpdateUseCaseInput(TypedDict, total=False):
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
