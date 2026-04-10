"""Tests for ImbraceClient and AsyncImbraceClient initialization."""
import os
import pytest
from unittest.mock import patch

from imbrace import ImbraceClient, AsyncImbraceClient


def test_default_base_url():
    client = ImbraceClient(api_key="key")
    assert client.base_url == "https://app-gatewayv2.imbrace.co"
    client.close()


def test_custom_base_url():
    client = ImbraceClient(base_url="https://staging.imbrace.co/", api_key="key")
    assert client.base_url == "https://staging.imbrace.co"  # trailing slash stripped
    client.close()


def test_reads_api_key_from_env():
    with patch.dict(os.environ, {"IMBRACE_API_KEY": "env_key"}):
        client = ImbraceClient()
        assert client.http.api_key == "env_key"
        client.close()


def test_explicit_api_key_overrides_env():
    with patch.dict(os.environ, {"IMBRACE_API_KEY": "env_key"}):
        client = ImbraceClient(api_key="explicit_key")
        assert client.http.api_key == "explicit_key"
        client.close()


def test_reads_base_url_from_env():
    with patch.dict(os.environ, {"IMBRACE_BASE_URL": "https://custom.imbrace.co"}):
        client = ImbraceClient()
        assert client.base_url == "https://custom.imbrace.co"
        client.close()


def test_all_resources_initialized():
    client = ImbraceClient(api_key="key")
    assert client.sessions is not None
    assert client.messages is not None
    assert client.health is not None
    assert client.marketplace is not None
    assert client.platform is not None
    assert client.channel is not None
    assert client.ips is not None
    assert client.agent is not None
    assert client.ai is not None
    client.close()


def test_set_access_token():
    client = ImbraceClient(api_key="key")
    client.set_access_token("new_token")
    assert client.token_manager.get_token() == "new_token"
    client.close()


def test_clear_access_token():
    client = ImbraceClient(api_key="key", access_token="initial")
    client.clear_access_token()
    assert client.token_manager.get_token() is None
    client.close()


def test_context_manager():
    with ImbraceClient(api_key="key") as client:
        assert client.sessions is not None


def test_async_client_default_base_url():
    client = AsyncImbraceClient(api_key="key")
    assert client.base_url == "https://app-gatewayv2.imbrace.co"


def test_async_client_all_resources():
    client = AsyncImbraceClient(api_key="key")
    assert client.sessions is not None
    assert client.messages is not None
    assert client.agent is not None
    assert client.ai is not None
