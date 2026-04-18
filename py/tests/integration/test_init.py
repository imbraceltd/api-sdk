"""Integration test — Nhiệm vụ 1: phải init được.

Kiểm tra:
- Client khởi tạo không ném exception
- health.check() trả về response thành công từ server thật
- init() với check_health=True chạy được
"""
import pytest
from imbrace import ImbraceClient, AsyncImbraceClient

pytestmark = pytest.mark.integration


def test_client_init_no_exception(api_key, gateway):
    """Client khởi tạo với api_key + env develop không ném exception."""
    client = ImbraceClient(env="develop", api_key=api_key)
    client.close()


def test_health_check_returns_ok(client):
    """health.check() gọi GET / trên gateway và server trả về JSON."""
    res = client.health.check()
    # Gateway root trả về {"name": "App Gateway Public Server", "version": ..., "env": ...}
    assert isinstance(res, dict), f"Expected dict, got {type(res)}: {res}"
    assert "name" in res or "status" in res, f"Unexpected response from gateway root: {res}"


def test_init_with_check_health(api_key):
    """init() với check_health=True gọi health check và không raise."""
    import os
    client = ImbraceClient(
        env="develop",
        api_key=api_key,
        check_health=True,
        organization_id=os.environ.get("IMBRACE_ORGANIZATION_ID"),
    )
    client.close()


@pytest.mark.asyncio
async def test_async_client_init_no_exception(api_key):
    """AsyncImbraceClient khởi tạo được."""
    async with AsyncImbraceClient(env="develop", api_key=api_key) as client:
        res = await client.health.check()
        assert isinstance(res, dict)
