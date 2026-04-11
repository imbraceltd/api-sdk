from typing import Any, Dict, Optional
from ...core.http import HttpTransport, AsyncHttpTransport


class ScheduleResource:
    """Schedule domain — Server Gateway. /3rd/organization/{org_id}/users/{user_id}/schedulers"""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base

    def list(self, organization_id: str, user_id: str,
             event_type: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if event_type:
            params["event_type"] = event_type
        return self._http.request(
            "GET",
            f"{self._base}/3rd/organization/{organization_id}/users/{user_id}/schedulers",
            params=params,
        ).json()


class AsyncScheduleResource:
    """Schedule domain — Server Gateway. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base

    async def list(self, organization_id: str, user_id: str,
                   event_type: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if event_type:
            params["event_type"] = event_type
        res = await self._http.request(
            "GET",
            f"{self._base}/3rd/organization/{organization_id}/users/{user_id}/schedulers",
            params=params,
        )
        return res.json()
