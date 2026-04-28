from typing import Any, Dict, List, Optional, Union
from ..http import HttpTransport, AsyncHttpTransport
from ..types.ips import (
    IpsProfile, Identity, Scheduler, SchedulerFilterOptions,
    IpsWorkflow, ExternalDataSync, EnableExternalDataSyncResponse
)
from ..types.common import PagedResponse

class IpsResource:
    """IPS — Profiles, Identities, Automation workflows, schedulers — Sync.

    @param base - ips base URL (ips-host/ips/v1)
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    # --- Profiles ---
    def get_profile(self, user_id: str) -> IpsProfile:
        return self._http.request("GET", f"{self._base}/profiles/{user_id}").json()

    def get_my_profile(self) -> IpsProfile:
        return self._http.request("GET", f"{self._base}/profiles/me").json()

    def update_profile(self, user_id: str, body: Dict[str, Any]) -> IpsProfile:
        return self._http.request("PATCH", f"{self._base}/profiles/{user_id}", json=body).json()

    def search_profiles(self, query: str, page: Optional[int] = None, limit: Optional[int] = None) -> PagedResponse[IpsProfile]:
        params = {"q": query}
        if page: params["page"] = page
        if limit: params["limit"] = limit
        return self._http.request("GET", f"{self._base}/profiles", params=params).json()

    def follow(self, target_user_id: str) -> None:
        self._http.request("POST", f"{self._base}/profiles/{target_user_id}/follow")

    def unfollow(self, target_user_id: str) -> None:
        self._http.request("DELETE", f"{self._base}/profiles/{target_user_id}/follow")

    def get_followers(self, user_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> PagedResponse[IpsProfile]:
        params = {}
        if page: params["page"] = page
        if limit: params["limit"] = limit
        return self._http.request("GET", f"{self._base}/profiles/{user_id}/followers", params=params).json()

    def get_following(self, user_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> PagedResponse[IpsProfile]:
        params = {}
        if page: params["page"] = page
        if limit: params["limit"] = limit
        return self._http.request("GET", f"{self._base}/profiles/{user_id}/following", params=params).json()

    # --- Identities ---
    def list_identities(self, user_id: str) -> List[Identity]:
        return self._http.request("GET", f"{self._base}/identities/{user_id}").json()

    def unlink_identity(self, user_id: str, provider: str) -> None:
        self._http.request("DELETE", f"{self._base}/identities/{user_id}/{provider}")

    # --- Schedulers ---
    def list_schedulers(self, filter: Optional[str] = None) -> List[Scheduler]:
        params = {}
        if filter: params["filter"] = filter
        return self._http.request("GET", f"{self._base}/schedulers", params=params).json()

    def delete_scheduler(self, scheduler_id: str) -> None:
        self._http.request("DELETE", f"{self._base}/schedulers/{scheduler_id}")

    def get_scheduler_filter_options(self, filter_type: str) -> SchedulerFilterOptions:
        return self._http.request("GET", f"{self._base}/schedulers/filter_options", params={"filter": filter_type}).json()

    # --- Workflows ---
    def list_workflows(self, params: Optional[Dict[str, Any]] = None) -> List[IpsWorkflow]:
        return self._http.request("GET", f"{self._base}/workflows/all", params=params or {}).json()

    def list_ap_workflows(self, params: Optional[Dict[str, Any]] = None) -> List[IpsWorkflow]:
        return self._http.request("GET", f"{self._base}/ap-workflows/all", params=params or {}).json()

    # --- External Data Sync ---
    def list_external_data_sync(self) -> List[ExternalDataSync]:
        return self._http.request("GET", f"{self._base}/external-data-sync").json()

    def delete_external_data_sync(self, sync_id: str) -> None:
        self._http.request("DELETE", f"{self._base}/external-data-sync/{sync_id}")

    def enable_external_data_sync(self, body: Dict[str, Any]) -> EnableExternalDataSyncResponse:
        return self._http.request("POST", f"{self._base}/external-data-sync/enable", json=body).json()


class AsyncIpsResource:
    """IPS — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    # --- Profiles (Async) ---
    async def get_profile(self, user_id: str) -> IpsProfile:
        res = await self._http.request("GET", f"{self._base}/profiles/{user_id}")
        return res.json()

    async def get_my_profile(self) -> IpsProfile:
        res = await self._http.request("GET", f"{self._base}/profiles/me")
        return res.json()

    async def update_profile(self, user_id: str, body: Dict[str, Any]) -> IpsProfile:
        res = await self._http.request("PATCH", f"{self._base}/profiles/{user_id}", json=body)
        return res.json()

    async def search_profiles(self, query: str, page: Optional[int] = None, limit: Optional[int] = None) -> PagedResponse[IpsProfile]:
        params = {"q": query}
        if page: params["page"] = page
        if limit: params["limit"] = limit
        res = await self._http.request("GET", f"{self._base}/profiles", params=params)
        return res.json()

    async def follow(self, target_user_id: str) -> None:
        await self._http.request("POST", f"{self._base}/profiles/{target_user_id}/follow")

    async def unfollow(self, target_user_id: str) -> None:
        await self._http.request("DELETE", f"{self._base}/profiles/{target_user_id}/follow")

    async def get_followers(self, user_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> PagedResponse[IpsProfile]:
        params = {}
        if page: params["page"] = page
        if limit: params["limit"] = limit
        res = await self._http.request("GET", f"{self._base}/profiles/{user_id}/followers", params=params)
        return res.json()

    async def get_following(self, user_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> PagedResponse[IpsProfile]:
        params = {}
        if page: params["page"] = page
        if limit: params["limit"] = limit
        res = await self._http.request("GET", f"{self._base}/profiles/{user_id}/following", params=params)
        return res.json()

    # --- Identities (Async) ---
    async def list_identities(self, user_id: str) -> List[Identity]:
        res = await self._http.request("GET", f"{self._base}/identities/{user_id}")
        return res.json()

    async def unlink_identity(self, user_id: str, provider: str) -> None:
        await self._http.request("DELETE", f"{self._base}/identities/{user_id}/{provider}")

    # --- Schedulers (Async) ---
    async def list_schedulers(self, filter: Optional[str] = None) -> List[Scheduler]:
        params = {}
        if filter: params["filter"] = filter
        res = await self._http.request("GET", f"{self._base}/schedulers", params=params)
        return res.json()

    async def delete_scheduler(self, scheduler_id: str) -> None:
        await self._http.request("DELETE", f"{self._base}/schedulers/{scheduler_id}")

    async def get_scheduler_filter_options(self, filter_type: str) -> SchedulerFilterOptions:
        res = await self._http.request("GET", f"{self._base}/schedulers/filter_options", params={"filter": filter_type})
        return res.json()

    # --- Workflows (Async) ---
    async def list_workflows(self, params: Optional[Dict[str, Any]] = None) -> List[IpsWorkflow]:
        res = await self._http.request("GET", f"{self._base}/workflows/all", params=params or {})
        return res.json()

    async def list_ap_workflows(self, params: Optional[Dict[str, Any]] = None) -> List[IpsWorkflow]:
        res = await self._http.request("GET", f"{self._base}/ap-workflows/all", params=params or {})
        return res.json()

    # --- External Data Sync (Async) ---
    async def list_external_data_sync(self) -> List[ExternalDataSync]:
        res = await self._http.request("GET", f"{self._base}/external-data-sync")
        return res.json()

    async def delete_external_data_sync(self, sync_id: str) -> None:
        await self._http.request("DELETE", f"{self._base}/external-data-sync/{sync_id}")

    async def enable_external_data_sync(self, body: Dict[str, Any]) -> EnableExternalDataSyncResponse:
        res = await self._http.request("POST", f"{self._base}/external-data-sync/enable", json=body)
        return res.json()
