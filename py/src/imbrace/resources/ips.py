from typing import Any, Dict, List, Optional
from ..http import HttpTransport, AsyncHttpTransport


class IpsResource:
    """IPS (Identity & Profile Service) domain — Sync."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/ips"

    # --- Profiles ---
    def get_profile(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/profiles/{user_id}").json()

    def get_my_profile(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/profiles/me").json()

    def update_profile(self, user_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._base}/profiles/{user_id}", json=body).json()

    def search_profiles(self, query: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        return self._http.request(
            "GET", f"{self._base}/profiles",
            params={"q": query, "page": page, "limit": limit}
        ).json()

    # --- Follow / Unfollow ---
    def follow(self, target_user_id: str) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/profiles/{target_user_id}/follow").json()

    def unfollow(self, target_user_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/profiles/{target_user_id}/follow").json()

    def get_followers(self, user_id: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        return self._http.request(
            "GET", f"{self._base}/profiles/{user_id}/followers",
            params={"page": page, "limit": limit}
        ).json()

    def get_following(self, user_id: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        return self._http.request(
            "GET", f"{self._base}/profiles/{user_id}/following",
            params={"page": page, "limit": limit}
        ).json()

    # --- Identities ---
    def list_identities(self, user_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/identities/{user_id}").json()

    def unlink_identity(self, user_id: str, provider: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/identities/{user_id}/{provider}").json()


class AsyncIpsResource:
    """IPS domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/ips"

    async def get_profile(self, user_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/profiles/{user_id}")
        return res.json()

    async def get_my_profile(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/profiles/me")
        return res.json()

    async def update_profile(self, user_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._base}/profiles/{user_id}", json=body)
        return res.json()

    async def search_profiles(self, query: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        res = await self._http.request(
            "GET", f"{self._base}/profiles",
            params={"q": query, "page": page, "limit": limit}
        )
        return res.json()

    async def follow(self, target_user_id: str) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/profiles/{target_user_id}/follow")
        return res.json()

    async def unfollow(self, target_user_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/profiles/{target_user_id}/follow")
        return res.json()

    async def get_followers(self, user_id: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        res = await self._http.request(
            "GET", f"{self._base}/profiles/{user_id}/followers",
            params={"page": page, "limit": limit}
        )
        return res.json()

    async def get_following(self, user_id: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        res = await self._http.request(
            "GET", f"{self._base}/profiles/{user_id}/following",
            params={"page": page, "limit": limit}
        )
        return res.json()

    async def list_identities(self, user_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/identities/{user_id}")
        return res.json()

    async def unlink_identity(self, user_id: str, provider: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/identities/{user_id}/{provider}")
        return res.json()
