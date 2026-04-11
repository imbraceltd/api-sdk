from typing import Any, Dict
from ...core.http import HttpTransport, AsyncHttpTransport


class MarketplaceResource:
    """Marketplace — Server Gateway.

    Endpoints:
        GET /3rd/organization/{organization_id}/marketplaces/email-templates/{template_id}
    """

    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = f"{base}/3rd/organization"

    def get_email_template(self, organization_id: str, template_id: str) -> Dict[str, Any]:
        return self._http.request(
            "GET",
            f"{self._base}/{organization_id}/marketplaces/email-templates/{template_id}",
        ).json()


class AsyncMarketplaceResource:
    """Marketplace — Server Gateway. Async."""

    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = f"{base}/3rd/organization"

    async def get_email_template(self, organization_id: str, template_id: str) -> Dict[str, Any]:
        res = await self._http.request(
            "GET",
            f"{self._base}/{organization_id}/marketplaces/email-templates/{template_id}",
        )
        return res.json()
