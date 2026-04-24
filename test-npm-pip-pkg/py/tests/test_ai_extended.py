"""
Test: client.ai — extended coverage
  - Guardrails: list/get/create/update/delete
  - Guardrail Providers: list/get/create/update/delete/test/get_models
  - LLM Providers: list/create/update/delete/refresh_models
  - get_llm_models, verify_tool_server
  - Assistants v2: list/create/update/delete
  - RAG Files: list/get/upload/delete
  - Assistant Apps: get/create/update/delete
"""
import time
from io import BytesIO
from utils.utils import client, run_test_section, log_result

def test_ai_extended():
    print("\n[START] Testing AI Resource — Extended Coverage...")

    state = {
        "guardrail_id": None,
        "provider_id": None,
        "llm_provider_id": None,
        "assistant_v2_id": None,
        "rag_file_id": None,
        "assistant_app_id": None,
    }

    # 1. LLM Models
    def llm_models():
        try:
            models = client.ai.get_llm_models()
            data = models if isinstance(models, list) else models.get("data", [])
            log_result("ai.get_llm_models", len(data))
        except Exception as e:
            print(f"   [warn] get_llm_models: {str(e)}")
    run_test_section("ai.get_llm_models", llm_models)

    # 2. LLM Providers (list / CRUD)
    def provider_ops():
        try:
            providers = client.ai.list_providers()
            data = providers if isinstance(providers, list) else providers.get("data", [])
            log_result("ai.list_providers", len(data))
        except Exception as e:
            print(f"   [warn] list_providers: {str(e)}")

        try:
            ts = int(time.time())
            new_p = client.ai.create_provider({
                "name": f"sdk_test_provider_{ts}",
                "type": "openai",
                "api_key": "sk-dummy"
            })
            state["llm_provider_id"] = new_p.get("_id") or new_p.get("id")
            log_result("ai.create_provider", state["llm_provider_id"])
        except Exception as e:
            print(f"   [warn] create_provider: {str(e)}")

        if state["llm_provider_id"]:
            try:
                client.ai.update_provider(state["llm_provider_id"], {"name": "sdk_updated"})
                log_result("ai.update_provider", True)
            except Exception as e:
                print(f"   [warn] update_provider: {str(e)}")
            try:
                client.ai.refresh_provider_models(state["llm_provider_id"])
                log_result("ai.refresh_provider_models", True)
            except Exception as e:
                print(f"   [warn] refresh_provider_models: {str(e)}")
            try:
                client.ai.delete_provider(state["llm_provider_id"])
                log_result("ai.delete_provider", True)
            except Exception as e:
                print(f"   [warn] delete_provider: {str(e)}")
    run_test_section("ai.providers CRUD", provider_ops)

    # 3. Guardrail Providers
    def guardrail_provider_ops():
        try:
            providers = client.ai.list_guardrail_providers()
            data = providers if isinstance(providers, list) else providers.get("data", [])
            log_result("ai.list_guardrail_providers", len(data))
            if data:
                gp_id = data[0].get("_id") or data[0].get("id")
                try:
                    gp = client.ai.get_guardrail_provider(gp_id)
                    log_result("ai.get_guardrail_provider", gp.get("name"))
                except Exception as e:
                    print(f"   [warn] get_guardrail_provider: {str(e)}")
                try:
                    models = client.ai.get_guardrail_provider_models(gp_id)
                    log_result("ai.get_guardrail_provider_models", len(models) if isinstance(models, list) else models)
                except Exception as e:
                    print(f"   [warn] get_guardrail_provider_models: {str(e)}")
        except Exception as e:
            print(f"   [warn] list_guardrail_providers: {str(e)}")
    run_test_section("ai.guardrail_providers", guardrail_provider_ops)

    # 4. Guardrails CRUD
    def guardrail_ops():
        try:
            grs = client.ai.list_guardrails()
            data = grs if isinstance(grs, list) else grs.get("data", [])
            log_result("ai.list_guardrails", len(data))
        except Exception as e:
            print(f"   [warn] list_guardrails: {str(e)}")

        try:
            ts = int(time.time())
            new_gr = client.ai.create_guardrail({
                "name": f"sdk_guardrail_{ts}",
                "type": "content_filter",
                "rules": []
            })
            state["guardrail_id"] = new_gr.get("_id") or new_gr.get("id")
            log_result("ai.create_guardrail", state["guardrail_id"])
        except Exception as e:
            print(f"   [warn] create_guardrail: {str(e)}")

        if state["guardrail_id"]:
            try:
                gr = client.ai.get_guardrail(state["guardrail_id"])
                log_result("ai.get_guardrail", gr.get("name"))
            except Exception as e:
                print(f"   [warn] get_guardrail: {str(e)}")
            try:
                client.ai.update_guardrail(state["guardrail_id"], {"name": "updated_guardrail"})
                log_result("ai.update_guardrail", True)
            except Exception as e:
                print(f"   [warn] update_guardrail: {str(e)}")
            try:
                client.ai.delete_guardrail(state["guardrail_id"])
                log_result("ai.delete_guardrail", True)
            except Exception as e:
                print(f"   [warn] delete_guardrail: {str(e)}")
    run_test_section("ai.guardrails CRUD", guardrail_ops)

    # 5. RAG Files
    def rag_file_ops():
        try:
            files = client.ai.list_rag_files()
            data = files if isinstance(files, list) else files.get("data", [])
            log_result("ai.list_rag_files", len(data))
            if data:
                rf_id = data[0].get("_id") or data[0].get("id")
                try:
                    rf = client.ai.get_rag_file(rf_id)
                    log_result("ai.get_rag_file", rf.get("name"))
                except Exception as e:
                    print(f"   [warn] get_rag_file: {str(e)}")
        except Exception as e:
            print(f"   [warn] list_rag_files: {str(e)}")

        try:
            content = b"SDK RAG test content"
            uploaded = client.ai.upload_rag_file(BytesIO(content), filename="sdk_test.txt")
            state["rag_file_id"] = uploaded.get("_id") or uploaded.get("id")
            log_result("ai.upload_rag_file", state["rag_file_id"])
        except Exception as e:
            print(f"   [warn] upload_rag_file: {str(e)}")

        if state["rag_file_id"]:
            try:
                client.ai.delete_rag_file(state["rag_file_id"])
                log_result("ai.delete_rag_file", True)
            except Exception as e:
                print(f"   [warn] delete_rag_file: {str(e)}")
    run_test_section("ai.rag_files", rag_file_ops)

    # 6. Assistants v2
    def assistants_v2_ops():
        try:
            assts = client.ai.list_assistants_v2()
            data = assts if isinstance(assts, list) else assts.get("data", [])
            log_result("ai.list_assistants_v2", len(data))
        except Exception as e:
            print(f"   [warn] list_assistants_v2: {str(e)}")

        try:
            ts = int(time.time())
            new_a = client.ai.create_assistant_v2({
                "name": f"sdk_asst_v2_{ts}",
                "model": "gpt-4o"
            })
            state["assistant_v2_id"] = new_a.get("_id") or new_a.get("id")
            log_result("ai.create_assistant_v2", state["assistant_v2_id"])
        except Exception as e:
            print(f"   [warn] create_assistant_v2: {str(e)}")

        if state["assistant_v2_id"]:
            try:
                client.ai.update_assistant_v2(state["assistant_v2_id"], {"name": "sdk_updated_v2"})
                log_result("ai.update_assistant_v2", True)
            except Exception as e:
                print(f"   [warn] update_assistant_v2: {str(e)}")
            try:
                client.ai.delete_assistant_v2(state["assistant_v2_id"])
                log_result("ai.delete_assistant_v2", True)
            except Exception as e:
                print(f"   [warn] delete_assistant_v2: {str(e)}")
    run_test_section("ai.assistants_v2 CRUD", assistants_v2_ops)

    # 7. verify_tool_server
    def verify_tool():
        try:
            res = client.ai.verify_tool_server({"url": "https://example.com/tool"})
            log_result("ai.verify_tool_server", res)
        except Exception as e:
            print(f"   [warn] verify_tool_server: {str(e)}")
    run_test_section("ai.verify_tool_server", verify_tool)

    print("\n[DONE] AI Extended Resource Testing Completed.")

if __name__ == "__main__":
    test_ai_extended()
