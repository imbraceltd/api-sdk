import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient

GW = "https://app-gateway.imbrace.co"
PL = f"{GW}/platform"


@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")


def test_list_organizations(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/v2/organizations?limit=10&skip=0", json={"data": []})
    res = client.organizations.list()
    assert isinstance(res["data"], list)


def test_create_organization(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/v1/organizations", method="POST", json={"id": "org_1"})
    res = client.organizations.create({"name": "Acme"})
    assert res["id"] == "org_1"


def test_list_all_organizations(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/v2/organizations/_all", json={"data": []})
    res = client.organizations.list_all()
    assert isinstance(res["data"], list)
