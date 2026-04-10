"""Tests for WorkflowsResource."""
import json
import pytest
from pytest_httpx import HTTPXMock

from imbrace import ImbraceClient

BASE = "https://app-gatewayv2.imbrace.co"
WORKFLOWS_URL = f"{BASE}/v1/backend/workflows"
WORKFLOW_URL = f"{BASE}/v1/backend/workflow"


@pytest.fixture
def client():
    c = ImbraceClient(api_key="test_key")
    yield c
    c.close()


def test_list_workflows(httpx_mock: HTTPXMock, client):
    payload = {"data": [{"_id": "wf_1", "name": "Welcome Flow"}]}
    httpx_mock.add_response(url=WORKFLOWS_URL, json=payload)
    result = client.workflows.list()
    assert result["data"][0]["name"] == "Welcome Flow"
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"


def test_list_workflows_with_tag(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(json={"data": []})
    client.workflows.list(tag="onboarding")
    req = httpx_mock.get_requests()[0]
    assert "tag=onboarding" in str(req.url)


def test_list_channel_automation(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{WORKFLOWS_URL}/channel_automation", json={"data": []})
    client.workflows.list_channel_automation()
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"


def test_create_workflow(httpx_mock: HTTPXMock, client):
    payload = {"_id": "wf_new", "name": "New Flow"}
    httpx_mock.add_response(url=WORKFLOW_URL, json=payload)
    result = client.workflows.create({"name": "New Flow"})
    assert result["_id"] == "wf_new"
    req = httpx_mock.get_requests()[0]
    assert req.method == "POST"
    body = json.loads(req.content)
    assert body["name"] == "New Flow"


def test_update_workflow(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{WORKFLOW_URL}/wf_1", json={"_id": "wf_1"})
    client.workflows.update("wf_1", {"active": True})
    req = httpx_mock.get_requests()[0]
    assert req.method == "PATCH"
    body = json.loads(req.content)
    assert body["active"] is True


def test_list_n8n_workflows(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{BASE}/v1/backend/n8n/workflows", json={"data": []})
    client.workflows.list_n8n()
    req = httpx_mock.get_requests()[0]
    assert req.method == "GET"
