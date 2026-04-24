import time
from io import BytesIO
from utils.utils import client, run_test_section, log_result

def test_ai_raw():
    print("\n🚀 Testing Raw AI Resource (Completions, Embeddings, Assistants v2/v3)...")

    # 1. Completions (client.ai)
    def ai_completions():
        from imbrace.types.ai import CompletionInput, CompletionMessage
        
        try:
            res = client.ai.complete(CompletionInput(
                model="gpt-4o",
                messages=[CompletionMessage(role="user", content="Say 'raw-ai-ready'")]
            ))
            log_result("Raw Completion", res.choices[0].message.content)
        except Exception as e:
            print(f"   ⚠️ Raw completion failed: {str(e)}")

        try:
            print("   Streaming raw AI: ", end="", flush=True)
            chunks = client.ai.stream(CompletionInput(
                model="gpt-4o",
                messages=[CompletionMessage(role="user", content="Count to 2")]
            ))
            for chunk in chunks:
                print(chunk.choices[0].delta.content or "", end="", flush=True)
            print("\n   ✅ Streaming Finished.")
        except Exception as e:
            print(f"\n   ⚠️ Raw streaming failed: {str(e)}")

    run_test_section("Raw AI Completions", ai_completions)

    # 2. Embeddings
    def ai_embeddings():
        from imbrace.types.ai import EmbeddingInput
        try:
            res = client.ai.embed(EmbeddingInput(
                model="text-embedding-3-small",
                input=["hello world"]
            ))
            log_result("Raw Embedding", f"Dim: {len(res.data[0].embedding)}")
        except Exception as e:
            print(f"   ⚠️ Raw embedding failed: {str(e)}")
    run_test_section("Raw AI Embeddings", ai_embeddings)

    # 3. Assistants v3
    def assistants_v3():
        try:
            assts = client.ai.list_assistants()
            log_result("Assistants v3 Count", len(assts) if isinstance(assts, list) else len(assts.get("data", [])))
            
            apps = client.ai.list_assistant_apps()
            log_result("Assistant Apps Count", len(apps) if isinstance(apps, list) else len(apps.get("data", [])))
            
            rag_files = client.ai.list_rag_files()
            log_result("RAG Files Count", len(rag_files) if isinstance(rag_files, list) else len(rag_files.get("data", [])))
        except Exception as e:
            print(f"   ⚠️ Assistants v3 failed: {str(e)}")
    run_test_section("Assistants v3 Ops", assistants_v3)

    # 4. Guardrails
    def guardrails_ops():
        try:
            grs = client.ai.list_guardrails()
            log_result("Guardrails Count", len(grs) if isinstance(grs, list) else len(grs.get("data", [])))
            
            providers = client.ai.list_guardrail_providers()
            log_result("Guardrail Providers", len(providers) if isinstance(providers, list) else len(providers.get("data", [])))
        except Exception as e:
            print(f"   ⚠️ Guardrails failed: {str(e)}")
    run_test_section("Guardrails Ops", guardrails_ops)

    print("\n✅ Raw AI Resource Testing Completed.")

if __name__ == "__main__":
    test_ai_raw()
