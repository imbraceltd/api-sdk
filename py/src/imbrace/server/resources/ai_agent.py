from typing import Any, Dict, Optional
from ...core.http import HttpTransport, AsyncHttpTransport


class AiAgentResource:
    """AI Agent — Server Gateway. RAG + file management.

    Endpoints:
        POST /3rd/ai-service/rag/answer_question
        GET  /3rd/ai-service/files/{file_id}
        POST /3rd/ai-service/rag/files
        DELETE /3rd/ai-service/rag/files/{file_id}
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/3rd/ai-service"

    def answer_question(self, text: str, assistant_id: str,
                        thread_id: Optional[str] = None,
                        instructions: str = "",
                        streaming: bool = False) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "text": text,
            "assistant_id": assistant_id,
            "instructions": instructions,
            "role": "user",
            "streaming": streaming,
        }
        if thread_id:
            body["thread_id"] = thread_id
        return self._http.request("POST", f"{self._base}/rag/answer_question", json=body).json()

    def get_file(self, file_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/files/{file_id}").json()

    def upload_file(self, file_content: bytes, filename: str,
                    content_type: str = "application/octet-stream",
                    text_input: Optional[str] = None) -> Dict[str, Any]:
        files: Dict[str, Any] = {"file": (filename, file_content, content_type)}
        data = {}
        if text_input:
            data["text_input"] = text_input
        return self._http.request("POST", f"{self._base}/rag/files", files=files, data=data).json()

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/rag/files/{file_id}").json()


class AsyncAiAgentResource:
    """AI Agent — Server Gateway. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/3rd/ai-service"

    async def answer_question(self, text: str, assistant_id: str,
                               thread_id: Optional[str] = None,
                               instructions: str = "",
                               streaming: bool = False) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "text": text,
            "assistant_id": assistant_id,
            "instructions": instructions,
            "role": "user",
            "streaming": streaming,
        }
        if thread_id:
            body["thread_id"] = thread_id
        res = await self._http.request("POST", f"{self._base}/rag/answer_question", json=body)
        return res.json()

    async def get_file(self, file_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/files/{file_id}")
        return res.json()

    async def delete_file(self, file_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/rag/files/{file_id}")
        return res.json()
