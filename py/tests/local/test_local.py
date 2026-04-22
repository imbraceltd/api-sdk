"""
Local package test — runs against the local source.
Usage:
    pip install -e .
    python tests/local/test_local.py
"""
import os
import warnings
import json
from imbrace import ImbraceClient

API_KEY      = os.environ.get("IMBRACE_API_KEY", "api_bf3be272-1bd1-4944-b167-5dd997f9302f")
ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_a9ff3bfa-7a97-4b5e-9c02-a567d15755d4")
ORG_ID       = os.environ.get("IMBRACE_ORGANIZATION_ID", "org_ee7e1814-1a77-419b-b95b-871353d81657")
BASE_URL     = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")

passed = 0
failed = 0

def ok(label):
    global passed
    print(f"  ✓ {label}")
    passed += 1

def fail(label, err):
    global failed
    print(f"  ✗ {label}: {err}")
    failed += 1

# [1] Instantiation
print("\n[1] Instantiation")
client = None
try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        client = ImbraceClient(
            api_key=API_KEY or None,
            access_token=ACCESS_TOKEN or None,
            gateway=BASE_URL,
        )
    ok("ImbraceClient created")
except Exception as e:
    fail("ImbraceClient created", e)
    exit(1)

# [2] Resource surface
print("\n[2] Resource surface")
expected = [
    "auth",
    "account",
    "organizations",
    "teams",
    "settings",
    "channel",
    "contacts",
    "conversations",
    "messages",
    "workflows",
    "boards",
    "ips",
    "ai",
    "marketplace",
    "agent",
    "campaign",
    "outbound",
    "license",
    "health",
    "sessions",
    "schedule",
    "platform",
]
for r in expected:
    if hasattr(client, r):
        ok(f"client.{r}")
    else:
        fail(f"client.{r}", "undefined")

# [3] Live API calls
if not API_KEY and not ACCESS_TOKEN:
    print("\n[3] Live API calls — SKIPPED (set IMBRACE_API_KEY or IMBRACE_ACCESS_TOKEN)")
else:
    method = "API Key" if API_KEY else "Access Token"
    print(f"\n[3] Live API calls (gateway: {BASE_URL}, via: {method})")
    
    checks = [
        ("health.check()", lambda: client.health.check()),
        ("account.get()", lambda: client.account.get()),
        ("channel.list()", lambda: client.channel.list()),
        ("contacts.list(limit=1)", lambda: client.contacts.list(limit=1)),
        ("teams.list()", lambda: client.teams.list()),
        ("conversations.get_views_count()", lambda: client.conversations.get_views_count()),
        ("boards.list()", lambda: client.boards.list()),
        ("agent.list()", lambda: client.agent.list()),
    ]

    for label, fn in checks:
        try:
            res = fn()
            # If the response is a Pydantic model, convert to dict first
            output = res.model_dump() if hasattr(res, "model_dump") else res
            print(f"  ✓ {label}  →  {json.dumps(output)[:60]}")
            passed += 1
        except Exception as e:
            fail(label, e)

print(f"\n{'─' * 50}")
print(f"  {passed} passed  |  {failed} failed")
if failed > 0:
    exit(1)
