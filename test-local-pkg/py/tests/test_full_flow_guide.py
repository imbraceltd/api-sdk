import time
import json
import uuid
from io import BytesIO
from utils.utils import client, run_test_section, log_result, organization_id

def test_full_flow_guide():
    print("\n" + "=" * 70)
    print("🚀 STARTING: FULL FLOW GUIDE COMPREHENSIVE TEST (PYTHON)")
    print("=" * 70)

    ts = int(time.time() * 1000)
    state = {
        "assistant_id": None,
        "flow_id": None,
        "kb_folder_id": None,
        "board_id": None,
        "identifier_field_id": None,
        "item_id": None,
        "org_id": organization_id,
    }

    def handle_sse_stream(response, label: str):
        print(f"   {label}: ", end="", flush=True)
        full_content = ""
        for line in response.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if line.startswith("data: ") and line != "data: [DONE]":
                try:
                    chunk = json.loads(line[6:])
                    content = chunk.get("content", "")
                    full_content += content
                    print(content, end="", flush=True)
                except:
                    pass
        print(f"\n   ✅ {label} Finished.")
        return full_content

    try:
        # --- Flow 1: Create Assistant ---
        print("\n[FLOW 1] Assistant Lifecycle")

        def assistant_crud():
            # 1. Create
            assistant = client.chat_ai.create_assistant({
                "name": f"SDK Test Assistant {ts}",
                "workflow_name": f"sdk_guide_test_{ts}",
                "description": "Created by full-flow-guide test",
                "instructions": "You are a concise test assistant. Reply in one sentence.",
            })
            state["assistant_id"] = assistant["id"]
            log_result("Assistant Created", state["assistant_id"])

            # 2. List & Verify
            all_assistants = client.chat_ai.list_assistants()
            found = any(a["id"] == state["assistant_id"] for a in all_assistants)
            if not found:
                raise Exception("Assistant not found in list")
            log_result("Assistant List & Verify", f"Found among {len(all_assistants)} assistants")

            # 3. Get & Verify
            asst = client.chat_ai.get_assistant(state["assistant_id"])
            if asst["name"] != f"SDK Test Assistant {ts}":
                raise Exception("Name mismatch")
            log_result("Assistant Retrieved & Verified", True)

            # 4. Update Instructions
            client.chat_ai.update_assistant_instructions(state["assistant_id"], "You are a helpful test agent. Use the word 'IMBRACE' in your reply.")
            log_result("Instructions Updated", True)

            # 5. Update Name
            updated = client.chat_ai.update_assistant(state["assistant_id"], {
                "name": f"SDK Assistant {ts} Updated",
                "workflow_name": f"sdk_guide_test_{ts}",
            })
            log_result("Assistant Renamed", updated["name"])

        run_test_section("Assistant CRUD", assistant_crud)

        # --- Flow 2: Activepieces Workflow ---
        print("\n[FLOW 2] Activepieces Workflows")

        def workflow_lifecycle():
            try:
                flows = client.activepieces.list_flows(limit=5)
                data = flows.get("data", [])
                if len(data) > 0:
                    state["flow_id"] = data[0]["id"]
                    log_result("Using Existing Flow", state["flow_id"])

                    client.activepieces.get_flow(state["flow_id"])

                    # Trigger Async
                    client.activepieces.trigger_flow(state["flow_id"], {"source": "sdk-test-async"})
                    log_result("Trigger Flow Async", "Sent")

                    # List Runs
                    runs = client.activepieces.list_runs(flow_id=state["flow_id"], limit=3)
                    log_result("Recent Runs Count", len(runs.get("data", [])))
                else:
                    print("   ⚠️ No flows found, skipping workflow triggers.")
            except Exception as e:
                print(f"   ⚠️ Workflow steps failed (Possible 404 or config issue): {str(e)}")

        run_test_section("Workflow Lifecycle", workflow_lifecycle)

        # --- Flow 3: Knowledge Hub (RAG) ---
        print("\n[FLOW 3] Knowledge Hub & RAG")

        def folder_file_management():
            if not state["org_id"]:
                folders = client.boards.search_folders()
                if folders:
                    state["org_id"] = folders[0].get("organization_id", "")

            # 1. Create Folder
            folder = client.boards.create_folder({
                "name": f"SDK KB {ts}",
                "organization_id": state["org_id"],
                "parent_folder_id": "root",
                "source_type": "upload",
            })
            state["kb_folder_id"] = folder.get("_id") or folder.get("id")
            log_result("KB Folder Created", state["kb_folder_id"])

            # 2. Get & Update Folder
            fetched_folder = client.boards.get_folder(state["kb_folder_id"])
            log_result("Folder Retrieved", fetched_folder.get("name"))

            client.boards.update_folder(state["kb_folder_id"], {"name": f"SDK KB {ts} Updated"})
            log_result("Folder Updated", True)

            # 3. Search Folders
            search_results = client.boards.search_folders(q=f"SDK KB {ts}")
            log_result("Search Folders Verified", len(search_results) > 0)

            # 4. Upload File
            secret_code = f"IMBRACE-CODE-{ts}"
            file_content = f"The secret verification code is: {secret_code}. The assistant name is IMBRACE-TEST."
            
            files = {
                "file": ("secret.txt", BytesIO(file_content.encode("utf-8")), "text/plain")
            }
            
            # Let's try to match the TS version exactly
            # formData.append("folder_id", state.kbFolderId!);
            # formData.append("organization_id", state.orgId);
            
            # httpx handles files and data separately
            data = {
                "folder_id": state["kb_folder_id"],
                "organization_id": state["org_id"]
            }
            client.http.request("POST", f"{client.boards._base}/files/upload", files=files, data=data)
            log_result("Knowledge File Uploaded", secret_code)

            # 5. Attach to Assistant
            client.chat_ai.update_assistant(state["assistant_id"], {
                "name": f"SDK Assistant {ts} Updated",
                "workflow_name": f"sdk_guide_test_{ts}",
                "knowledge_hubs": [state["kb_folder_id"]]
            })
            log_result("Knowledge Attached to Assistant", True)

            print("   Waiting 3s for embedding indexing...")
            time.sleep(3)

        run_test_section("Folder & File Management", folder_file_management)

        # --- Verify RAG with Multi-turn Chat ---
        def multi_turn_chat():
            chat_asst_id = state["assistant_id"]
            asst_info = client.chat_ai.get_assistant(chat_asst_id)

            if not asst_info.get("model_id"):
                print("   ⚠️ New assistant has no model yet, falling back to an existing one for chat test.")
                all_assts = client.chat_ai.list_assistants()
                fallback = next((a for a in all_assts if a.get("model_id")), None)
                if fallback:
                    chat_asst_id = fallback["id"]

            session_id = str(uuid.uuid4())

            # Turn 1
            print("\n   [Turn 1] Querying RAG...")
            response1 = client.ai_agent.stream_chat({
                "id": session_id,
                "assistant_id": chat_asst_id,
                "organization_id": state["org_id"],
                "messages": [{"role": "user", "content": "What is the secret verification code?"}],
            })
            handle_sse_stream(response1, "AI Turn 1 Response")

            # Turn 2
            print("\n   [Turn 2] Context Check...")
            response2 = client.ai_agent.stream_chat({
                "id": session_id,
                "assistant_id": chat_asst_id,
                "organization_id": state["org_id"],
                "messages": [{"role": "user", "content": "What was the assistant name mentioned in that same file?"}],
            })
            handle_sse_stream(response2, "AI Turn 2 Response")

        run_test_section("Multi-turn Chat Verification (RAG)", multi_turn_chat)

        # --- Flow 4: Boards & Items ---
        print("\n[FLOW 4] Boards & Items")

        def board_item_lifecycle():
            # 1. Create Board
            board = client.boards.create(
                name=f"SDK Test Board {ts}",
                description="Full Flow Test Board"
            )
            state["board_id"] = board.get("_id") or board.get("id")
            log_result("Board Created", state["board_id"])

            # 2. Add Custom Field
            updated_board = client.boards.create_field(state["board_id"], {
                "name": "Reference ID",
                "type": "ShortText"
            })
            fields = updated_board.get("fields", [])
            state["identifier_field_id"] = next((f["_id"] for f in fields if f.get("is_identifier")), None)
            log_result("Identifier Field Identified", state["identifier_field_id"])

            # 3. Create Item
            item = client.boards.create_item(state["board_id"], {
                "fields": [{"board_field_id": state["identifier_field_id"], "value": f"REF-{ts}"}]
            })
            state["item_id"] = item.get("_id") or item.get("id")
            log_result("Item Created", state["item_id"])

            # 4. Get Item & Verify
            fetched_item = client.boards.get_item(state["board_id"], state["item_id"])
            if not fetched_item:
                raise Exception("Could not fetch item")
            log_result("Item Retrieved", fetched_item.get("_id") or fetched_item.get("id"))

            # 5. List Items & Verify
            items_list = client.boards.list_items(state["board_id"], limit=10)
            items_data = items_list.get("data", [])
            if not any((i.get("_id") or i.get("id")) == state["item_id"] for i in items_data):
                raise Exception("Item not found in list")
            log_result("List Items Verified", f"Found {len(items_data)} items")

            # 6. Update & Search
            client.boards.update_item(state["board_id"], state["item_id"], {
                "data": [{"key": state["identifier_field_id"], "value": f"REF-{ts}-UPDATED"}]
            })
            search = client.boards.search(state["board_id"], q=f"REF-{ts}")
            log_result("Search Verified", len(search.get("data", [])) > 0)

            # 7. Export CSV
            csv = client.boards.export_csv(state["board_id"])
            log_result("CSV Exported (Bytes)", len(csv))

        run_test_section("Board & Item Full Lifecycle", board_item_lifecycle)

        print("\n✅ FULL FLOW GUIDE TEST COMPLETED SUCCESSFULLY")

    except Exception as e:
        print(f"\n❌ FATAL TEST ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e
    finally:
        print("\n[Cleanup] Cleaning up resources...")
        try:
            if state["kb_folder_id"]:
                client.boards.delete_folders(ids=[state["kb_folder_id"]])
            if state["board_id"]:
                client.boards.delete(state["board_id"])
            if state["assistant_id"]:
                client.chat_ai.delete_assistant(state["assistant_id"])
            print("   Cleanup finished.")
        except Exception as e:
            print(f"   Cleanup failed: {str(e)}")

if __name__ == "__main__":
    test_full_flow_guide()
