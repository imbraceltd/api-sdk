from typing import Any, Dict, List, Optional
from ..http import HttpTransport, AsyncHttpTransport
from ..types.marketplace import Product, Order, CreateOrderInput


class MarketplaceResource:
    """Marketplace domain — Sync. Server-side only (API Key)."""

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/marketplace"

    def list_products(
        self,
        page: int = 1,
        limit: int = 20,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if category:
            params["category"] = category
        if search:
            params["search"] = search
        return self._http.request("GET", f"{self._base}/products", params=params).json()

    def get_product(self, product_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/products/{product_id}").json()

    def create_product(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/products", json=body).json()

    def update_product(self, product_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._base}/products/{product_id}", json=body).json()

    def delete_product(self, product_id: str) -> Dict[str, Any]:
        return self._http.request("DELETE", f"{self._base}/products/{product_id}").json()

    # Orders
    def list_orders(self, page: int = 1, limit: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        return self._http.request("GET", f"{self._base}/orders", params=params).json()

    def get_order(self, order_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._base}/orders/{order_id}").json()

    def create_order(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._base}/orders", json=body).json()

    def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._base}/orders/{order_id}/status", json={"status": status}).json()


class AsyncMarketplaceResource:
    """Marketplace domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/marketplace"

    async def list_products(
        self,
        page: int = 1,
        limit: int = 20,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if category:
            params["category"] = category
        if search:
            params["search"] = search
        res = await self._http.request("GET", f"{self._base}/products", params=params)
        return res.json()

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/products/{product_id}")
        return res.json()

    async def create_product(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/products", json=body)
        return res.json()

    async def update_product(self, product_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._base}/products/{product_id}", json=body)
        return res.json()

    async def delete_product(self, product_id: str) -> Dict[str, Any]:
        res = await self._http.request("DELETE", f"{self._base}/products/{product_id}")
        return res.json()

    async def list_orders(self, page: int = 1, limit: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        res = await self._http.request("GET", f"{self._base}/orders", params=params)
        return res.json()

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._base}/orders/{order_id}")
        return res.json()

    async def create_order(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._base}/orders", json=body)
        return res.json()

    async def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._base}/orders/{order_id}/status", json={"status": status})
        return res.json()
