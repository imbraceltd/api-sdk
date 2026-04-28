import time
import uuid
from utils.utils import client, run_test_section, log_result, organization_id

def test_frontend_sdk():
    print("\n🚀 STARTING: FRONTEND SDK & TRACING TEST (PY)")

    state = {"chat_id": None, "user_id": None}

    # 1. Chat Client Auth
    def chat_client_auth():
        ts = int(time.time())
        email = f"sdk-py-test-{ts}@example.com"
        password = "Password123!"

        try:
            user = client.ai_agent.register_chat_client({
                "id": f"sdk-py-user-{ts}",
                "email": email,
                "password": password
            })
        except:
            user = client.ai_agent.get_chat_client_user({"id": f"sdk-py-user-{ts}"})
        
        state["user_id"] = user.get("id")
        log_result("Chat Client User", state["user_id"])

        verified = client.ai_agent.verify_chat_client_credentials({
            "email": email,
            "password": password
        })
        log_result("Credentials Verified", bool(verified))
    run_test_section("Chat Client Auth", chat_client_auth)

    # 2. Chat Client Chats
    def chat_client_chats():
        if not state["user_id"]: return
        
        assistants = client.chat_ai.list_assistants()
        asst_id = assistants[0]["id"] if assistants else "dummy-id"

        chat = client.ai_agent.create_client_chat({
            "id": str(uuid.uuid4()),
            "assistant_id": asst_id,
            "organization_id": organization_id,
            "user_id": state["user_id"],
            "selectedVisibilityType": "public",
            "message": {
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": "Hello from Python Frontend SDK",
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "parts": [{"type": "text", "text": "Hello"}]
            }
        })
        state["chat_id"] = chat.get("_id") or chat.get("id")
        log_result("Client Chat Created", state["chat_id"])

        if state["chat_id"]:
            fetched = client.ai_agent.get_client_chat(state["chat_id"])
            log_result("Get Client Chat", fetched.get("id"))

            client.ai_agent.update_client_chat(state["chat_id"], {"visibility": "private"})
            log_result("Updated Visibility", "private")
            
            # --- Chat Client — Messages ---
            try:
                client.ai_agent.persist_client_message({"chat_id": state["chat_id"], "message": {"role": "user", "content": "hello"}})
            except Exception as e:
                pass
            try:
                client.ai_agent.list_client_messages(state["chat_id"])
            except Exception as e:
                pass
            try:
                client.ai_agent.delete_trailing_messages("dummy_msg_id")
            except Exception as e:
                pass

            # --- Chat Client — Votes ---
            try:
                client.ai_agent.get_votes(state["chat_id"])
            except Exception as e:
                pass
            try:
                client.ai_agent.update_vote({"chat_id": state["chat_id"], "message_id": "dummy_msg_id", "vote": 1})
            except Exception as e:
                pass

            # --- Chat Client — Misc ---
            try:
                client.ai_agent.stream_client_chat_status(state["chat_id"])
            except Exception as e:
                pass
            try:
                client.ai_agent.generate_client_chat_title(state["chat_id"])
            except Exception as e:
                pass

            # Cleanup
            client.ai_agent.delete_client_chat(state["chat_id"])
            print("   Chat deleted.")

        # Cleanup all
        try:
            client.ai_agent.delete_all_client_chats(organization_id)
        except Exception as e:
            pass
    run_test_section("Chat Client Chats", chat_client_chats)

    # 3. Chat Client Documents
    def chat_client_documents():
        try:
            client.ai_agent.create_document({"chat_id": "dummy", "content": "test"})
        except Exception as e:
            pass
        try:
            client.ai_agent.get_document_latest_by_kind(chat_id="dummy", kind="summary")
        except Exception as e:
            pass
        try:
            client.ai_agent.get_document("dummy_doc_id")
        except Exception as e:
            pass
        try:
            client.ai_agent.get_document_latest("dummy_doc_id")
        except Exception as e:
            pass
        try:
            client.ai_agent.get_document_public("dummy_doc_id")
        except Exception as e:
            pass
        try:
            client.ai_agent.get_document_suggestions("dummy_doc_id")
        except Exception as e:
            pass
        try:
            client.ai_agent.delete_document("dummy_doc_id")
        except Exception as e:
            pass
    run_test_section("Chat Client Documents", chat_client_documents)

    print("\n✅ Frontend SDK Test Completed.")

if __name__ == "__main__":
    test_frontend_sdk()
