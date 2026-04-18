import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient, AsyncImbraceClient

BASE = "https://app-gateway.imbrace.co"
URL = f"{BASE}/channel-service/v1/campaign"

@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")

@pytest.fixture
async def async_client():
    client = AsyncImbraceClient(api_key="test_key")
    yield client
    await client.close()

def test_list_campaigns(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=URL, json={"data": []})
    res = client.campaigns.list()
    assert res["data"] == []

def test_get_campaign(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{URL}/cp1", json={"id": "cp1"})
    res = client.campaigns.get("cp1")
    assert res["id"] == "cp1"

def test_create_campaign(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=URL, method="POST", json={"id": "cp2"})
    res = client.campaigns.create({"name": "New"})
    assert res["id"] == "cp2"

@pytest.mark.anyio
async def test_async_list_campaigns(httpx_mock: HTTPXMock, async_client):
    httpx_mock.add_response(url=URL, json={"data": []})
    res = await async_client.campaigns.list()
    assert res["data"] == []
