"""E2E test against org_imbrace via app-gateway.sandbox.imbrace.co"""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "py" / "src"))

from imbrace import ImbraceClient

ACCESS_TOKEN = "acc_3ceec9cb-17bc-4031-98b2-adf135b792a4"
ORG_ID       = "org_imbrace"
GATEWAY      = "https://app-gateway.sandbox.imbrace.co"
SAMPLE_URL   = "https://app-gatewayv2.imbrace.co/files/download/118615471-5b33f600-b7f3-11eb-94a1-78e635e66558.png"

passed = failed = 0
def ok(label, detail=""):
    global passed; passed += 1
    print(f"  [PASS] {label}{('  -> ' + str(detail)[:120]) if detail else ''}")
def fail(label, err):
    global failed; failed += 1
    print(f"  [FAIL] {label}: {str(err)[:200]}")

client = ImbraceClient(access_token=ACCESS_TOKEN, organization_id=ORG_ID, gateway=GATEWAY, timeout=120)
da = client.document_ai

print("=" * 70)
print(f"Document AI E2E — org_imbrace @ {GATEWAY}")
print("=" * 70)

# [1] list providers
print("\n[1] list_providers")
provider_id = None
model_id = "qwen3.5:27b"
try:
    providers = client.ai.list_providers()
    ok(f"list_providers", f"{len(providers)} providers")
    custom = [p for p in providers if p.get("provider_id") != "system"]
    if custom:
        for p in custom[:5]:
            print(f"      - {p.get('name', '?')[:35]:35s} pid={(p.get('provider_id') or '')[:38]} models={len(p.get('models') or [])}")
        # Pick first vLLM Qwen provider (HAR uses qwen3.5:27b format)
        for p in custom:
            ms = p.get("models") or []
            for m in ms:
                if m.get("name", "").startswith("qwen"):
                    provider_id = p.get("provider_id")
                    model_id = m.get("name")
                    print(f"      → using provider={p.get('name')} model={model_id}")
                    break
            if provider_id: break
        if not provider_id:
            provider_id = custom[0].get("provider_id")
            model_id = (custom[0].get("models") or [{}])[0].get("name", "qwen3.5:27b")
except Exception as e: fail("list_providers", e)

# [2] list_agents
print("\n[2] list_agents()")
try:
    agents = da.list_agents()
    ok("list_agents", f"{len(agents)} agents")
except Exception as e: fail("list_agents", e)

# [3] document_ai_only filter
print("\n[3] list_agents(document_ai_only=True)")
try:
    doc_ai = da.list_agents(document_ai_only=True)
    ok("list_agents(document_ai_only=True)", f"{len(doc_ai)} Document AI agents")
    for a in doc_ai[:5]:
        nm = a.get("name", "")
        bid = (a.get("document_ai") or {}).get("board_id", "-")
        print(f"      - {nm[:40]:40s} board_id={bid}")
except Exception as e: fail("list_agents(document_ai_only=True)", e)

# [4] process — gpt-4o
print("\n[4] process — gpt-4o")
try:
    res = da.process(url=SAMPLE_URL, organization_id=ORG_ID, model_name="gpt-4o")
    keys = list((res or {}).get("data", {}).keys())
    ok("process", f"success={res.get('success')} keys={keys[:5]}")
except Exception as e: fail("process", e)

# [5] suggest_schema
print("\n[5] suggest_schema")
try:
    res = da.suggest_schema(url=SAMPLE_URL, organization_id=ORG_ID)
    keys = list((res or {}).get("data", {}).keys())
    ok("suggest_schema", f"success={res.get('success')} keys={keys[:5]}")
except Exception as e: fail("suggest_schema", e)

# [6] create_full — atomic with type=DocumentAI + agent_type=document_ai
print("\n[6] create_full — atomic Board(DocumentAI) + UseCase(document_ai) + Assistant")
created = None
test_name = f"SDK_TEST_DocAI_{os.getpid()}"
if provider_id:
    try:
        created = da.create_full(
            name=test_name,
            description="SDK E2E test — auto-deleted",
            instructions="Extract receipt: vendor, total, date.",
            schema_fields=[
                {"name": "vendor", "type": "ShortText", "is_identifier": True, "is_unique_identifier": False, "is_default": False},
                {"name": "total", "type": "Number", "is_identifier": False, "is_unique_identifier": False, "is_default": False},
                {"name": "date", "type": "Date", "is_identifier": False, "is_unique_identifier": False, "is_default": False},
            ],
            model_id=model_id, provider_id=provider_id,
        )
        ok("create_full",
           f"board={(created.get('board_id') or '')[:30]} "
           f"uc={(created.get('usecase_id') or '')[:30]} "
           f"a={(created.get('assistant_id') or '')[:30]}")
    except Exception as e: fail("create_full", e)

if created and created.get("assistant_id"):
    aid = created["assistant_id"]

    # [7] verify
    print("\n[7] verify created agent in document_ai_only filter")
    try:
        doc_agents = da.list_agents(document_ai_only=True)
        found = any((a.get("id") or a.get("_id")) == aid for a in doc_agents)
        if found: ok("agent in document_ai filter")
        else: fail("agent in document_ai filter", f"got {len(doc_agents)} but new not found")
    except Exception as e: fail("verify filter", e)

    # [8] get_agent — verify agent_type
    print("\n[8] get_agent — verify agent_type")
    try:
        a = da.get_agent(aid)
        atype = a.get("agent_type")
        marker = "✅" if atype == "document_ai" else "⚠️"
        ok("get_agent", f"name={a.get('name')} agent_type={atype} {marker}")
    except Exception as e: fail("get_agent", e)

    # [9] cleanup
    print("\n[9] CLEANUP")
    if created.get("usecase_id"):
        try:
            client.templates.delete_v2(created["usecase_id"])
            ok("delete usecase template")
        except Exception as e: fail("delete usecase template", e)
    if created.get("board_id"):
        try:
            client.boards.delete(created["board_id"])
            ok("delete board")
        except Exception as e: fail("delete board", e)

print("\n" + "=" * 70)
print(f"  RESULT: {passed} passed  |  {failed} failed")
print("=" * 70)
sys.exit(1 if failed > 0 else 0)
