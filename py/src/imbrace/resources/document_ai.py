from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


def _json_or_none(res) -> Any:
    if res.status_code == 204 or res.headers.get("content-length") == "0":
        return None
    return res.json()


class DocumentAIResource:
    """Document AI / Financial Documents — Sync.

    Routes `/v2/ai/financial_documents/*` on the gateway.

    @param base - AI service base URL (gateway root). Methods append `/v2/ai/financial_documents/...`.
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2/ai/financial_documents"

    # ── File / Report detail (paginated) ───────────────────────────────────────

    def get_file(self, id: str, page: Optional[int] = None,
                 limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return self._http.request("GET", f"{self._v2}/{id}", params=params).json()

    def get_report(self, id: str, page: Optional[int] = None,
                   limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        return self._http.request("GET", f"{self._v2}/reports/{id}", params=params).json()

    # ── Errors ─────────────────────────────────────────────────────────────────

    def list_errors(self, file_id: str, limit: int = -1) -> Dict[str, Any]:
        return self._http.request(
            "GET",
            f"{self._v2}/errors-files/{file_id}",
            params={"limit": limit},
        ).json()

    # ── Suggest / Fix / Reset ──────────────────────────────────────────────────

    def suggest(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v2}/suggest", json=body).json()

    def fix(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v2}/fix", json=body).json()

    def reset(self, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v2}/reset", json=body or {}).json()

    # ── Update ─────────────────────────────────────────────────────────────────

    def update_file(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v2}/{id}", json=body).json()

    def update_report(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v2}/reports/{id}", json=body).json()

    # ── Delete ─────────────────────────────────────────────────────────────────

    def delete_file(self, id: str) -> None:
        _json_or_none(self._http.request("DELETE", f"{self._v2}/{id}"))

    def delete_report(self, id: str) -> None:
        _json_or_none(self._http.request("DELETE", f"{self._v2}/reports/{id}"))


class AsyncDocumentAIResource:
    """Document AI / Financial Documents — Async.

    Routes `/v2/ai/financial_documents/*` on the gateway.
    """

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2/ai/financial_documents"

    # ── File / Report detail (paginated) ───────────────────────────────────────

    async def get_file(self, id: str, page: Optional[int] = None,
                       limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        res = await self._http.request("GET", f"{self._v2}/{id}", params=params)
        return res.json()

    async def get_report(self, id: str, page: Optional[int] = None,
                         limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        res = await self._http.request("GET", f"{self._v2}/reports/{id}", params=params)
        return res.json()

    # ── Errors ─────────────────────────────────────────────────────────────────

    async def list_errors(self, file_id: str, limit: int = -1) -> Dict[str, Any]:
        res = await self._http.request(
            "GET",
            f"{self._v2}/errors-files/{file_id}",
            params={"limit": limit},
        )
        return res.json()

    # ── Suggest / Fix / Reset ──────────────────────────────────────────────────

    async def suggest(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v2}/suggest", json=body)
        return res.json()

    async def fix(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v2}/fix", json=body)
        return res.json()

    async def reset(self, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v2}/reset", json=body or {})
        return res.json()

    # ── Update ─────────────────────────────────────────────────────────────────

    async def update_file(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v2}/{id}", json=body)
        return res.json()

    async def update_report(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v2}/reports/{id}", json=body)
        return res.json()

    # ── Delete ─────────────────────────────────────────────────────────────────

    async def delete_file(self, id: str) -> None:
        res = await self._http.request("DELETE", f"{self._v2}/{id}")
        _json_or_none(res)

    async def delete_report(self, id: str) -> None:
        res = await self._http.request("DELETE", f"{self._v2}/reports/{id}")
        _json_or_none(res)
