"""Tests for AccountResource."""
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"


@pytest.fixture
def client():
    c = ImbraceClient(app_api_key="test_key")
    yield c
    c.close()


def test_get_account(httpx_mock: HTTPXMock, client):
    payload = {
        "object_name": "account",
        "id": "u_123",
        "email": "test@imbrace.co",
        "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",
    }
    httpx_mock.add_response(url=f"{BASE}/v1/backend/account", json=payload)
    result = client.app.account.get()
    assert result["id"] == "u_123"
    assert result["object_name"] == "account"


def test_get_account_sends_auth(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{BASE}/v1/backend/account", json={})
    client.app.account.get()
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"
    assert req.headers.get("x-access-token") == "test_key"
