"""Tests for ImbraceClient — v2 3-gateway architecture."""
import os
import pytest
from unittest.mock import patch

from imbrace import ImbraceClient, AsyncImbraceClient


def test_app_gateway_initialized():
    client = ImbraceClient(app_api_key="key")
    assert client.app is not None
    client.close()


def test_server_gateway_initialized():
    client = ImbraceClient(server_api_key="api_key")
    assert client.server is not None
    client.close()



def test_app_base_url_default():
    client = ImbraceClient(app_api_key="key")
    assert client.app.base_url == "https://app-gatewayv2.imbrace.co"
    client.close()


def test_app_base_url_custom_strips_trailing_slash():
    client = ImbraceClient(app_base_url="https://staging.imbrace.co/", app_api_key="key")
    assert client.app.base_url == "https://staging.imbrace.co"
    client.close()


def test_reads_server_api_key_from_env():
    with patch.dict(os.environ, {"IMBRACE_API_KEY": "env_key"}):
        client = ImbraceClient()
        assert client.server._http.api_key == "env_key"
        client.close()


def test_explicit_server_api_key_overrides_env():
    with patch.dict(os.environ, {"IMBRACE_API_KEY": "env_key"}):
        client = ImbraceClient(server_api_key="explicit_key")
        assert client.server._http.api_key == "explicit_key"
        client.close()


def test_all_app_resources_initialized():
    client = ImbraceClient(app_api_key="key")
    assert client.app.auth is not None
    assert client.app.account is not None
    assert client.app.agent is not None
    assert client.app.ai is not None
    assert client.app.boards is not None
    assert client.app.channel is not None
    assert client.app.contacts is not None
    assert client.app.conversations is not None
    assert client.app.health is not None
    assert client.app.messages is not None
    assert client.app.organizations is not None
    assert client.app.sessions is not None
    assert client.app.settings is not None
    assert client.app.teams is not None
    assert client.app.workflows is not None
    client.close()


def test_all_server_resources_initialized():
    client = ImbraceClient(server_api_key="key")
    assert client.server.boards is not None
    assert client.server.ai_agent is not None
    assert client.server.categories is not None
    assert client.server.schedule is not None
    assert client.server.marketplace is not None
    client.close()



def test_set_access_token():
    client = ImbraceClient(app_api_key="key")
    client.app.set_access_token("new_token")
    assert client.app.token_manager.get_token() == "new_token"
    client.close()


def test_clear_access_token():
    client = ImbraceClient(app_access_token="initial")
    client.app.clear_access_token()
    assert client.app.token_manager.get_token() is None
    client.close()


def test_context_manager():
    with ImbraceClient(app_api_key="key") as client:
        assert client.app.sessions is not None


def test_async_client_initialized():
    client = AsyncImbraceClient(app_api_key="key")
    assert client.app is not None
    assert client.server is not None


def test_async_client_all_app_resources():
    client = AsyncImbraceClient(app_api_key="key")
    assert client.app.sessions is not None
    assert client.app.messages is not None
    assert client.app.agent is not None
    assert client.app.ai is not None
