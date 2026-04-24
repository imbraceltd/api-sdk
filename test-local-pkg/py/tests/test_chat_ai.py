import time
from utils.utils import client, run_test_section, log_result, organization_id

def test_chat_ai():
    print("\n🚀 Testing Chat AI Resource...")

    state = {"assistant_id": None, "folder_id": None}

    # 1. Assistants
    def assistant_ops():
        list_res = client.chat_ai.list_assistants()
        log_result("Assistants", list_res)
        
        created = client.chat_ai.create_assistant({
            "name": f"SDK_PY_TEST_{int(time.time())}",
            "workflow_name": f"sdk_py_test_{int(time.time())}",
            "description": "Temp assistant",
        })
        state["assistant_id"] = created["id"]
        log_result("Created Assistant", state["assistant_id"])

        fetched = client.chat_ai.get_assistant(state["assistant_id"])
        log_result("Fetched Assistant", fetched)

        updated = client.chat_ai.update_assistant(state["assistant_id"], {
            "name": f"SDK_PY_TEST_UPDATED_{int(time.time())}",
            "workflow_name": f"sdk_py_test_{int(time.time())}",
        })
        log_result("Updated Assistant", updated)

        client.chat_ai.update_assistant_instructions(state["assistant_id"], "New instructions")
        log_result("Updated Instructions", True)

    run_test_section("Assistant CRUD", assistant_ops)

    # 2. Chat Sessions
    def chat_sessions():
        chats = client.chat_ai.list_chats()
        log_result("Chats Count", len(chats))

        new_chat = client.chat_ai.create_chat({"title": f"SDK Test Chat {int(time.time())}"})
        chat_id = new_chat.get("id") or new_chat.get("_id")
        log_result("Created Chat", chat_id)

        if chat_id:
            msgs = client.chat_ai.list_messages(chat_id)
            log_result("Messages Count", len(msgs))

            client.chat_ai.delete_chat(chat_id)
            log_result("Deleted Chat", True)
    run_test_section("Chat Sessions", chat_sessions)

    # 3. Models
    run_test_section("chat_ai.list_models", lambda: log_result("Models", client.chat_ai.list_models()))

    # 4. Completions
    def chat_completion():
        res = client.chat_ai.chat({
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": "Hello, say 'py-ready' if you hear me."}]
        })
        log_result("Chat Response", res["choices"][0]["message"]["content"])
    run_test_section("chat_ai.chat", chat_completion)

    # 5. Folders & Knowledge Hubs
    def folder_ops():
        list_res = client.chat_ai.list_folders()
        log_result("Folders", list_res)

        kb_hubs = client.chat_ai.list_knowledge_hubs()
        log_result("Knowledge Hubs", len(kb_hubs))

        created = client.chat_ai.create_folder(f"TEST_PY_FOLDER_{int(time.time())}")
        state["folder_id"] = created.get("id") or created.get("_id")
        log_result("Created Folder", state["folder_id"])
    run_test_section("Folder & KB Ops", folder_ops)

    # Cleanup
    def cleanup():
        if state["folder_id"]:
            client.chat_ai.delete_folder(state["folder_id"])
            print("   Folder deleted.")
        if state["assistant_id"]:
            client.chat_ai.delete_assistant(state["assistant_id"])
            print("   Assistant deleted.")
    run_test_section("Cleanup", cleanup)

    # 6. Prompts & Tools
    run_test_section("chat_ai.list_prompts", lambda: log_result("Prompts", client.chat_ai.list_prompts()))
    run_test_section("chat_ai.list_tools", lambda: log_result("Tools", client.chat_ai.list_tools()))

    # 7. Document AI
    run_test_section("chat_ai.list_document_models", lambda: log_result("Document Models", client.chat_ai.list_document_models()))
    def test_process_doc():
        try:
            res = client.chat_ai.process_document(
                model_name="gpt-4o",
                url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                organization_id=organization_id or "dummy_org"
            )
            log_result("Process Document", res)
        except Exception as e:
            print(f"   ⚠️ process_document failed: {str(e)}")
    run_test_section("chat_ai.process_document", test_process_doc)

    print("\n✅ Chat AI Resource Testing Completed.")

if __name__ == "__main__":
    test_chat_ai()
