"""
AiAgent resource test — runs against prodv2 gateway.
Usage: python examples/07_ai_agent.py
"""

import os
import json
from imbrace import ImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c8c27f3b-e147-4735-b641-61e8d3706692")
GATEWAY      = os.environ.get("IMBRACE_GATEWAY_URL",  "https://app-gatewayv2.imbrace.co")
ORG_ID       = os.environ.get("IMBRACE_ORG_ID",       "org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c")
ASSISTANT_ID = os.environ.get("IMBRACE_ASSISTANT_ID", "b64b4dfd-7f02-4f8d-962e-c3f48569af20")

client   = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY, organization_id=ORG_ID)
ai_agent = client.ai_agent

passed, failed, skipped = 0, 0, 0

def ok(label, detail=""):
    global passed
    print(f"  ✓ {label}{f'  →  {str(detail)[:120]}' if detail else ''}")
    passed += 1

def fail(label, err):
    global failed
    print(f"  ✗ {label}: {str(err)[:120]}")
    failed += 1

def skip(label, reason):
    global skipped
    print(f"  - {label}  (skipped: {reason})")
    skipped += 1

# ─────────────────────────────────────────────────────────────────────────────
# System
# ─────────────────────────────────────────────────────────────────────────────

print("\n[1] System")

try:
    cfg = ai_agent.get_config()
    ok("get_config()", str(cfg)[:100])
except Exception as e:
    fail("get_config()", e)

try:
    h = ai_agent.get_health()
    ok("get_health()", str(h)[:100])
except Exception as e:
    fail("get_health()", e)

try:
    v = ai_agent.get_version()
    ok("get_version()", str(v)[:100])
except Exception as e:
    fail("get_version()", e)

# ─────────────────────────────────────────────────────────────────────────────
# Chat v1
# ─────────────────────────────────────────────────────────────────────────────

print("\n[2] Chat v1")

first_chat_id = None
try:
    res = ai_agent.list_chats(organization_id=ORG_ID, limit=5)
    chats = res.get("chats", res) if isinstance(res, dict) else res
    first_chat_id = chats[0].get("id") if isinstance(chats, list) and chats else None
    ok("list_chats()", f"count={res.get('count', len(chats) if isinstance(chats, list) else '?')}")
except Exception as e:
    fail("list_chats()", e)

if first_chat_id:
    try:
        chat = ai_agent.get_chat(first_chat_id)
        ok("get_chat()", f"id={chat.get('id')}")
    except Exception as e:
        fail("get_chat()", e)
else:
    skip("get_chat()", "no chats found")

# ─────────────────────────────────────────────────────────────────────────────
# Prompt suggestions
# ─────────────────────────────────────────────────────────────────────────────

print("\n[3] Prompt suggestions")

try:
    res = ai_agent.get_agent_prompt_suggestion(ASSISTANT_ID)
    suggestions = res.get("data", res) if isinstance(res, dict) else res
    ok("get_agent_prompt_suggestion()", f"{len(suggestions) if isinstance(suggestions, list) else '?'} suggestions")
except Exception as e:
    fail("get_agent_prompt_suggestion()", e)

# ─────────────────────────────────────────────────────────────────────────────
# Embeddings / files
# ─────────────────────────────────────────────────────────────────────────────

print("\n[4] Embeddings")

try:
    res = ai_agent.list_embedding_files()
    files = res if isinstance(res, list) else res.get("files", res.get("data", []))
    ok("list_embedding_files()", f"{len(files) if isinstance(files, list) else '?'} files")
except Exception as e:
    fail("list_embedding_files()", e)

try:
    res = ai_agent.get_embedding_statistics()
    ok("get_embedding_statistics()", str(res)[:100])
except Exception as e:
    fail("get_embedding_statistics()", e)

# ─────────────────────────────────────────────────────────────────────────────
# Parquet
# ─────────────────────────────────────────────────────────────────────────────

print("\n[5] Parquet")

try:
    res = ai_agent.list_parquet_files()
    ok("list_parquet_files()", str(res)[:100])
except Exception as e:
    fail("list_parquet_files()", e)

# ─────────────────────────────────────────────────────────────────────────────
# Admin Guides
# ─────────────────────────────────────────────────────────────────────────────

print("\n[6] Admin guides")

first_guide = None
try:
    res = ai_agent.list_admin_guides()
    guides = res if isinstance(res, list) else res.get("guides", res.get("data", []))
    first_guide = (guides[0].get("filename") or guides[0].get("name")) if isinstance(guides, list) and guides else None
    ok("list_admin_guides()", f"{len(guides) if isinstance(guides, list) else '?'} guides")
except Exception as e:
    fail("list_admin_guides()", e)

if first_guide:
    try:
        r = ai_agent.get_admin_guide(first_guide)
        ok("get_admin_guide()", f"status={r.status_code}, type={r.headers.get('content-type', '?')}")
    except Exception as e:
        fail("get_admin_guide()", e)
else:
    skip("get_admin_guide()", "no guides listed")

# ─────────────────────────────────────────────────────────────────────────────
# Chat Client
# ─────────────────────────────────────────────────────────────────────────────

print("\n[7] Chat Client")

try:
    res = ai_agent.list_client_chats(organization_id=ORG_ID, limit=5)
    chats = res.get("chats", res.get("data", res)) if isinstance(res, dict) else res
    ok("list_client_chats()", f"count={len(chats) if isinstance(chats, list) else '?'}")
except Exception as e:
    fail("list_client_chats()", e)

# ─────────────────────────────────────────────────────────────────────────────

client.close()
print(f"\n{'─' * 55}")
print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
if failed > 0:
    raise SystemExit(1)
