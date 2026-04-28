import time
import uuid
from utils.utils import client, run_test_section, log_result, organization_id

def test_multi_agent():
    print("\n🚀 STARTING: MULTI-AGENT & SUB-AGENTS TEST (PY)")

    state = {"assistant_id": None, "chat_id": None, "session_id": str(uuid.uuid4())}

    # 1. Preparation
    def preparation():
        assistants = client.chat_ai.list_assistants()
        if assistants:
            state["assistant_id"] = assistants[0]["id"]
        else:
            ts = int(time.time())
            asst = client.chat_ai.create_assistant({
                "name": f"SDK Sub-Agent Test {ts}",
                "workflow_name": f"sub_agent_test_{ts}"
            })
            state["assistant_id"] = asst["id"]
        log_result("Using Assistant", state["assistant_id"])
    run_test_section("Preparation", preparation)

    # 2. Sub-Agent Chat
    def sub_agent_chat():
        # Create a client chat first
        user = client.ai_agent.get_chat_client_user({"id": f"sdk-py-user-{int(time.time())}"})
        client_chat = client.ai_agent.create_client_chat({
            "id": str(uuid.uuid4()),
            "assistantId": state["assistant_id"],
            "organizationId": organization_id,
            "userId": user["id"],
            "message": {
                "id": str(uuid.uuid4()),
                "role": "user",
                "parts": [{"type": "text", "text": "Hello Sub-agent"}]
            }
        })
        state["chat_id"] = client_chat.get("_id") or client_chat.get("id")
        log_result("Chat Created for Sub-agent", state["chat_id"])

        if state["chat_id"]:
            try:
                res = client.ai_agent.stream_sub_agent_chat({
                    "assistant_id": state["assistant_id"],
                    "organization_id": organization_id,
                    "session_id": state["session_id"],
                    "chat_id": state["chat_id"],
                    "messages": [{"role": "user", "content": "Tell me about yourself"}]
                })
                if res.status_code == 200:
                    log_result("Sub-agent Chat Stream", "Started (200 OK)")
            except Exception as e:
                print(f"   ⚠️ Sub-agent chat stream failed: {str(e)}")

            try:
                history = client.ai_agent.get_sub_agent_history(
                    session_id=state["session_id"],
                    chat_id=state["chat_id"]
                )
                log_result("Sub-agent History", len(history.get("messages", [])))
            except Exception as e:
                print(f"   ⚠️ Sub-agent history failed: {str(e)}")
            
            # Cleanup
            client.ai_agent.delete_client_chat(state["chat_id"])
    run_test_section("Sub-Agent Chat", sub_agent_chat)

    print("\n✅ Multi-Agent Test Completed.")

if __name__ == "__main__":
    test_multi_agent()
