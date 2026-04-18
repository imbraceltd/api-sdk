import pytest
from pytest_httpx import HTTPXMock
from imbrace import ImbraceClient

GW = "https://app-gateway.imbrace.co"
PL = f"{GW}/platform/v1"


@pytest.fixture
def client():
    return ImbraceClient(api_key="test_key")


def test_sign_in(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(
        url=f"{PL}/login/sign_in", method="POST",
        json={"accessToken": "tok_abc"},
    )
    res = client.auth.sign_in("user@x.com", "pass")
    assert res["accessToken"] == "tok_abc"


def test_signin_email_request(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(url=f"{PL}/login/_signin_email_request", method="POST", status_code=200)
    client.auth.signin_email_request("user@x.com")


def test_signin_with_email_otp(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(
        url=f"{PL}/login/_signin_with_email", method="POST",
        json={"accessToken": "tok_otp"},
    )
    res = client.auth.signin_with_email("user@x.com", "123456")
    assert res["accessToken"] == "tok_otp"


def test_exchange_access_token(httpx_mock: HTTPXMock, client):
    httpx_mock.add_response(
        url=f"{PL}/access/_exchange_access_token", method="POST",
        json={"accessToken": "tok_exchanged"},
    )
    res = client.auth.exchange_access_token("old_tok", "org_1")
    assert res["accessToken"] == "tok_exchanged"


def test_login_stores_token(httpx_mock: HTTPXMock):
    """client.login() extracts token and stores it in token_manager."""
    client = ImbraceClient(api_key="test_key")
    httpx_mock.add_response(
        url=f"{PL}/login/sign_in", method="POST",
        json={"accessToken": "tok_stored"},
    )
    client.login("user@x.com", "pass")
    assert client.token_manager.get_token() == "tok_stored"
