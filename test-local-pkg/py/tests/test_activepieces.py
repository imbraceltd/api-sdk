import time
import uuid
from utils.utils import client, run_test_section, log_result

def test_activepieces():
    print("\n🚀 Testing Activepieces Resource...")

    state = {"project_id": None, "flow_id": None, "folder_id": None, "run_id": None}

    # 1. List Flows + capture projectId
    def flows_list():
        res = client.activepieces.list_flows(limit=5)
        data = res.get("data", [])
        log_result("list_flows", len(data))
        if data:
            state["project_id"] = data[0].get("projectId")
    run_test_section("activepieces.list_flows", flows_list)

    # 2. Create Flow (Nhóm B — cần project_id thực)
    def create_flow():
        if state["project_id"]:
            try:
                ts = int(time.time())
                new_flow = client.activepieces.create_flow({
                    "displayName": f"SDK Test Flow {ts}",
                    "projectId": state["project_id"]
                })
                state["flow_id"] = new_flow.get("id") or new_flow.get("_id")
                log_result("create_flow", state["flow_id"])
            except Exception as e:
                print(f"   ⚠️ create_flow failed: {str(e)}")
        else:
            print("   ⚠️ No project_id — skipping create_flow")
    run_test_section("activepieces.create_flow", create_flow)

    # 3. Get Flow
    def get_flow():
        fid = state["flow_id"]
        if fid:
            try:
                flow = client.activepieces.get_flow(fid)
                log_result("get_flow", flow.get("id"))
            except Exception as e:
                print(f"   ⚠️ get_flow failed: {str(e)}")
        else:
            print("   [skip] get_flow — no flow_id")
    run_test_section("activepieces.get_flow", get_flow)

    # 4. Trigger Flow Async
    def trigger_flow_async():
        fid = state["flow_id"]
        if fid:
            try:
                client.activepieces.trigger_flow(fid, {"source": "sdk-test"})
                log_result("trigger_flow (async)", "Sent")
            except Exception as e:
                print(f"   ⚠️ trigger_flow failed: {str(e)}")
        else:
            print("   [skip] trigger_flow — no flow_id")
    run_test_section("activepieces.trigger_flow", trigger_flow_async)

    # 5. Trigger Flow Sync (Nhóm B)
    def trigger_flow_sync():
        fid = state["flow_id"]
        if fid:
            try:
                res = client.activepieces.trigger_flow_sync(fid, {"source": "sdk-test-sync"})
                log_result("trigger_flow_sync", res)
            except Exception as e:
                print(f"   ⚠️ trigger_flow_sync failed: {str(e)}")
        else:
            print("   [skip] trigger_flow_sync — no flow_id")
    run_test_section("activepieces.trigger_flow_sync", trigger_flow_sync)

    # 6. List Runs + get_run
    def runs_ops():
        res = client.activepieces.list_runs(limit=5)
        data = res.get("data", [])
        log_result("list_runs", len(data))
        if data:
            state["run_id"] = data[0].get("id") or data[0].get("_id")

        if state["run_id"]:
            try:
                run = client.activepieces.get_run(state["run_id"])
                log_result("get_run", run.get("id"))
            except Exception as e:
                print(f"   ⚠️ get_run failed: {str(e)}")
    run_test_section("activepieces.runs_ops", runs_ops)

    # 7. Delete Flow (cleanup)
    def delete_flow():
        fid = state["flow_id"]
        if fid:
            try:
                client.activepieces.delete_flow(fid)
                log_result("delete_flow", True)
                state["flow_id"] = None
            except Exception as e:
                print(f"   ⚠️ delete_flow failed: {str(e)}")
        else:
            print("   [skip] delete_flow — no flow_id")
    run_test_section("activepieces.delete_flow", delete_flow)

    # 8. Folders + create_folder
    def folder_ops():
        res = client.activepieces.list_folders(limit=5)
        data = res.get("data", [])
        log_result("list_folders", len(data))

        if state["project_id"]:
            try:
                ts = int(time.time())
                new_folder = client.activepieces.create_folder({
                    "displayName": f"SDK Folder {ts}",
                    "projectId": state["project_id"]
                })
                state["folder_id"] = new_folder.get("id") or new_folder.get("_id")
                log_result("create_folder", state["folder_id"])
            except Exception as e:
                print(f"   ⚠️ create_folder failed: {str(e)}")
        else:
            print("   [skip] create_folder — no project_id")
    run_test_section("activepieces.folder_ops", folder_ops)

    # 9. Connections
    run_test_section("activepieces.list_connections", lambda: log_result("Connections", client.activepieces.list_connections(limit=5).get("data", [])))

    # 10. upsert_connection (Nhóm B — cần connection config thực)
    def upsert_connection():
        try:
            # Gửi với dummy data để xác nhận endpoint tồn tại
            client.activepieces.upsert_connection({
                "name": f"sdk-test-conn-{int(time.time())}",
                "type": "APP_CONNECTION",
                "projectIds": [state["project_id"] or "dummy"],
                "value": {"type": "NO_AUTH"}
            })
            log_result("upsert_connection", True)
        except Exception as e:
            print(f"   ⚠️ upsert_connection failed (expected with dummy data): {str(e)}")
    run_test_section("activepieces.upsert_connection", upsert_connection)

    # 11. Tables
    run_test_section("activepieces.list_tables", lambda: log_result("Tables", client.activepieces.list_tables().get("data", [])))

    # 12. Pieces
    run_test_section("activepieces.list_pieces", lambda: log_result("Pieces Count", len(client.activepieces.list_pieces())))

    # 13. MCP Servers
    def mcp_servers():
        if state["project_id"]:
            try:
                res = client.activepieces.list_mcp_servers(project_id=state["project_id"])
                log_result("MCP Servers", res)
            except Exception as e:
                print(f"   ⚠️ list_mcp_servers failed: {str(e)}")
        else:
            print("   ⚠️ No project_id found, skipping.")
    run_test_section("activepieces.list_mcp_servers", mcp_servers)

    print("\n✅ Activepieces Resource Testing Completed.")

if __name__ == "__main__":
    test_activepieces()
