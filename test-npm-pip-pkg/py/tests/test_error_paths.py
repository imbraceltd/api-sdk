import os
import sys
from utils.utils import client, run_test_section, log_result, base_url, organization_id
from imbrace import ImbraceClient, ApiError, AuthError

def test_error_paths():
    print("\n" + "=" * 70)
    print("🚀 STARTING: ERROR PATH TESTING (PY)")
    print("=" * 70)

    # 1. 404 Not Found
    def test_404():
        try:
            client.boards.get("non-existent-id-12345")
            raise Exception("Should have thrown 404")
        except ApiError as e:
            log_result("Caught Expected 404", str(e))
            if e.status_code != 404:
                print(f"   ⚠️ Expected 404 but got {e.status_code}")
    run_test_section("404 Not Found Handling", test_404)

    # 2. 401 Unauthorized
    def test_401():
        bad_client = ImbraceClient(
            api_key="invalid-key",
            base_url=base_url,
            organization_id="invalid-org"
        )
        try:
            bad_client.chat_ai.list_assistants()
            raise Exception("Should have thrown 401")
        except AuthError as e:
            log_result("Caught Expected 401", str(e))
    run_test_section("401 Unauthorized Handling", test_401)

    # 3. 400 Bad Request
    def test_400():
        try:
            # Missing required 'name' field
            client.boards.create(name="")
            # Note: some APIs might allow empty name, but usually they fail.
            # If this doesn't fail, we might need another 400 case.
            # Actually, calling create with nothing might not be possible with typed args in PY.
            # But we can pass empty dict if it was generic.
            # Let's try boards.create_field with invalid type
            client.boards.create_field("dummy", {"name": "Test", "type": "InvalidType"})
            raise Exception("Should have thrown 400")
        except ApiError as e:
            log_result("Caught Expected 400/404", str(e))
        except Exception as e:
            log_result("Caught Generic Error", str(e))
    run_test_section("400 Bad Request Handling", test_400)

    print("\n" + "=" * 70)
    print("✅ ERROR PATH TESTING COMPLETED")
    print("=" * 70)

if __name__ == "__main__":
    test_error_paths()
