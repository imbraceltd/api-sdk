import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient

GW = "https://app-gateway.imbrace.co"
CS = f"{GW}/channel-service/v1"
PL = f"{GW}/platform/v1"


@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")


def test_list_workflows(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{CS}/automations", json={"data": []})
    res = client.workflows.list()
    assert isinstance(res["data"], list)


def test_create_workflow(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{CS}/automations", method="POST", json={"id": "wf_1"})
    res = client.workflows.create({"name": "My Flow"})
    assert res["id"] == "wf_1"


def test_update_workflow(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{CS}/automations/wf_1", method="PATCH", json={"id": "wf_1"})
    res = client.workflows.update("wf_1", {"active": True})
    assert res["id"] == "wf_1"


def test_list_n8n_workflows(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/workflows", json={"data": []})
    res = client.workflows.list_n8n()
    assert isinstance(res["data"], list)
