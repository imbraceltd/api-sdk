"""
Boards resource test — sync + async, runs against prodv2 gateway.
Usage:
    pip install -e ".[dev]"
    python tests/local/test_boards.py
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

created = {
    "board_id": None,
    "identifier_field_id": None,
    "field_id": None,
    "field_id2": None,
    "item_id": None,
    "item_id2": None,
    "segment_id": None,
}

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

def find_field(board_res, name):
    fields = board_res.get("fields", [])
    for f in fields:
        if f.get("name") == name:
            return f
    return None

# ─────────────────────────────────────────────────────────────────────────────
# Sync
# ─────────────────────────────────────────────────────────────────────────────

def test_sync():
    print("\n--- Synchronous Tests ---")
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    boards = client.boards

    # [1] List boards
    print("\n[1] List boards")
    try:
        res = boards.list(limit=20)
        # Handle both wrapped {data: []} and direct []
        data = res.get("data") if isinstance(res, dict) else res
        ok("list()", f"{len(data) if isinstance(data, list) else '?'} boards")
    except Exception as e: fail("list()", e)

    # [2] Get board
    print("\n[2] Get board")
    try:
        res = boards.list(limit=1)
        data = res.get("data") if isinstance(res, dict) else res
        if data and len(data) > 0:
            b_id = data[0].get("_id") or data[0].get("id")
            b = boards.get(b_id)
            ok("get()", f"id={b.get('_id') or b.get('id')} name={b.get('name')} fields={len(b.get('fields', []))}")
        else:
            skip("get()", "no boards found")
    except Exception as e: fail("get()", e)

    # [3] Create test board
    print("\n[3] Create board")
    try:
        # FIX: SDK expects 'name' as string, not dict
        b = boards.create("SDK Test Board (Py)")
        created["board_id"] = b.get("_id") or b.get("id")
        ok("create()", f"id={created['board_id']}")
    except Exception as e: fail("create()", e)

    # [4] Update board
    print("\n[4] Update board")
    if not created["board_id"]:
        skip("update()", "no board created")
    else:
        try:
            b = boards.update(created["board_id"], {"name": "SDK Test Board Updated (Py)"})
            ok("update()", f"name={b.get('name')}")
        except Exception as e: fail("update()", e)

    # Get auto-created identifier field
    if created["board_id"]:
        try:
            b = boards.get(created["board_id"])
            fields = b.get("fields", [])
            for f in fields:
                if f.get("is_identifier"):
                    created["identifier_field_id"] = f.get("_id") or f.get("id")
                    break
        except Exception: pass

    # [5] Create fields
    print("\n[5] Create fields")
    if not created["board_id"]:
        skip("create_field()", "no board created")
    else:
        try:
            res = boards.create_field(created["board_id"], {"name": "Tags", "type": "ShortText"})
            f = find_field(res, "Tags")
            created["field_id"] = f.get("_id") or f.get("id") if f else None
            ok("create_field() Tags", f"id={created['field_id']}")
        except Exception as e: fail("create_field() Tags", e)

        try:
            res = boards.create_field(created["board_id"], {"name": "Notes", "type": "ShortText"})
            f = find_field(res, "Notes")
            created["field_id2"] = f.get("_id") or f.get("id") if f else None
            ok("create_field() Notes", f"id={created['field_id2']}")
        except Exception as e: fail("create_field() Notes", e)

    # [6] Update field
    print("\n[6] Update field")
    if not created["board_id"] or not created["field_id"]:
        skip("update_field()", "no field created")
    else:
        try:
            boards.update_field(created["board_id"], created["field_id"], {"name": "Tags Updated"})
            ok("update_field()", "Tags → Tags Updated")
        except Exception as e: fail("update_field()", e)

    # [7] Reorder fields
    print("\n[7] Reorder fields")
    if not created["board_id"] or not created["field_id"] or not created["field_id2"] or not created["identifier_field_id"]:
        skip("reorder_fields()", "fields not ready")
    else:
        try:
            boards.reorder_fields(created["board_id"], {
                "fields": [created["identifier_field_id"], created["field_id2"], created["field_id"]],
            })
            ok("reorder_fields()")
        except Exception as e: fail("reorder_fields()", e)

    # [8] Bulk update fields
    print("\n[8] Bulk update fields")
    if not created["board_id"] or not created["field_id"]:
        skip("bulk_update_fields()", "no field created")
    else:
        try:
            boards.bulk_update_fields(created["board_id"], {
                "fields": [{"_id": created["field_id"], "name": "Tags v2", "type": "ShortText", "hidden": False}],
            })
            ok("bulk_update_fields()")
        except Exception as e: fail("bulk_update_fields()", e)

    # [9] Create items
    print("\n[9] Create items")
    if not created["board_id"] or not created["identifier_field_id"]:
        skip("create_item()", "board or identifier field not found")
    else:
        try:
            item = boards.create_item(created["board_id"], {
                "fields": [{"board_field_id": created["identifier_field_id"], "value": "SDK Test Item 1"}]
            })
            created["item_id"] = item.get("_id") or item.get("id")
            ok("create_item() #1", f"id={created['item_id']}")
        except Exception as e: fail("create_item() #1", e)

    # [10] Get item
    print("\n[10] Get item")
    if not created["board_id"] or not created["item_id"]:
        skip("get_item()", "no item created")
    else:
        try:
            item = boards.get_item(created["board_id"], created["item_id"])
            ok("get_item()", f"id={item.get('_id') or item.get('id')}")
        except Exception as e: fail("get_item()", e)

    # [11] Update item
    print("\n[11] Update item")
    if not created["board_id"] or not created["item_id"] or not created["identifier_field_id"]:
        skip("update_item()", "no item created")
    else:
        try:
            item = boards.update_item(created["board_id"], created["item_id"], {
                "data": [{"key": created["identifier_field_id"], "value": "SDK Test Item 1 Updated"}]
            })
            ok("update_item()", f"id={item.get('_id') or item.get('id')}")
        except Exception as e: fail("update_item()", e)

    # [12] List items
    print("\n[12] List items")
    if not created["board_id"]:
        skip("list_items()", "no board created")
    else:
        try:
            res = boards.list_items(created["board_id"], limit=10)
            data = res.get("data") if isinstance(res, dict) else res
            ok("list_items()", f"{len(data) if isinstance(data, list) else '?'} items")
        except Exception as e: fail("list_items()", e)

    # [13] Search items
    print("\n[13] Search items")
    if not created["board_id"]:
        skip("search()", "no board created")
    else:
        try:
            res = boards.search(created["board_id"], q="", limit=5)
            data = res.get("data") if isinstance(res, dict) else res
            ok("search()", f"{len(data) if isinstance(data, list) else '?'} results")
        except Exception as e:
            if "400" in str(e): skip("search()", "meilisearch organization_id issue")
            else: fail("search()", e)

    # [14] Link preview
    print("\n[14] Link preview")
    try:
        res = boards.get_link_preview("https://imbrace.co")
        ok("get_link_preview()", f"title={res.get('title')}")
    except Exception as e: fail("get_link_preview()", e)

    # [15] Cleanup
    print("\n[15] Cleanup")
    if created["board_id"]:
        try: 
            boards.delete(created["board_id"])
            ok("delete() board cleanup")
        except Exception as e: fail("delete() board cleanup", e)

# ─────────────────────────────────────────────────────────────────────────────
# Async
# ─────────────────────────────────────────────────────────────────────────────

async def test_async():
    print("\n--- Asynchronous Tests ---")
    async with AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY) as client:
        boards = client.boards
        try:
            res = await boards.list(limit=1)
            data = res.get("data") if isinstance(res, dict) else res
            ok("async list()", f"count={len(data) if isinstance(data, list) else '?'}")
        except Exception as e: fail("async list()", e)

if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())

    print(f"\n{'─' * 55}")
    print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
