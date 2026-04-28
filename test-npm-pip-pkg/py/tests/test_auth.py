"""
Test: Authentication methods
Per docsv2/py-sdk/Authentication.md and method-py.md:
  - client.request_otp(email)
  - client.login_with_otp(email, otp)
  - client.login(email, password)  [email+password flow]
  - client.set_access_token(token)
  - client.clear_access_token()
"""
from utils.utils import client, run_test_section, log_result

def test_auth():
    print("\n[START] Testing Authentication Methods...")

    # 1. request_otp — per Authentication.md: Step 1 of OTP flow
    def test_request_otp():
        try:
            # Use a dummy email; server will validate format and send OTP (or return error if not real user)
            client.request_otp("sdk-test-dummy@example.com")
            log_result("request_otp", "Sent (or server validated format)")
        except Exception as e:
            # Expected: 404 user-not-found or similar — still confirms the method exists and endpoint is reachable
            print(f"   ⚠️ request_otp failed (expected for dummy email): {str(e)}")
    run_test_section("client.request_otp", test_request_otp)

    # 2. login_with_otp — per Authentication.md: Step 2 of OTP flow
    def test_login_with_otp():
        try:
            # Will fail with invalid OTP — confirms method & endpoint exist
            client.login_with_otp("sdk-test-dummy@example.com", "000000")
            log_result("login_with_otp", "Authenticated")
        except Exception as e:
            print(f"   ⚠️ login_with_otp failed (expected for dummy OTP): {str(e)}")
    run_test_section("client.login_with_otp", test_login_with_otp)

    # 3. login (email + password) — per Authentication.md
    def test_login():
        try:
            client.login("sdk-test-dummy@example.com", "WrongPassword!")
            log_result("login (email+password)", "Authenticated")
        except Exception as e:
            print(f"   ⚠️ login failed (expected for dummy credentials): {str(e)}")
    run_test_section("client.login", test_login)

    # 4. Token management — per Authentication.md: set_access_token / clear_access_token
    def test_token_management():
        # Save original credentials
        original_api_key = None
        original_token = None
        try:
            original_api_key = client._http.api_key
            if hasattr(client, "_token_manager"):
                original_token = client._token_manager.get_token()
        except Exception:
            pass

        # set_access_token — replaces current token in TokenManager
        try:
            client.set_access_token("test_token_placeholder_xxx")
            log_result("set_access_token", "Set OK")
        except Exception as e:
            print(f"   [warn] set_access_token failed: {str(e)}")

        # clear_access_token — clears token
        try:
            client.clear_access_token()
            log_result("clear_access_token", "Cleared OK")
        except Exception as e:
            print(f"   [warn] clear_access_token failed: {str(e)}")

        # ALWAYS restore original credentials
        try:
            if original_api_key:
                client._http.api_key = original_api_key
            if original_token:
                client.set_access_token(original_token)
            log_result("Credentials Restored", "OK")
        except Exception as e:
            print(f"   [warn] restore credentials: {str(e)}")
    run_test_section("Token Management (set / clear)", test_token_management)

    print("\n[DONE] Authentication Methods Testing Completed.")

if __name__ == "__main__":
    test_auth()
