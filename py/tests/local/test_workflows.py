"""
Workflows resource test — sync + async, runs against prodv2 gateway.
Usage:
    pip install -e ".[dev]"
    python tests/local/test_workflows.py
"""
import os
import asyncio
from imbrace import ImbraceClient
from imbrace.async_client import AsyncImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c8c27f3b-e147-4735-b641-61e8d3706692")
GATEWAY = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")

passed = 0
failed = 0
skipped = 0


def ok(label, detail=""):
    global passed
    detail_str = f"  →  {str(detail)[:100]}" if detail else ""
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


def test_sync():
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    w = client.workflows

    print("\n[1] List channel automations (sync)")
    try:
        res = w.list_channel_automation()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("list_channel_automation()", f"{len(lst)} automations")
    except Exception as e:
        fail("list_channel_automation()", e)

    print("\n[2] Filter by channel type (sync)")
    try:
        res = w.list_channel_automation(channel_type="whatsapp")
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("list_channel_automation(whatsapp)", f"{len(lst)} automations")
    except Exception as e:
        fail("list_channel_automation(whatsapp)", e)


async def test_async():
    client = AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    w = client.workflows

    print("\n[3] List channel automations (async)")
    try:
        res = await w.list_channel_automation()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("async list_channel_automation()", f"{len(lst)} automations")
    except Exception as e:
        fail("async list_channel_automation()", e)

    await client.close()


if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())

    print(f"\n{'─' * 55}")
    print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
