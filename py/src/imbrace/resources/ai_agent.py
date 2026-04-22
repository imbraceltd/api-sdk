from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, quote
from ..http import HttpTransport, AsyncHttpTransport


def _qs(params: Dict[str, Any]) -> str:
    filtered = {k: v for k, v in params.items() if v is not None}
    if not filtered:
        return ""
    return "?" + urlencode(filtered)


class AiAgentResource:
    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    # --- System ---

    def get_config(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/config").json()

    def get_health(self, detailed: bool = False) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/health{_qs({'detailed': detailed or None})}").json()

    def get_version(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/version").json()

    # --- Chat v1 ---

    def list_chats(self, organization_id: str, user_id: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/chat{_qs({'organization_id': organization_id, 'user_id': user_id, 'limit': limit})}").json()

    def get_chat(self, chat_id: str, include_messages: bool = False) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/chat/{chat_id}{_qs({'include_messages': True if include_messages else None})}").json()

    def delete_chat(self, chat_id: str, organization_id: str, user_id: Optional[str] = None) -> Any:
        return self._http.request("DELETE", f"{self._base}/chat/{chat_id}{_qs({'organization_id': organization_id, 'user_id': user_id})}").json()

    # --- Chat v2 (streaming — returns raw httpx.Response; iterate with .iter_lines()) ---

    def stream_chat(self, body: Dict[str, Any]) -> Any:
        return self._http.request("POST", f"{self._base}/v2/chat", json=body)

    # --- Sub-agent chat v2 ---

    def stream_sub_agent_chat(self, body: Dict[str, Any]) -> Any:
        return self._http.request("POST", f"{self._base}/v2/sub-agent-chat", json=body)

    def get_sub_agent_history(self, session_id: str, chat_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/v2/sub-agent-chat/history{_qs({'session_id': session_id, 'chat_id': chat_id})}").json()

    # --- Prompt suggestions ---

    def get_agent_prompt_suggestion(self, assistant_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/chat/get-agent-prompt-suggestion{_qs({'assistant_id': assistant_id})}").json()

    # --- Embeddings / files ---

    def process_embedding(self, file_id: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/embedding/process", json={"fileId": file_id, "options": options or {}}).json()

    def list_embedding_files(self, **params) -> Any:
        return self._http.request("GET", f"{self._base}/embedding/files{_qs(params)}").json()

    def get_embedding_file(self, file_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/embedding/files/{file_id}").json()

    def preview_embedding_file(self, **params) -> Any:
        return self._http.request("GET", f"{self._base}/embedding/files/preview{_qs(params)}").json()

    def update_embedding_file_status(self, file_id: str, status: str) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/embedding/files/{file_id}/status", json={"status": status}).json()

    def delete_embedding_file(self, file_id: str) -> Any:
        return self._http.request("DELETE", f"{self._base}/embedding/files/{file_id}").json()

    def classify_file(self, **params) -> Any:
        return self._http.request("GET", f"{self._base}/embedding/classify{_qs(params)}").json()

    # --- Data Board ---

    def suggest_field_types(self, fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/data-board/suggest-field-types", json={"fields": fields}).json()

    # --- Parquet ---

    def generate_parquet(self, data: List[Any], file_name: Optional[str] = None, folder_name: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"data": data}
        if file_name:
            body["fileName"] = file_name
        if folder_name:
            body["folderName"] = folder_name
        return self._http.request("POST", f"{self._base}/parquet/generate", json=body).json()

    def list_parquet_files(self) -> Any:
        return self._http.request("GET", f"{self._base}/parquet/files").json()

    def delete_parquet_file(self, file_name: str) -> Any:
        return self._http.request("DELETE", f"{self._base}/parquet/{quote(file_name)}").json()

    # --- Trace (Tempo) ---

    def get_traces(self, service: Optional[str] = None, limit: Optional[int] = None, time_range: Optional[int] = None, org_id: Optional[str] = None, details: Optional[bool] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/trace/traces{_qs({'service': service, 'limit': limit, 'timeRange': time_range, 'orgId': org_id, 'details': details})}").json()

    def get_trace(self, trace_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/trace/traces/{trace_id}").json()

    def get_trace_services(self) -> Any:
        return self._http.request("GET", f"{self._base}/trace/services").json()

    def get_trace_tags(self) -> Any:
        return self._http.request("GET", f"{self._base}/trace/tags").json()

    def get_trace_tag_values(self, tag_name: str) -> Any:
        return self._http.request("GET", f"{self._base}/trace/tags/{tag_name}/values").json()

    def search_traceql(self, q: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/trace/search/traceql{_qs({'q': q})}").json()

    # --- Chat Client — Auth ---

    def verify_chat_client_credentials(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/chat-client/auth/verify-credentials", json=body).json()

    def register_chat_client(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/chat-client/auth/register", json=body).json()

    def get_chat_client_user(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/chat-client/auth/user", json=body).json()

    # --- Chat Client — Chats ---

    def create_client_chat(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/chat-client/chats", json=body).json()

    def list_client_chats(self, organization_id: Optional[str] = None, limit: Optional[int] = None, starting_after: Optional[str] = None, ending_before: Optional[str] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/chat-client/chats{_qs({'organization_id': organization_id, 'limit': limit, 'starting_after': starting_after, 'ending_before': ending_before})}").json()

    def delete_all_client_chats(self, organization_id: str) -> Any:
        return self._http.request("DELETE", f"{self._base}/chat-client/chats{_qs({'organization_id': organization_id})}").json()

    def get_client_chat(self, chat_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/chat-client/chats/{chat_id}").json()

    def update_client_chat(self, chat_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._base}/chat-client/chats/{chat_id}", json=body).json()

    def delete_client_chat(self, chat_id: str) -> Any:
        return self._http.request("DELETE", f"{self._base}/chat-client/chats/{chat_id}").json()

    def stream_client_chat_status(self, chat_id: str) -> Any:
        return self._http.request("GET", f"{self._base}/chat-client/chats/{chat_id}/status/stream")

    def generate_client_chat_title(self, chat_id: str) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/chat-client/chats/{chat_id}/title").json()

    # --- Chat Client — Messages ---

    def persist_client_message(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/chat-client/messages", json=body).json()

    def list_client_messages(self, chat_id: str) -> Any:
        return self._http.request("GET", f"{self._base}/chat-client/chats/{chat_id}/messages").json()

    def delete_trailing_messages(self, message_id: str) -> Any:
        return self._http.request("DELETE", f"{self._base}/chat-client/messages/{message_id}/trailing").json()

    # --- Chat Client — Votes ---

    def get_votes(self, chat_id: str) -> Any:
        return self._http.request("GET", f"{self._base}/chat-client/chats/{chat_id}/votes").json()

    def update_vote(self, body: Dict[str, Any]) -> Any:
        return self._http.request("PATCH", f"{self._base}/chat-client/votes", json=body).json()

    # --- Chat Client — Documents ---

    def create_document(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/chat-client/documents", json=body).json()

    def get_document_latest_by_kind(self, **params) -> Any:
        return self._http.request("GET", f"{self._base}/chat-client/documents/latest-by-kind{_qs(params)}").json()

    def get_document(self, doc_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/chat-client/documents/{doc_id}").json()

    def get_document_latest(self, doc_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/chat-client/documents/{doc_id}/latest").json()

    def get_document_public(self, doc_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/chat-client/documents/{doc_id}/public").json()

    def delete_document(self, doc_id: str) -> Any:
        return self._http.request("DELETE", f"{self._base}/chat-client/documents/{doc_id}").json()

    def get_document_suggestions(self, document_id: str) -> Any:
        return self._http.request("GET", f"{self._base}/chat-client/documents/{document_id}/suggestions").json()

    # --- Admin Guides ---

    def list_admin_guides(self) -> Any:
        return self._http.request("GET", f"{self._base}/admin/guides").json()

    def get_admin_guide(self, filename: str) -> Any:
        return self._http.request("GET", f"{self._base}/admin/guides/{quote(filename)}")


class AsyncAiAgentResource:
    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    # --- System ---

    async def get_config(self) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/config")).json()

    async def get_health(self, detailed: bool = False) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/health{_qs({'detailed': detailed or None})}")).json()

    async def get_version(self) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/version")).json()

    # --- Chat v1 ---

    async def list_chats(self, organization_id: str, user_id: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/chat{_qs({'organization_id': organization_id, 'user_id': user_id, 'limit': limit})}")).json()

    async def get_chat(self, chat_id: str, include_messages: bool = False) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/chat/{chat_id}{_qs({'include_messages': True if include_messages else None})}")).json()

    async def delete_chat(self, chat_id: str, organization_id: str, user_id: Optional[str] = None) -> Any:
        return await (await self._http.request("DELETE", f"{self._base}/chat/{chat_id}{_qs({'organization_id': organization_id, 'user_id': user_id})}")).json()

    # --- Chat v2 (streaming — returns raw httpx.Response; iterate with .aiter_lines()) ---

    async def stream_chat(self, body: Dict[str, Any]) -> Any:
        return await self._http.request("POST", f"{self._base}/v2/chat", json=body)

    # --- Sub-agent chat v2 ---

    async def stream_sub_agent_chat(self, body: Dict[str, Any]) -> Any:
        return await self._http.request("POST", f"{self._base}/v2/sub-agent-chat", json=body)

    async def get_sub_agent_history(self, session_id: str, chat_id: str) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/v2/sub-agent-chat/history{_qs({'session_id': session_id, 'chat_id': chat_id})}")).json()

    # --- Prompt suggestions ---

    async def get_agent_prompt_suggestion(self, assistant_id: str) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/chat/get-agent-prompt-suggestion{_qs({'assistant_id': assistant_id})}")).json()

    # --- Embeddings / files ---

    async def process_embedding(self, file_id: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await (await self._http.request("POST", f"{self._base}/embedding/process", json={"fileId": file_id, "options": options or {}})).json()

    async def list_embedding_files(self, **params) -> Any:
        return await (await self._http.request("GET", f"{self._base}/embedding/files{_qs(params)}")).json()

    async def get_embedding_file(self, file_id: str) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/embedding/files/{file_id}")).json()

    async def preview_embedding_file(self, **params) -> Any:
        return await (await self._http.request("GET", f"{self._base}/embedding/files/preview{_qs(params)}")).json()

    async def update_embedding_file_status(self, file_id: str, status: str) -> Dict[str, Any]:
        return await (await self._http.request("PUT", f"{self._base}/embedding/files/{file_id}/status", json={"status": status})).json()

    async def delete_embedding_file(self, file_id: str) -> Any:
        return await (await self._http.request("DELETE", f"{self._base}/embedding/files/{file_id}")).json()

    async def classify_file(self, **params) -> Any:
        return await (await self._http.request("GET", f"{self._base}/embedding/classify{_qs(params)}")).json()

    # --- Data Board ---

    async def suggest_field_types(self, fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        return await (await self._http.request("POST", f"{self._base}/data-board/suggest-field-types", json={"fields": fields})).json()

    # --- Parquet ---

    async def generate_parquet(self, data: List[Any], file_name: Optional[str] = None, folder_name: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"data": data}
        if file_name:
            body["fileName"] = file_name
        if folder_name:
            body["folderName"] = folder_name
        return await (await self._http.request("POST", f"{self._base}/parquet/generate", json=body)).json()

    async def list_parquet_files(self) -> Any:
        return await (await self._http.request("GET", f"{self._base}/parquet/files")).json()

    async def delete_parquet_file(self, file_name: str) -> Any:
        return await (await self._http.request("DELETE", f"{self._base}/parquet/{quote(file_name)}")).json()

    # --- Trace (Tempo) ---

    async def get_traces(self, service: Optional[str] = None, limit: Optional[int] = None, time_range: Optional[int] = None, org_id: Optional[str] = None, details: Optional[bool] = None) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/trace/traces{_qs({'service': service, 'limit': limit, 'timeRange': time_range, 'orgId': org_id, 'details': details})}")).json()

    async def get_trace(self, trace_id: str) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/trace/traces/{trace_id}")).json()

    async def get_trace_services(self) -> Any:
        return await (await self._http.request("GET", f"{self._base}/trace/services")).json()

    async def get_trace_tags(self) -> Any:
        return await (await self._http.request("GET", f"{self._base}/trace/tags")).json()

    async def get_trace_tag_values(self, tag_name: str) -> Any:
        return await (await self._http.request("GET", f"{self._base}/trace/tags/{tag_name}/values")).json()

    async def search_traceql(self, q: str) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/trace/search/traceql{_qs({'q': q})}")).json()

    # --- Chat Client — Auth ---

    async def verify_chat_client_credentials(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return await (await self._http.request("POST", f"{self._base}/chat-client/auth/verify-credentials", json=body)).json()

    async def register_chat_client(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return await (await self._http.request("POST", f"{self._base}/chat-client/auth/register", json=body)).json()

    async def get_chat_client_user(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return await (await self._http.request("POST", f"{self._base}/chat-client/auth/user", json=body)).json()

    # --- Chat Client — Chats ---

    async def create_client_chat(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return await (await self._http.request("POST", f"{self._base}/chat-client/chats", json=body)).json()

    async def list_client_chats(self, organization_id: Optional[str] = None, limit: Optional[int] = None, starting_after: Optional[str] = None, ending_before: Optional[str] = None) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/chat-client/chats{_qs({'organization_id': organization_id, 'limit': limit, 'starting_after': starting_after, 'ending_before': ending_before})}")).json()

    async def delete_all_client_chats(self, organization_id: str) -> Any:
        return await (await self._http.request("DELETE", f"{self._base}/chat-client/chats{_qs({'organization_id': organization_id})}")).json()

    async def get_client_chat(self, chat_id: str) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/chat-client/chats/{chat_id}")).json()

    async def update_client_chat(self, chat_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return await (await self._http.request("PATCH", f"{self._base}/chat-client/chats/{chat_id}", json=body)).json()

    async def delete_client_chat(self, chat_id: str) -> Any:
        return await (await self._http.request("DELETE", f"{self._base}/chat-client/chats/{chat_id}")).json()

    async def stream_client_chat_status(self, chat_id: str) -> Any:
        return await self._http.request("GET", f"{self._base}/chat-client/chats/{chat_id}/status/stream")

    async def generate_client_chat_title(self, chat_id: str) -> Dict[str, Any]:
        return await (await self._http.request("POST", f"{self._base}/chat-client/chats/{chat_id}/title")).json()

    # --- Chat Client — Messages ---

    async def persist_client_message(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return await (await self._http.request("POST", f"{self._base}/chat-client/messages", json=body)).json()

    async def list_client_messages(self, chat_id: str) -> Any:
        return await (await self._http.request("GET", f"{self._base}/chat-client/chats/{chat_id}/messages")).json()

    async def delete_trailing_messages(self, message_id: str) -> Any:
        return await (await self._http.request("DELETE", f"{self._base}/chat-client/messages/{message_id}/trailing")).json()

    # --- Chat Client — Votes ---

    async def get_votes(self, chat_id: str) -> Any:
        return await (await self._http.request("GET", f"{self._base}/chat-client/chats/{chat_id}/votes")).json()

    async def update_vote(self, body: Dict[str, Any]) -> Any:
        return await (await self._http.request("PATCH", f"{self._base}/chat-client/votes", json=body)).json()

    # --- Chat Client — Documents ---

    async def create_document(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return await (await self._http.request("POST", f"{self._base}/chat-client/documents", json=body)).json()

    async def get_document_latest_by_kind(self, **params) -> Any:
        return await (await self._http.request("GET", f"{self._base}/chat-client/documents/latest-by-kind{_qs(params)}")).json()

    async def get_document(self, doc_id: str) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/chat-client/documents/{doc_id}")).json()

    async def get_document_latest(self, doc_id: str) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/chat-client/documents/{doc_id}/latest")).json()

    async def get_document_public(self, doc_id: str) -> Dict[str, Any]:
        return await (await self._http.request("GET", f"{self._base}/chat-client/documents/{doc_id}/public")).json()

    async def delete_document(self, doc_id: str) -> Any:
        return await (await self._http.request("DELETE", f"{self._base}/chat-client/documents/{doc_id}")).json()

    async def get_document_suggestions(self, document_id: str) -> Any:
        return await (await self._http.request("GET", f"{self._base}/chat-client/documents/{document_id}/suggestions")).json()

    # --- Admin Guides ---

    async def list_admin_guides(self) -> Any:
        return await (await self._http.request("GET", f"{self._base}/admin/guides")).json()

    async def get_admin_guide(self, filename: str) -> Any:
        return await self._http.request("GET", f"{self._base}/admin/guides/{quote(filename)}")
