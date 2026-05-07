"""
Workflows resource test — sync + async, runs against prodv2 gateway.

Covers:
  - Channel automation (v2/backend/workflows/channel_automation)
  - Flow engine (formerly client.activepieces — flows, runs, folders,
    connections, pieces, tables, MCP servers, invitations).

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
created = {"flow_id": None, "folder_id": None}


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


# ── Sync Tests ────────────────────────────────────────────────────────────────

def test_sync():
    global created
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    w = client.workflows

    print("\n[1] Channel automations (sync)")
    try:
        res = w.list_channel_automation()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("list_channel_automation()", f"{len(lst)} automations")
    except Exception as e:
        fail("list_channel_automation()", e)

    try:
        res = w.list_channel_automation(channel_type="whatsapp")
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("list_channel_automation(whatsapp)", f"{len(lst)} automations")
    except Exception as e:
        fail("list_channel_automation(whatsapp)", e)

    print("\n[2] Flows (sync)")
    project_id = None
    try:
        res = w.list_flows(limit=3)
        ok("list_flows()", f"{len(res['data'])} flows")
        if res["data"]:
            flow = w.get_flow(res["data"][0]["id"])
            ok("get_flow()", f"id={flow['id']} status={flow['status']}")
            project_id = res["data"][0]["projectId"]
        else:
            skip("get_flow()", "no flows")
    except Exception as e:
        fail("Flows", e)

    print("\n[3] Create Flow (sync)")
    try:
        if not project_id:
            skip("create_flow()", "no projectId")
        else:
            flow = w.create_flow("SDK Python Test Flow", project_id)
            created["flow_id"] = flow["id"]
            ok("create_flow()", f"id={flow['id']}")
    except Exception as e:
        fail("create_flow()", e)

    print("\n[4] Trigger Flow (sync)")
    try:
        flows = w.list_flows(limit=3)
        enabled = next((f for f in flows["data"] if f["status"] == "ENABLED"), None)
        if not enabled:
            skip("trigger_flow()", "no ENABLED flow")
        else:
            res = w.trigger_flow(enabled["id"], {"test": True, "source": "sdk-python-test"})
            ok("trigger_flow()", str(res)[:60])
    except Exception as e:
        fail("trigger_flow()", e)

    print("\n[5] Flow Runs (sync)")
    try:
        res = w.list_runs(limit=3)
        ok("list_runs()", f"{len(res['data'])} runs")
        if res["data"]:
            run = w.get_run(res["data"][0]["id"])
            ok("get_run()", f"id={run['id']} status={run['status']}")
        else:
            skip("get_run()", "no runs")
    except Exception as e:
        fail("Flow Runs", e)

    print("\n[6] Folders (sync)")
    try:
        if not project_id:
            skip("Folders", "no projectId")
        else:
            res = w.list_folders(limit=3)
            ok("list_folders()", f"{len(res['data'])} folders")

            folder = w.create_folder("SDK Python Test Folder", project_id)
            created["folder_id"] = folder["id"]
            ok("create_folder()", f"id={folder['id']}")

            updated = w.update_folder(folder["id"], "SDK Python Test Folder Updated")
            ok("update_folder()", f"name={updated['displayName']}")

            fetched = w.get_folder(folder["id"])
            ok("get_folder()", f"id={fetched['id']}")
    except Exception as e:
        fail("Folders", e)

    print("\n[7] App Connections (sync)")
    try:
        res = w.list_connections(limit=3)
        ok("list_connections()", f"{len(res['data'])} connections")
        if res["data"]:
            conn = w.get_connection(res["data"][0]["id"])
            ok("get_connection()", f"id={conn['id']}")
        else:
            skip("get_connection()", "no connections")
    except Exception as e:
        fail("App Connections", e)

    print("\n[8] Pieces (sync)")
    try:
        res = w.list_pieces(limit=5)
        ok("list_pieces()", f"{len(res)} pieces, first={res[0]['displayName'] if res else 'n/a'}")
    except Exception as e:
        fail("list_pieces()", e)

    print("\n[9] Triggers (sync)")
    try:
        res = w.get_trigger_run_status()
        ok("get_trigger_run_status()", f"{len(res.get('pieces', {}))} pieces tracked")
    except Exception as e:
        fail("get_trigger_run_status()", e)

    print("\n[10] Tables & Records (sync)")
    try:
        tables = w.list_tables(limit=3)
        ok("list_tables()", f"{len(tables['data'])} tables")
        if tables["data"]:
            table = w.get_table(tables["data"][0]["id"])
            ok("get_table()", f"id={table['id']}")
            records = w.list_records(table["id"], limit=3)
            ok("list_records()", f"{len(records['data'])} records")
        else:
            skip("get_table() / list_records()", "no tables")
    except Exception as e:
        fail("Tables & Records", e)

    print("\n[11] MCP Servers (sync)")
    try:
        if not project_id:
            skip("MCP Servers", "no projectId")
        else:
            res = w.list_mcp_servers(project_id)
            ok("list_mcp_servers()", f"{len(res['data'])} MCP servers")
            if res["data"]:
                server = w.get_mcp_server(res["data"][0]["id"])
                ok("get_mcp_server()", f"id={server['id']}")
            else:
                skip("get_mcp_server()", "no MCP servers")
    except Exception as e:
        fail("MCP Servers", e)

    print("\n[12] User Invitations (sync)")
    try:
        res = w.list_invitations(type="PLATFORM", limit=3)
        ok("list_invitations(PLATFORM)", f"{len(res['data'])} invitations")
    except Exception as e:
        fail("list_invitations(PLATFORM)", e)
    try:
        res = w.list_invitations(type="PROJECT", limit=3)
        ok("list_invitations(PROJECT)", f"{len(res['data'])} invitations")
    except Exception as e:
        fail("list_invitations(PROJECT)", e)

    print("\n[13] Cleanup (sync)")
    if created["folder_id"]:
        try:
            w.delete_folder(created["folder_id"])
            ok(f"delete_folder({created['folder_id']})")
        except Exception as e:
            fail("delete_folder()", e)
    if created["flow_id"]:
        try:
            w.delete_flow(created["flow_id"])
            ok(f"delete_flow({created['flow_id']})")
        except Exception as e:
            fail("delete_flow()", e)


# ── Async Tests ───────────────────────────────────────────────────────────────

async def test_async():
    created_async = {"flow_id": None, "folder_id": None}
    client = AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    w = client.workflows

    print("\n[14] Channel automations (async)")
    try:
        res = await w.list_channel_automation()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("async list_channel_automation()", f"{len(lst)} automations")
    except Exception as e:
        fail("async list_channel_automation()", e)

    print("\n[15] Flows (async)")
    project_id = None
    try:
        res = await w.list_flows(limit=2)
        ok("async list_flows()", f"{len(res['data'])} flows")
        project_id = res["data"][0]["projectId"] if res["data"] else None
    except Exception as e:
        fail("async Flows", e)

    print("\n[16] Create + Delete Flow (async)")
    try:
        if not project_id:
            skip("async create_flow()", "no projectId")
        else:
            flow = await w.create_flow("SDK Python Async Test Flow", project_id)
            created_async["flow_id"] = flow["id"]
            ok("async create_flow()", f"id={flow['id']}")
    except Exception as e:
        fail("async create_flow()", e)

    print("\n[17] Folders (async)")
    try:
        if not project_id:
            skip("async Folders", "no projectId")
        else:
            res = await w.list_folders(limit=2)
            ok("async list_folders()", f"{len(res['data'])} folders")

            folder = await w.create_folder("SDK Python Async Folder", project_id)
            created_async["folder_id"] = folder["id"]
            ok("async create_folder()", f"id={folder['id']}")
    except Exception as e:
        fail("async Folders", e)

    print("\n[18] Runs + Pieces + Triggers (async)")
    try:
        runs = await w.list_runs(limit=2)
        ok("async list_runs()", f"{len(runs['data'])} runs")
        pieces = await w.list_pieces(limit=3)
        ok("async list_pieces()", f"{len(pieces)} pieces")
        status = await w.get_trigger_run_status()
        ok("async get_trigger_run_status()", f"{len(status.get('pieces', {}))} pieces")
    except Exception as e:
        fail("async Runs/Pieces/Triggers", e)

    print("\n[19] Async Cleanup")
    if created_async["folder_id"]:
        try:
            await w.delete_folder(created_async["folder_id"])
            ok(f"async delete_folder({created_async['folder_id']})")
        except Exception as e:
            fail("async delete_folder()", e)
    if created_async["flow_id"]:
        try:
            await w.delete_flow(created_async["flow_id"])
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
