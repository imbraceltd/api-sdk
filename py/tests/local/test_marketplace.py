"""
Marketplace resource test — sync + async, runs against prodv2 gateway.
Usage:
    pip install -e ".[dev]"
    python tests/local/test_marketplace.py
"""
import os
import asyncio
from imbrace import ImbraceClient
from imbrace.async_client import AsyncImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c8c27f3b-e147-4735-b641-61e8d3706692")
GATEWAY      = os.environ.get("IMBRACE_GATEWAY_URL",  "https://app-gatewayv2.imbrace.co")

passed = 0
failed = 0
skipped = 0

def ok(label, detail=""):
    global passed
    detail_str = f"  →  {str(detail)[:80]}" if detail else ""
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
    marketplace = client.marketplace

    # [1] Use case templates
    print("\n[1] Use case templates")
    try:
        res = marketplace.list_use_case_templates()
        lst = res.get("data", res) if isinstance(res, dict) else res
        ok("list_use_case_templates()", f"{len(lst) if isinstance(lst, list) else '?'} templates")
    except Exception as e: fail("list_use_case_templates()", e)

    # [2] Products
    print("\n[2] Products")
    first_product_id = None
    try:
        res = marketplace.list_products(limit=3)
        lst = res.get("data", res) if isinstance(res, dict) else res
        ok("list_products()", f"{len(lst) if isinstance(lst, list) else '?'} products")
        if isinstance(lst, list) and len(lst) > 0:
            first_product_id = lst[0].get("_id") or lst[0].get("id")
    except Exception as e: fail("list_products()", e)

    # [3] Get product
    print("\n[3] Get product")
    if not first_product_id:
        skip("get_product()", "no products found")
    else:
        try:
            p = marketplace.get_product(first_product_id)
            p_data = p.get("data", p) if isinstance(p, dict) else p
            ok("get_product()", f"id={p_data.get('_id') or p_data.get('id')} name={p_data.get('name')}")
        except Exception as e: fail("get_product()", e)

    # [4] Orders
    print("\n[4] Orders")
    first_order_id = None
    try:
        res = marketplace.list_orders(limit=3)
        lst = res.get("data", res) if isinstance(res, dict) else res
        ok("list_orders()", f"{len(lst) if isinstance(lst, list) else '?'} orders")
        if isinstance(lst, list) and len(lst) > 0:
            first_order_id = lst[0].get("_id") or lst[0].get("id")
    except Exception as e:
        if "404" in str(e): skip("list_orders()", "route not available")
        else: fail("list_orders()", e)

    # [5] Get order
    print("\n[5] Get order")
    if not first_order_id:
        skip("get_order()", "no orders found")
    else:
        try:
            o = marketplace.get_order(first_order_id)
            o_data = o.get("data", o) if isinstance(o, dict) else o
            ok("get_order()", f"id={o_data.get('_id') or o_data.get('id')}")
        except Exception as e: fail("get_order()", e)

    # [6] Email templates
    print("\n[6] Email templates")
    try:
        res = marketplace.list_email_templates()
        lst = res.get("data", res) if isinstance(res, dict) else res
        ok("list_email_templates()", f"{len(lst) if isinstance(lst, list) else '?'} templates")
    except Exception as e:
        if "400" in str(e) or "404" in str(e): skip("list_email_templates()", "requires org context or route unavailable")
        else: fail("list_email_templates()", e)

    # [7] Categories
    print("\n[7] Categories")
    try:
        res = marketplace.list_categories()
        lst = res.get("data", res) if isinstance(res, dict) else res
        ok("list_categories()", f"{len(lst) if isinstance(lst, list) else '?'} categories")
    except Exception as e:
        if "404" in str(e): skip("list_categories()", "route not available")
        else: fail("list_categories()", e)

# ─────────────────────────────────────────────────────────────────────────────
# Async
# ─────────────────────────────────────────────────────────────────────────────

async def test_async():
    print("\n--- Asynchronous Tests ---")
    async with AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY) as client:
        marketplace = client.marketplace
        try:
            res = await marketplace.list_use_case_templates()
            lst = res.get("data", res) if isinstance(res, dict) else res
            ok("async list_use_case_templates()", f"count={len(lst) if isinstance(lst, list) else '?'}")
        except Exception as e: fail("async list_use_case_templates()", e)

if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())

    print(f"\n{'─' * 50}")
    print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
