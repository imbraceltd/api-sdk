"""
AiAgent resource test — sync + async, runs against prodv2 gateway.
Usage:
    pip install -e ".[dev]"
    python tests/local/test_ai_agent.py
"""
import os
import asyncio
import uuid
import time
from imbrace import ImbraceClient
from imbrace.async_client import AsyncImbraceClient

ACCESS_TOKEN  = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c8c27f3b-e147-4735-b641-61e8d3706692")
GATEWAY       = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")
# Fallback values
ORG_ID        = os.environ.get("IMBRACE_ORG_ID", "org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c")
ASSISTANT_ID  = os.environ.get("IMBRACE_ASSISTANT_ID", "b64b4dfd-7f02-4f8d-962e-c3f48569af20")

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

# ─────────────────────────────────────────────────────────────────────────────
# Sync
# ─────────────────────────────────────────────────────────────────────────────

def test_sync():
    print("\n--- Synchronous Tests ---")
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    ai_agent = client.ai_agent
    global ORG_ID

    # [1] System
    print("\n[1] System")
    try:
        cfg = ai_agent.get_config()
        ok("get_config()", str(cfg)[:100])
    except Exception as e: fail("get_config()", e)

    try:
        h = ai_agent.get_health()
        ok("get_health()", str(h)[:100])
    except Exception as e: fail("get_health()", e)

    try:
        v = ai_agent.get_version()
        ok("get_version()", str(v)[:100])
    except Exception as e: fail("get_version()", e)

    # [2] Chat v1
    print("\n[2] Chat v1")
    first_chat_id = None
    try:
        res = ai_agent.list_chats(organization_id=ORG_ID, limit=5)
        # unwrap
        data = res.get("data", res)
        chats = data.get("chats", data) if isinstance(data, dict) else data
        if isinstance(chats, list) and len(chats) > 0:
            first_chat_id = chats[0].get("id")
            # Try to update ORG_ID if available
            if chats[0].get("organization_id"):
                ORG_ID = chats[0].get("organization_id")
        
        count = res.get("count") if isinstance(res, dict) else len(chats) if isinstance(chats, list) else "?"
        ok("list_chats()", f"count={count}")
    except Exception as e: fail("list_chats()", e)

    if first_chat_id:
        try:
            chat = ai_agent.get_chat(first_chat_id)
            chat_data = chat.get("data", chat) if isinstance(chat, dict) else chat
            ok("get_chat()", f"id={chat_data.get('id') if isinstance(chat_data, dict) else '?'}")
        except Exception as e: fail("get_chat()", e)
    else:
        skip("get_chat()", "no chats found")

    # [3] Prompt suggestions
    print("\n[3] Prompt suggestions")
    try:
        res = ai_agent.get_agent_prompt_suggestion(ASSISTANT_ID)
        suggestions = res.get("data", res) if isinstance(res, dict) else res
        ok("get_agent_prompt_suggestion()", f"{len(suggestions) if isinstance(suggestions, list) else '?'} suggestions")
    except Exception as e: 
        if "404" in str(e): skip("get_agent_prompt_suggestion()", "assistant not found")
        else: fail("get_agent_prompt_suggestion()", e)

    # [4] Embeddings
    print("\n[4] Embeddings")
    try:
        res = ai_agent.list_embedding_files()
        files = res.get("files") or res.get("data") or res if isinstance(res, dict) else res
        ok("list_embedding_files()", f"{len(files) if isinstance(files, list) else '?'} files")
    except Exception as e: fail("list_embedding_files()", e)

    try:
        res = ai_agent.classify_file(url="https://example.com/test.pdf", mime_type="application/pdf")
        ok("classify_file()", str(res)[:100])
    except Exception as e: fail("classify_file()", e)

    # [5] Data Board
    print("\n[5] Data Board")
    skip("suggest_field_types()", "route not wired in this app-gateway build")

    # [6] Parquet
    print("\n[6] Parquet")
    try:
        res = ai_agent.list_parquet_files()
        ok("list_parquet_files()", str(res)[:100])
    except Exception as e: fail("list_parquet_files()", e)

    generated_file_name = None
    try:
        res = ai_agent.generate_parquet(
            file_name=f"sdk_test_{int(time.time())}",
            data=[{"id": 1, "name": "test", "value": 42}],
        )
        data = res.get("data", res) if isinstance(res, dict) else res
        generated_file_name = data.get("fileName") if isinstance(data, dict) else None
        ok("generate_parquet()", str(res)[:100])
    except Exception as e: fail("generate_parquet()", e)

    if generated_file_name:
        try:
            ai_agent.delete_parquet_file(generated_file_name)
            ok("delete_parquet_file()")
        except Exception as e: fail("delete_parquet_file()", e)
    else:
        skip("delete_parquet_file()", "generate_parquet failed or returned no fileName")

    # [7] Trace
    print("\n[7] Trace")
    skip("get_trace_services()", "Grafana Tempo URL not configured")

    # [8] Admin guides
    print("\n[8] Admin guides")
    first_guide = None
    try:
        res = ai_agent.list_admin_guides()
        # unwrap
        guides = res.get("guides") or res.get("data") or res if isinstance(res, dict) else res
        if isinstance(guides, list) and len(guides) > 0:
            first_guide = guides[0].get("filename") or guides[0].get("name")
        ok("list_admin_guides()", f"{len(guides) if isinstance(guides, list) else '?'} guides")
    except Exception as e: 
        if "404" in str(e): skip("list_admin_guides()", "endpoint not found")
        else: fail("list_admin_guides()", e)

    if first_guide:
        try:
            res = ai_agent.get_admin_guide(first_guide)
            ok("get_admin_guide()", f"type={type(res)}")
        except Exception as e: fail("get_admin_guide()", e)
    else:
        skip("get_admin_guide()", "no guides listed")

    # [9] Chat Client
    print("\n[9] Chat Client")
    try:
        res = ai_agent.list_client_chats(limit=5)
        chats = res.get("chats") or res.get("data") or res if isinstance(res, dict) else res
        ok("list_client_chats()", f"count={len(chats) if isinstance(chats, list) else '?'}")
    except Exception as e: fail("list_client_chats()", e)

    new_chat_id = str(uuid.uuid4())
    created_chat = None
    try:
        created_chat = ai_agent.create_client_chat({
            "id": new_chat_id,
            "message": {"id": str(uuid.uuid4()), "role": "user", "parts": [{"type": "text", "text": "SDK test message"}]},
            "selected_visibility_type": "private",
            "assistant_id": ASSISTANT_ID,
            "organization_id": ORG_ID
        })
        data = created_chat.get("data", created_chat) if isinstance(created_chat, dict) else created_chat
        ok("create_client_chat()", f"id={data.get('id') if isinstance(data, dict) else new_chat_id}")
    except Exception as e: fail("create_client_chat()", e)

    if created_chat:
        try:
            chat = ai_agent.get_client_chat(new_chat_id)
            data = chat.get("data", chat) if isinstance(chat, dict) else chat
            ok("get_client_chat()", f"id={data.get('id') if isinstance(data, dict) else '?'}")
        except Exception as e: fail("get_client_chat()", e)

        try:
            msgs = ai_agent.list_client_messages(new_chat_id)
            list_msgs = msgs.get("messages") or msgs.get("data") or msgs if isinstance(msgs, dict) else msgs
            ok("list_client_messages()", f"{len(list_msgs) if isinstance(list_msgs, list) else '?'} messages")
        except Exception as e: fail("list_client_messages()", e)

        try:
            ai_agent.delete_client_chat(new_chat_id)
            ok("delete_client_chat()")
        except Exception as e: fail("delete_client_chat()", e)
    else:
        skip("get_client_chat()", "create_client_chat failed")

# ─────────────────────────────────────────────────────────────────────────────
# Async
# ─────────────────────────────────────────────────────────────────────────────

async def test_async():
    print("\n--- Asynchronous Tests ---")
    async with AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY) as client:
        ai_agent = client.ai_agent

        # [1] System
        print("\n[1] System (async)")
        try:
            cfg = await ai_agent.get_config()
            ok("async get_config()", str(cfg)[:100])
        except Exception as e: fail("async get_config()", e)

        # [9] Chat Client
        print("\n[9] Chat Client (async)")
        try:
            res = await ai_agent.list_client_chats(limit=5)
            chats = res.get("chats") or res.get("data") or res if isinstance(res, dict) else res
            ok("async list_client_chats()", f"count={len(chats) if isinstance(chats, list) else '?'}")
        except Exception as e: fail("async list_client_chats()", e)

if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())

    print(f"\n{'─' * 55}")
    print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
