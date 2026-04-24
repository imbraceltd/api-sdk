import time
import uuid
from utils.utils import client, run_test_section, log_result, organization_id

def test_ai_agent():
    print("\n🚀 Testing AI Agent Resource...")

    # 1. System
    run_test_section("ai_agent.get_health", lambda: log_result("Health", client.ai_agent.get_health(detailed=True)))
    run_test_section("ai_agent.get_config", lambda: log_result("Config", client.ai_agent.get_config()))
    run_test_section("ai_agent.get_version", lambda: log_result("Version", client.ai_agent.get_version()))

    # 2. Chat v1
    def chat_v1_ops():
        try:
            res = client.ai_agent.list_chats(organization_id=organization_id, limit=5)
            log_result("Chats List", len(res.get("data", [])) if isinstance(res, dict) else len(res))
        except Exception as e:
            print(f"   ⚠️ list_chats failed: {str(e)}")
            
        try:
            client.ai_agent.get_chat("dummy_chat_id", organization_id=organization_id)
        except Exception as e:
            print(f"   ⚠️ get_chat failed (Expected if dummy): {str(e)}")

        try:
            client.ai_agent.delete_chat("dummy_chat_id", organization_id=organization_id)
        except Exception as e:
            print(f"   ⚠️ delete_chat failed (Expected if dummy): {str(e)}")
    run_test_section("Chat v1 Ops", chat_v1_ops)

    # 3. Prompt Suggestions & Chat v2
    def chat_v2_ops():
        try:
            assistants = client.chat_ai.list_assistants()
            if assistants:
                suggestions = client.ai_agent.get_agent_prompt_suggestion(assistants[0]["id"])
                log_result("Suggestions", suggestions)
        except Exception as e:
            print(f"   ⚠️ get_agent_prompt_suggestion failed: {str(e)}")

        try:
            client.ai_agent.get_sub_agent_history("dummy_agent_id", "dummy_session_id")
        except Exception as e:
            print(f"   ⚠️ get_sub_agent_history failed: {str(e)}")

        try:
            client.ai_agent.stream_chat({"message": "hello"})
        except Exception as e:
            print(f"   ⚠️ stream_chat failed (Expected if dummy): {str(e)}")

        try:
            client.ai_agent.stream_sub_agent_chat({"message": "hello"})
        except Exception as e:
            print(f"   ⚠️ stream_sub_agent_chat failed (Expected if dummy): {str(e)}")
    run_test_section("Chat v2 Ops", chat_v2_ops)

    # 4. Embeddings
    def embedding_ops():
        try:
            client.ai_agent.process_embedding("dummy_id")
        except Exception as e:
            pass

        try:
            res = client.ai_agent.list_embedding_files()
            log_result("Embedding Files", len(res) if isinstance(res, list) else res)
        except Exception as e:
            print(f"   ⚠️ list_embedding_files failed: {str(e)}")

        try:
            client.ai_agent.get_embedding_file("dummy_id")
        except Exception as e:
            pass
        try:
            client.ai_agent.preview_embedding_file("dummy_id")
        except Exception as e:
            pass
        try:
            client.ai_agent.update_embedding_file_status("dummy_id", "active")
        except Exception as e:
            pass
        try:
            client.ai_agent.delete_embedding_file("dummy_id")
        except Exception as e:
            pass
        try:
            client.ai_agent.classify_file("dummy_id", "invoice")
        except Exception as e:
            pass
    run_test_section("Embedding Ops", embedding_ops)

    # 5. Data Board
    def field_suggestions():
        result = client.ai_agent.suggest_field_types([
            {"name": "amount", "samples": [100, 200, 300]},
            {"name": "date", "samples": ["2024-01-01", "2024-01-02"]}
        ])
        log_result("Field Suggestions", result)
    run_test_section("ai_agent.suggest_field_types", field_suggestions)

    # 6. Parquet
    def parquet_ops():
        try:
            res = client.ai_agent.generate_parquet(
                data=[{"id": 1, "name": "Test"}],
                file_name=f"test_{int(time.time())}"
            )
            log_result("Parquet Result", res)
        except Exception as e:
            print(f"   ⚠️ generate_parquet failed: {str(e)}")
            
        try:
            client.ai_agent.list_parquet_files()
        except Exception as e:
            pass
        try:
            client.ai_agent.delete_parquet_file("dummy.parquet")
        except Exception as e:
            pass
    run_test_section("Parquet Ops", parquet_ops)

    # 7. Tracing (Tempo)
    def trace_ops():
        try:
            res = client.ai_agent.get_trace_services()
            log_result("Trace Services", len(res.get("services", [])) if isinstance(res, dict) else res)
        except Exception as e:
            print(f"   ⚠️ get_trace_services failed: {str(e)}")

        try:
            res = client.ai_agent.get_trace_tags()
            log_result("Trace Tags", len(res.get("tags", [])) if isinstance(res, dict) else res)
        except Exception as e:
            print(f"   ⚠️ get_trace_tags failed: {str(e)}")

        try:
            client.ai_agent.get_traces()
        except Exception as e:
            pass
        try:
            client.ai_agent.get_trace("dummy_trace_id")
        except Exception as e:
            pass
        try:
            # get_trace_tag_values — per method-py.md
            client.ai_agent.get_trace_tag_values("http.status_code")
        except Exception as e:
            pass
        try:
            client.ai_agent.search_traceql("dummy_query")
        except Exception as e:
            pass
    run_test_section("Tracing Ops", trace_ops)

    # 8. Chat Client sub-API
    run_test_section("ai_agent.list_client_chats", lambda: log_result("Client Chats", client.ai_agent.list_client_chats(organization_id=organization_id, limit=5)))

    # 9. Admin Guides
    run_test_section("ai_agent.list_admin_guides", lambda: log_result("Admin Guides", client.ai_agent.list_admin_guides()))

    # 10. get_admin_guide — per method-py.md (returns raw response, don't write file)
    def admin_guide_download():
        try:
            guides = client.ai_agent.list_admin_guides()
            if guides:
                guide_name = guides[0].get("name") or guides[0].get("file") or "guide.pdf"
                resp = client.ai_agent.get_admin_guide(guide_name)
                log_result("Admin Guide Downloaded (bytes)", len(resp.content) if hasattr(resp, "content") else resp)
            else:
                print("   ⚠️ No admin guides found, skipping get_admin_guide")
        except Exception as e:
            print(f"   ⚠️ get_admin_guide failed: {str(e)}")
    run_test_section("ai_agent.get_admin_guide", admin_guide_download)

    print("\n✅ AI Agent Resource Testing Completed.")

if __name__ == "__main__":
    test_ai_agent()
