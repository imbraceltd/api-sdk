"""Tests for SettingsResource."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
MSG_TPL_V2 = f"{BASE}/v2/backend/message_templates"
MSG_TPL_V1 = f"{BASE}/v1/backend/message_templates"
USERS_URL = f"{BASE}/v1/backend/users"


@pytest.fixture
def client():
    c = ImbraceClient(app_api_key="test_key")
    yield c
    c.close()


def test_list_message_templates(httpx_mock: HTTPXMock, client):
    payload = {"data": [{"_id": "tpl_1", "name": "Welcome"}]}
    httpx_mock.add_response(url=f"{MSG_TPL_V2}?limit=20&skip=0", json=payload)
    result = client.app.settings.list_message_templates()
    assert result["data"][0]["name"] == "Welcome"
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"


def test_list_message_templates_with_business_unit(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(json={"data": []})
    client.app.settings.list_message_templates(business_unit_id="bu_1")
    req = httpx_mock.get_requests()[0]
    assert "business_unit_id=bu_1" in str(req.url)


def test_create_message_template(httpx_mock: HTTPXMock, client):
    payload = {"_id": "tpl_new"}
    httpx_mock.add_response(url=MSG_TPL_V1, json=payload)
    result = client.app.settings.create_message_template({"name": "My Tpl", "body": "Hello {{name}}"})
    assert result["_id"] == "tpl_new"
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"


def test_delete_message_template(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{MSG_TPL_V1}/tpl_1", json={"success": True})
    client.app.settings.delete_message_template("tpl_1")
    req = httpx_mock.get_requests()[0]
    assert req.method == "DELETE"


def test_list_users(httpx_mock: HTTPXMock, client):
    payload = {"data": [{"id": "u_1", "email": "user@example.com"}]}
    httpx_mock.add_response(url=f"{USERS_URL}?skip=0&limit=20", json=payload)
    result = client.app.settings.list_users()
    assert result["data"][0]["id"] == "u_1"
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"


def test_list_users_with_search(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(json={"data": []})
    client.app.settings.list_users(search="alice")
    req = httpx_mock.get_requests()[0]
    assert "search=alice" in str(req.url)


def test_get_user_roles_count(httpx_mock: HTTPXMock, client):
    payload = {"admin": 2, "agent": 10}
    httpx_mock.add_response(url=f"{USERS_URL}/_roles_count", json=payload)
    result = client.app.settings.get_user_roles_count()
    assert result["admin"] == 2


def test_bulk_invite_users(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{USERS_URL}/_bulk_invite", json={"success": True})
    client.app.settings.bulk_invite_users({"emails": ["a@b.com"], "role": "agent"})
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"
    body = json.loads(req.content)
    assert body["role"] == "agent"
