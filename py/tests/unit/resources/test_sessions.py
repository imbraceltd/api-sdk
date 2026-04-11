"""Tests for SessionsResource (sync)."""
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"

@pytest.fixture
def client():
    c = ImbraceClient(app_api_key="key_test")
    yield c
    c.close()


def test_list_sessions(httpx_mock: HTTPXMock, client: ImbraceClient):
    payload = [{"id": "s1"}, {"id": "s2"}]
    httpx_mock.add_response(url=f"{BASE}/session", json=payload)

    result = client.app.sessions.list()
    assert result == payload


def test_list_sessions_with_directory(httpx_mock: HTTPXMock, client: ImbraceClient):
    httpx_mock.add_response(json=[])

    client.app.sessions.list(directory="/workspace/proj")

    request = httpx_mock.get_requests()[0]
    assert "directory" in str(request.url)


def test_get_session(httpx_mock: HTTPXMock, client: ImbraceClient):
    payload = {"id": "s1", "title": "My session"}
    httpx_mock.add_response(url=f"{BASE}/session/s1", json=payload)

    result = client.app.sessions.get("s1")
    assert result["id"] == "s1"


def test_create_session(httpx_mock: HTTPXMock, client: ImbraceClient):
    payload = {"id": "s_new"}
    httpx_mock.add_response(url=f"{BASE}/session", json=payload)

    result = client.app.sessions.create()
    assert result["id"] == "s_new"

    request = httpx_mock.get_requests()[0]
    assert request.method == "POST"


def test_create_session_with_body(httpx_mock: HTTPXMock, client: ImbraceClient):
    httpx_mock.add_response(url=f"{BASE}/session", json={"id": "s2"})

    client.app.sessions.create(directory="/home/user", workspace="ws1")

    request = httpx_mock.get_requests()[0]
    import json
    body = json.loads(request.content)
    assert body["directory"] == "/home/user"
    assert body["workspace"] == "ws1"


def test_delete_session(httpx_mock: HTTPXMock, client: ImbraceClient):
    httpx_mock.add_response(url=f"{BASE}/session/s1", json={"deleted": True})

    result = client.app.sessions.delete("s1")
    assert result["deleted"] is True

    request = httpx_mock.get_requests()[0]
    assert request.method == "DELETE"
