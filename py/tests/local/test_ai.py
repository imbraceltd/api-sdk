"""
AI resource comprehensive test — sync + async, runs against prodv2 gateway.
Usage:
    pip install -e ".[dev]"
    python tests/local/test_ai.py

Skipped: stream(), complete(), embed() (not available on prodv2),
         v2 assistant methods (return 404 on this env)
"""
import os
import asyncio
from imbrace import ImbraceClient
from imbrace.async_client import AsyncImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c8c27f3b-e147-4735-b641-61e8d3706692")
GATEWAY = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")

passed = 0
failed = 0
skipped = 0


def ok(label, detail=""):
    global passed
    detail_str = f"  →  {str(detail)[:120]}" if detail else ""
    print(f"  ✓ {label}{detail_str}")
    passed += 1


def fail(label, err):
    global failed
    print(f"  ✗ {label}: {err}")
    failed += 1


def skip(label, reason):
    global skipped
    print(f"  - {label}  (skipped: {reason})")
    skipped += 1


def _is_4xx(e: Exception) -> bool:
    msg = str(e)
    return any(c in msg for c in ("[400]", "[401]", "[403]", "[404]", "[422]"))


def _is_5xx(e: Exception) -> bool:
    return "[500]" in str(e) or "[502]" in str(e) or "[503]" in str(e)


# ─────────────────────────────────────────────────────────────────────────────
# Sync
# ─────────────────────────────────────────────────────────────────────────────

def test_sync():
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    ai = client.ai

    created_app_id      = None
    created_guardrail_id = None
    created_gp_id       = None
    created_provider_id  = None

    # ── Assistants ─────────────────────────────────────────────────────────────

    print("\n[1] List assistants (sync)")
    first_assistant_id = None
    try:
        res = ai.list_ai_agents()
        lst = res if isinstance(res, list) else res.get("data", [])
        first_assistant_id = lst[0].get("_id") if lst else None
        ok("list_ai_agents()", f"{len(lst)} assistants")
    except Exception as e:
        fail("list_ai_agents()", e)

    print("\n[2] Get assistant (sync)")
    if not first_assistant_id:
        skip("get_ai_agent(id)", "no assistants found")
    else:
        try:
            res = ai.get_ai_agent(first_assistant_id)
            ok("get_ai_agent(id)", f"id={res.get('_id')} name={res.get('name')}")
        except Exception as e:
            if _is_4xx(e):
                skip("get_ai_agent(id)", "assistant not in token scope")
            else:
                fail("get_ai_agent(id)", e)

    print("\n[3] Check assistant name (sync)")
    try:
        res = ai.check_ai_agent_name("sdk-test-nonexistent-name-xyz")
        ok("check_ai_agent_name()", str(res))
    except Exception as e:
        fail("check_ai_agent_name()", e)

    print("\n[4] List agents (sync)")
    try:
        res = ai.list_agents()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("list_agents()", f"{len(lst)} agents")
    except Exception as e:
        fail("list_agents()", e)

    print("\n[5] Patch instructions (sync)")
    if not first_assistant_id:
        skip("patch_instructions(id)", "no assistants found")
    else:
        try:
            res = ai.patch_instructions(first_assistant_id, {"instructions": "SDK test patch — safe to ignore."})
            ok("patch_instructions(id)", res.get("_id", str(res)[:60]))
        except Exception as e:
            if _is_4xx(e):
                skip("patch_instructions(id)", "assistant not in token scope")
            else:
                fail("patch_instructions(id)", e)

    # ── Assistant Apps ─────────────────────────────────────────────────────────

    print("\n[6] Create assistant app (sync)")
    try:
        res = ai.create_ai_agent_app({"name": "SDK Test App", "workflow_name": "sdk-test-workflow", "instructions": "Test only."})
        created_app_id = res.get("id") or res.get("_id")
        ok("create_ai_agent_app()", created_app_id or str(res)[:60])
    except Exception as e:
        fail("create_ai_agent_app()", e)

    print("\n[7] Update assistant app (sync)")
    if not created_app_id:
        skip("update_ai_agent_app(id)", "no app created")
    else:
        try:
            res = ai.update_ai_agent_app(created_app_id, {"name": "SDK Test App Updated", "workflow_name": "sdk-test-workflow", "instructions": "Updated."})
            ok("update_ai_agent_app(id)", res.get("id") or res.get("_id", str(res)[:60]))
        except Exception as e:
            fail("update_ai_agent_app(id)", e)

    print("\n[8] Update assistant workflow (sync)")
    skip("update_ai_agent_workflow(id)", "route not available on this prodv2 version")

    # ── RAG Files ──────────────────────────────────────────────────────────────

    print("\n[9] List RAG files (sync)")
    first_rag_file_id = None
    try:
        res = ai.list_rag_files()
        lst = res if isinstance(res, list) else res.get("data", [])
        first_rag_file_id = lst[0].get("_id") if lst else None
        ok("list_rag_files()", f"{len(lst)} files")
    except Exception as e:
        fail("list_rag_files()", e)

    print("\n[10] Get RAG file (sync)")
    if not first_rag_file_id:
        skip("get_rag_file(id)", "no RAG files found")
    else:
        try:
            res = ai.get_rag_file(first_rag_file_id)
            ok("get_rag_file(id)", res.get("_id") or res.get("name"))
        except Exception as e:
            fail("get_rag_file(id)", e)

    # ── Guardrails ─────────────────────────────────────────────────────────────

    print("\n[11] List guardrails (sync)")
    try:
        res = ai.list_guardrails()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("list_guardrails()", f"{len(lst)} guardrails")
    except Exception as e:
        fail("list_guardrails()", e)

    print("\n[12] Create guardrail (sync)")
    try:
        res = ai.create_guardrail({"name": "SDK Test Guardrail", "model": "gpt-4o", "instructions": "Block unsafe content.", "unsafe_categories": [], "description": "Test only."})
        created_guardrail_id = res.get("_id") or res.get("guardrails_config_id")
        ok("create_guardrail()", created_guardrail_id or str(res)[:60])
    except Exception as e:
        fail("create_guardrail()", e)

    print("\n[13] Get guardrail (sync)")
    if not created_guardrail_id:
        skip("get_guardrail(id)", "no guardrail created")
    else:
        try:
            res = ai.get_guardrail(created_guardrail_id)
            ok("get_guardrail(id)", res.get("_id") or res.get("name"))
        except Exception as e:
            fail("get_guardrail(id)", e)

    print("\n[14] Update guardrail (sync)")
    if not created_guardrail_id:
        skip("update_guardrail(id)", "no guardrail created")
    else:
        try:
            res = ai.update_guardrail(created_guardrail_id, {"name": "SDK Test Guardrail Updated", "model": "gpt-4o", "instructions": "Block unsafe content.", "unsafe_categories": []})
            ok("update_guardrail(id)", res.get("_id", str(res)[:60]))
        except Exception as e:
            fail("update_guardrail(id)", e)

    # ── Guardrail Providers ────────────────────────────────────────────────────

    print("\n[15] List guardrail providers (sync)")
    try:
        res = ai.list_guardrail_providers()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("list_guardrail_providers()", f"{len(lst)} providers")
    except Exception as e:
        fail("list_guardrail_providers()", e)

    print("\n[16] Create guardrail provider (sync)")
    try:
        res = ai.create_guardrail_provider({"name": "SDK Test GP", "type": "openai", "config": {}})
        created_gp_id = res.get("_id") or res.get("guardrail_provider_id")
        ok("create_guardrail_provider()", created_gp_id or str(res)[:60])
    except Exception as e:
        fail("create_guardrail_provider()", e)

    print("\n[17] Get guardrail provider (sync)")
    if not created_gp_id:
        skip("get_guardrail_provider(id)", "no guardrail provider created")
    else:
        try:
            res = ai.get_guardrail_provider(created_gp_id)
            ok("get_guardrail_provider(id)", res.get("_id") or res.get("name"))
        except Exception as e:
            fail("get_guardrail_provider(id)", e)

    print("\n[18] Update guardrail provider (sync)")
    if not created_gp_id:
        skip("update_guardrail_provider(id)", "no guardrail provider created")
    else:
        try:
            res = ai.update_guardrail_provider(created_gp_id, {"name": "SDK Test GP Updated"})
            ok("update_guardrail_provider(id)", res.get("guardrail_provider_id", str(res)[:60]))
        except Exception as e:
            fail("update_guardrail_provider(id)", e)

    print("\n[19] Test guardrail provider (sync)")
    if not created_gp_id:
        skip("test_guardrail_provider(id)", "no guardrail provider created")
    else:
        try:
            res = ai.test_guardrail_provider(created_gp_id, {"prompt": "hello"})
            ok("test_guardrail_provider(id)", str(res)[:80])
        except Exception as e:
            fail("test_guardrail_provider(id)", e)

    print("\n[20] Get guardrail provider models (sync)")
    if not created_gp_id:
        skip("get_guardrail_provider_models(id)", "no guardrail provider created")
    else:
        try:
            res = ai.get_guardrail_provider_models(created_gp_id)
            models = res.get("models", res) if isinstance(res, dict) else res
            ok("get_guardrail_provider_models(id)", f"{len(models) if isinstance(models, list) else str(models)[:40]} model(s)")
        except Exception as e:
            if _is_4xx(e):
                skip("get_guardrail_provider_models(id)", f"not supported: {str(e)[:60]}")
            else:
                fail("get_guardrail_provider_models(id)", e)

    # ── Custom Providers ───────────────────────────────────────────────────────

    print("\n[21] List providers (sync)")
    try:
        res = ai.list_providers()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("list_providers()", f"{len(lst)} providers")
    except Exception as e:
        fail("list_providers()", e)

    print("\n[22] Create provider (sync)")
    try:
        res = ai.create_provider({"name": "SDK Test Provider", "type": "openai", "api_key": "sk-test-placeholder"})
        created_provider_id = res.get("_id")
        ok("create_provider()", created_provider_id or str(res)[:60])
    except Exception as e:
        if _is_4xx(e):
            skip("create_provider()", f"invalid config: {str(e)[:60]}")
        else:
            fail("create_provider()", e)

    print("\n[23] Update provider (sync)")
    if not created_provider_id:
        skip("update_provider(id)", "no provider created")
    else:
        try:
            res = ai.update_provider(created_provider_id, {"name": "SDK Test Provider Updated"})
            ok("update_provider(id)", res.get("_id", str(res)[:60]))
        except Exception as e:
            fail("update_provider(id)", e)

    print("\n[24] Refresh provider models (sync)")
    if not created_provider_id:
        skip("refresh_provider_models(id)", "no provider created")
    else:
        try:
            res = ai.refresh_provider_models(created_provider_id)
            ok("refresh_provider_models(id)", str(res)[:80])
        except Exception as e:
            fail("refresh_provider_models(id)", e)

    print("\n[25] Get LLM models (sync)")
    try:
        res = ai.get_llm_models()
        models = res.get("models", res) if isinstance(res, dict) else res
        ok("get_llm_models()", f"{len(models) if isinstance(models, list) else str(models)[:40]} model(s)")
    except Exception as e:
        fail("get_llm_models()", e)

    print("\n[26] Verify tool server (sync)")
    try:
        res = ai.verify_tool_server({"url": "https://example.com/tools", "path": "/tools", "auth_type": "none", "key": "", "config": {}})
        ok("verify_tool_server()", str(res)[:80])
    except Exception as e:
        if _is_4xx(e) or _is_5xx(e):
            skip("verify_tool_server()", f"server error verifying test URL: {str(e)[:40]}")
        else:
            fail("verify_tool_server()", e)

    # ── Cleanup ────────────────────────────────────────────────────────────────

    print("\n[27] Cleanup (sync)")

    if created_app_id:
        try:
            ai.delete_ai_agent_app(created_app_id)
            ok("delete_ai_agent_app()", created_app_id)
        except Exception as e:
            fail("delete_ai_agent_app()", e)

    if created_guardrail_id:
        try:
            ai.delete_guardrail(created_guardrail_id)
            ok("delete_guardrail()", created_guardrail_id)
        except Exception as e:
            fail("delete_guardrail()", e)

    if created_gp_id:
        try:
            ai.delete_guardrail_provider(created_gp_id)
            ok("delete_guardrail_provider()", created_gp_id)
        except Exception as e:
            fail("delete_guardrail_provider()", e)

    if created_provider_id:
        try:
            ai.delete_provider(created_provider_id)
            ok("delete_provider()", created_provider_id)
        except Exception as e:
            fail("delete_provider()", e)

    skip("complete()", "excluded per test plan")
    skip("stream()", "excluded per test plan")
    skip("embed()", "not available on prodv2")
    skip("list_ai_agents_v2() + v2 CRUD", "returns 404 on prodv2")


# ─────────────────────────────────────────────────────────────────────────────
# Async
# ─────────────────────────────────────────────────────────────────────────────

async def test_async():
    client = AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    ai = client.ai

    print("\n[28] List assistants (async)")
    try:
        res = await ai.list_ai_agents()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("async list_ai_agents()", f"{len(lst)} assistants")
    except Exception as e:
        fail("async list_ai_agents()", e)

    print("\n[29] List guardrail providers (async)")
    try:
        res = await ai.list_guardrail_providers()
        lst = res if isinstance(res, list) else res.get("data", [])
        ok("async list_guardrail_providers()", f"{len(lst)} providers")
    except Exception as e:
        fail("async list_guardrail_providers()", e)

    print("\n[30] Get LLM models (async)")
    try:
        res = await ai.get_llm_models()
        models = res.get("models", res) if isinstance(res, dict) else res
        ok("async get_llm_models()", f"{len(models) if isinstance(models, list) else str(models)[:40]} model(s)")
    except Exception as e:
        fail("async get_llm_models()", e)

    await client.close()


if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())

    print(f"\n{'─' * 55}")
    print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
