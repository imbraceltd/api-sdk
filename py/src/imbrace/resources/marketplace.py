from typing import Any, Dict, List, Optional
from ..http import HttpTransport, AsyncHttpTransport
from ..types.marketplace import Product, Order, CreateOrderInput


class MarketplaceResource:
    """Marketplace domain — Sync.
    
    @param base - marketplaces base URL (`{gateway}/v2/backend`)
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._marketplaces = base.rstrip("/")
        # templates are usually at the same level as marketplaces in v2/backend
        self._templates = self._marketplaces.replace("/marketplaces", "/templates")

    # --- Marketplace templates ---
    def list_use_case_templates(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._templates}").json()

    def install_from_json(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._templates}/v1/market-places/templates/install-from-json", json=body).json()

    # --- Marketplace products ---
    def list_products(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._marketplaces}/products", params=params or {}).json()

    def get_product(self, product_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._marketplaces}/products/{product_id}").json()

    # --- Orders ---
    def create_order(self, body: Dict[str, Any]) -> Dict[str, Any]:
        product_id = body.get("product_id", "")
        return self._http.request("POST", f"{self._marketplaces}/installations/{product_id}", json=body).json()

    def list_orders(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._marketplaces}/orders", params=params or {}).json()

    def get_order(self, order_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._marketplaces}/orders/{order_id}").json()

    def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._marketplaces}/orders/{order_id}/status", json={"status": status}).json()

    # --- Files ---
    def upload_file(self, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._marketplaces}/files", files=files).json()

    def delete_file(self, file_id: str) -> None:
        self._http.request("DELETE", f"{self._marketplaces}/files/{file_id}")

    def get_file_details(self, file_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._marketplaces}/file-details/{file_id}").json()

    def download_file(self, short_path: str) -> Any:
        return self._http.request("GET", f"{self._marketplaces}/download/{short_path}")

    # --- Email Templates ---
    def list_email_templates(self, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._marketplaces}/email-templates/search", params=params or {}).json()

    def create_email_template(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._marketplaces}/email-templates", json=body).json()

    def post_channel_workflows(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._marketplaces}/channel-workflows", json=body).json()

    # --- Categories ---
    def list_categories(self, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._marketplaces}/categories", params=params or {}).json()


class AsyncMarketplaceResource:
    """Marketplace domain — Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._marketplaces = base.rstrip("/")
        self._templates = self._marketplaces.replace("/marketplaces", "/templates")

    async def list_use_case_templates(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._templates}")
        return res.json()

    async def install_from_json(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._templates}/v1/market-places/templates/install-from-json", json=body)
        return res.json()

    async def list_products(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._marketplaces}/products", params=params or {})
        return res.json()

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._marketplaces}/products/{product_id}")
        return res.json()

    async def create_order(self, body: Dict[str, Any]) -> Dict[str, Any]:
        product_id = body.get("product_id", "")
        res = await self._http.request("POST", f"{self._marketplaces}/installations/{product_id}", json=body)
        return res.json()

    async def list_orders(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._marketplaces}/orders", params=params or {})
        return res.json()

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._marketplaces}/orders/{order_id}")
        return res.json()

    async def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._marketplaces}/orders/{order_id}/status", json={"status": status})
        return res.json()

    async def list_categories(self, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._marketplaces}/categories", params=params or {})
        return res.json()
