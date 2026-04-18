"""Script lấy JWT access token qua OTP email — platform v1 flow.

Flow (non-legacy, trả về JWT eyJ...):
    1. POST /platform/v1/login/_signin_email_request  → gửi OTP
    2. POST /platform/v1/login/_signin_with_email     → session token
    3. GET  /platform/v2/organizations                → danh sách org
    4. POST /platform/v1/access/_exchange_access_token → JWT (eyJ...)

JWT được dùng cho JWT Bearer mode:
    Authorization: Bearer <jwt> + x-organization-id: <org_id>

Cách dùng:
    python scripts/get_access_token.py

Kết quả: tự động ghi IMBRACE_ACCESS_TOKEN và IMBRACE_ORGANIZATION_ID vào .env
"""
import os
import sys
import re
import httpx
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ENV_FILE = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=ENV_FILE)

GATEWAY = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gateway.dev.imbrace.co").rstrip("/")
PLATFORM = f"{GATEWAY}/platform/v1"
PLATFORM_V2 = f"{GATEWAY}/platform/v2"
BACKEND = f"{GATEWAY}/backend/v1"
BACKEND_V2 = f"{GATEWAY}/backend/v2"


def request_otp(email: str) -> None:
    # Dùng /backend/v1/ — token trả về được backend/v2/organizations chấp nhận
    url = f"{BACKEND}/login/_signin_email_request"
    print(f"Gửi OTP đến {email} ...")
    r = httpx.post(url, json={"email": email}, timeout=15)
    if r.status_code not in (200, 201):
        print(f"Lỗi gửi OTP: {r.status_code} — {r.text}")
        sys.exit(1)
    print("OTP đã được gửi. Kiểm tra email.")


def signin_with_otp(email: str, otp: str) -> str:
    """Xác thực OTP qua backend/v1, trả về session token (login_acc_...)."""
    url = f"{BACKEND}/login/_signin_with_email"
    r = httpx.post(url, json={"email": email, "otp": otp}, timeout=15)
    if r.status_code not in (200, 201):
        print(f"Lỗi login: {r.status_code} — {r.text}")
        sys.exit(1)
    data = r.json()
    print(f"[DEBUG] OTP login response: {data}")

    nested = data.get("data") or {}
    token = (
        data.get("token") or data.get("accessToken") or data.get("access_token")
        or nested.get("token") or nested.get("accessToken") or nested.get("access_token")
    )
    if not token:
        print("Không tìm thấy token trong response.")
        sys.exit(1)
    print(f"[DEBUG] Session token: {token[:40]}... (JWT={token.startswith('eyJ')})")
    return token


def fetch_organizations(session_token: str) -> list:
    """Lấy danh sách org qua backend/v2 với x-access-token (login_acc_ token)."""
    url = f"{BACKEND_V2}/organizations?limit=50&skip=0&is_active=true"
    r = httpx.get(url, headers={"x-access-token": session_token}, timeout=15)
    print(f"[DEBUG] fetch_orgs status={r.status_code}")
    if r.status_code == 200:
        return r.json().get("data", [])
    print(f"[WARN] Không lấy được org list: {r.status_code} — {r.text[:200]}")
    return []


def exchange_for_jwt(session_token: str, org_id: str) -> str | None:
    """Exchange session token + org_id → access token.

    Thử platform v1 trước (có thể trả JWT eyJ...), fallback backend v1 (trả acc_).
    """
    is_jwt_session = session_token.startswith("eyJ")
    candidates = [
        (f"{PLATFORM}/access/_exchange_access_token",
         {"Authorization": f"Bearer {session_token}"} if is_jwt_session else {"x-access-token": session_token}),
        (f"{BACKEND}/access/_exchange_access_token",
         {"x-access-token": session_token}),
    ]

    for url, headers in candidates:
        print(f"Exchange token cho org {org_id} via {url.split('/')[5]}/v1 ...")
        r = httpx.post(url, json={"organization_id": org_id}, headers=headers, timeout=15)
        print(f"[DEBUG] Exchange status={r.status_code} response={r.text[:400]}")
        if r.status_code not in (200, 201):
            continue
        data = r.json()
        nested = data.get("data") or {}
        token = (
            data.get("token") or data.get("accessToken") or data.get("access_token")
            or nested.get("token") or nested.get("accessToken") or nested.get("access_token")
        )
        if token:
            print(f"[DEBUG] Exchange result: {token[:40]}... (JWT={token.startswith('eyJ')})")
            return token
    return None


def write_env_value(key: str, value: str) -> None:
    content = ENV_FILE.read_text(encoding="utf-8")
    if re.search(rf"^{key}=", content, re.MULTILINE):
        content = re.sub(
            rf"^({key}=).*$",
            lambda m: f"{m.group(1)}{value}",
            content,
            flags=re.MULTILINE,
        )
    else:
        content += f"\n{key}={value}\n"
    ENV_FILE.write_text(content, encoding="utf-8")


def signin_with_password(email: str, password: str) -> str | None:
    """Sign in với email/password qua platform v1. Trả về session token (JWT) hoặc None."""
    url = f"{PLATFORM}/login/sign_in"
    r = httpx.post(url, json={"email": email, "password": password}, timeout=15)
    print(f"[DEBUG] platform sign_in: {r.status_code} {r.text[:200]}")
    if r.status_code not in (200, 201):
        return None
    data = r.json()
    nested = data.get("data") or {}
    return (
        data.get("token") or data.get("accessToken")
        or nested.get("token") or nested.get("accessToken")
    )


def fetch_organizations_platform(session_token: str) -> list:
    """Lấy danh sách org qua platform v2 với Authorization: Bearer."""
    url = f"{PLATFORM_V2}/organizations?limit=50&skip=0&is_active=true"
    r = httpx.get(url, headers={"Authorization": f"Bearer {session_token}"}, timeout=15)
    print(f"[DEBUG] platform orgs: {r.status_code}")
    if r.status_code == 200:
        return r.json().get("data", [])
    return []


def exchange_platform_jwt(session_token: str, org_id: str) -> str | None:
    """Exchange platform session token → org-scoped JWT."""
    url = f"{PLATFORM}/access/_exchange_access_token"
    r = httpx.post(
        url,
        json={"organization_id": org_id},
        headers={"Authorization": f"Bearer {session_token}"},
        timeout=15,
    )
    print(f"[DEBUG] platform exchange: {r.status_code} {r.text[:200]}")
    if r.status_code not in (200, 201):
        return None
    data = r.json()
    nested = data.get("data") or {}
    return (
        data.get("token") or data.get("accessToken")
        or nested.get("token") or nested.get("accessToken")
    )


def main():
    # ── Flow 1: Platform account (password) → JWT ─────────────────────────────
    platform_email = os.environ.get("IMBRACE_PLATFORM_EMAIL")
    platform_pw = os.environ.get("IMBRACE_PLATFORM_PASSWORD")

    if platform_email and platform_pw:
        print(f"\n[Platform flow] Đăng nhập {platform_email} ...")
        session = signin_with_password(platform_email, platform_pw)
        if session:
            orgs = fetch_organizations_platform(session)
            if orgs:
                jwt = exchange_platform_jwt(session, orgs[0]["id"])
                if jwt and jwt.startswith("eyJ"):
                    write_env_value("IMBRACE_PLATFORM_EMAIL", platform_email)
                    write_env_value("IMBRACE_PLATFORM_PASSWORD", platform_pw)
                    print(f"\n✓ Platform JWT lấy thành công!")
                    print(f"  test_jwt_bearer_server_auth sẽ PASS với account này.")
                    print("\nHoàn tất! Chạy test:")
                    print("  python -m pytest tests/integration/ -v -m integration")
                    return
                else:
                    print(f"[WARN] Platform exchange không trả về JWT: {jwt!r:.40}")
            else:
                print("[WARN] Platform account không có org nào.")
        else:
            print("[WARN] Platform sign_in thất bại — kiểm tra email/password.")

    # ── Flow 2: Legacy OTP (backend v1) → acc_ token ──────────────────────────
    print("\n[Legacy OTP flow] Lấy acc_ token cho channel-service tests ...")
    email = os.environ.get("IMBRACE_TEST_EMAIL") or input("Email: ").strip()
    if not email:
        print("Cần nhập email.")
        sys.exit(1)

    request_otp(email)

    otp = input("Nhập mã OTP từ email: ").strip()
    if not otp:
        print("Cần nhập OTP.")
        sys.exit(1)

    session_token = signin_with_otp(email, otp)
    print(f"\nSession token: {session_token[:40]}...")

    orgs = fetch_organizations(session_token)
    if not orgs:
        print("[WARN] Không tìm được org nào.")
        write_env_value("IMBRACE_ACCESS_TOKEN", session_token)
        sys.exit(1)

    print(f"\nTìm thấy {len(orgs)} org(s):")
    for i, org in enumerate(orgs):
        print(f"  [{i}] {org['id']} — {org['name']}")

    final_token = None
    final_org_id = None
    for org in orgs:
        token = exchange_for_jwt(session_token, org["id"])
        if token:
            final_token = token
            final_org_id = org["id"]
            print(f"Exchange OK: org {org['id']} ({org['name']})")
            break

    if final_token:
        write_env_value("IMBRACE_ACCESS_TOKEN", final_token)
        write_env_value("IMBRACE_ORGANIZATION_ID", final_org_id or "")
        print(f"\nĐã ghi IMBRACE_ACCESS_TOKEN và IMBRACE_ORGANIZATION_ID vào {ENV_FILE}")
    else:
        write_env_value("IMBRACE_ACCESS_TOKEN", session_token)
        print("[WARN] Không exchange được. Lưu session token.")

    print("\nHoàn tất! Chạy test:")
    print("  python -m pytest tests/integration/ -v -m integration")


if __name__ == "__main__":
    main()
