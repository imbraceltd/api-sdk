from typing import Any, AsyncIterator, Dict, Iterator, List, Optional
import json
from ..http import HttpTransport, AsyncHttpTransport


class AiResource:
    """AI domain — Sync. Completions, embeddings (+ streaming).

    Resource class cho AI domain, cung cấp các phương thức:
    - complete(): Tạo completion đồng bộ
    - stream(): Tạo completion streaming
    - embed(): Tạo embeddings
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/ai"

    def complete(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Tạo completion đồng bộ.

        Args:
            model: Tên model
            messages: Danh sách messages
            temperature: Tham số
            max_tokens: Số lượng token tối đa
            metadata: Metadata bổ sung

        Returns:
            Kết quả completion
        """
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if metadata:
            body["metadata"] = metadata
        return self._http.request("POST", f"{self._base}/completions", json=body).json()

    def stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Streaming completion — yields chunks via SSE."""
        import httpx
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": True}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens

        # Tái dụng api_key / token từ http transport
        headers: Dict[str, str] = {"Content-Type": "application/json", "Accept": "text/event-stream"}
        if self._http.api_key:
            headers["X-Api-Key"] = self._http.api_key
        token = self._http.token_manager.get_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"

        with httpx.Client(timeout=None) as client:
            with client.stream(
                "POST", f"{self._base}/completions",
                json=body, headers=headers
            ) as res:
                for line in res.iter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            yield json.loads(data)
                        except json.JSONDecodeError:
                            continue

    def embed(self, model: str, input: List[str]) -> Dict[str, Any]:
        """Generate embeddings for a list of strings."""
        return self._http.request(
            "POST", f"{self._base}/embeddings",
            json={"model": model, "input": input}
        ).json()


class AsyncAiResource:
    """AI domain — Async. Completions, embeddings (+ streaming)."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/ai"

    async def complete(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Async completion — returns full response."""
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if metadata:
            body["metadata"] = metadata
        res = await self._http.request("POST", f"{self._base}/completions", json=body)
        return res.json()

    async def stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Any]]:
        """Async streaming completion — yields SSE chunks."""
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
            async with client.stream(
                "POST", f"{self._base}/completions",
                json=body, headers=headers
            ) as res:
                async for line in res.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            yield json.loads(data)
                        except json.JSONDecodeError:
                            continue

    async def embed(self, model: str, input: List[str]) -> Dict[str, Any]:
        """Generate embeddings."""
        res = await self._http.request(
            "POST", f"{self._base}/embeddings",
            json={"model": model, "input": input}
        )
        return res.json()
