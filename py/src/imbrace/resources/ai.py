from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union
import json
from typing_extensions import TypedDict
from ..http import HttpTransport, AsyncHttpTransport
from ..types.ai import Completion, StreamChunk, Embedding, CompletionInput, EmbeddingInput


class Assistant(TypedDict, total=False):
    _id: str
    name: str
    description: Optional[str]
    instructions: Optional[str]
    model: Optional[str]
    mode: Optional[str]
    model_id: Optional[str]
    provider_id: Optional[str]
    show_thinking_process: Optional[bool]
    streaming: Optional[bool]
    channel: Optional[str]
    channel_id: Optional[str]
    teams: Optional[Union[str, List[str]]]
    categories: Optional[List[int]]
    guardrail_id: Optional[str]
    personality_and_role: Optional[str]
    core_task: Optional[str]
    agent_type: Optional[str]
    sub_agents: Optional[List[Any]]
    team_leads: Optional[List[Any]]
    is_orchestrator: Optional[bool]
    preload_information: Optional[str]
    tone_and_style: Optional[str]
    response_length: Optional[str]
    list_of_banned_words: Optional[str]
    files: Optional[Any]
    selected_board_id: Optional[str]
    folder_ids: Optional[List[str]]
    default_folder_id: Optional[List[str]]
    board_ids: Optional[List[str]]
    knowledge_hubs: Optional[List[str]]
    workflow_functions: Optional[List[Any]]
    temperature: Optional[float]
    use_memory: Optional[bool]
    tool_server: Optional[Any]
    enable_echart: Optional[bool]
    top_k_relevant_results: Optional[int]
    top_k: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]


class AssistantListResponse(TypedDict, total=False):
    data: List[Assistant]
    total: Optional[int]


class AssistantNameCheckResponse(TypedDict):
    available: bool
    name: str


class PatchInstructionsInput(TypedDict, total=False):
    instructions: str


class AssistantApp(TypedDict, total=False):
    _id: str
    name: str
    assistant_id: Optional[str]
    mode: Optional[str]
    model_id: Optional[str]
    provider_id: Optional[str]
    instructions: Optional[str]
    agent_type: Optional[str]
    workflow: Optional[Dict[str, Any]]
    created_at: Optional[str]
    updated_at: Optional[str]


class AssistantAppListResponse(TypedDict, total=False):
    data: List[AssistantApp]
    total: Optional[int]


class CreateAssistantAppInput(TypedDict, total=False):
    name: str
    assistant_id: str
    mode: Optional[str]
    model_id: Optional[str]
    provider_id: Optional[str]
    instructions: Optional[str]
    agent_type: Optional[str]


class UpdateAssistantAppInput(TypedDict, total=False):
    name: str
    mode: Optional[str]
    model_id: Optional[str]
    provider_id: Optional[str]
    instructions: Optional[str]
    agent_type: Optional[str]


class UpdateAssistantWorkflowInput(TypedDict, total=False):
    workflow: Dict[str, Any]


class RagFile(TypedDict, total=False):
    _id: str
    name: str
    size: Optional[int]
    status: Optional[str]
    created_at: Optional[str]


class RagFileListResponse(TypedDict, total=False):
    data: List[RagFile]
    total: Optional[int]


class Guardrail(TypedDict, total=False):
    _id: str
    name: str
    type: Optional[str]
    config: Optional[Dict[str, Any]]
    created_at: Optional[str]
    updated_at: Optional[str]


class GuardrailListResponse(TypedDict, total=False):
    data: List[Guardrail]
    total: Optional[int]


class CreateGuardrailInput(TypedDict, total=False):
    name: str
    type: str
    config: Dict[str, Any]


class UpdateGuardrailInput(TypedDict, total=False):
    name: str
    config: Dict[str, Any]


class GuardrailProvider(TypedDict, total=False):
    _id: str
    name: str
    type: Optional[str]
    config: Optional[Dict[str, Any]]
    created_at: Optional[str]
    updated_at: Optional[str]


class GuardrailProviderListResponse(TypedDict, total=False):
    data: List[GuardrailProvider]
    total: Optional[int]


class CreateGuardrailProviderInput(TypedDict, total=False):
    name: str
    type: str
    config: Dict[str, Any]


class UpdateGuardrailProviderInput(TypedDict, total=False):
    name: str
    config: Dict[str, Any]


class TestGuardrailProviderInput(TypedDict, total=False):
    prompt: str


class GuardrailProviderTestResponse(TypedDict, total=False):
    success: bool
    result: Optional[Dict[str, Any]]


class GuardrailProviderModelsResponse(TypedDict, total=False):
    models: List[Dict[str, Any]]


class AiProvider(TypedDict, total=False):
    _id: str
    name: str
    type: Optional[str]
    api_key: Optional[str]
    base_url: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


class AiProviderListResponse(TypedDict, total=False):
    data: List[AiProvider]
    total: Optional[int]


class CreateAiProviderInput(TypedDict, total=False):
    name: str
    type: str
    api_key: str
    base_url: str


class UpdateAiProviderInput(TypedDict, total=False):
    name: str
    api_key: str
    base_url: str


class LlmModelsResponse(TypedDict, total=False):
    models: List[Dict[str, Any]]


class VerifyToolServerInput(TypedDict, total=False):
    url: str


class VerifyToolServerResponse(TypedDict, total=False):
    success: bool
    tools: Optional[List[Dict[str, Any]]]


class FinancialDoc(TypedDict, total=False):
    _id: str
    name: Optional[str]
    status: Optional[str]
    pages: Optional[List[Any]]
    created_at: Optional[str]
    updated_at: Optional[str]


class FinancialFixInput(TypedDict, total=False):
    doc_id: str


class FinancialErrorFilesResponse(TypedDict, total=False):
    files: Optional[List[Any]]


class FinancialReport(TypedDict, total=False):
    _id: str
    name: Optional[str]
    status: Optional[str]


class AiResource:
    """AI domain — Sync. Completions, embeddings, assistants, RAG, guardrails, financial docs."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v2(self) -> str:
        return f"{self._base.rstrip('/')}/v2/ai"

    @property
    def _v3(self) -> str:
        return f"{self._base.rstrip('/')}/v3/ai"

    @property
    def _assistant_base(self) -> str:
        return self._v2 if "app-gatewayv2" in self._base else self._v3

    # --- Completions / Embeddings ---
    def complete(self, input: CompletionInput) -> Completion:
        """Create chat completion."""
        body = {**input.model_dump(exclude_none=True), "stream": False}
        res = self._http.request("POST", f"{self._v3}/completions", json=body).json()
        if "data" in res and "success" in res:
            return Completion(**res["data"])
        return Completion(**res)

    def stream(self, input: CompletionInput) -> Iterator[StreamChunk]:
        """Stream chat completion."""
        import httpx
        body = {**input.model_dump(exclude_none=True), "stream": True}

        headers: Dict[str, str] = {"Content-Type": "application/json", "Accept": "text/event-stream"}
        if self._http.api_key:
            headers["X-Api-Key"] = self._http.api_key
        token = self._http.token_manager.get_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"

        with httpx.Client(timeout=None) as client:
            with client.stream("POST", f"{self._v3}/completions", json=body, headers=headers) as res:
                for line in res.iter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk_data = json.loads(data)
                            yield StreamChunk(**chunk_data)
                        except json.JSONDecodeError:
                            continue

    def embed(self, input: EmbeddingInput) -> Embedding:
        """Create embeddings."""
        res = self._http.request("POST", f"{self._v3}/embeddings", json=input.model_dump()).json()
        if "data" in res and "success" in res:
            return Embedding(**res["data"])
        return Embedding(**res)

    # --- Assistants ---
    def list_assistants(self) -> AssistantListResponse:
        return self._http.request("GET", f"{self._assistant_base}/accounts/assistants").json()

    def get_assistant(self, assistant_id: str) -> Assistant:
        return self._http.request("GET", f"{self._assistant_base}/assistants/{assistant_id}").json()

    def check_assistant_name(self, name: str) -> AssistantNameCheckResponse:
        return self._http.request("GET", f"{self._assistant_base}/assistants/check-name", params={"name": name}).json()

    def list_agents(self) -> AssistantListResponse:
        return self._http.request("GET", f"{self._assistant_base}/assistants/agents").json()

    def patch_instructions(self, assistant_id: str, body: PatchInstructionsInput) -> Assistant:
        return self._http.request("PATCH", f"{self._assistant_base}/assistants/{assistant_id}/instructions", json=body).json()

    # --- Assistant Apps ---
    def list_assistant_apps(self) -> AssistantAppListResponse:
        return self._http.request("GET", f"{self._assistant_base}/assistant_apps").json()

    def get_assistant_app(self, assistant_id: str) -> AssistantApp:
        return self._http.request("GET", f"{self._assistant_base}/assistant_apps/{assistant_id}").json()

    def create_assistant_app(self, body: CreateAssistantAppInput) -> AssistantApp:
        return self._http.request("POST", f"{self._assistant_base}/assistant_apps", json=body).json()

    def update_assistant_app(self, assistant_id: str, body: UpdateAssistantAppInput) -> AssistantApp:
        return self._http.request("PUT", f"{self._assistant_base}/assistant_apps/{assistant_id}", json=body).json()

    def delete_assistant_app(self, assistant_id: str) -> None:
        self._http.request("DELETE", f"{self._assistant_base}/assistant_apps/{assistant_id}")

    def update_assistant_workflow(self, assistant_id: str, body: UpdateAssistantWorkflowInput) -> AssistantApp:
        return self._http.request("PUT", f"{self._assistant_base}/assistant_apps/{assistant_id}/workflow", json=body).json()

    # --- RAG Files ---
    def list_rag_files(self) -> RagFileListResponse:
        return self._http.request("GET", f"{self._v3}/rag/files").json()

    def get_rag_file(self, file_id: str) -> RagFile:
        return self._http.request("GET", f"{self._v3}/rag/files/{file_id}").json()

    def upload_rag_file(self, files: Any) -> RagFile:
        return self._http.request("POST", f"{self._v3}/rag/files", files=files).json()

    def delete_rag_file(self, file_id: str) -> None:
        self._http.request("DELETE", f"{self._v3}/rag/files/{file_id}")

    # --- Guardrails ---
    def list_guardrails(self) -> GuardrailListResponse:
        return self._http.request("GET", f"{self._v3}/guardrail/all").json()

    def get_guardrail(self, guardrail_id: str) -> Guardrail:
        return self._http.request("GET", f"{self._v3}/guardrail/{guardrail_id}").json()

    def create_guardrail(self, body: CreateGuardrailInput) -> Guardrail:
        return self._http.request("POST", f"{self._v3}/guardrail/create", json=body).json()

    def update_guardrail(self, guardrail_id: str, body: UpdateGuardrailInput) -> Guardrail:
        return self._http.request("PUT", f"{self._v3}/guardrail/update/{guardrail_id}", json=body).json()

    def delete_guardrail(self, guardrail_id: str) -> None:
        self._http.request("DELETE", f"{self._v3}/guardrail/delete/{guardrail_id}")

    # --- Guardrail Providers ---
    def list_guardrail_providers(self) -> GuardrailProviderListResponse:
        return self._http.request("GET", f"{self._v3}/guardrail-providers").json()

    def get_guardrail_provider(self, provider_id: str) -> GuardrailProvider:
        return self._http.request("GET", f"{self._v3}/guardrail-providers/{provider_id}").json()

    def create_guardrail_provider(self, body: CreateGuardrailProviderInput) -> GuardrailProvider:
        return self._http.request("POST", f"{self._v3}/guardrail-providers", json=body).json()

    def update_guardrail_provider(self, provider_id: str, body: UpdateGuardrailProviderInput) -> GuardrailProvider:
        return self._http.request("PUT", f"{self._v3}/guardrail-providers/{provider_id}", json=body).json()

    def delete_guardrail_provider(self, provider_id: str) -> None:
        self._http.request("DELETE", f"{self._v3}/guardrail-providers/{provider_id}")

    def test_guardrail_provider(self, provider_id: str, body: TestGuardrailProviderInput) -> GuardrailProviderTestResponse:
        return self._http.request("POST", f"{self._v3}/guardrail-providers/{provider_id}/test", json=body).json()

    def get_guardrail_provider_models(self, provider_id: str) -> GuardrailProviderModelsResponse:
        return self._http.request("GET", f"{self._v3}/guardrail-providers/{provider_id}/models").json()

    # --- Custom Providers ---
    def list_providers(self) -> AiProviderListResponse:
        return self._http.request("GET", f"{self._v3}/providers").json()

    def create_provider(self, body: CreateAiProviderInput) -> AiProvider:
        return self._http.request("POST", f"{self._v3}/providers", json=body).json()

    def update_provider(self, provider_id: str, body: UpdateAiProviderInput) -> AiProvider:
        return self._http.request("PUT", f"{self._v3}/providers/{provider_id}", json=body).json()

    def delete_provider(self, provider_id: str) -> None:
        self._http.request("DELETE", f"{self._v3}/providers/{provider_id}")

    def refresh_provider_models(self, provider_id: str) -> AiProvider:
        return self._http.request("POST", f"{self._v3}/providers/{provider_id}/models/refresh").json()

    def get_llm_models(self) -> LlmModelsResponse:
        return self._http.request("GET", f"{self._v3}/workflow-agent/models").json()

    def verify_tool_server(self, body: VerifyToolServerInput) -> VerifyToolServerResponse:
        return self._http.request("POST", f"{self._v3}/configs/tool_servers/verify", json=body).json()

    # --- Financial Documents (v2) ---
    def get_financial_doc(self, doc_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> FinancialDoc:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return self._http.request("GET", f"{self._v2}/financial_documents/{doc_id}", params=params).json()

    def update_financial_doc(self, doc_id: str, body: Dict[str, Any]) -> FinancialDoc:
        return self._http.request("PUT", f"{self._v2}/financial_documents/{doc_id}", json=body).json()

    def delete_financial_doc(self, doc_id: str) -> None:
        self._http.request("DELETE", f"{self._v2}/financial_documents/{doc_id}")

    def suggest_financial_fix(self, body: FinancialFixInput) -> FinancialDoc:
        return self._http.request("POST", f"{self._v2}/financial_documents/suggest", json=body).json()

    def fix_financial_doc(self, body: FinancialFixInput) -> FinancialDoc:
        return self._http.request("POST", f"{self._v2}/financial_documents/fix", json=body).json()

    def reset_financial_doc(self, body: FinancialFixInput) -> FinancialDoc:
        return self._http.request("POST", f"{self._v2}/financial_documents/reset", json=body).json()

    def get_financial_doc_error_files(self, file_id: str) -> FinancialErrorFilesResponse:
        return self._http.request("GET", f"{self._v2}/financial_documents/errors-files/{file_id}").json()

    def get_financial_report(self, report_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> FinancialReport:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return self._http.request("GET", f"{self._v2}/financial_documents/reports/{report_id}", params=params).json()

    def update_financial_report(self, report_id: str, body: Dict[str, Any]) -> FinancialReport:
        return self._http.request("PUT", f"{self._v2}/financial_documents/reports/{report_id}", json=body).json()

    def delete_financial_report(self, report_id: str) -> None:
        self._http.request("DELETE", f"{self._v2}/financial_documents/reports/{report_id}")

    # --- AI Assistants (v2) ---

    def list_assistants_v2(self) -> AssistantListResponse:
        """List assistants (v2)."""
        return self._http.request("GET", f"{self._v2}/ai/assistants").json()

    def create_assistant_v2(self, body: Dict[str, Any]) -> Assistant:
        """Create assistant (v2)."""
        return self._http.request("POST", f"{self._v2}/ai/assistants", json=body).json()

    def update_assistant_v2(self, assistant_id: str, body: Dict[str, Any]) -> Assistant:
        """Update assistant (v2)."""
        return self._http.request("PUT", f"{self._v2}/ai/assistants/{assistant_id}", json=body).json()

    def delete_assistant_v2(self, assistant_id: str) -> None:
        """Delete assistant (v2)."""
        self._http.request("DELETE", f"{self._v2}/ai/assistants/{assistant_id}")

    def create_assistant_app_v2(self, body: Dict[str, Any]) -> AssistantApp:
        """Create assistant app (v2)."""
        return self._http.request("POST", f"{self._v2}/ai/assistant_apps", json=body).json()


class AsyncAiResource:
    """AI domain — Async. Full parity with sync AiResource."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v2(self) -> str:
        return f"{self._base.rstrip('/')}/v2/ai"

    @property
    def _v3(self) -> str:
        return f"{self._base.rstrip('/')}/v3/ai"

    @property
    def _assistant_base(self) -> str:
        return self._v2 if "app-gatewayv2" in self._base else self._v3

    # --- Completions / Embeddings ---

    async def complete(self, input: CompletionInput) -> Completion:
        """Create chat completion (async)."""
        body = {**input.model_dump(exclude_none=True), "stream": False}
        res = await self._http.request("POST", f"{self._v3}/completions", json=body)
        data = res.json()
        if "data" in data and "success" in data:
            return Completion(**data["data"])
        return Completion(**data)

    async def stream(self, input: CompletionInput) -> AsyncIterator[StreamChunk]:
        """Stream chat completion (async)."""
        import httpx
        body = {**input.model_dump(exclude_none=True), "stream": True}

        headers: Dict[str, str] = {"Content-Type": "application/json", "Accept": "text/event-stream"}
        if self._http.api_key:
            headers["X-Api-Key"] = self._http.api_key
        token = self._http.token_manager.get_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", f"{self._v3}/completions", json=body, headers=headers) as res:
                async for line in res.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk_data = json.loads(data)
                            yield StreamChunk(**chunk_data)
                        except json.JSONDecodeError:
                            continue

    async def embed(self, model: str, input: List[str]) -> Embedding:
        """Create embeddings (async)."""
        res = await self._http.request("POST", f"{self._v3}/embeddings", json={"model": model, "input": input})
        data = res.json()
        if "data" in data and "success" in data:
            return Embedding(**data["data"])
        return Embedding(**data)

    # --- Assistants ---

    async def list_assistants(self) -> AssistantListResponse:
        res = await self._http.request("GET", f"{self._assistant_base}/accounts/assistants")
        return res.json()

    async def get_assistant(self, assistant_id: str) -> Assistant:
        res = await self._http.request("GET", f"{self._assistant_base}/assistants/{assistant_id}")
        return res.json()

    async def check_assistant_name(self, name: str) -> AssistantNameCheckResponse:
        res = await self._http.request("GET", f"{self._assistant_base}/assistants/check-name", params={"name": name})
        return res.json()

    async def list_agents(self) -> AssistantListResponse:
        res = await self._http.request("GET", f"{self._assistant_base}/assistants/agents")
        return res.json()

    async def patch_instructions(self, assistant_id: str, body: PatchInstructionsInput) -> Assistant:
        res = await self._http.request("PATCH", f"{self._assistant_base}/assistants/{assistant_id}/instructions", json=body)
        return res.json()

    # --- Assistant Apps ---

    async def list_assistant_apps(self) -> AssistantAppListResponse:
        res = await self._http.request("GET", f"{self._assistant_base}/assistant_apps")
        return res.json()

    async def get_assistant_app(self, assistant_id: str) -> AssistantApp:
        res = await self._http.request("GET", f"{self._assistant_base}/assistant_apps/{assistant_id}")
        return res.json()

    async def create_assistant_app(self, body: CreateAssistantAppInput) -> AssistantApp:
        res = await self._http.request("POST", f"{self._assistant_base}/assistant_apps", json=body)
        return res.json()

    async def update_assistant_app(self, assistant_id: str, body: UpdateAssistantAppInput) -> AssistantApp:
        res = await self._http.request("PUT", f"{self._assistant_base}/assistant_apps/{assistant_id}", json=body)
        return res.json()

    async def delete_assistant_app(self, assistant_id: str) -> None:
        await self._http.request("DELETE", f"{self._assistant_base}/assistant_apps/{assistant_id}")

    async def update_assistant_workflow(self, assistant_id: str, body: UpdateAssistantWorkflowInput) -> AssistantApp:
        res = await self._http.request("PUT", f"{self._assistant_base}/assistant_apps/{assistant_id}/workflow", json=body)
        return res.json()

    # --- RAG Files ---

    async def list_rag_files(self) -> RagFileListResponse:
        res = await self._http.request("GET", f"{self._v3}/rag/files")
        return res.json()

    async def get_rag_file(self, file_id: str) -> RagFile:
        res = await self._http.request("GET", f"{self._v3}/rag/files/{file_id}")
        return res.json()

    async def upload_rag_file(self, files: Any) -> RagFile:
        res = await self._http.request("POST", f"{self._v3}/rag/files", files=files)
        return res.json()

    async def delete_rag_file(self, file_id: str) -> None:
        await self._http.request("DELETE", f"{self._v3}/rag/files/{file_id}")

    # --- Guardrails ---

    async def list_guardrails(self) -> GuardrailListResponse:
        res = await self._http.request("GET", f"{self._v3}/guardrail/all")
        return res.json()

    async def get_guardrail(self, guardrail_id: str) -> Guardrail:
        res = await self._http.request("GET", f"{self._v3}/guardrail/{guardrail_id}")
        return res.json()

    async def create_guardrail(self, body: CreateGuardrailInput) -> Guardrail:
        res = await self._http.request("POST", f"{self._v3}/guardrail/create", json=body)
        return res.json()

    async def update_guardrail(self, guardrail_id: str, body: UpdateGuardrailInput) -> Guardrail:
        res = await self._http.request("PUT", f"{self._v3}/guardrail/update/{guardrail_id}", json=body)
        return res.json()

    async def delete_guardrail(self, guardrail_id: str) -> None:
        await self._http.request("DELETE", f"{self._v3}/guardrail/delete/{guardrail_id}")

    # --- Guardrail Providers ---

    async def list_guardrail_providers(self) -> GuardrailProviderListResponse:
        res = await self._http.request("GET", f"{self._v3}/guardrail-providers")
        return res.json()

    async def get_guardrail_provider(self, provider_id: str) -> GuardrailProvider:
        res = await self._http.request("GET", f"{self._v3}/guardrail-providers/{provider_id}")
        return res.json()

    async def create_guardrail_provider(self, body: CreateGuardrailProviderInput) -> GuardrailProvider:
        res = await self._http.request("POST", f"{self._v3}/guardrail-providers", json=body)
        return res.json()

    async def update_guardrail_provider(self, provider_id: str, body: UpdateGuardrailProviderInput) -> GuardrailProvider:
        res = await self._http.request("PUT", f"{self._v3}/guardrail-providers/{provider_id}", json=body)
        return res.json()

    async def delete_guardrail_provider(self, provider_id: str) -> None:
        await self._http.request("DELETE", f"{self._v3}/guardrail-providers/{provider_id}")

    async def test_guardrail_provider(self, provider_id: str, body: TestGuardrailProviderInput) -> GuardrailProviderTestResponse:
        res = await self._http.request("POST", f"{self._v3}/guardrail-providers/{provider_id}/test", json=body)
        return res.json()

    async def get_guardrail_provider_models(self, provider_id: str) -> GuardrailProviderModelsResponse:
        res = await self._http.request("GET", f"{self._v3}/guardrail-providers/{provider_id}/models")
        return res.json()

    # --- Custom Providers ---

    async def list_providers(self) -> AiProviderListResponse:
        res = await self._http.request("GET", f"{self._v3}/providers")
        return res.json()

    async def create_provider(self, body: CreateAiProviderInput) -> AiProvider:
        res = await self._http.request("POST", f"{self._v3}/providers", json=body)
        return res.json()

    async def update_provider(self, provider_id: str, body: UpdateAiProviderInput) -> AiProvider:
        res = await self._http.request("PUT", f"{self._v3}/providers/{provider_id}", json=body)
        return res.json()

    async def delete_provider(self, provider_id: str) -> None:
        await self._http.request("DELETE", f"{self._v3}/providers/{provider_id}")

    async def refresh_provider_models(self, provider_id: str) -> AiProvider:
        res = await self._http.request("POST", f"{self._v3}/providers/{provider_id}/models/refresh")
        return res.json()

    async def get_llm_models(self) -> LlmModelsResponse:
        res = await self._http.request("GET", f"{self._v3}/workflow-agent/models")
        return res.json()

    async def verify_tool_server(self, body: VerifyToolServerInput) -> VerifyToolServerResponse:
        res = await self._http.request("POST", f"{self._v3}/configs/tool_servers/verify", json=body)
        return res.json()

    # --- Financial Documents (v2) ---

    async def get_financial_doc(self, doc_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> FinancialDoc:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        res = await self._http.request("GET", f"{self._v2}/financial_documents/{doc_id}", params=params)
        return res.json()

    async def update_financial_doc(self, doc_id: str, body: Dict[str, Any]) -> FinancialDoc:
        res = await self._http.request("PUT", f"{self._v2}/financial_documents/{doc_id}", json=body)
        return res.json()

    async def delete_financial_doc(self, doc_id: str) -> None:
        await self._http.request("DELETE", f"{self._v2}/financial_documents/{doc_id}")

    async def suggest_financial_fix(self, body: FinancialFixInput) -> FinancialDoc:
        res = await self._http.request("POST", f"{self._v2}/financial_documents/suggest", json=body)
        return res.json()

    async def fix_financial_doc(self, body: FinancialFixInput) -> FinancialDoc:
        res = await self._http.request("POST", f"{self._v2}/financial_documents/fix", json=body)
        return res.json()

    async def reset_financial_doc(self, body: FinancialFixInput) -> FinancialDoc:
        res = await self._http.request("POST", f"{self._v2}/financial_documents/reset", json=body)
        return res.json()

    async def get_financial_doc_error_files(self, file_id: str) -> FinancialErrorFilesResponse:
        res = await self._http.request("GET", f"{self._v2}/financial_documents/errors-files/{file_id}")
        return res.json()

    async def get_financial_report(self, report_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> FinancialReport:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        res = await self._http.request("GET", f"{self._v2}/financial_documents/reports/{report_id}", params=params)
        return res.json()

    async def update_financial_report(self, report_id: str, body: Dict[str, Any]) -> FinancialReport:
        res = await self._http.request("PUT", f"{self._v2}/financial_documents/reports/{report_id}", json=body)
        return res.json()

    async def delete_financial_report(self, report_id: str) -> None:
        await self._http.request("DELETE", f"{self._v2}/financial_documents/reports/{report_id}")

    # --- AI Assistants (v2) ---

    async def list_assistants_v2(self) -> AssistantListResponse:
        """List assistants (v2) (async)."""
        res = await self._http.request("GET", f"{self._v2}/ai/assistants")
        return res.json()

    async def create_assistant_v2(self, body: Dict[str, Any]) -> Assistant:
        """Create assistant (v2) (async)."""
        res = await self._http.request("POST", f"{self._v2}/ai/assistants", json=body)
        return res.json()

    async def update_assistant_v2(self, assistant_id: str, body: Dict[str, Any]) -> Assistant:
        """Update assistant (v2) (async)."""
        res = await self._http.request("PUT", f"{self._v2}/ai/assistants/{assistant_id}", json=body)
        return res.json()

    async def delete_assistant_v2(self, assistant_id: str) -> None:
        """Delete assistant (v2) (async)."""
        await self._http.request("DELETE", f"{self._v2}/ai/assistants/{assistant_id}")

    async def create_assistant_app_v2(self, body: Dict[str, Any]) -> AssistantApp:
        """Create assistant app (v2) (async)."""
        res = await self._http.request("POST", f"{self._v2}/ai/assistant_apps", json=body)
        return res.json()
