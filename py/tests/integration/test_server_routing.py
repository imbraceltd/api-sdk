"""Integration test — Nhiệm vụ 3: phải gọi đúng server.

Kiểm tra:
- Service base URLs trỏ đúng gateway + path (env develop)
- Thực sự gọi được từng service endpoint và nhận 200/2xx (không phải 404/502)
- API Key được gắn đúng header x-api-key (không phải x-access-token)
"""
import pytest
from imbrace import ImbraceClient

pytestmark = pytest.mark.integration

DEV_GW = "https://app-gateway.dev.imbrace.co"


# ── 1. Verify URL construction ─────────────────────────────────────────────

def test_platform_url(client):
    assert client.auth._base == f"{DEV_GW}/platform", client.auth._base
    assert client.account._base == f"{DEV_GW}/platform", client.account._base
    assert client.organizations._base == f"{DEV_GW}/platform", client.organizations._base


def test_channel_service_url(client):
    cs = f"{DEV_GW}/channel-service"
    assert client.channel._base == cs, client.channel._base
    assert client.conversations._base == cs, client.conversations._base
    assert client.contacts._base == cs, client.contacts._base
    # messages embeds the version path in _base by design
    assert client.messages._base == f"{cs}/v1/conversation_messages", client.messages._base


def test_ai_url(client):
    assert client.ai._base == f"{DEV_GW}/ai", client.ai._base


def test_boards_url(client):
    # Trong develop, data-board dùng direct LAN host
    assert "data-board" in client.boards._base, client.boards._base


def test_ips_url(client):
    # Trong develop, IPS dùng direct LAN host
    assert "ips" in client.ips._base, client.ips._base


def test_health_url(client):
    assert client.health._base == DEV_GW, client.health._base


# ── 2. Verify real server calls (smoke) ────────────────────────────────────

def _is_jwt(token: str) -> bool:
    parts = token.split(".")
    return len(parts) == 3 and token.startswith("eyJ")


def test_platform_responds(api_key):
    """platform service reachable — trả về 401 auth error (không phải 404/502 routing error)."""
    import httpx
    gw = "https://app-gateway.dev.imbrace.co"
    # Ping platform với API key — expect 401 (authed service) chứ không phải 404/502 (routing sai)
    r = httpx.get(
        f"{gw}/platform/v1/health",
        headers={"x-api-key": api_key},
        timeout=10,
    )
    assert r.status_code != 404, f"platform/v1/health trả về 404 — routing sai: {r.text[:100]}"
    assert r.status_code != 502, f"platform/v1/health trả về 502 — service down: {r.text[:100]}"
    assert r.status_code in (200, 201, 401, 403), (
        f"Unexpected status {r.status_code}: {r.text[:100]}"
    )


def test_channel_service_responds(access_token):
    """channel-service trả về 200 — acc_ và JWT tokens đều được chấp nhận."""
    import os
    org_id = os.environ.get("IMBRACE_ORGANIZATION_ID")
    client = ImbraceClient(
        env="develop",
        access_token=access_token,
        organization_id=org_id if _is_jwt(access_token) else None,
    )
    res = client.channel.list()
    assert res is not None
    assert isinstance(res.data, list)
    client.close()


def test_api_key_header_not_access_token(api_key):
    """x-api-key được gắn đúng; x-access-token không được gắn khi chỉ dùng api_key."""
    import httpx
    from unittest.mock import patch, MagicMock

    client = ImbraceClient(env="develop", api_key=api_key)
    captured = {}

    original_request = client.http._client.request

    def capture(*args, **kwargs):
        captured["headers"] = dict(kwargs.get("headers", {}))
        # Gọi thật để lấy response
        return original_request(*args, **kwargs)

    with patch.object(client.http._client, "request", side_effect=capture):
        try:
            client.health.check()
        except Exception:
            pass

    assert captured.get("headers", {}).get("x-api-key") == api_key, (
        f"x-api-key not set correctly: {captured.get('headers')}"
    )
    assert "x-access-token" not in captured.get("headers", {}), (
        "x-access-token must NOT be set when only api_key is used"
    )
    client.close()
