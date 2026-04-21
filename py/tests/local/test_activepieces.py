"""
Full ActivePieces resource test — sync + async, runs against prodv2 gateway.
Usage:
    pip install -e ".[dev]"
    python tests/local/test_activepieces.py
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
created = {"flow_id": None, "folder_id": None}


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


# ── Sync Tests ────────────────────────────────────────────────────────────────

def test_sync():
    global created
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    ap = client.activepieces

    print("\n[1] Flows (sync)")
    try:
        res = ap.list_flows(limit=3)
        ok("list_flows()", f"{len(res['data'])} flows")
        if res["data"]:
            flow = ap.get_flow(res["data"][0]["id"])
            ok("get_flow()", f"id={flow['id']} status={flow['status']}")
            project_id = res["data"][0]["projectId"]
        else:
            skip("get_flow()", "no flows")
            project_id = None
    except Exception as e:
        fail("Flows", e)
        project_id = None

    print("\n[2] Create Flow (sync)")
    try:
        if not project_id:
            skip("create_flow()", "no projectId")
        else:
            flow = ap.create_flow("SDK Python Test Flow", project_id)
            created["flow_id"] = flow["id"]
            ok("create_flow()", f"id={flow['id']}")
    except Exception as e:
        fail("create_flow()", e)

    print("\n[3] Trigger Flow (sync)")
    try:
        flows = ap.list_flows(limit=3)
        enabled = next((f for f in flows["data"] if f["status"] == "ENABLED"), None)
        if not enabled:
            skip("trigger_flow()", "no ENABLED flow")
        else:
            res = ap.trigger_flow(enabled["id"], {"test": True, "source": "sdk-python-test"})
            ok("trigger_flow()", str(res)[:60])
    except Exception as e:
        fail("trigger_flow()", e)

    print("\n[4] Flow Runs (sync)")
    try:
        res = ap.list_runs(limit=3)
        ok("list_runs()", f"{len(res['data'])} runs")
        if res["data"]:
            run = ap.get_run(res["data"][0]["id"])
            ok("get_run()", f"id={run['id']} status={run['status']}")
        else:
            skip("get_run()", "no runs")
    except Exception as e:
        fail("Flow Runs", e)

    print("\n[5] Folders (sync)")
    try:
        if not project_id:
            skip("Folders", "no projectId")
        else:
            res = ap.list_folders(limit=3)
            ok("list_folders()", f"{len(res['data'])} folders")

            folder = ap.create_folder("SDK Python Test Folder", project_id)
            created["folder_id"] = folder["id"]
            ok("create_folder()", f"id={folder['id']}")

            updated = ap.update_folder(folder["id"], "SDK Python Test Folder Updated")
            ok("update_folder()", f"name={updated['displayName']}")

            fetched = ap.get_folder(folder["id"])
            ok("get_folder()", f"id={fetched['id']}")
    except Exception as e:
        fail("Folders", e)

    print("\n[6] App Connections (sync)")
    try:
        res = ap.list_connections(limit=3)
        ok("list_connections()", f"{len(res['data'])} connections")
        if res["data"]:
            conn = ap.get_connection(res["data"][0]["id"])
            ok("get_connection()", f"id={conn['id']}")
        else:
            skip("get_connection()", "no connections")
    except Exception as e:
        fail("App Connections", e)

    print("\n[7] Pieces (sync)")
    try:
        res = ap.list_pieces(limit=5)
        ok("list_pieces()", f"{len(res)} pieces, first={res[0]['displayName'] if res else 'n/a'}")
    except Exception as e:
        fail("list_pieces()", e)

    print("\n[8] Triggers (sync)")
    try:
        res = ap.get_trigger_run_status()
        ok("get_trigger_run_status()", f"{len(res.get('pieces', {}))} pieces tracked")
    except Exception as e:
        fail("get_trigger_run_status()", e)

    print("\n[9] Tables & Records (sync)")
    try:
        tables = ap.list_tables(limit=3)
        ok("list_tables()", f"{len(tables['data'])} tables")
        if tables["data"]:
            table = ap.get_table(tables["data"][0]["id"])
            ok("get_table()", f"id={table['id']}")
            records = ap.list_records(table["id"], limit=3)
            ok("list_records()", f"{len(records['data'])} records")
        else:
            skip("get_table() / list_records()", "no tables")
    except Exception as e:
        fail("Tables & Records", e)

    print("\n[10] MCP Servers (sync)")
    try:
        if not project_id:
            skip("MCP Servers", "no projectId")
        else:
            res = ap.list_mcp_servers(project_id)
            ok("list_mcp_servers()", f"{len(res['data'])} MCP servers")
            if res["data"]:
                server = ap.get_mcp_server(res["data"][0]["id"])
                ok("get_mcp_server()", f"id={server['id']}")
            else:
                skip("get_mcp_server()", "no MCP servers")
    except Exception as e:
        fail("MCP Servers", e)

    print("\n[11] User Invitations (sync)")
    try:
        res = ap.list_invitations(type="PLATFORM", limit=3)
        ok("list_invitations(PLATFORM)", f"{len(res['data'])} invitations")
    except Exception as e:
        fail("list_invitations(PLATFORM)", e)
    try:
        res = ap.list_invitations(type="PROJECT", limit=3)
        ok("list_invitations(PROJECT)", f"{len(res['data'])} invitations")
    except Exception as e:
        fail("list_invitations(PROJECT)", e)

    print("\n[12] Cleanup (sync)")
    if created["folder_id"]:
        try:
            ap.delete_folder(created["folder_id"])
            ok(f"delete_folder({created['folder_id']})")
        except Exception as e:
            fail("delete_folder()", e)
    if created["flow_id"]:
        try:
            ap.delete_flow(created["flow_id"])
            ok(f"delete_flow({created['flow_id']})")
        except Exception as e:
            fail("delete_flow()", e)


# ── Async Tests ───────────────────────────────────────────────────────────────

async def test_async():
    created_async = {"flow_id": None, "folder_id": None}
    client = AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    ap = client.activepieces

    print("\n[13] Flows (async)")
    try:
        res = await ap.list_flows(limit=2)
        ok("async list_flows()", f"{len(res['data'])} flows")
        project_id = res["data"][0]["projectId"] if res["data"] else None
    except Exception as e:
        fail("async Flows", e)
        project_id = None

    print("\n[14] Create + Delete Flow (async)")
    try:
        if not project_id:
            skip("async create_flow()", "no projectId")
        else:
            flow = await ap.create_flow("SDK Python Async Test Flow", project_id)
            created_async["flow_id"] = flow["id"]
            ok("async create_flow()", f"id={flow['id']}")
    except Exception as e:
        fail("async create_flow()", e)

    print("\n[15] Folders (async)")
    try:
        if not project_id:
            skip("async Folders", "no projectId")
        else:
            res = await ap.list_folders(limit=2)
            ok("async list_folders()", f"{len(res['data'])} folders")

            folder = await ap.create_folder("SDK Python Async Folder", project_id)
            created_async["folder_id"] = folder["id"]
            ok("async create_folder()", f"id={folder['id']}")
    except Exception as e:
        fail("async Folders", e)

    print("\n[16] Runs + Pieces + Triggers (async)")
    try:
        runs = await ap.list_runs(limit=2)
        ok("async list_runs()", f"{len(runs['data'])} runs")
        pieces = await ap.list_pieces(limit=3)
        ok("async list_pieces()", f"{len(pieces)} pieces")
        status = await ap.get_trigger_run_status()
        ok("async get_trigger_run_status()", f"{len(status.get('pieces', {}))} pieces")
    except Exception as e:
        fail("async Runs/Pieces/Triggers", e)

    print("\n[17] Async Cleanup")
    if created_async["folder_id"]:
        try:
            await ap.delete_folder(created_async["folder_id"])
            ok(f"async delete_folder({created_async['folder_id']})")
        except Exception as e:
            fail("async delete_folder()", e)
    if created_async["flow_id"]:
        try:
            await ap.delete_flow(created_async["flow_id"])
            ok(f"async delete_flow({created_async['flow_id']})")
        except Exception as e:
            fail("async delete_flow()", e)

    await client.close()


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())

    print(f"\n{'─' * 55}")
    print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
