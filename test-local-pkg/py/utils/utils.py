import os
import sys
import time
from typing import Optional, Callable, Any
from dotenv import load_dotenv
from imbrace import ImbraceClient

# Load environment variables
load_dotenv()

api_key = os.getenv("IMBRACE_API_KEY")
access_token = os.getenv("IMBRACE_ACCESS_TOKEN")
organization_id = os.getenv("IMBRACE_ORGANIZATION_ID")
base_url = os.getenv("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")
timeout = int(os.getenv("IMBRACE_TIMEOUT", "60"))
skip_unstable = os.getenv("IMBRACE_SKIP_UNSTABLE", "0") == "1"

if (not api_key and not access_token) or not organization_id:
    print("❌ ERROR: Missing configuration in .env!")
    print("Required: (IMBRACE_API_KEY OR IMBRACE_ACCESS_TOKEN) AND IMBRACE_ORGANIZATION_ID")
    sys.exit(1)

# Initialize Client
use_access_token = bool(access_token)
client = ImbraceClient(
    api_key=None if use_access_token else api_key,
    access_token=access_token if use_access_token else None,
    base_url=base_url,
    timeout=timeout,
    organization_id=organization_id,
)

def run_test_section(name: str, fn: Callable[[], Any]):
    print(f"\n--- [TEST] {name} ---")
    try:
        start = time.time()
        result = fn()
        end = time.time()
        print(f"✅ Passed ({(end - start) * 1000:.0f}ms)")
        return result
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        print(f"❌ Failed: {str(e)}")
        if status_code:
            print(f"   HTTP Status: {status_code}")
        
        if status_code in (401, 403, 404, 500, 501, 502, 503):
            print(f"   ⚠️ Skipping section due to {status_code} (Auth/Endpoint issue)")
            return None
        raise e

def run_stable_section(name: str, fn: Callable[[], Any], unstable: bool = False):
    """Like run_test_section but can be skipped when IMBRACE_SKIP_UNSTABLE=1.
    
    Use unstable=True for sections known to hit 502/backend-pending endpoints.
    When IMBRACE_SKIP_UNSTABLE=1, these sections are skipped instantly instead
    of waiting for retry timeouts (~4-5 min per section).
    """
    if unstable and skip_unstable:
        print(f"\n--- [SKIP] {name} (IMBRACE_SKIP_UNSTABLE=1 — backend-pending) ---")
        return None
    return run_test_section(name, fn)

def log_result(label: str, data: Any):
    display = "N/A"
    if isinstance(data, list):
        display = f"{len(data)} items"
    elif isinstance(data, dict):
        display = data.get("_id") or data.get("id") or str(data)[:100]
    elif data:
        # If it's a pydantic model or other object
        display = getattr(data, "id", None) or getattr(data, "_id", None) or str(data)[:100]
    
    print(f"   {label}: {display}")
