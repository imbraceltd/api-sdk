import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient

GW = "https://app-gatewayv2.imbrace.co"
FIN = f"{GW}/v2/ai/financial_documents"


@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")


# ── get_file / get_report ──────────────────────────────────────────────────────

def test_get_file(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/file_123", json={"message": "ok"})
    res = client.document_ai.get_file("file_123")
    assert res["message"] == "ok"


def test_get_file_with_pagination(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/file_123?page=2&limit=10", json={})
    client.document_ai.get_file("file_123", page=2, limit=10)


def test_get_report(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/reports/rep_456", json={"data": []})
    res = client.document_ai.get_report("rep_456")
    assert "data" in res


# ── list_errors ────────────────────────────────────────────────────────────────

def test_list_errors_default_limit(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/errors-files/file_123?limit=-1", json={"data": []})
    res = client.document_ai.list_errors("file_123")
    assert "data" in res


def test_list_errors_custom_limit(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/errors-files/file_123?limit=50", json={})
    client.document_ai.list_errors("file_123", limit=50)


# ── suggest / fix / reset ─────────────────────────────────────────────────────

def test_suggest(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/suggest", method="POST", json={"suggestions": []})
    res = client.document_ai.suggest({"file_id": "f1"})
    assert "suggestions" in res


def test_fix(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/fix", method="POST", json={"success": True})
    res = client.document_ai.fix({"file_id": "f1", "fixes": []})
    assert res["success"] is True


def test_reset_no_body(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/reset", method="POST", json={"success": True})
    res = client.document_ai.reset()
    assert res["success"] is True


def test_reset_with_body(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/reset", method="POST", json={"success": True})
    client.document_ai.reset({"file_id": "f1"})


# ── update ─────────────────────────────────────────────────────────────────────

def test_update_file(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/file_123", method="PUT", json={"updated": True})
    res = client.document_ai.update_file("file_123", {"name": "new"})
    assert res["updated"] is True


def test_update_report(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/reports/rep_456", method="PUT", json={"updated": True})
    res = client.document_ai.update_report("rep_456", {"status": "approved"})
    assert res["updated"] is True


# ── delete ─────────────────────────────────────────────────────────────────────

def test_delete_file(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/file_123", method="DELETE", json={})
    client.document_ai.delete_file("file_123")


def test_delete_report(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/reports/rep_456", method="DELETE", json={})
    client.document_ai.delete_report("rep_456")
