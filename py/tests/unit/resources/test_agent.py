"""Tests for AgentResource — endpoint /v2/backend/templates."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
TEMPLATES = f"{BASE}/v2/backend/templates"


@pytest.fixture
def client():
    c = ImbraceClient(api_key="test_key")
    yield c
    c.close()


def test_list_agents(httpx_mock: HTTPXMock, client):
    payload = {"data": [{"_id": "uc_1", "title": "Agent A"}]}
    httpx_mock.add_response(url=TEMPLATES, json=payload)
    result = client.agent.list()
    assert result == payload


def test_get_agent(httpx_mock: HTTPXMock, client):
    payload = {"data": {"_id": "uc_1", "title": "Agent A"}}
    httpx_mock.add_response(url=f"{TEMPLATES}/uc_1", json=payload)
    result = client.agent.get("uc_1")
    assert result["data"]["title"] == "Agent A"


def test_create_agent(httpx_mock: HTTPXMock, client):
    payload = {"data": {"_id": "uc_new", "title": "Test Agent"}}
    httpx_mock.add_response(url=f"{TEMPLATES}/custom", json=payload)
    body = {
        "assistant": {"name": "Test Agent"},
        "usecase": {"title": "Test Agent"},
    }
    result = client.agent.create(body)
    assert result["data"]["title"] == "Test Agent"
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"
    assert json.loads(req.content)["assistant"]["name"] == "Test Agent"


def test_update_agent(httpx_mock: HTTPXMock, client):
    payload = {"data": {"_id": "uc_1", "title": "Updated"}}
    httpx_mock.add_response(url=f"{TEMPLATES}/uc_1/custom", json=payload)
    result = client.agent.update("uc_1", {"usecase": {"title": "Updated"}})
    assert result["data"]["title"] == "Updated"
    req = httpx_mock.get_requests()[0]
    assert req.method == "PATCH"


def test_delete_agent(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{TEMPLATES}/uc_1", json={"success": True})
    result = client.agent.delete("uc_1")
    assert result["success"] is True
    req = httpx_mock.get_requests()[0]
    assert req.method == "DELETE"


def test_auth_header_sent(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=TEMPLATES, json={})
    client.agent.list()
    req = httpx_mock.get_requests()[0]
    assert req.headers.get("x-access-token") == "test_key"
