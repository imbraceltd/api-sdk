from utils.utils import client, run_test_section, log_result

def test_activepieces():
    print("\n🚀 Testing Activepieces Resource...")

    state = {"project_id": None}

    # 1. Flows
    def flows_list():
        res = client.activepieces.list_flows(limit=5)
        log_result("Flows", res.get("data", []))
        if res.get("data"):
            state["project_id"] = res["data"][0].get("projectId")
    run_test_section("activepieces.list_flows", flows_list)

    # 2. Runs
    run_test_section("activepieces.list_runs", lambda: log_result("Runs", client.activepieces.list_runs(limit=5).get("data", [])))

    # 3. Folders
    run_test_section("activepieces.list_folders", lambda: log_result("Folders", client.activepieces.list_folders(limit=5).get("data", [])))

    # 4. Connections
    run_test_section("activepieces.list_connections", lambda: log_result("Connections", client.activepieces.list_connections(limit=5).get("data", [])))

    # 5. Tables
    run_test_section("activepieces.list_tables", lambda: log_result("Tables", client.activepieces.list_tables().get("data", [])))

    # 6. Pieces
    run_test_section("activepieces.list_pieces", lambda: log_result("Pieces Count", len(client.activepieces.list_pieces())))

    # 7. MCP Servers
    def mcp_servers():
        if state["project_id"]:
            res = client.activepieces.list_mcp_servers(project_id=state["project_id"])
            log_result("MCP Servers", res)
        else:
            print("   ⚠️ No project_id found, skipping.")
    run_test_section("activepieces.list_mcp_servers", mcp_servers)

    print("\n✅ Activepieces Resource Testing Completed.")

if __name__ == "__main__":
    test_activepieces()
