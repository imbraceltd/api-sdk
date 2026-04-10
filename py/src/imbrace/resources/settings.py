from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


class SettingsResource:
    """Settings domain — Sync."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def list_message_templates(self, business_unit_id: Optional[str] = None,
                                limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        params: Dict[str, Any] = {"limit": limit, "skip": skip}
        if business_unit_id:
            params["business_unit_id"] = business_unit_id
        return self._http.request("GET", f"{self._base}/v2/backend/message_templates", params=params).json()

    def create_message_template(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/v1/backend/message_templates", json=body).json()

    def delete_message_template(self, template_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/v1/backend/message_templates/{template_id}").json()

    def list_users(self, skip: int = 0, limit: int = 20, search: Optional[str] = None,
                   status: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        if status:
            params["status"] = status
        return self._http.request("GET", f"{self._base}/v1/backend/users", params=params).json()

    def get_user_roles_count(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/v1/backend/users/_roles_count").json()

    def bulk_invite_users(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/v1/backend/users/_bulk_invite", json=body).json()


class AsyncSettingsResource:
    """Settings domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def list_message_templates(self, business_unit_id: Optional[str] = None,
                                      limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        params: Dict[str, Any] = {"limit": limit, "skip": skip}
        if business_unit_id:
            params["business_unit_id"] = business_unit_id
        res = await self._http.request("GET", f"{self._base}/v2/backend/message_templates", params=params)
        return res.json()

    async def list_users(self, skip: int = 0, limit: int = 20, search: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        res = await self._http.request("GET", f"{self._base}/v1/backend/users", params=params)
        return res.json()
