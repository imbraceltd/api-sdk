"""Tests for AuthResource."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
TOKEN_URL = f"{BASE}/private/backend/v1/thrid_party_token"


@pytest.fixture
def client():
    c = ImbraceClient(app_api_key="test_key")
    yield c
    c.close()


def test_get_third_party_token(httpx_mock: HTTPXMock, client):
    payload = {"apiKey": {"apiKey": "api_new_xxx"}, "expires_in": 864000}
    httpx_mock.add_response(url=TOKEN_URL, json=payload)
    result = client.app.auth.get_third_party_token()
    assert result["apiKey"]["apiKey"] == "api_new_xxx"
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"
    body = json.loads(req.content)
    assert body["expirationDays"] == 10


def test_get_third_party_token_custom_days(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=TOKEN_URL, json={"apiKey": {}})
    client.app.auth.get_third_party_token(expiration_days=30)
    req = httpx_mock.get_requests()[0]
    body = json.loads(req.content)
    assert body["expirationDays"] == 30


def test_get_third_party_token_sends_auth_header(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=TOKEN_URL, json={})
    client.app.auth.get_third_party_token()
    req = httpx_mock.get_requests()[0]
    assert req.headers.get("x-access-token") == "test_key"
