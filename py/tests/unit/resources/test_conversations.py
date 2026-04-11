"""Tests for ConversationsResource."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
ORG_ID = "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd"


@pytest.fixture
def client():
    c = ImbraceClient(app_api_key="test_key")
    yield c
    c.close()


def test_get_views_count(httpx_mock: HTTPXMock, client):
    payload = {"all": 975, "yours": 293, "closed": 61}
    httpx_mock.add_response(
        url=f"{BASE}/v2/backend/team_conversations/_views_count", json=payload
    )
    result = client.app.conversations.get_views_count()
    assert result["all"] == 975


def test_create_conversation(httpx_mock: HTTPXMock, client):
    payload = {"object_name": "conversation", "id": "conv_123", "status": "active"}
    httpx_mock.add_response(url=f"{BASE}/v1/backend/conversation", json=payload)
    result = client.app.conversations.create()
    assert result["id"] == "conv_123"
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"


def test_search(httpx_mock: HTTPXMock, client):
    payload = {"success": True, "message": {"hits": [], "total": 0}}
    httpx_mock.add_response(
        url=f"{BASE}/v1/backend/meilisearch/{ORG_ID}/search", json=payload
    )
    result = client.app.conversations.search(ORG_ID, q="hello")
    assert result["success"] is True
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"
    body = json.loads(req.content)
    assert body["q"] == "hello"
