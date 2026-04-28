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
            # get_chat(chat_id, include_messages=False) — no organization_id param
            client.ai_agent.get_chat("dummy_chat_id", include_messages=False)
        except Exception as e:
            print(f"   ⚠️ get_chat failed (Expected if dummy): {str(e)}")

        try:
            # delete_chat(chat_id, organization_id, user_id=None)
            client.ai_agent.delete_chat("dummy_chat_id", organization_id)
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
        # POST /ai-agent/data-board/suggest-field-types
        # ⚠️ 404 on prodv2 — backend route not yet deployed. Skip gracefully.
        try:
            result = client.ai_agent.suggest_field_types([
                {"name": "amount", "samples": [100, 200, 300]},
                {"name": "date", "samples": ["2024-01-01", "2024-01-02"]}
            ])
            log_result("Field Suggestions", result)
        except Exception as e:
            if "404" in str(e):
                print(f"   ⚠️ suggest_field_types: 404 — backend route not deployed yet (expected)")
            else:
                print(f"   ⚠️ suggest_field_types failed: {str(e)}")
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
    # ⚠️ Tempo service is returning 500 due to missing URL config on prodv2.
    # All trace methods are wrapped in try/except — will not block test.
    def trace_ops():
        try:
            res = client.ai_agent.get_trace_services()
            log_result("Trace Services", res)
        except Exception as e:
            code = getattr(e, "status_code", "?")
            print(f"   ⚠️ get_trace_services: {code} — Tempo URL not configured (expected on prodv2)")

        try:
            res = client.ai_agent.get_trace_tags()
            log_result("Trace Tags", res)
        except Exception as e:
            code = getattr(e, "status_code", "?")
            print(f"   ⚠️ get_trace_tags: {code} — Tempo URL not configured (expected)")

        try:
            client.ai_agent.get_traces(limit=1)
            log_result("get_traces", True)
        except Exception as e:
            print(f"   ⚠️ get_traces: {str(e)[:60]}")

        try:
            client.ai_agent.get_trace("dummy_trace_id")
        except Exception as e:
            print(f"   ⚠️ get_trace (dummy): {str(e)[:60]}")

        try:
            client.ai_agent.get_trace_tag_values("http.status_code")
        except Exception as e:
            print(f"   ⚠️ get_trace_tag_values: {str(e)[:60]}")

        try:
            client.ai_agent.search_traceql("{ .service.name = \"ai-agent\" }")
        except Exception as e:
            print(f"   ⚠️ search_traceql: {str(e)[:60]}")
    run_test_section("Tracing Ops", trace_ops)

    # 8. Chat Client sub-API
    state_chat = {"client_chat_id": None, "message_id": None}

    def client_chat_ops():
        try:
            chats = client.ai_agent.list_client_chats(organization_id=organization_id, limit=5)
            data = chats if isinstance(chats, list) else chats.get("data", [])
            log_result("list_client_chats", len(data))
            if data:
                state_chat["client_chat_id"] = data[0].get("_id") or data[0].get("id")
        except Exception as e:
            print(f"   ⚠️ list_client_chats failed: {str(e)}")

        if state_chat["client_chat_id"]:
            try:
                msgs = client.ai_agent.list_client_messages(state_chat["client_chat_id"])
                data_msgs = msgs if isinstance(msgs, list) else msgs.get("data", [])
                log_result("list_client_messages", len(data_msgs))
                if data_msgs:
                    state_chat["message_id"] = data_msgs[0].get("_id") or data_msgs[0].get("id")
            except Exception as e:
                print(f"   ⚠️ list_client_messages failed: {str(e)}")

            try:
                votes = client.ai_agent.get_votes(state_chat["client_chat_id"])
                log_result("get_votes", votes)
            except Exception as e:
                print(f"   ⚠️ get_votes failed: {str(e)}")

            if state_chat["message_id"]:
                try:
                    client.ai_agent.update_vote({"messageId": state_chat["message_id"], "vote": "up"})
                    log_result("update_vote", True)
                except Exception as e:
                    print(f"   ⚠️ update_vote failed: {str(e)}")

                try:
                    client.ai_agent.delete_trailing_messages(state_chat["message_id"])
                    log_result("delete_trailing_messages", True)
                except Exception as e:
                    print(f"   ⚠️ delete_trailing_messages failed: {str(e)}")

            try:
                client.ai_agent.generate_client_chat_title(state_chat["client_chat_id"])
                log_result("generate_client_chat_title", True)
            except Exception as e:
                print(f"   ⚠️ generate_client_chat_title failed: {str(e)}")
    run_test_section("ai_agent.client_chat_ops", client_chat_ops)

    # 9. Documents sub-API
    # ⚠️ create_document requires: id, chatId, kind, content, createdAt
    def document_ops():
        doc_id = None
        try:
            import uuid as _uuid
            from datetime import datetime, timezone
            doc = client.ai_agent.create_document({
                "id": str(_uuid.uuid4()),
                "chatId": str(_uuid.uuid4()),
                "kind": "text",
                "content": "SDK test document",
                "title": "SDK Test",
                "createdAt": datetime.now(timezone.utc).isoformat(),
            })
            doc_id = doc.get("_id") or doc.get("id")
            log_result("create_document", doc_id)
        except Exception as e:
            code = getattr(e, "status_code", "?")
            print(f"   ⚠️ create_document: {code} — {str(e)[:120]}")
            print(f"   ℹ️ Note: backend may require additional fields (assistantId, userId, etc.)")

        if doc_id:
            try:
                fetched = client.ai_agent.get_document(doc_id)
                log_result("get_document", fetched.get("_id") or fetched.get("id"))
            except Exception as e:
                print(f"   ⚠️ get_document failed: {str(e)}")

            try:
                latest = client.ai_agent.get_document_latest(doc_id)
                log_result("get_document_latest", latest)
            except Exception as e:
                print(f"   ⚠️ get_document_latest failed: {str(e)}")

            try:
                pub = client.ai_agent.get_document_public(doc_id)
                log_result("get_document_public", pub)
            except Exception as e:
                print(f"   ⚠️ get_document_public failed: {str(e)}")

            try:
                by_kind = client.ai_agent.get_document_latest_by_kind(kind="text")
                log_result("get_document_latest_by_kind", by_kind)
            except Exception as e:
                print(f"   ⚠️ get_document_latest_by_kind failed: {str(e)}")

            try:
                suggestions = client.ai_agent.get_document_suggestions(doc_id)
                log_result("get_document_suggestions", suggestions)
            except Exception as e:
                print(f"   ⚠️ get_document_suggestions failed: {str(e)}")

            try:
                client.ai_agent.delete_document(doc_id)
                log_result("delete_document", True)
            except Exception as e:
                print(f"   ⚠️ delete_document failed: {str(e)}")
    run_test_section("ai_agent.document_ops", document_ops)

    # 10. Admin Guides
    # ⚠️ /ai-agent/admin/guides route is 404 on prodv2 — not yet deployed.
    def admin_guides_ops():
        guides = []
        try:
            guides = client.ai_agent.list_admin_guides()
            log_result("list_admin_guides", len(guides) if isinstance(guides, list) else guides)
        except Exception as e:
            code = getattr(e, "status_code", "?")
            print(f"   ⚠️ list_admin_guides: {code} — route not deployed on prodv2 (expected)")

        if guides:
            try:
                guide_name = guides[0].get("name") or guides[0].get("file") or "guide.pdf"
                resp = client.ai_agent.get_admin_guide(guide_name)
                log_result("get_admin_guide (bytes)", len(resp.content) if hasattr(resp, "content") else resp)
            except Exception as e:
                print(f"   ⚠️ get_admin_guide failed: {str(e)[:80]}")
        else:
            print("   ⚠️ get_admin_guide — skipped (no guides or 404)")
    run_test_section("ai_agent.admin_guides", admin_guides_ops)

    print("\n✅ AI Agent Resource Testing Completed.")

if __name__ == "__main__":
    test_ai_agent()
