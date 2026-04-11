"""Tests for TeamsResource."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"


@pytest.fixture
def client():
    c = ImbraceClient(app_api_key="test_key")
    yield c
    c.close()


def test_list_teams(httpx_mock: HTTPXMock, client):
    payload = {"object_name": "list", "data": [{"id": "t_1", "name": "general"}]}
    httpx_mock.add_response(url=f"{BASE}/v2/backend/teams?limit=20&skip=0", json=payload)
    result = client.app.teams.list()
    assert result["data"][0]["name"] == "general"


def test_list_my_teams(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{BASE}/v2/backend/teams/my", json={"data": []})
    client.app.teams.list_my()
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"


def test_add_users(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(
        url=f"{BASE}/v2/backend/teams/_add_users", json={"success": True}
    )
    result = client.app.teams.add_users("t_1", ["u_1", "u_2"])
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"
    body = json.loads(req.content)
    assert body["team_id"] == "t_1"
    assert body["user_ids"] == ["u_1", "u_2"]


def test_delete_team(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{BASE}/v2/backend/teams/t_1", json={"success": True})
    client.app.teams.delete("t_1")
    req = httpx_mock.get_requests()[0]
    assert req.method == "DELETE"
