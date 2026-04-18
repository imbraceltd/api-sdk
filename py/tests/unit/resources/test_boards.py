import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient

GW = "https://app-gateway.imbrace.co"
DB = f"{GW}/data-board"


@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")


def test_list_boards(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{DB}/boards?limit=20&skip=0", json={"data": []})
    res = client.boards.list()
    assert isinstance(res["data"], list)


def test_get_board(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{DB}/boards/b_1", json={"id": "b_1"})
    res = client.boards.get("b_1")
    assert res["id"] == "b_1"


def test_create_board(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{DB}/boards", method="POST", json={"id": "b_2"})
    res = client.boards.create("My Board")
    assert res["id"] == "b_2"


def test_update_board(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{DB}/boards/b_1", method="PUT", json={"id": "b_1", "name": "Updated"})
    res = client.boards.update("b_1", {"name": "Updated"})
    assert res["name"] == "Updated"


def test_delete_board(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{DB}/boards/b_1", method="DELETE", status_code=204)
    client.boards.delete("b_1")
