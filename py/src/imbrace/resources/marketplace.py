from typing import Any, Dict, List, Optional
from ..http import HttpTransport, AsyncHttpTransport
from ..types.marketplace import Product, Order, CreateOrderInput


class MarketplaceResource:
    """Marketplace domain — Sync.

    Two backends:
    - Standalone marketplaces service: gateway/marketplaces/v1
    - Platform v2 marketplaces: gateway/platform/v2/marketplaces

    @param marketplaces_base - standalone marketplaces base (gateway/marketplaces/v1)
    @param platform_base     - platform service base (gateway/platform)
    """

    def __init__(self, http: HttpTransport, marketplaces_base: str, platform_base: str):
        self._http = http
        self._standalone_v1 = f"{marketplaces_base.rstrip('/')}/v1"
        self._platform_v2 = f"{platform_base.rstrip('/')}/v2/marketplaces"

    # --- Standalone marketplaces service ---
    def list_use_case_templates(self) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._standalone_v1}/market-places/templates").json()

    def install_from_json(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._standalone_v1}/market-places/templates/install-from-json", json=body).json()

    # --- Platform v2 products ---
    def list_products(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._platform_v2}", params=params or {}).json()

    def get_product(self, product_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._platform_v2}/{product_id}").json()

    def create_product(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._platform_v2}", json=body).json()

    def update_product(self, product_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._platform_v2}/{product_id}", json=body).json()

    def delete_product(self, product_id: str) -> None:
        self._http.request("DELETE", f"{self._platform_v2}/{product_id}")

    # --- Orders ---
    def create_order(self, body: Dict[str, Any]) -> Dict[str, Any]:
        product_id = body.get("product_id", "")
        return self._http.request("POST", f"{self._platform_v2}/installations/{product_id}", json=body).json()

    def list_orders(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._platform_v2}/orders", params=params or {}).json()

    def get_order(self, order_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._platform_v2}/orders/{order_id}").json()

    def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        return self._http.request("PATCH", f"{self._platform_v2}/orders/{order_id}/status", json={"status": status}).json()

    # --- Files ---
    def upload_file(self, files: Any) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._platform_v2}/files", files=files).json()

    def delete_file(self, file_id: str) -> None:
        self._http.request("DELETE", f"{self._platform_v2}/files/{file_id}")

    def get_file_details(self, file_id: str) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._platform_v2}/file-details/{file_id}").json()

    def download_file(self, short_path: str) -> Any:
        return self._http.request("GET", f"{self._platform_v2}/download/{short_path}")

    # --- Email Templates ---
    def list_email_templates(self, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._platform_v2}/email-templates/search", params=params or {}).json()

    def create_email_template(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._platform_v2}/email-templates", json=body).json()

    def post_channel_workflows(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._http.request("POST", f"{self._platform_v2}/channel-workflows", json=body).json()

    # --- Categories ---
    def list_categories(self, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._http.request("GET", f"{self._platform_v2}/categories", params=params or {}).json()


class AsyncMarketplaceResource:
    """Marketplace domain — Async."""

    def __init__(self, http: AsyncHttpTransport, marketplaces_base: str, platform_base: str):
        self._http = http
        self._standalone_v1 = f"{marketplaces_base.rstrip('/')}/v1"
        self._platform_v2 = f"{platform_base.rstrip('/')}/v2/marketplaces"

    async def list_use_case_templates(self) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._standalone_v1}/market-places/templates")
        return res.json()

    async def list_products(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._platform_v2}", params=params or {})
        return res.json()

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._platform_v2}/{product_id}")
        return res.json()

    async def create_product(self, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("POST", f"{self._platform_v2}", json=body)
        return res.json()

    async def update_product(self, product_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._platform_v2}/{product_id}", json=body)
        return res.json()

    async def delete_product(self, product_id: str) -> None:
        await self._http.request("DELETE", f"{self._platform_v2}/{product_id}")

    async def create_order(self, body: Dict[str, Any]) -> Dict[str, Any]:
        product_id = body.get("product_id", "")
        res = await self._http.request("POST", f"{self._platform_v2}/installations/{product_id}", json=body)
        return res.json()

    async def list_orders(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._platform_v2}/orders", params=params or {})
        return res.json()

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._platform_v2}/orders/{order_id}")
        return res.json()

    async def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        res = await self._http.request("PATCH", f"{self._platform_v2}/orders/{order_id}/status", json={"status": status})
        return res.json()

    async def list_categories(self, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        res = await self._http.request("GET", f"{self._platform_v2}/categories", params=params or {})
        return res.json()
