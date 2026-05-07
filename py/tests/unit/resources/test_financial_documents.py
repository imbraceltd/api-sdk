import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient
from imbrace.resources.financial_documents import FinancialDocumentsNotDeployedError

GW = "https://app-gatewayv2.imbrace.co"
FIN = f"{GW}/v2/ai/financial_documents"


@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")


# ── get_file / get_report ─────────────────────────────────────────────────────

def test_get_file(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/file_123", json={"message": "ok"})
    res = client.financial_documents.get_file("file_123")
    assert res["message"] == "ok"


def test_get_file_with_pagination(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/file_123?page=2&limit=10", json={})
    client.financial_documents.get_file("file_123", page=2, limit=10)


def test_get_report(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/reports/rep_456", json={"data": []})
    res = client.financial_documents.get_report("rep_456")
    assert "data" in res


# ── list_errors ───────────────────────────────────────────────────────────────

def test_list_errors_default_limit(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/errors-files/file_123?limit=-1", json={"data": []})
    res = client.financial_documents.list_errors("file_123")
    assert "data" in res


def test_list_errors_custom_limit(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/errors-files/file_123?limit=50", json={})
    client.financial_documents.list_errors("file_123", limit=50)


# ── suggest / fix / reset ─────────────────────────────────────────────────────

def test_suggest(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/suggest", method="POST", json={"suggestions": []})
    res = client.financial_documents.suggest({"file_id": "f1"})
    assert "suggestions" in res


def test_fix(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/fix", method="POST", json={"success": True})
    res = client.financial_documents.fix({"file_id": "f1"})
    assert res["success"] is True


def test_reset_no_body(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/reset", method="POST", json={"success": True})
    res = client.financial_documents.reset()
    assert res["success"] is True


# ── update ────────────────────────────────────────────────────────────────────

def test_update_file(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/file_123", method="PUT", json={"updated": True})
    res = client.financial_documents.update_file("file_123", {"name": "new"})
    assert res["updated"] is True


def test_update_report(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/reports/rep_456", method="PUT", json={"updated": True})
    res = client.financial_documents.update_report("rep_456", {"status": "ok"})
    assert res["updated"] is True


# ── delete ────────────────────────────────────────────────────────────────────

def test_delete_file(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/file_123", method="DELETE", json={})
    client.financial_documents.delete_file("file_123")


def test_delete_report(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{FIN}/reports/rep_456", method="DELETE", json={})
    client.financial_documents.delete_report("rep_456")


# ── NotDeployedError ──────────────────────────────────────────────────────────

def test_raises_not_deployed_on_fastapi_default_404(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(
        url=f"{FIN}/file_x",
        method="GET",
        status_code=404,
        json={"detail": "Not Found"},
    )
    with pytest.raises(FinancialDocumentsNotDeployedError):
        client.financial_documents.get_file("file_x")


def test_does_not_raise_not_deployed_on_custom_404(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(
        url=f"{FIN}/file_x",
        method="GET",
        status_code=404,
        json={"detail": "[ERROR: File not found]"},
    )
    with pytest.raises(Exception) as exc_info:
        client.financial_documents.get_file("file_x")
    assert not isinstance(exc_info.value, FinancialDocumentsNotDeployedError)


def test_delete_file_raises_not_deployed(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(
        url=f"{FIN}/file_x",
        method="DELETE",
        status_code=404,
        json={"detail": "Not Found"},
    )
    with pytest.raises(FinancialDocumentsNotDeployedError):
        client.financial_documents.delete_file("file_x")
