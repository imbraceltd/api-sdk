from typing import Any, AsyncIterator, Dict, Iterator, List, Optional
import json
from ...core.http import HttpTransport, AsyncHttpTransport


class AiResource:
    """AI domain — Sync. Completions + embeddings (+ streaming)."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/ai"

    def complete(self, model: str, messages: List[Dict[str, str]],
                 temperature: Optional[float] = None, max_tokens: Optional[int] = None,
                 metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if metadata:
            body["metadata"] = metadata
        return self._http.request("POST", f"{self._base}/completions", json=body).json()

    def stream(self, model: str, messages: List[Dict[str, str]],
               temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> Iterator[Dict[str, Any]]:
        """Streaming completion — yields SSE chunks."""
        import httpx
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": True}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens

        headers: Dict[str, str] = {"Content-Type": "application/json", "Accept": "text/event-stream"}
        if self._http.api_key:
            headers[self._http.token_header] = self._http.api_key
        token = self._http.token_manager.get_token()
        if token:
            headers[self._http.token_header] = token

        with httpx.Client(timeout=None) as client:
            with client.stream("POST", f"{self._base}/completions", json=body, headers=headers) as res:
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
        return self._http.request("POST", f"{self._base}/embeddings",
                                  json={"model": model, "input": input}).json()


class AsyncAiResource:
    """AI domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/ai"

    async def complete(self, model: str, messages: List[Dict[str, str]],
                       temperature: Optional[float] = None, max_tokens: Optional[int] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if metadata:
            body["metadata"] = metadata
        res = await self._http.request("POST", f"{self._base}/completions", json=body)
        return res.json()

    async def stream(self, model: str, messages: List[Dict[str, str]],
                     temperature: Optional[float] = None,
                     max_tokens: Optional[int] = None) -> AsyncIterator[Dict[str, Any]]:
        import httpx
        body: Dict[str, Any] = {"model": model, "messages": messages, "stream": True}
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens

        headers: Dict[str, str] = {"Content-Type": "application/json", "Accept": "text/event-stream"}
        if self._http.api_key:
            headers[self._http.token_header] = self._http.api_key
        token = self._http.token_manager.get_token()
        if token:
            headers[self._http.token_header] = token

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", f"{self._base}/completions", json=body, headers=headers) as res:
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
        res = await self._http.request("POST", f"{self._base}/embeddings",
                                       json={"model": model, "input": input})
        return res.json()
