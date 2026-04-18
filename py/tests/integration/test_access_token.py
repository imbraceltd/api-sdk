"""Integration test — Nhiệm vụ 2: phải pass được accessToken.

Cách chạy:
    1. Lấy access token:
         python scripts/get_access_token.py
       (script ghi IMBRACE_ACCESS_TOKEN tự động vào .env)
    2. python -m pytest tests/integration/test_access_token.py -v -m integration

Auth mode được chọn tự động:
    - Có IMBRACE_ORGANIZATION_ID + token là JWT (eyJ...) → JWT Bearer mode:
        Authorization: Bearer <token> + x-organization-id
    - Không có IMBRACE_ORGANIZATION_ID hoặc token không phải JWT → Legacy mode:
        x-access-token: <token>
"""
import os
import pytest
from imbrace import ImbraceClient, AsyncImbraceClient
from imbrace.exceptions import AuthError

pytestmark = pytest.mark.integration


def _is_jwt(token: str) -> bool:
    parts = token.split(".")
    return len(parts) == 3 and token.startswith("eyJ")


@pytest.fixture(scope="module")
def org_id() -> str | None:
    return os.environ.get("IMBRACE_ORGANIZATION_ID")


# ── 1. Token được lưu đúng ────────────────────────────────────────────────────

def test_set_access_token_stores_in_manager(access_token: str):
    """set_access_token() lưu token vào token_manager."""
    client = ImbraceClient(env="develop")
    client.set_access_token(access_token)

    stored = client.token_manager.get_token()
    assert stored == access_token, f"Token not stored correctly: {stored!r}"
    client.close()


def test_token_is_non_empty(access_token: str):
    """Token từ env có giá trị thực, không rỗng."""
    assert len(access_token) > 20, f"Token quá ngắn, có thể không hợp lệ: {access_token!r}"


# ── 2. Token được gắn vào request ─────────────────────────────────────────────

def test_legacy_token_header_sent(access_token: str):
    """Không có org_id → legacy mode: chỉ x-access-token, không Authorization: Bearer."""
    # Pass access_token in constructor so IMBRACE_API_KEY from env is not loaded
    client = ImbraceClient(env="develop", access_token=access_token)  # no organization_id
    captured = {}

    original = client.http._client.request

    def intercept(*args, **kwargs):
        captured["headers"] = dict(kwargs.get("headers", {}))
        return original(*args, **kwargs)

    client.http._client.request = intercept
    try:
        client.health.check()
    except Exception:
        pass

    assert captured.get("headers", {}).get("x-access-token") == access_token, (
        f"x-access-token header không đúng: {captured.get('headers')}"
    )
    assert "authorization" not in captured.get("headers", {}), (
        f"authorization không được gửi trong legacy mode: {captured.get('headers')}"
    )
    client.close()


def test_jwt_bearer_header_sent():
    """JWT Bearer mode: Authorization: Bearer + x-organization-id được gắn đúng.

    Dùng fake JWT để test SDK header logic — không cần server accept.
    Server-side auth với real JWT được cover riêng ở test_server_routing.py.
    """
    # Minimal valid-format JWT (3 base64 parts, starts with eyJ)
    fake_jwt = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1c2VyXzEifQ.signature"
    org_id = os.environ.get("IMBRACE_ORGANIZATION_ID") or "org_test_123"

    client = ImbraceClient(env="develop", organization_id=org_id)
    client.set_access_token(fake_jwt)
    captured = {}

    original = client.http._client.request

    def intercept(*args, **kwargs):
        captured["headers"] = dict(kwargs.get("headers", {}))
        return original(*args, **kwargs)

    client.http._client.request = intercept
    try:
        client.health.check()
    except Exception:
        pass

    assert captured.get("headers", {}).get("authorization") == f"Bearer {fake_jwt}", (
        f"Authorization header không đúng: {captured.get('headers')}"
    )
    assert captured.get("headers", {}).get("x-organization-id") == org_id, (
        f"x-organization-id không đúng: {captured.get('headers')}"
    )
    assert "x-access-token" not in captured.get("headers", {}), (
        f"x-access-token không được gửi trong JWT Bearer mode: {captured.get('headers')}"
    )
    client.close()
    client.close()


# ── 3. Server chấp nhận token ─────────────────────────────────────────────────

def test_account_get_with_token(access_token: str, org_id: str | None):
    """API call thành công — server xác thực token OK."""
    client = ImbraceClient(
        env="develop",
        organization_id=org_id if _is_jwt(access_token) else None,
    )
    client.set_access_token(access_token)
    # channel-service accepts both acc_ and JWT tokens
    res = client.channel.list()
    assert res is not None
    assert isinstance(res.data, list)
    client.close()


def test_set_token_then_api_call(access_token: str, org_id: str | None):
    """Client mới set_access_token() rồi gọi API ngay — không cần login."""
    client = ImbraceClient(
        env="develop",
        organization_id=org_id if _is_jwt(access_token) else None,
    )
    client.set_access_token(access_token)

    channels = client.channel.list()
    assert channels is not None
    assert isinstance(channels.data, list)
    client.close()


# ── 4. Clear token → mất quyền ────────────────────────────────────────────────

def test_clear_token_causes_auth_error(access_token: str):
    """Sau clear_access_token(), request tiếp theo trả về AuthError (401/403)."""
    client = ImbraceClient(env="develop")
    client.set_access_token(access_token)
    client.clear_access_token()

    assert client.token_manager.get_token() is None

    with pytest.raises(AuthError):
        client.account.get()
    client.close()


# ── 5. Async ──────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_async_set_token_stores(access_token: str):
    """AsyncImbraceClient.set_access_token() lưu token."""
    async with AsyncImbraceClient(env="develop") as client:
        client.set_access_token(access_token)
        assert client.token_manager.get_token() == access_token


@pytest.mark.asyncio
async def test_async_account_get_with_token(access_token: str, org_id: str | None):
    """AsyncImbraceClient: account.get() thành công với token hợp lệ."""
    async with AsyncImbraceClient(
        env="develop",
        organization_id=org_id if _is_jwt(access_token) else None,
    ) as client:
        client.set_access_token(access_token)
        res = await client.channel.list()
        assert res is not None
        assert isinstance(res.data, list)


# ── 6. JWT Bearer — server-side auth (requires platform account) ──────────────

def test_jwt_bearer_server_auth(platform_jwt: tuple[str, str]):
    """JWT Bearer mode: server xác thực JWT thật — channel-service trả về 200.

    Chạy khi IMBRACE_PLATFORM_EMAIL + IMBRACE_PLATFORM_PASSWORD được set.
    Xem docs/TESTING_GUIDE.md để setup platform account.
    """
    jwt, org_id = platform_jwt
    client = ImbraceClient(env="develop", organization_id=org_id)
    client.set_access_token(jwt)
    res = client.channel.list()
    assert res is not None
    assert isinstance(res.data, list)
    client.close()


@pytest.mark.asyncio
async def test_async_jwt_bearer_server_auth(platform_jwt: tuple[str, str]):
    """AsyncImbraceClient JWT Bearer mode: server xác thực JWT thật."""
    jwt, org_id = platform_jwt
    async with AsyncImbraceClient(env="develop", organization_id=org_id) as client:
        client.set_access_token(jwt)
        res = await client.channel.list()
        assert res is not None
        assert isinstance(res.data, list)
