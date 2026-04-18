import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient

BASE = "https://app-gateway.imbrace.co"
MP = f"{BASE}/marketplaces"
PL = f"{BASE}/platform"

@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")

def test_list_use_case_templates(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{MP}/v1/market-places/templates", json={"data": []})
    res = client.marketplace.list_use_case_templates()
    assert res == {"data": []}

def test_list_products(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/v2/marketplaces", json={"data": []})
    res = client.marketplace.list_products()
    assert res == {"data": []}

def test_get_product(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/v2/marketplaces/p_1", json={"id": "p_1"})
    res = client.marketplace.get_product("p_1")
    assert res["id"] == "p_1"

def test_create_order(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/v2/marketplaces/installations/p_1", method="POST", json={"id": "o_1"})
    res = client.marketplace.create_order({"product_id": "p_1"})
    assert res["id"] == "o_1"

def test_list_orders(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/v2/marketplaces/orders", json={"data": []})
    res = client.marketplace.list_orders()
    assert res == {"data": []}

def test_update_order_status(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/v2/marketplaces/orders/o_1/status", method="PATCH", json={"success": True})
    res = client.marketplace.update_order_status("o_1", "paid")
    assert res["success"] is True

def test_list_categories(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/v2/marketplaces/categories", json={"data": []})
    res = client.marketplace.list_categories()
    assert res == {"data": []}
