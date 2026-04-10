"""Tests for OrganizationsResource."""
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
ORGS_URL = f"{BASE}/v2/backend/organizations"


@pytest.fixture
def client():
    c = ImbraceClient(api_key="test_key")
    yield c
    c.close()


def test_list_organizations(httpx_mock: HTTPXMock, client):
    payload = {"data": [{"id": "org_1", "name": "Acme Corp"}]}
    httpx_mock.add_response(url=f"{ORGS_URL}?limit=10&skip=0", json=payload)
    result = client.organizations.list()
    assert result["data"][0]["name"] == "Acme Corp"
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"


def test_list_organizations_pagination(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(json={"data": []})
    client.organizations.list(limit=5, skip=10)
    req = httpx_mock.get_requests()[0]
    assert "limit=5" in str(req.url)
    assert "skip=10" in str(req.url)


def test_list_organizations_sends_auth_header(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{ORGS_URL}?limit=10&skip=0", json={"data": []})
    client.organizations.list()
    req = httpx_mock.get_requests()[0]
    assert req.headers.get("x-access-token") == "test_key"
