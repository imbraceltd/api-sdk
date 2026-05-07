from typing import Any, Awaitable, Callable, Dict, Optional, TypeVar
from ..http import HttpTransport, AsyncHttpTransport


class FinancialDocumentsNotDeployedError(Exception):
    """Raised when a Financial Documents endpoint returns the FastAPI default
    "Not Found" 404 — meaning the route is not registered on the gateway.

    Distinct from "ID not found" (which has a custom error message).
    """

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        super().__init__(
            f"Financial Documents endpoint \"{endpoint}\" is not deployed on this "
            f"gateway. These methods (get_file/get_report/list_errors/suggest/fix/"
            f"reset/update_*/delete_*) belong to a backend module that may not be "
            f"exposed on every iMBRACE environment. Contact the iMBRACE backend team "
            f"or use a gateway URL that fronts the Financial Management module."
        )


def _is_not_deployed_error(exc: BaseException) -> bool:
    """Detect FastAPI default 'Not Found' 404 wrapped in ApiError."""
    msg = str(exc)
    return "[404]" in msg and '"detail":"Not Found"' in msg


T = TypeVar("T")


def _wrap(endpoint: str, fn: Callable[[], T]) -> T:
    """Sync: run fn, convert FastAPI default 404 → FinancialDocumentsNotDeployedError."""
    try:
        return fn()
    except Exception as e:
        if _is_not_deployed_error(e):
            raise FinancialDocumentsNotDeployedError(endpoint) from e
        raise


async def _awrap(endpoint: str, fn: Callable[[], Awaitable[T]]) -> T:
    """Async: run awaitable fn, convert FastAPI default 404 → FinancialDocumentsNotDeployedError."""
    try:
        return await fn()
    except Exception as e:
        if _is_not_deployed_error(e):
            raise FinancialDocumentsNotDeployedError(endpoint) from e
        raise


class FinancialDocumentsResource:
    """Financial Documents — Sync.

    Multi-step review/correction workflow for documents extracted via
    :meth:`ChatAiResource.process_document`.

    All methods route to ``/v2/ai/financial_documents/*``. **EXPERIMENTAL**:
    requires the Financial Management backend module to be deployed on your
    gateway. If not deployed, calls raise
    :class:`FinancialDocumentsNotDeployedError` with a clear message.

    For one-shot extraction, use :meth:`ChatAiResource.process_document`.
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2/ai/financial_documents"

    # ── File / Report — experimental ─────────────────────────────────────────

    def get_file(self, id: str, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None: params["page"] = page
        if limit is not None: params["limit"] = limit
        return _wrap(
            f"GET /v2/ai/financial_documents/{id}",
            lambda: self._http.request("GET", f"{self._v2}/{id}", params=params).json(),
        )

    def get_report(self, id: str, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None: params["page"] = page
        if limit is not None: params["limit"] = limit
        return _wrap(
            f"GET /v2/ai/financial_documents/reports/{id}",
            lambda: self._http.request("GET", f"{self._v2}/reports/{id}", params=params).json(),
        )

    # ── Errors — experimental ────────────────────────────────────────────────

    def list_errors(self, file_id: str, limit: int = -1) -> Dict[str, Any]:
        return _wrap(
            f"GET /v2/ai/financial_documents/errors-files/{file_id}",
            lambda: self._http.request("GET", f"{self._v2}/errors-files/{file_id}", params={"limit": limit}).json(),
        )

    # ── Suggest / Fix / Reset — experimental ─────────────────────────────────

    def suggest(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return _wrap(
            "POST /v2/ai/financial_documents/suggest",
            lambda: self._http.request("POST", f"{self._v2}/suggest", json=body).json(),
        )

    def fix(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return _wrap(
            "POST /v2/ai/financial_documents/fix",
            lambda: self._http.request("POST", f"{self._v2}/fix", json=body).json(),
        )

    def reset(self, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return _wrap(
            "POST /v2/ai/financial_documents/reset",
            lambda: self._http.request("POST", f"{self._v2}/reset", json=body or {}).json(),
        )

    # ── Update — experimental ────────────────────────────────────────────────

    def update_file(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return _wrap(
            f"PUT /v2/ai/financial_documents/{id}",
            lambda: self._http.request("PUT", f"{self._v2}/{id}", json=body).json(),
        )

    def update_report(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return _wrap(
            f"PUT /v2/ai/financial_documents/reports/{id}",
            lambda: self._http.request("PUT", f"{self._v2}/reports/{id}", json=body).json(),
        )

    # ── Delete — experimental ────────────────────────────────────────────────

    def delete_file(self, id: str) -> None:
        _wrap(
            f"DELETE /v2/ai/financial_documents/{id}",
            lambda: self._http.request("DELETE", f"{self._v2}/{id}"),
        )

    def delete_report(self, id: str) -> None:
        _wrap(
            f"DELETE /v2/ai/financial_documents/reports/{id}",
            lambda: self._http.request("DELETE", f"{self._v2}/reports/{id}"),
        )


class AsyncFinancialDocumentsResource:
    """Financial Documents — Async. See :class:`FinancialDocumentsResource` for full docs."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2/ai/financial_documents"

    async def get_file(self, id: str, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None: params["page"] = page
        if limit is not None: params["limit"] = limit

        async def _fn() -> Dict[str, Any]:
            r = await self._http.request("GET", f"{self._v2}/{id}", params=params)
            return r.json()
        return await _awrap(f"GET /v2/ai/financial_documents/{id}", _fn)

    async def get_report(self, id: str, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if page is not None: params["page"] = page
        if limit is not None: params["limit"] = limit

        async def _fn() -> Dict[str, Any]:
            r = await self._http.request("GET", f"{self._v2}/reports/{id}", params=params)
            return r.json()
        return await _awrap(f"GET /v2/ai/financial_documents/reports/{id}", _fn)

    async def list_errors(self, file_id: str, limit: int = -1) -> Dict[str, Any]:
        async def _fn() -> Dict[str, Any]:
            r = await self._http.request("GET", f"{self._v2}/errors-files/{file_id}", params={"limit": limit})
            return r.json()
        return await _awrap(f"GET /v2/ai/financial_documents/errors-files/{file_id}", _fn)

    async def suggest(self, body: Dict[str, Any]) -> Dict[str, Any]:
        async def _fn() -> Dict[str, Any]:
            r = await self._http.request("POST", f"{self._v2}/suggest", json=body)
            return r.json()
        return await _awrap("POST /v2/ai/financial_documents/suggest", _fn)

    async def fix(self, body: Dict[str, Any]) -> Dict[str, Any]:
        async def _fn() -> Dict[str, Any]:
            r = await self._http.request("POST", f"{self._v2}/fix", json=body)
            return r.json()
        return await _awrap("POST /v2/ai/financial_documents/fix", _fn)

    async def reset(self, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async def _fn() -> Dict[str, Any]:
            r = await self._http.request("POST", f"{self._v2}/reset", json=body or {})
            return r.json()
        return await _awrap("POST /v2/ai/financial_documents/reset", _fn)

    async def update_file(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        async def _fn() -> Dict[str, Any]:
            r = await self._http.request("PUT", f"{self._v2}/{id}", json=body)
            return r.json()
        return await _awrap(f"PUT /v2/ai/financial_documents/{id}", _fn)

    async def update_report(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        async def _fn() -> Dict[str, Any]:
            r = await self._http.request("PUT", f"{self._v2}/reports/{id}", json=body)
            return r.json()
        return await _awrap(f"PUT /v2/ai/financial_documents/reports/{id}", _fn)

    async def delete_file(self, id: str) -> None:
        async def _fn() -> None:
            await self._http.request("DELETE", f"{self._v2}/{id}")
        await _awrap(f"DELETE /v2/ai/financial_documents/{id}", _fn)

    async def delete_report(self, id: str) -> None:
        async def _fn() -> None:
            await self._http.request("DELETE", f"{self._v2}/reports/{id}")
        await _awrap(f"DELETE /v2/ai/financial_documents/reports/{id}", _fn)
