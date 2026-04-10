from typing import Any, Dict, Optional
from ..http import HttpTransport, AsyncHttpTransport


class PlatformResource:
    """Platform domain — Sync. Users, Organizations, Permissions."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/platform"

    # --- Users ---
    def list_users(self, page: int = 1, limit: int = 20, search: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if search:
            params["search"] = search
        return self._http.request("GET", f"{self._base}/users", params=params).json()

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/users/{user_id}").json()

    def get_me(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/users/me").json()

    def update_user(self, user_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._base}/users/{user_id}", json=body).json()

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/users/{user_id}").json()

    # --- Organizations ---
    def list_orgs(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/organizations", params={"page": page, "limit": limit}).json()

    def get_org(self, org_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/organizations/{org_id}").json()

    def create_org(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/organizations", json=body).json()

    def update_org(self, org_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._base}/organizations/{org_id}", json=body).json()

    def delete_org(self, org_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/organizations/{org_id}").json()

    # --- Permissions ---
    def list_permissions(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/users/{user_id}/permissions").json()

    def grant_permission(self, user_id: str, resource: str, action: str) -> Dict[str, Any]:
        return self._http.request(
            "POST", f"{self._base}/users/{user_id}/permissions",
            json={"resource": resource, "action": action}
        ).json()

    def revoke_permission(self, user_id: str, permission_id: str) -> Dict[str, Any]:
        return self._http.request(
            "DELETE", f"{self._base}/users/{user_id}/permissions/{permission_id}"
        ).json()


class AsyncPlatformResource:
    """Platform domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/platform"

    async def list_users(self, page: int = 1, limit: int = 20, search: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if search:
            params["search"] = search
        res = await self._http.request("GET", f"{self._base}/users", params=params)
        return res.json()

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/users/{user_id}")
        return res.json()

    async def get_me(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/users/me")
        return res.json()

    async def update_user(self, user_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._base}/users/{user_id}", json=body)
        return res.json()

    async def list_orgs(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/organizations", params={"page": page, "limit": limit})
        return res.json()

    async def get_org(self, org_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/organizations/{org_id}")
        return res.json()

    async def create_org(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/organizations", json=body)
        return res.json()

    async def update_org(self, org_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._base}/organizations/{org_id}", json=body)
        return res.json()

    async def list_permissions(self, user_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/users/{user_id}/permissions")
        return res.json()

    async def delete_user(self, user_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/users/{user_id}")
        return res.json()

    async def delete_org(self, org_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/organizations/{org_id}")
        return res.json()

    async def grant_permission(self, user_id: str, resource: str, action: str) -> Dict[str, Any]:
        res = await self._http.request(
            "POST", f"{self._base}/users/{user_id}/permissions",
            json={"resource": resource, "action": action}
        )
        return res.json()

    async def revoke_permission(self, user_id: str, permission_id: str) -> Dict[str, Any]:
        res = await self._http.request(
            "DELETE", f"{self._base}/users/{user_id}/permissions/{permission_id}"
        )
        return res.json()
