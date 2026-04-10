"""Tests for ChannelResource."""
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
CHANNELS = f"{BASE}/v1/backend/channels"


@pytest.fixture
def client():
    c = ImbraceClient(api_key="test_key")
    yield c
    c.close()


def test_list_channels(httpx_mock: HTTPXMock, client):
    payload = {"object_name": "list", "data": [{"id": "ch_1", "name": "Web"}]}
    httpx_mock.add_response(url=CHANNELS, json=payload)
    result = client.channel.list()
    assert len(result["data"]) == 1


def test_list_channels_with_type(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(json={"data": []})
    client.channel.list(type="web")
    req = httpx_mock.get_requests()[0]
    assert "type=web" in str(req.url)


def test_get_channel(httpx_mock: HTTPXMock, client):
    payload = {"id": "ch_1", "name": "Web Channel"}
    httpx_mock.add_response(url=f"{CHANNELS}/ch_1", json=payload)
    result = client.channel.get("ch_1")
    assert result["name"] == "Web Channel"


def test_get_conv_count(httpx_mock: HTTPXMock, client):
    payload = {"web": 757, "facebook": 46, "all": 975}
    httpx_mock.add_response(url=f"{CHANNELS}/_conv_count?view=all", json=payload)
    result = client.channel.get_conv_count(view="all")
    assert result["all"] == 975


def test_delete_channel(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{CHANNELS}/ch_1", json={"success": True})
    result = client.channel.delete("ch_1")
    req = httpx_mock.get_requests()[0]
    assert req.method == "DELETE"
