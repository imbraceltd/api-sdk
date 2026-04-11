"""Tests for BoardsResource."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
BOARDS = f"{BASE}/v1/backend/board"


@pytest.fixture
def client():
    c = ImbraceClient(app_api_key="test_key")
    yield c
    c.close()


def test_list_boards(httpx_mock: HTTPXMock, client):
    payload = {"data": [{"id": "b_1", "name": "CRM"}]}
    httpx_mock.add_response(url=f"{BOARDS}?limit=20&skip=0", json=payload)
    result = client.app.boards.list()
    assert result["data"][0]["name"] == "CRM"


def test_create_board(httpx_mock: HTTPXMock, client):
    payload = {"id": "b_new", "name": "My Board"}
    httpx_mock.add_response(url=BOARDS, json=payload)
    result = client.app.boards.create("My Board", description="Test")
    assert result["name"] == "My Board"
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"
    body = json.loads(req.content)
    assert body["name"] == "My Board"
    assert body["description"] == "Test"


def test_list_board_items(httpx_mock: HTTPXMock, client):
    payload = {"data": [{"id": "bi_1"}]}
    httpx_mock.add_response(url=f"{BOARDS}/b_1/board_items?limit=20&skip=0", json=payload)
    result = client.app.boards.list_items("b_1")
    assert len(result["data"]) == 1


def test_create_board_item(httpx_mock: HTTPXMock, client):
    payload = {"id": "bi_new"}
    httpx_mock.add_response(url=f"{BOARDS}/b_1/board_items", json=payload)
    client.app.boards.create_item("b_1", {"fields": [{"key": "name", "value": "Test"}]})
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"


def test_delete_board(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{BOARDS}/b_1", json={"success": True})
    client.app.boards.delete("b_1")
    req = httpx_mock.get_requests()[0]
    assert req.method == "DELETE"
