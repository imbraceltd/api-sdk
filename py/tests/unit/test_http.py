"""Tests for HttpTransport — uses pytest-httpx to mock."""
import pytest
import httpx
from pytest_httpx import HTTPXMock

from imbrace.auth.token_manager import TokenManager
from imbrace.http import HttpTransport
from imbrace.exceptions import AuthError, ApiError, NetworkError

BASE = "https://app-gatewayv2.imbrace.co"


@pytest.fixture
def transport():
    tm = TokenManager("tok_test")
    return HttpTransport(token_manager=tm, timeout=5, api_key="key_test")


def test_get_success(httpx_mock: HTTPXMock, transport: HttpTransport):
    httpx_mock.add_response(url=f"{BASE}/global/health", json={"status": "ok"})
    res = transport.request("GET", f"{BASE}/global/health")
    assert res.json() == {"status": "ok"}


def test_sets_api_key_header(httpx_mock: HTTPXMock):
    tm = TokenManager()
    t = HttpTransport(token_manager=tm, timeout=5, api_key="key_test")
    httpx_mock.add_response(url=f"{BASE}/global/health", json={})

    t.request("GET", f"{BASE}/global/health")

    request = httpx_mock.get_requests()[0]
    assert request.headers["x-access-token"] == "key_test"


def test_sets_bearer_token_header(httpx_mock: HTTPXMock, transport: HttpTransport):
    httpx_mock.add_response(url=f"{BASE}/global/health", json={})

    transport.request("GET", f"{BASE}/global/health")

    request = httpx_mock.get_requests()[0]
    assert request.headers["x-access-token"] == "tok_test"


def test_no_bearer_when_token_cleared(httpx_mock: HTTPXMock):
    tm = TokenManager()
    t = HttpTransport(token_manager=tm, timeout=5)
    httpx_mock.add_response(url=f"{BASE}/global/health", json={})

    t.request("GET", f"{BASE}/global/health")

    request = httpx_mock.get_requests()[0]
    assert "Authorization" not in request.headers


def test_401_raises_auth_error(httpx_mock: HTTPXMock, transport: HttpTransport):
    httpx_mock.add_response(status_code=401, text="Unauthorized")
    with pytest.raises(AuthError):
        transport.request("GET", f"{BASE}/session")


def test_403_raises_auth_error(httpx_mock: HTTPXMock, transport: HttpTransport):
    httpx_mock.add_response(status_code=403, text="Forbidden")
    with pytest.raises(AuthError):
        transport.request("GET", f"{BASE}/session")


def test_404_raises_api_error(httpx_mock: HTTPXMock, transport: HttpTransport):
    httpx_mock.add_response(status_code=404, text="Not Found")
    with pytest.raises(ApiError) as exc_info:
        transport.request("GET", f"{BASE}/session/missing")
    assert exc_info.value.status_code == 404


def test_500_retries_then_raises(httpx_mock: HTTPXMock, transport: HttpTransport):
    # max_retries = 2, so 3 total responses needed
    for _ in range(3):
        httpx_mock.add_response(status_code=500, text="Server Error")
    with pytest.raises(ApiError) as exc_info:
        transport.request("GET", f"{BASE}/session")
    assert exc_info.value.status_code == 500


def test_network_error_retries_then_raises(httpx_mock: HTTPXMock, transport: HttpTransport):
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))
    with pytest.raises(NetworkError):
        transport.request("GET", f"{BASE}/session")


def test_close(transport: HttpTransport):
    transport.close()  # should not raise
