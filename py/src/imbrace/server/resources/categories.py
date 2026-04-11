from typing import Any, Dict, List, Optional
from ...core.http import HttpTransport, AsyncHttpTransport


class CategoriesResource:
    """Categories domain — Server Gateway. /3rd/categories"""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/3rd/categories"

    def list(self, organization_id: str) -> List[Dict[str, Any]]:
        return self._http.request("GET", self._base, params={"organization_id": organization_id}).json()

    def get(self, category_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/{category_id}").json()

    def create(self, organization_id: str, name: str,
               apply_to: Optional[List[str]] = None,
               description: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name}
        if apply_to is not None:
            body["apply_to"] = apply_to
        if description is not None:
            body["description"] = description
        return self._http.request("POST", self._base, json=body,
                                  headers={"organization_id": organization_id}).json()

    def update(self, organization_id: str, category_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PUT", f"{self._base}/{category_id}", json=body,
                                  headers={"organization_id": organization_id}).json()

    def delete(self, category_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/{category_id}").json()


class AsyncCategoriesResource:
    """Categories domain — Server Gateway. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/3rd/categories"

    async def list(self, organization_id: str) -> List[Dict[str, Any]]:
        res = await self._http.request("GET", self._base, params={"organization_id": organization_id})
        return res.json()

    async def get(self, category_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/{category_id}")
        return res.json()

    async def create(self, organization_id: str, name: str,
                     apply_to: Optional[List[str]] = None,
                     description: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"name": name}
        if apply_to is not None:
            body["apply_to"] = apply_to
        if description is not None:
            body["description"] = description
        res = await self._http.request("POST", self._base, json=body,
                                       headers={"organization_id": organization_id})
        return res.json()

    async def delete(self, category_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/{category_id}")
        return res.json()
