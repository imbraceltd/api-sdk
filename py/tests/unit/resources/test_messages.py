"""Tests for MessagesResource — endpoint /v1/backend/conversation_messages."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
MESSAGES_URL = f"{BASE}/v1/backend/conversation_messages"


@pytest.fixture
def client():
    c = ImbraceClient(app_api_key="test_key")
    yield c
    c.close()


def test_list_messages(httpx_mock: HTTPXMock, client):
    payload = {"object_name": "list", "data": [{"id": "msg_1", "type": "text"}]}
    httpx_mock.add_response(url=f"{MESSAGES_URL}?limit=10&skip=0", json=payload)
    result = client.app.messages.list()
    assert result["data"][0]["id"] == "msg_1"
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"


def test_list_messages_pagination(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(json={"data": []})
    client.app.messages.list(limit=20, skip=10)
    req = httpx_mock.get_requests()[0]
    assert "limit=20" in str(req.url)
    assert "skip=10" in str(req.url)


def test_send_text_message(httpx_mock: HTTPXMock, client):
    payload = {"object_name": "message", "id": "msg_new", "type": "text"}
    httpx_mock.add_response(url=MESSAGES_URL, json=payload)
    result = client.app.messages.send(type="text", text="Hello!")
    assert result["type"] == "text"
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"
    body = json.loads(req.content)
    assert body["type"] == "text"
    assert body["text"] == "Hello!"


def test_send_image_message(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=MESSAGES_URL, json={"id": "msg_2"})
    client.app.messages.send(type="image", url="http://img.url", caption="Photo")
    req = httpx_mock.get_requests()[0]
    body = json.loads(req.content)
    assert body["type"] == "image"
    assert body["url"] == "http://img.url"
    assert body["caption"] == "Photo"
