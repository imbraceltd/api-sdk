from typing import Any, Dict, List, Optional, Union
from ..http import HttpTransport, AsyncHttpTransport
from ..types.team import TeamMembershipResponse, TeamUserItem, TeamWorkflowItem


class TeamsResource:
    """Teams domain — Sync.

    @param base         - platform service base URL (gateway/platform)
    @param backend_base - backend base URL (gateway/v1/backend) for file upload
    """

    def __init__(self, http: HttpTransport, base: str, backend_base: Optional[str] = None):
        self._http = http
        self._base = base.rstrip("/")
        self._backend_base = backend_base.rstrip("/") if backend_base else None

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2"

    def upload_icon(self, files: Any) -> Dict[str, Any]:
        """Upload team icon. Endpoint: /v1/backend/teams/_fileupload"""
        base = self._backend_base or f"{self._v1.replace('/platform/v1', '')}/v1/backend"
        return self._http.request("POST", f"{base}/teams/_fileupload", files=files).json()

    def list(self, limit: Optional[int] = None, skip: Optional[int] = None, q: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if skip is not None:
            params["skip"] = skip
        if q:
            params["q"] = q
        return self._http.request("GET", f"{self._v1}/teams", params=params).json()

    def list_my(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._v2}/teams/my").json()

    def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v1}/teams", json=body).json()

    def update(self, team_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._v2}/teams/{team_id}", json=body).json()

    def delete(self, team_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._v2}/teams/{team_id}").json()

    def add_users(self, team_id: str, user_ids: List[str]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v2}/teams/_add_users",
                                  json={"team_id": team_id, "user_ids": user_ids}).json()

    def remove_users(self, user_ids: List[str]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._v2}/teams/_remove_users",
                                  json={"user_ids": user_ids}).json()

    def get_users(self, team_id: str) -> List[TeamUserItem]:
        """Get users in a team."""
        return self._http.request("GET", f"{self._v1}/team_users",
                                   params={"team_id": team_id}).json()

    def get_users_v1(self, team_id: str) -> List[TeamUserItem]:
        """Get team users via v1 backend path."""
        base = self._backend_base or f"{self._v1.replace('/platform/v1', '')}/v1/backend"
        return self._http.request("GET", f"{base}/team/{team_id}/users").json()

    def join(self, team_id: str) -> TeamMembershipResponse:
        """Join a team directly (for administrators)."""
        return self._http.request("POST", f"{self._v2}/teams/_join_team", json={"team_id": team_id}).json()

    def leave(self, team_id: str) -> TeamMembershipResponse:
        """Leave a team."""
        return self._http.request("POST", f"{self._v2}/teams/_leave", json={"team_id": team_id}).json()

    def approve_join_request(self, team_id: str, team_user_id: str) -> TeamMembershipResponse:
        """Approve a user's request to join the team."""
        return self._http.request("POST", f"{self._v2}/teams/{team_id}/user/{team_user_id}/approve").json()

    def get_workflows(self, team_id: str) -> List[TeamWorkflowItem]:
        """Get workflows associated with a team."""
        return self._http.request("GET", f"{self._v1}/teams/{team_id}/workflows").json()

    def request_join(self, team_id: str) -> TeamMembershipResponse:
        """Request to join a team."""
        return self._http.request("POST", f"{self._v2}/teams/{team_id}/join_request").json()

    def update_user_role(self, team_id: str, user_id: str, role: str) -> TeamMembershipResponse:
        """Update a user's role in a team."""
        return self._http.request("PUT", f"{self._v2}/teams/{team_id}/user/{user_id}/role", json={"role": role}).json()

    def get_invite_list(self, team_id: str) -> Dict[str, Any]:
        """Get list of users eligible for invitation."""
        return self._http.request("GET", f"{self._v2}/team_users/_invite_list", params={"type": "team_id", "team_id": team_id}).json()


class AsyncTeamsResource:
    """Teams domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str, backend_base: Optional[str] = None):
        self._http = http
        self._base = base.rstrip("/")
        self._backend_base = backend_base.rstrip("/") if backend_base else None

    @property
    def _v1(self) -> str:
        return f"{self._base}/v1"

    @property
    def _v2(self) -> str:
        return f"{self._base}/v2"

    async def upload_icon(self, files: Any) -> Dict[str, Any]:
        """Upload team icon. Endpoint: /v1/backend/teams/_fileupload"""
        base = self._backend_base or f"{self._v1.replace('/platform/v1', '')}/v1/backend"
        res = await self._http.request("POST", f"{base}/teams/_fileupload", files=files)
        return res.json()

    async def list(self, limit: Optional[int] = None, skip: Optional[int] = None, q: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if skip is not None:
            params["skip"] = skip
        if q:
            params["q"] = q
        res = await self._http.request("GET", f"{self._v1}/teams", params=params)
        return res.json()

    async def list_my(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._v2}/teams/my")
        return res.json()

    async def create(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v1}/teams", json=body)
        return res.json()

    async def update(self, team_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PUT", f"{self._v2}/teams/{team_id}", json=body)
        return res.json()

    async def delete(self, team_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._v2}/teams/{team_id}")
        return res.json()

    async def add_users(self, team_id: str, user_ids: List[str]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v2}/teams/_add_users",
                                       json={"team_id": team_id, "user_ids": user_ids})
        return res.json()

    async def remove_users(self, user_ids: List[str]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._v2}/teams/_remove_users",
                                       json={"user_ids": user_ids})
        return res.json()

    async def get_users(self, team_id: str) -> List[TeamUserItem]:
        """Get users in a team (async)."""
        res = await self._http.request("GET", f"{self._v1}/team_users",
                                       params={"team_id": team_id})
        return res.json()

    async def get_users_v1(self, team_id: str) -> List[TeamUserItem]:
        """Get team users via v1 backend path (async)."""
        base = self._backend_base or f"{self._v1.replace('/platform/v1', '')}/v1/backend"
        res = await self._http.request("GET", f"{base}/team/{team_id}/users")
        return res.json()

    async def join(self, team_id: str) -> TeamMembershipResponse:
        """Join a team directly (async)."""
        res = await self._http.request("POST", f"{self._v2}/teams/_join_team", json={"team_id": team_id})
        return res.json()

    async def leave(self, team_id: str) -> TeamMembershipResponse:
        """Leave a team (async)."""
        res = await self._http.request("POST", f"{self._v2}/teams/_leave", json={"team_id": team_id})
        return res.json()

    async def approve_join_request(self, team_id: str, team_user_id: str) -> TeamMembershipResponse:
        """Approve a user's request to join the team (async)."""
        res = await self._http.request("POST", f"{self._v2}/teams/{team_id}/user/{team_user_id}/approve")
        return res.json()

    async def get_workflows(self, team_id: str) -> List[TeamWorkflowItem]:
        """Get workflows associated with a team (async)."""
        res = await self._http.request("GET", f"{self._v1}/teams/{team_id}/workflows")
        return res.json()

    async def request_join(self, team_id: str) -> TeamMembershipResponse:
        """Request to join a team (async)."""
        res = await self._http.request("POST", f"{self._v2}/teams/{team_id}/join_request")
        return res.json()

    async def update_user_role(self, team_id: str, user_id: str, role: str) -> TeamMembershipResponse:
        """Update a user's role in a team (async)."""
        res = await self._http.request("PUT", f"{self._v2}/teams/{team_id}/user/{user_id}/role", json={"role": role})
        return res.json()

    async def get_invite_list(self, team_id: str) -> Dict[str, Any]:
        """Get list of users eligible for invitation (async)."""
        res = await self._http.request("GET", f"{self._v2}/team_users/_invite_list", params={"type": "team_id", "team_id": team_id})
        return res.json()
