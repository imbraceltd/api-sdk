from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport

class ActivePiecesResource:
    """ActivePieces Backend Proxy — Sync."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip('/')

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        full_path = f"{self._base}/{path.lstrip('/')}"
        return self._http.request("GET", full_path, params=params or {}).json()

    def post(self, path: str, body: Any) -> Any:
        full_path = f"{self._base}/{path.lstrip('/')}"
        return self._http.request("POST", full_path, json=body).json()

    def put(self, path: str, body: Any) -> Any:
        full_path = f"{self._base}/{path.lstrip('/')}"
        return self._http.request("PUT", full_path, json=body).json()

    def delete(self, path: str) -> Any:
        full_path = f"{self._base}/{path.lstrip('/')}"
        return self._http.request("DELETE", full_path).json()


class AsyncActivePiecesResource:
    """ActivePieces Backend Proxy — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip('/')

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:    
        full_path = f"{self._base}/{path.lstrip('/')}"
        res = await self._http.request("GET", full_path, params=params or {})
        return res.json()

    async def post(self, path: str, body: Any) -> Any:
        full_path = f"{self._base}/{path.lstrip('/')}"
        res = await self._http.request("POST", full_path, json=body)
        return res.json()

    async def put(self, path: str, body: Any) -> Any:
        full_path = f"{self._base}/{path.lstrip('/')}"
        res = await self._http.request("PUT", full_path, json=body)
        return res.json()

    async def delete(self, path: str) -> Any:
        full_path = f"{self._base}/{path.lstrip('/')}"
        res = await self._http.request("DELETE", full_path)
        return res.json()
