"""Tests for exception hierarchy."""
import pytest
from imbrace.core.exceptions import ImbraceError, AuthError, ApiError, NetworkError


def test_hierarchy():
    assert issubclass(AuthError, ImbraceError)
    assert issubclass(ApiError, ImbraceError)
    assert issubclass(NetworkError, ImbraceError)


def test_api_error_message():
    err = ApiError(404, "Not Found")
    assert err.status_code == 404
    assert "[404]" in str(err)
    assert "Not Found" in str(err)


def test_auth_error_is_catchable_as_imbrace_error():
    with pytest.raises(ImbraceError):
        raise AuthError("Unauthorized")


def test_network_error():
    err = NetworkError("timeout")
    assert "timeout" in str(err)
