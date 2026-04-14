"""
Script lấy JWT Access Token qua OTP login flow.
Chạy: python scripts/get_access_token.py
"""
import os
import sys
from pathlib import Path

# Load .env trước
from dotenv import load_dotenv, set_key
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

import httpx

BASE_URL = os.getenv("IMBRACE_BASE_URL", "https://app-gatewayv2.imbrace.co")
ORG_ID = os.getenv("IMBRACE_ORG_ID", "")
ENV_FILE = Path(__file__).parent.parent / ".env"


def _safe_json(resp: httpx.Response) -> dict:
    """Parse JSON an toàn — trả về dict rỗng nếu body trống hoặc không phải JSON."""
    if not resp.content:
        print(f"      [warn] Response body trống (status={resp.status_code})")
        return {}
    try:
        return resp.json()
    except Exception:
        print(f"      [warn] Không parse được JSON. Raw: {resp.text[:200]}")
        return {}


def step1_request_otp(email: str) -> bool:
    print(f"\n[1/3] Gửi OTP đến {email} ...")
    resp = httpx.post(
        f"{BASE_URL}/v1/backend/login/_signin_email_request",
        json={"email": email},
    )
    data = _safe_json(resp)
    print(f"      status={resp.status_code} response={data}")
    return resp.status_code < 300


def step2_verify_otp(email: str, otp: str) -> tuple[str | None, str | None]:
    print(f"\n[2/3] Xác thực OTP ...")
    resp = httpx.post(
        f"{BASE_URL}/v1/backend/login/_signin_with_email",
        json={"email": email, "otp": otp},
    )
    data = _safe_json(resp)
    print(f"      status={resp.status_code} full response={data}")
    inner = data.get("data") or data
    token = (
        inner.get("token")
        or inner.get("loginToken")
        or inner.get("login_token")
    )
    # Lấy org_id từ response nếu có (ưu tiên hơn env)
    org_id = (
        inner.get("organizationId")
        or inner.get("organization_id")
        or inner.get("orgId")
        or inner.get("org_id")
    )
    if org_id:
        print(f"      org_id từ response: {org_id}")
    return token, org_id


def step3_exchange_token(login_token: str, org_id: str) -> str | None:
    print(f"\n[3/3] Đổi login token lấy access token cho org {org_id} ...")
    print(f"      login_token (preview): {login_token[:40]}...")

    attempts = [
        # token trong body
        {"body": {"token": login_token, "organization_id": org_id}, "headers": {}},
        {"body": {"loginToken": login_token, "organization_id": org_id}, "headers": {}},
        # token trong header x-access-token, chỉ org trong body
        {"body": {"organization_id": org_id}, "headers": {"x-access-token": login_token}},
        # token trong header Authorization Bearer
        {"body": {"organization_id": org_id}, "headers": {"Authorization": f"Bearer {login_token}"}},
    ]

    for attempt in attempts:
        print(f"      Thử body={list(attempt['body'].keys())} headers={list(attempt['headers'].keys())}")
        resp = httpx.post(
            f"{BASE_URL}/v1/backend/access/_exchange_access_token",
            json=attempt["body"],
            headers=attempt["headers"],
        )
        data = _safe_json(resp)
        print(f"      status={resp.status_code} response={data}")
        if resp.status_code < 300:
            inner = data.get("data") or data
            access_token = (
                inner.get("accessToken")
                or inner.get("access_token")
                or inner.get("token")
            )
            return access_token

    return None


def main():
    print("=== iMBRACE — Lấy JWT Access Token ===")
    print(f"Base URL : {BASE_URL}")
    print(f"Org ID   : {ORG_ID or '(chưa set, sẽ hỏi sau)'}")
    print(f".env file: {ENV_FILE}")

    email = input("\nNhập email tài khoản iMBRACE: ").strip()
    if not email:
        print("Email không được để trống.")
        sys.exit(1)

    ok = step1_request_otp(email)
    if not ok:
        print("Gửi OTP thất bại, kiểm tra lại email hoặc BASE_URL.")
        sys.exit(1)

    otp = input("\nNhập OTP nhận được trong email: ").strip()
    login_token, org_id_from_response = step2_verify_otp(email, otp)
    if not login_token:
        print("Không lấy được login token. Kiểm tra OTP có đúng không.")
        sys.exit(1)

    print(f"\n      Login token: {login_token[:40]}...")

    # Ưu tiên org_id từ response, rồi env, rồi hỏi user
    org_id = org_id_from_response or ORG_ID or input("\nNhập Organization ID (IMBRACE_ORG_ID): ").strip()
    print(f"      Dùng org_id: {org_id}")
    access_token = step3_exchange_token(login_token, org_id)
    if not access_token:
        print("Không lấy được access token. Kiểm tra org_id có đúng không.")
        sys.exit(1)

    print(f"\n Access token lấy thành công!")
    print(f"  {access_token[:60]}...")

    save = input("\nTự động cập nhật IMBRACE_ACCESS_TOKEN trong .env? [Y/n]: ").strip().lower()
    if save in ("", "y", "yes"):
        set_key(str(ENV_FILE), "IMBRACE_ACCESS_TOKEN", access_token)
        print(f"  Đã lưu vào {ENV_FILE}")
    else:
        print(f"\n  Copy thủ công vào .env:")
        print(f"  IMBRACE_ACCESS_TOKEN={access_token}")


if __name__ == "__main__":
    main()
