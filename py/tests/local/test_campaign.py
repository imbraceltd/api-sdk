"""
Campaign resource test — sync + async, runs against prodv2 gateway.
Usage:
    pip install -e ".[dev]"
    python tests/local/test_campaign.py
"""
import os
import asyncio
import time
from imbrace import ImbraceClient
from imbrace.async_client import AsyncImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c8c27f3b-e147-4735-b641-61e8d3706692")
GATEWAY      = os.environ.get("IMBRACE_GATEWAY_URL",  "https://app-gatewayv2.imbrace.co")

passed = 0
failed = 0
skipped = 0

def ok(label, detail=""):
    global passed
    detail_str = f"  →  {str(detail)[:120]}" if detail else ""
    print(f"  ✓ {label}{detail_str}")
    passed += 1

def fail(label, err):
    global failed
    print(f"  ✗ {label}: {err}")
    failed += 1

def skip(label, reason):
    global skipped
    print(f"  - {label}  (skipped: {reason})")
    skipped += 1

# ─────────────────────────────────────────────────────────────────────────────
# Sync
# ─────────────────────────────────────────────────────────────────────────────

def test_sync():
    print("\n--- Synchronous Tests ---")
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    campaign = client.campaigns # Note: it's 'campaigns' in Python client.py

    created_campaign_id = None
    created_touchpoint_id = None

    print("\n[1] List campaigns")
    try:
        res = campaign.list()
        lst = res.get("data", [])
        ok("list()", f"{len(lst)} campaigns")
    except Exception as e: fail("list()", e)

    print("\n[2] Create campaign")
    try:
        res = campaign.create({
            "name": f"SDK Test Campaign (Py) — {int(time.time())}",
            "channel_type": "whatsapp",
        })
        created_campaign_id = res.get("_id") or res.get("id")
        ok("create()", f"id={created_campaign_id}")
    except Exception as e: fail("create()", e)

    print("\n[3] Get campaign")
    if not created_campaign_id:
        skip("get()", "no campaign created")
    else:
        try:
            res = campaign.get(created_campaign_id)
            ok("get()", f"id={res.get('_id') or res.get('id')} name={res.get('name')}")
        except Exception as e: fail("get()", e)

    print("\n[4] Create touchpoint")
    if not created_campaign_id:
        skip("create_touchpoint()", "no campaign created")
    else:
        try:
            # Note: touchpoints might be handled by client.touchpoints or campaign resource
            # In TS it's campaign.createTouchpoint
            # Checking py/src/imbrace/resources/campaigns.py
            res = campaign.create_touchpoint({
                "name": "SDK Test Touchpoint (Py)",
                "campaign_id": created_campaign_id,
                "type": "message",
                "message": "Hello from SDK Test (Py)",
            })
            created_touchpoint_id = res.get("_id") or res.get("id")
            ok("create_touchpoint()", f"id={created_touchpoint_id}")
        except Exception as e: fail("create_touchpoint()", e)

    print("\n[5] Cleanup")
    if created_touchpoint_id:
        try:
            # Need to check if delete_touchpoint is on campaign or touchpoints
            campaign.delete_touchpoint(created_touchpoint_id)
            ok("delete_touchpoint()", created_touchpoint_id)
        except Exception as e: fail("delete_touchpoint()", e)

    if created_campaign_id:
        try:
            campaign.delete(created_campaign_id)
            ok("delete() campaign", created_campaign_id)
        except Exception as e: fail("delete()", e)

# ─────────────────────────────────────────────────────────────────────────────
# Async
# ─────────────────────────────────────────────────────────────────────────────

async def test_async():
    print("\n--- Asynchronous Tests ---")
    async with AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY) as client:
        campaign = client.campaigns
        try:
            res = await campaign.list()
            ok("async list()", f"count={len(res.get('data', []))}")
        except Exception as e: fail("async list()", e)

if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())

    print(f"\n{'─' * 55}")
    print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
