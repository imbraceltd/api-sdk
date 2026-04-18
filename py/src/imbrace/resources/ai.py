from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union
import json
from ..http import HttpTransport, AsyncHttpTransport
from ..types.ai import Completion, StreamChunk, Embedding


class AiResource:
    """AI domain — Sync. Completions, embeddings, assistants, RAG, guardrails, financial docs."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2"

    @property
    def _v3(self) -> str:
        return f"{self._base}/v3"

    # --- Completions / Embeddings ---
    def complete(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Completion:
        """Tạo chat completion."""
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if metadata:
            body["metadata"] = metadata
        res = self._http.request("POST", f"{self._v3}/completions", json=body).json()
        if "data" in res and "success" in res:
            return Completion(**res["data"])
        return Completion(**res)

    def stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Iterator[StreamChunk]:
        """Stream chat completion."""
        import httpx
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": True}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens

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

    def embed(self, model: str, input: List[str]) -> Embedding:
        """Tạo embeddings cho danh sách text."""
        res = self._http.request("POST", f"{self._v3}/embeddings", json={"model": model, "input": input}).json()
        if "data" in res and "success" in res:
            return Embedding(**res["data"])
        return Embedding(**res)

    # --- Assistants ---
    def list_assistants(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/accounts/assistants").json()

    def get_assistant(self, assistant_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/assistants/{assistant_id}").json()

    def check_assistant_name(self, name: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/assistants/check-name", params={"name": name}).json()

    def list_agents(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/assistants/agents").json()

    def patch_instructions(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._v3}/assistants/{assistant_id}/instructions", json=body).json()

    # --- Assistant Apps ---
    def list_assistant_apps(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/assistant_apps").json()

    def get_assistant_app(self, assistant_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/assistant_apps/{assistant_id}").json()

    def create_assistant_app(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v3}/assistant_apps", json=body).json()

    def update_assistant_app(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v3}/assistant_apps/{assistant_id}", json=body).json()

    def delete_assistant_app(self, assistant_id: str) -> None:
        self._http.request("DELETE", f"{self._v3}/assistant_apps/{assistant_id}")

    def update_assistant_workflow(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v3}/assistant_apps/{assistant_id}/workflow", json=body).json()

    # --- RAG Files ---
    def list_rag_files(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/rag/files").json()

    def get_rag_file(self, file_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/rag/files/{file_id}").json()

    def upload_rag_file(self, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v3}/rag/files", files=files).json()

    def delete_rag_file(self, file_id: str) -> None:
        self._http.request("DELETE", f"{self._v3}/rag/files/{file_id}")

    # --- Guardrails ---
    def list_guardrails(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/guardrail/all").json()

    def get_guardrail(self, guardrail_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/guardrail/{guardrail_id}").json()

    def create_guardrail(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v3}/guardrail/create", json=body).json()

    def update_guardrail(self, guardrail_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v3}/guardrail/update/{guardrail_id}", json=body).json()

    def delete_guardrail(self, guardrail_id: str) -> None:
        self._http.request("DELETE", f"{self._v3}/guardrail/delete/{guardrail_id}")

    # --- Guardrail Providers ---
    def list_guardrail_providers(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/guardrail-providers").json()

    def get_guardrail_provider(self, provider_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/guardrail-providers/{provider_id}").json()

    def create_guardrail_provider(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v3}/guardrail-providers", json=body).json()

    def update_guardrail_provider(self, provider_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v3}/guardrail-providers/{provider_id}", json=body).json()

    def delete_guardrail_provider(self, provider_id: str) -> None:
        self._http.request("DELETE", f"{self._v3}/guardrail-providers/{provider_id}")

    def test_guardrail_provider(self, provider_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v3}/guardrail-providers/{provider_id}/test", json=body).json()

    def get_guardrail_provider_models(self, provider_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/guardrail-providers/{provider_id}/models").json()

    # --- Custom Providers ---
    def list_providers(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/providers").json()

    def create_provider(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v3}/providers", json=body).json()

    def update_provider(self, provider_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v3}/providers/{provider_id}", json=body).json()

    def delete_provider(self, provider_id: str) -> None:
        self._http.request("DELETE", f"{self._v3}/providers/{provider_id}")

    def refresh_provider_models(self, provider_id: str) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v3}/providers/{provider_id}/models/refresh").json()

    def get_llm_models(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v3}/workflow-agent/models").json()

    def verify_tool_server(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v3}/configs/tool_servers/verify", json=body).json()

    # --- Financial Documents (v2) ---
    def get_financial_doc(self, doc_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return self._http.request("GET", f"{self._v2}/financial_documents/{doc_id}", params=params).json()

    def update_financial_doc(self, doc_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v2}/financial_documents/{doc_id}", json=body).json()

    def delete_financial_doc(self, doc_id: str) -> None:
        self._http.request("DELETE", f"{self._v2}/financial_documents/{doc_id}")

    def suggest_financial_fix(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v2}/financial_documents/suggest", json=body).json()

    def fix_financial_doc(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v2}/financial_documents/fix", json=body).json()

    def reset_financial_doc(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v2}/financial_documents/reset", json=body).json()

    def get_financial_doc_error_files(self, file_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v2}/financial_documents/errors-files/{file_id}").json()

    def get_financial_report(self, report_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return self._http.request("GET", f"{self._v2}/financial_documents/reports/{report_id}", params=params).json()

    def update_financial_report(self, report_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v2}/financial_documents/reports/{report_id}", json=body).json()

    def delete_financial_report(self, report_id: str) -> None:
        self._http.request("DELETE", f"{self._v2}/financial_documents/reports/{report_id}")


class AsyncAiResource:
    """AI domain — Async. Full parity với AiResource sync."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2"

    @property
    def _v3(self) -> str:
        return f"{self._base}/v3"

    # --- Completions / Embeddings ---

    async def complete(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Completion:
        """Tạo chat completion (bất đồng bộ)."""
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if metadata:
            body["metadata"] = metadata
        res = await self._http.request("POST", f"{self._v3}/completions", json=body)
        data = res.json()
        if "data" in data and "success" in data:
            return Completion(**data["data"])
        return Completion(**data)

    async def stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[StreamChunk]:
        """Stream chat completion (bất đồng bộ)."""
        import httpx
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": True}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens

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
        """Tạo embeddings (bất đồng bộ)."""
        res = await self._http.request("POST", f"{self._v3}/embeddings", json={"model": model, "input": input})
        data = res.json()
        if "data" in data and "success" in data:
            return Embedding(**data["data"])
        return Embedding(**data)

    # --- Assistants ---

    async def list_assistants(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/accounts/assistants")
        return res.json()

    async def get_assistant(self, assistant_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/assistants/{assistant_id}")
        return res.json()

    async def check_assistant_name(self, name: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/assistants/check-name", params={"name": name})
        return res.json()

    async def list_agents(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/assistants/agents")
        return res.json()

    async def patch_instructions(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._v3}/assistants/{assistant_id}/instructions", json=body)
        return res.json()

    # --- Assistant Apps ---

    async def list_assistant_apps(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/assistant_apps")
        return res.json()

    async def get_assistant_app(self, assistant_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/assistant_apps/{assistant_id}")
        return res.json()

    async def create_assistant_app(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v3}/assistant_apps", json=body)
        return res.json()

    async def update_assistant_app(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v3}/assistant_apps/{assistant_id}", json=body)
        return res.json()

    async def delete_assistant_app(self, assistant_id: str) -> None:
        await self._http.request("DELETE", f"{self._v3}/assistant_apps/{assistant_id}")

    async def update_assistant_workflow(self, assistant_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v3}/assistant_apps/{assistant_id}/workflow", json=body)
        return res.json()

    # --- RAG Files ---

    async def list_rag_files(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/rag/files")
        return res.json()

    async def get_rag_file(self, file_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/rag/files/{file_id}")
        return res.json()

    async def upload_rag_file(self, files: Any) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v3}/rag/files", files=files)
        return res.json()

    async def delete_rag_file(self, file_id: str) -> None:
        await self._http.request("DELETE", f"{self._v3}/rag/files/{file_id}")

    # --- Guardrails ---

    async def list_guardrails(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/guardrail/all")
        return res.json()

    async def get_guardrail(self, guardrail_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/guardrail/{guardrail_id}")
        return res.json()

    async def create_guardrail(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v3}/guardrail/create", json=body)
        return res.json()

    async def update_guardrail(self, guardrail_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v3}/guardrail/update/{guardrail_id}", json=body)
        return res.json()

    async def delete_guardrail(self, guardrail_id: str) -> None:
        await self._http.request("DELETE", f"{self._v3}/guardrail/delete/{guardrail_id}")

    # --- Guardrail Providers ---

    async def list_guardrail_providers(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/guardrail-providers")
        return res.json()

    async def get_guardrail_provider(self, provider_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/guardrail-providers/{provider_id}")
        return res.json()

    async def create_guardrail_provider(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v3}/guardrail-providers", json=body)
        return res.json()

    async def update_guardrail_provider(self, provider_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v3}/guardrail-providers/{provider_id}", json=body)
        return res.json()

    async def delete_guardrail_provider(self, provider_id: str) -> None:
        await self._http.request("DELETE", f"{self._v3}/guardrail-providers/{provider_id}")

    async def test_guardrail_provider(self, provider_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v3}/guardrail-providers/{provider_id}/test", json=body)
        return res.json()

    async def get_guardrail_provider_models(self, provider_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/guardrail-providers/{provider_id}/models")
        return res.json()

    # --- Custom Providers ---

    async def list_providers(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/providers")
        return res.json()

    async def create_provider(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v3}/providers", json=body)
        return res.json()

    async def update_provider(self, provider_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v3}/providers/{provider_id}", json=body)
        return res.json()

    async def delete_provider(self, provider_id: str) -> None:
        await self._http.request("DELETE", f"{self._v3}/providers/{provider_id}")

    async def refresh_provider_models(self, provider_id: str) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v3}/providers/{provider_id}/models/refresh")
        return res.json()

    async def get_llm_models(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v3}/workflow-agent/models")
        return res.json()

    async def verify_tool_server(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v3}/configs/tool_servers/verify", json=body)
        return res.json()

    # --- Financial Documents (v2) ---

    async def get_financial_doc(self, doc_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        res = await self._http.request("GET", f"{self._v2}/financial_documents/{doc_id}", params=params)
        return res.json()

    async def update_financial_doc(self, doc_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v2}/financial_documents/{doc_id}", json=body)
        return res.json()

    async def delete_financial_doc(self, doc_id: str) -> None:
        await self._http.request("DELETE", f"{self._v2}/financial_documents/{doc_id}")

    async def suggest_financial_fix(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v2}/financial_documents/suggest", json=body)
        return res.json()

    async def fix_financial_doc(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v2}/financial_documents/fix", json=body)
        return res.json()

    async def reset_financial_doc(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v2}/financial_documents/reset", json=body)
        return res.json()

    async def get_financial_doc_error_files(self, file_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v2}/financial_documents/errors-files/{file_id}")
        return res.json()

    async def get_financial_report(self, report_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        res = await self._http.request("GET", f"{self._v2}/financial_documents/reports/{report_id}", params=params)
        return res.json()

    async def update_financial_report(self, report_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v2}/financial_documents/reports/{report_id}", json=body)
        return res.json()

    async def delete_financial_report(self, report_id: str) -> None:
        await self._http.request("DELETE", f"{self._v2}/financial_documents/reports/{report_id}")
