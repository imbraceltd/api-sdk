from typing import Any, Dict, List, Optional
from ..http import HttpTransport, AsyncHttpTransport


class ChatAiResource:
    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    def list_models(self) -> Dict[str, Any]:
        """Get available models from chat-ai (aiv2)."""
        return self._http.request("GET", f"{self._base}/models").json()

    def chat(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create chat completion (aiv2)."""
        return self._http.request("POST", f"{self._base}/openai/chat/completions", json=body).json()

    # --- Chats ---

    def list_chats(self) -> List[Dict[str, Any]]:
        """List user chats."""
        return self._http.request("GET", f"{self._base}/chats/").json()

    def get_chat(self, chat_id: str) -> Dict[str, Any]:
        """Get chat by ID."""
        return self._http.request("GET", f"{self._base}/chats/{chat_id}").json()       

    def create_chat(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create new chat."""
        return self._http.request("POST", f"{self._base}/chats/new", json=body).json() 

    def delete_chat(self, chat_id: str) -> bool:
        """Delete chat by ID."""
        return self._http.request("DELETE", f"{self._base}/chats/{chat_id}").json()    

    # --- Files ---

    def list_files(self) -> List[Dict[str, Any]]:
        """List uploaded files."""
        return self._http.request("GET", f"{self._base}/files/").json()

    def upload_file(self, files: Any) -> Dict[str, Any]:
        """Upload file."""
        return self._http.request("POST", f"{self._base}/files/", files=files).json()  

    def upload_agent_file(self, files: Any, agent_id: str) -> Dict[str, Any]:
        """Upload agent specific file."""
        return self._http.request("POST", f"{self._base}/files/agent", files=files, data={"agent_id": agent_id}).json()

    def extract_file(self, files: Any) -> Dict[str, Any]:
        """Extract file content."""
        return self._http.request("POST", f"{self._base}/files/extract", files=files).json()

    def get_file_data(self, file_id: str) -> Dict[str, Any]:
        """Get file data content."""
        return self._http.request("GET", f"{self._base}/files/{file_id}/data/content").json()

    def update_file_data(self, file_id: str, content: str) -> Dict[str, Any]:
        """Update file data content."""
        return self._http.request("POST", f"{self._base}/files/{file_id}/data/content/update", json={"content": content}).json()

    def delete_file(self, file_id: str) -> bool:
        """Delete file by ID."""
        return self._http.request("DELETE", f"{self._base}/files/{file_id}").json()    

    # --- Audio ---

    def transcribe(self, files: Any) -> Dict[str, Any]:
        """Transcribe audio to text."""
        return self._http.request("POST", f"{self._base}/audio/transcriptions", files=files).json()

    def speech(self, body: Dict[str, Any]) -> Any:
        """Generate speech from text."""
        return self._http.request("POST", f"{self._base}/audio/speech", json=body)     

    # --- Knowledge ---

    def list_knowledge(self) -> List[Dict[str, Any]]:
        """List knowledge bases."""
        return self._http.request("GET", f"{self._base}/knowledge/").json()

    def get_knowledge(self, knowledge_id: str) -> Dict[str, Any]:
        """Get knowledge base by ID."""
        return self._http.request("GET", f"{self._base}/knowledge/{knowledge_id}").json()

    def create_knowledge(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create new knowledge base."""
        return self._http.request("POST", f"{self._base}/knowledge/create", json=body).json()

    def delete_knowledge(self, knowledge_id: str) -> bool:
        """Delete knowledge base by ID."""
        return self._http.request("DELETE", f"{self._base}/knowledge/{knowledge_id}/delete").json()

    # --- Folders ---

    def list_folders(self) -> List[Dict[str, Any]]:
        """List chat folders."""
        return self._http.request("GET", f"{self._base}/folders/").json()

    def create_folder(self, name: str) -> Dict[str, Any]:
        """Create chat folder."""
        return self._http.request("POST", f"{self._base}/folders/", json={"name": name}).json()

    def update_folder(self, folder_id: str, name: str) -> Dict[str, Any]:
        """Update folder name."""
        return self._http.request("POST", f"{self._base}/folders/{folder_id}/update", json={"name": name}).json()

    def delete_folder(self, folder_id: str) -> bool:
        """Delete folder."""
        return self._http.request("DELETE", f"{self._base}/folders/{folder_id}").json()

    # --- Prompts ---

    def list_prompts(self) -> List[Dict[str, Any]]:
        """List custom prompts."""
        return self._http.request("GET", f"{self._base}/prompts/").json()

    def create_prompt(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create custom prompt."""
        return self._http.request("POST", f"{self._base}/prompts/create", json=body).json()

    def get_prompt(self, command: str) -> Dict[str, Any]:
        """Get prompt by command."""
        return self._http.request("GET", f"{self._base}/prompts/command/{command}").json()

    def update_prompt(self, command: str, body: Dict[str, Any]) -> Dict[str, Any]:     
        """Update prompt by command."""
        return self._http.request("POST", f"{self._base}/prompts/command/{command}/update", json=body).json()

    def delete_prompt(self, command: str) -> bool:
        """Delete prompt by command."""
        return self._http.request("DELETE", f"{self._base}/prompts/command/{command}/delete").json()

    # --- Tools ---

    def list_tools(self) -> List[Dict[str, Any]]:
        """List custom tools."""
        return self._http.request("GET", f"{self._base}/tools/").json()

    def create_tool(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create custom tool."""
        return self._http.request("POST", f"{self._base}/tools/create", json=body).json()

    def get_tool(self, tool_id: str) -> Dict[str, Any]:
        """Get tool by ID."""
        return self._http.request("GET", f"{self._base}/tools/id/{tool_id}").json()    

    def update_tool(self, tool_id: str, body: Dict[str, Any]) -> Dict[str, Any]:       
        """Update tool by ID."""
        return self._http.request("POST", f"{self._base}/tools/id/{tool_id}/update", json=body).json()

    def delete_tool(self, tool_id: str) -> bool:
        """Delete tool by ID."""
        return self._http.request("DELETE", f"{self._base}/tools/id/{tool_id}/delete").json()

    # --- Document AI ---

    def process_document(
        self,
        model_name: str,
        url: str,
        organization_id: str,
        *,
        board_id: Optional[str] = None,
        language: Optional[str] = None,
        additional_instructions: Optional[str] = None,
        additional_document_instructions: Optional[str] = None,
        process_model_name: Optional[str] = None,
        file_url_to_fill: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        utc: Optional[int] = None,
        chunk_size: Optional[int] = None,
        max_concurrent: Optional[int] = None,
        max_retries: Optional[int] = None,
        use_enhanced_processing: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Process a document with a vision model and extract structured data."""
        body: Dict[str, Any] = {"modelName": model_name, "url": url, "organizationId": organization_id}
        if board_id is not None: body["boardId"] = board_id
        if language is not None: body["language"] = language
        if additional_instructions is not None: body["additionalInstructions"] = additional_instructions
        if additional_document_instructions is not None: body["additionalDocumentInstructions"] = additional_document_instructions
        if process_model_name is not None: body["processModelName"] = process_model_name
        if file_url_to_fill is not None: body["fileUrlToFill"] = file_url_to_fill
        if tools is not None: body["tools"] = tools
        if utc is not None: body["utc"] = utc
        if chunk_size is not None: body["chunkSize"] = chunk_size
        if max_concurrent is not None: body["maxConcurrent"] = max_concurrent
        if max_retries is not None: body["maxRetries"] = max_retries
        if use_enhanced_processing is not None: body["useEnhancedProcessing"] = use_enhanced_processing
        return self._http.request("POST", f"{self._base}/document", json=body).json()

    def list_document_models(self) -> List[Dict[str, Any]]:
        """List LLM providers configured by the user — these are the models available for document AI."""
        return self._http.request("GET", f"{self._base}/providers").json()

    # --- Assistants ---

    def list_assistants(self) -> List[Dict[str, Any]]:
        """List all assistants for the account."""
        return self._http.request("GET", f"{self._base}/accounts/assistants").json()

    def get_assistant(self, assistant_id: str) -> Dict[str, Any]:
        """Get assistant by UUID."""
        return self._http.request("GET", f"{self._base}/assistants/{assistant_id}").json()

    def create_assistant(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new assistant. Required: name, workflow_name."""
        return self._http.request("POST", f"{self._base}/assistant_apps", json=body).json()

    def update_assistant(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Update assistant by UUID."""
        return self._http.request("PUT", f"{self._base}/assistant_apps/{assistant_id}", json=body).json()

    def delete_assistant(self, assistant_id: str) -> bool:
        """Delete assistant by UUID."""
        r = self._http.request("DELETE", f"{self._base}/assistant_apps/{assistant_id}")
        return r.is_success

    def update_assistant_instructions(self, assistant_id: str, instructions: str) -> Dict[str, Any]:
        """Update only the instructions field of an assistant."""
        return self._http.request("PATCH", f"{self._base}/assistants/{assistant_id}/instructions", json={"instructions": instructions}).json()

    def list_assistant_agents(self) -> List[Dict[str, Any]]:
        """List all assistant agents."""
        return self._http.request("GET", f"{self._base}/assistants/agents").json()


class AsyncChatAiResource:
    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    async def list_models(self) -> Dict[str, Any]:
        """Get available models from chat-ai (aiv2) (async)."""
        res = await self._http.request("GET", f"{self._base}/models")
        return res.json()

    async def chat(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create chat completion (aiv2) (async)."""
        res = await self._http.request("POST", f"{self._base}/openai/chat/completions", json=body)
        return res.json()

    # --- Chats ---

    async def list_chats(self) -> List[Dict[str, Any]]:
        """List user chats (async)."""
        res = await self._http.request("GET", f"{self._base}/chats/")
        return res.json()

    async def get_chat(self, chat_id: str) -> Dict[str, Any]:
        """Get chat by ID (async)."""
        res = await self._http.request("GET", f"{self._base}/chats/{chat_id}")
        return res.json()

    async def create_chat(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create new chat (async)."""
        res = await self._http.request("POST", f"{self._base}/chats/new", json=body)   
        return res.json()

    async def delete_chat(self, chat_id: str) -> bool:
        """Delete chat by ID (async)."""
        res = await self._http.request("DELETE", f"{self._base}/chats/{chat_id}")      
        return res.json()

    # --- Files ---

    async def list_files(self) -> List[Dict[str, Any]]:
        """List uploaded files (async)."""
        res = await self._http.request("GET", f"{self._base}/files/")
        return res.json()

    async def upload_file(self, files: Any) -> Dict[str, Any]:
        """Upload file (async)."""
        res = await self._http.request("POST", f"{self._base}/files/", files=files)    
        return res.json()

    async def upload_agent_file(self, files: Any, agent_id: str) -> Dict[str, Any]:    
        """Upload agent file (async)."""
        res = await self._http.request("POST", f"{self._base}/files/agent", files=files, data={"agent_id": agent_id})
        return res.json()

    async def extract_file(self, files: Any) -> Dict[str, Any]:
        """Extract file content (async)."""
        res = await self._http.request("POST", f"{self._base}/files/extract", files=files)
        return res.json()

    async def get_file_data(self, file_id: str) -> Dict[str, Any]:
        """Get file data content (async)."""
        res = await self._http.request("GET", f"{self._base}/files/{file_id}/data/content")
        return res.json()

    async def update_file_data(self, file_id: str, content: str) -> Dict[str, Any]:    
        """Update file data (async)."""
        res = await self._http.request("POST", f"{self._base}/files/{file_id}/data/content/update", json={"content": content})
        return res.json()

    async def delete_file(self, file_id: str) -> bool:
        """Delete file by ID (async)."""
        res = await self._http.request("DELETE", f"{self._base}/files/{file_id}")      
        return res.json()

    # --- Audio ---

    async def transcribe(self, files: Any) -> Dict[str, Any]:
        """Transcribe audio (async)."""
        res = await self._http.request("POST", f"{self._base}/audio/transcriptions", files=files)
        return res.json()

    async def speech(self, body: Dict[str, Any]) -> Any:
        """Generate speech (async)."""
        return await self._http.request("POST", f"{self._base}/audio/speech", json=body)

    # --- Knowledge ---

    async def list_knowledge(self) -> List[Dict[str, Any]]:
        """List knowledge (async)."""
        res = await self._http.request("GET", f"{self._base}/knowledge/")
        return res.json()

    async def get_knowledge(self, knowledge_id: str) -> Dict[str, Any]:
        """Get knowledge (async)."""
        res = await self._http.request("GET", f"{self._base}/knowledge/{knowledge_id}")
        return res.json()

    async def create_knowledge(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create knowledge (async)."""
        res = await self._http.request("POST", f"{self._base}/knowledge/create", json=body)
        return res.json()

    async def delete_knowledge(self, knowledge_id: str) -> bool:
        """Delete knowledge (async)."""
        res = await self._http.request("DELETE", f"{self._base}/knowledge/{knowledge_id}/delete")
        return res.json()

    # --- Folders ---

    async def list_folders(self) -> List[Dict[str, Any]]:
        """List folders (async)."""
        res = await self._http.request("GET", f"{self._base}/folders/")
        return res.json()

    async def create_folder(self, name: str) -> Dict[str, Any]:
        """Create folder (async)."""
        res = await self._http.request("POST", f"{self._base}/folders/", json={"name": name})
        return res.json()

    async def update_folder(self, folder_id: str, name: str) -> Dict[str, Any]:
        """Update folder (async)."""
        res = await self._http.request("POST", f"{self._base}/folders/{folder_id}/update", json={"name": name})
        return res.json()

    async def delete_folder(self, folder_id: str) -> bool:
        """Delete folder (async)."""
        res = await self._http.request("DELETE", f"{self._base}/folders/{folder_id}")
        return res.json()

    # --- Prompts ---

    async def list_prompts(self) -> List[Dict[str, Any]]:
        """List prompts (async)."""
        res = await self._http.request("GET", f"{self._base}/prompts/")
        return res.json()

    async def create_prompt(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create prompt (async)."""
        res = await self._http.request("POST", f"{self._base}/prompts/create", json=body)
        return res.json()

    async def get_prompt(self, command: str) -> Dict[str, Any]:
        """Get prompt (async)."""
        res = await self._http.request("GET", f"{self._base}/prompts/command/{command}")
        return res.json()

    async def update_prompt(self, command: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Update prompt (async)."""
        res = await self._http.request("POST", f"{self._base}/prompts/command/{command}/update", json=body)
        return res.json()

    async def delete_prompt(self, command: str) -> bool:
        """Delete prompt (async)."""
        res = await self._http.request("DELETE", f"{self._base}/prompts/command/{command}/delete")
        return res.json()

    # --- Tools ---

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List tools (async)."""
        res = await self._http.request("GET", f"{self._base}/tools/")
        return res.json()

    async def create_tool(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create tool (async)."""
        res = await self._http.request("POST", f"{self._base}/tools/create", json=body)
        return res.json()

    async def get_tool(self, tool_id: str) -> Dict[str, Any]:
        """Get tool (async)."""
        res = await self._http.request("GET", f"{self._base}/tools/id/{tool_id}")
        return res.json()

    async def update_tool(self, tool_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Update tool (async)."""
        res = await self._http.request("POST", f"{self._base}/tools/id/{tool_id}/update", json=body)
        return res.json()

    async def delete_tool(self, tool_id: str) -> bool:
        """Delete tool (async)."""
        res = await self._http.request("DELETE", f"{self._base}/tools/id/{tool_id}/delete")
        return res.json()

    # --- Document AI ---

    async def process_document(
        self,
        model_name: str,
        url: str,
        organization_id: str,
        *,
        board_id: Optional[str] = None,
        language: Optional[str] = None,
        additional_instructions: Optional[str] = None,
        additional_document_instructions: Optional[str] = None,
        process_model_name: Optional[str] = None,
        file_url_to_fill: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        utc: Optional[int] = None,
        chunk_size: Optional[int] = None,
        max_concurrent: Optional[int] = None,
        max_retries: Optional[int] = None,
        use_enhanced_processing: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Process a document with a vision model and extract structured data (async)."""
        body: Dict[str, Any] = {"modelName": model_name, "url": url, "organizationId": organization_id}
        if board_id is not None: body["boardId"] = board_id
        if language is not None: body["language"] = language
        if additional_instructions is not None: body["additionalInstructions"] = additional_instructions
        if additional_document_instructions is not None: body["additionalDocumentInstructions"] = additional_document_instructions
        if process_model_name is not None: body["processModelName"] = process_model_name
        if file_url_to_fill is not None: body["fileUrlToFill"] = file_url_to_fill
        if tools is not None: body["tools"] = tools
        if utc is not None: body["utc"] = utc
        if chunk_size is not None: body["chunkSize"] = chunk_size
        if max_concurrent is not None: body["maxConcurrent"] = max_concurrent
        if max_retries is not None: body["maxRetries"] = max_retries
        if use_enhanced_processing is not None: body["useEnhancedProcessing"] = use_enhanced_processing
        res = await self._http.request("POST", f"{self._base}/document", json=body)
        return res.json()

    async def list_document_models(self) -> List[Dict[str, Any]]:
        """List LLM providers configured by the user — these are the models available for document AI (async)."""
        res = await self._http.request("GET", f"{self._base}/providers")
        return res.json()

    # --- Assistants ---

    async def list_assistants(self) -> List[Dict[str, Any]]:
        """List all assistants for the account (async)."""
        res = await self._http.request("GET", f"{self._base}/accounts/assistants")
        return res.json()

    async def get_assistant(self, assistant_id: str) -> Dict[str, Any]:
        """Get assistant by UUID (async)."""
        res = await self._http.request("GET", f"{self._base}/assistants/{assistant_id}")
        return res.json()

    async def create_assistant(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new assistant. Required: name, workflow_name (async)."""
        res = await self._http.request("POST", f"{self._base}/assistant_apps", json=body)
        return res.json()

    async def update_assistant(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Update assistant by UUID (async)."""
        res = await self._http.request("PUT", f"{self._base}/assistant_apps/{assistant_id}", json=body)
        return res.json()

    async def delete_assistant(self, assistant_id: str) -> bool:
        """Delete assistant by UUID (async)."""
        r = await self._http.request("DELETE", f"{self._base}/assistant_apps/{assistant_id}")
        return r.is_success

    async def update_assistant_instructions(self, assistant_id: str, instructions: str) -> Dict[str, Any]:
        """Update only the instructions field of an assistant (async)."""
        res = await self._http.request("PATCH", f"{self._base}/assistants/{assistant_id}/instructions", json={"instructions": instructions})
        return res.json()

    async def list_assistant_agents(self) -> List[Dict[str, Any]]:
        """List all assistant agents (async)."""
        res = await self._http.request("GET", f"{self._base}/assistants/agents")
        return res.json()
