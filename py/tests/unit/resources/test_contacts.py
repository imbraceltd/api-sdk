"""Tests for ContactsResource."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
CONTACTS = f"{BASE}/v1/backend/contacts"
NOTIFICATIONS = f"{BASE}/v1/backend/notifications"


@pytest.fixture
def client():
    c = ImbraceClient(app_api_key="test_key")
    yield c
    c.close()


def test_list_contacts(httpx_mock: HTTPXMock, client):
    payload = {"data": [{"_id": "c_1", "name": "Alice"}]}
    httpx_mock.add_response(url=f"{CONTACTS}?limit=20&skip=0", json=payload)
    result = client.app.contacts.list()
    assert result["data"][0]["name"] == "Alice"
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"


def test_list_contacts_pagination(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(json={"data": []})
    client.app.contacts.list(limit=10, skip=5)
    req = httpx_mock.get_requests()[0]
    assert "limit=10" in str(req.url)
    assert "skip=5" in str(req.url)


def test_search_contacts(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{CONTACTS}/_search?q=alice", json={"data": []})
    client.app.contacts.search("alice")
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"
    assert "q=alice" in str(req.url)


def test_update_contact(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{CONTACTS}/c_1", json={"_id": "c_1"})
    client.app.contacts.update("c_1", {"name": "Bob"})
    req = httpx_mock.get_requests()[0]
    assert req.method == "PUT"
    body = json.loads(req.content)
    assert body["name"] == "Bob"


def test_get_contact_conversations(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{CONTACTS}/c_1/conversations", json={"data": []})
    client.app.contacts.get_conversations("c_1")
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"


def test_list_notifications(httpx_mock: HTTPXMock, client):
    payload = {"data": [{"id": "n_1"}]}
    httpx_mock.add_response(url=f"{NOTIFICATIONS}?limit=20&skip=0", json=payload)
    result = client.app.contacts.list_notifications()
    assert result["data"][0]["id"] == "n_1"


def test_dismiss_notification(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{NOTIFICATIONS}/dismiss", json={"success": True})
    client.app.contacts.dismiss_notification("n_1")
    req = httpx_mock.get_requests()[0]
    assert req.method == "DELETE"
    body = json.loads(req.content)
    assert body["notification_id"] == "n_1"


def test_dismiss_all_notifications(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{NOTIFICATIONS}/dismiss/all", json={"success": True})
    client.app.contacts.dismiss_all_notifications()
    req = httpx_mock.get_requests()[0]
    assert req.method == "DELETE"
