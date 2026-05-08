"""E2E test of client.document_ai across SANDBOX + CLOUD environments."""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "py" / "src"))

from imbrace import ImbraceClient

ENVS = [
    {
        "label":   "SANDBOX (org_imbrace — Document AI module ENABLED)",
        "gateway": "https://app-gateway.sandbox.imbrace.co",
        "token":   "acc_3ceec9cb-17bc-4031-98b2-adf135b792a4",
        "org":     "org_imbrace",
    },
    {
        "label":   "CLOUD   (org_8f4ed5b3 — Document AI module NOT yet deployed)",
        "gateway": "https://app-gatewayv2.imbrace.co",
        "token":   "acc_8310ed73-107c-47d1-b5bb-dbc281b32ab2",
        "org":     "org_8f4ed5b3-0666-46a9-89ad-e17b24a5be4e",
    },
]
SAMPLE_URL = "https://app-gatewayv2.imbrace.co/files/download/118615471-5b33f600-b7f3-11eb-94a1-78e635e66558.png"


def run_env(env):
    print()
    print("═" * 76)
    print(f"  ENV: {env['label']}")
    print(f"  GW:  {env['gateway']}")
    print(f"  ORG: {env['org']}")
    print("═" * 76)
    client = ImbraceClient(
        access_token=env["token"], organization_id=env["org"],
        gateway=env["gateway"], timeout=120,
    )
    da = client.document_ai
    pp = ff = ef = 0
    def ok(label, detail=""):
        nonlocal pp; pp += 1
        print(f"  [PASS] {label}{('  -> ' + str(detail)[:120]) if detail else ''}")
    def fail(label, err):
        nonlocal ff; ff += 1
        print(f"  [FAIL] {label}: {str(err)[:200]}")
    def expect_fail(label, err):
        nonlocal ef; ef += 1
        print(f"  [EXPECTED FAIL] {label}: {str(err)[:160]}")

    # READ-ONLY
    print("\n  ── READ-ONLY ─────────────────────────────────────────")
    provider_id = None
    model_id = "qwen3.5:27b"
    try:
        providers = client.ai.list_providers()
        ok("client.ai.list_providers()", f"{len(providers)} providers")
        custom = [p for p in providers if p.get("provider_id") != "system"]
        for p in custom:
            ms = p.get("models") or []
            for m in ms:
                nm = m.get("name", "")
                if nm.startswith("qwen") or nm == "Default":
                    provider_id = p.get("provider_id"); model_id = nm; break
            if provider_id: break
        if not provider_id and custom:
            provider_id = custom[0].get("provider_id")
            model_id = (custom[0].get("models") or [{}])[0].get("name") or "qwen3.5:27b"
    except Exception as e: fail("client.ai.list_providers()", e)

    try:
        agents = da.list_agents()
        ok("client.document_ai.list_agents()", f"{len(agents)} total")
    except Exception as e: fail("client.document_ai.list_agents()", e)

    try:
        doc_ai = da.list_agents(document_ai_only=True)
        ok("client.document_ai.list_agents(document_ai_only=True)", f"{len(doc_ai)} Document AI")
    except Exception as e: fail("client.document_ai.list_agents(document_ai_only=True)", e)

    # PROCESS
    print("\n  ── PROCESS DOCUMENT (gpt-4o) ─────────────────────────")
    try:
        res = da.process(url=SAMPLE_URL, organization_id=env["org"], model_name="gpt-4o")
        keys = list((res or {}).get("data", {}).keys())[:5]
        ok("client.document_ai.process()", f"success={res.get('success')} keys={keys}")
    except Exception as e: fail("client.document_ai.process()", e)

    try:
        res = da.suggest_schema(url=SAMPLE_URL, organization_id=env["org"])
        keys = list((res or {}).get("data", {}).keys())[:5]
        ok("client.document_ai.suggest_schema()", f"success={res.get('success')} keys={keys}")
    except Exception as e: fail("client.document_ai.suggest_schema()", e)

    # CREATE_FULL
    print("\n  ── CREATE_FULL (Board + UseCase + Assistant atomic) ─")
    created = None
    test_name = f"SDK_TEST_DocAI_{os.getpid()}_{env['org'][:10]}"
    if provider_id:
        try:
            created = da.create_full(
                name=test_name,
                description="SDK E2E test — auto-deleted",
                instructions="Extract receipt: vendor, total.",
                schema_fields=[
                    {"name": "vendor", "type": "ShortText", "is_identifier": True, "is_unique_identifier": False, "is_default": False},
                    {"name": "total", "type": "Number", "is_identifier": False, "is_unique_identifier": False, "is_default": False},
                ],
                model_id=str(model_id), provider_id=str(provider_id),
            )
            ok("client.document_ai.create_full()",
               f"board={(created.get('board_id') or '')[:30]} a={(created.get('assistant_id') or '')[:30]}")
        except Exception as e:
            if "DocumentAI" in str(e) or "document_ai" in str(e) or "enum" in str(e):
                expect_fail("client.document_ai.create_full()", e)
            else:
                fail("client.document_ai.create_full()", e)

    if created and created.get("assistant_id"):
        aid = created["assistant_id"]

        try:
            doc_agents = da.list_agents(document_ai_only=True)
            found = any((a.get("id") or a.get("_id")) == aid for a in doc_agents)
            if found: ok("verify created agent in document_ai_only filter")
            else: fail("verify filter", f"got {len(doc_agents)} but new not found")
        except Exception as e: fail("verify filter", e)

        try:
            a = da.get_agent(aid)
            ok("client.document_ai.get_agent()",
               f"name={a.get('name')} model={a.get('model_id')} agent_type={a.get('agent_type')}")
        except Exception as e: fail("client.document_ai.get_agent()", e)

        # CLEANUP
        print("\n  ── CLEANUP ───────────────────────────────────────────")
        if created.get("usecase_id"):
            try:
                client.templates.delete_v2(created["usecase_id"])
                ok("client.templates.delete_v2()")
            except Exception as e: fail("cleanup template", e)
        if created.get("board_id"):
            try:
                client.boards.delete(created["board_id"])
                ok("client.boards.delete()")
            except Exception as e: fail("cleanup board", e)

    return pp, ff, ef


total_p = total_f = total_e = 0
for env in ENVS:
    p, f, e = run_env(env)
    total_p += p; total_f += f; total_e += e

print()
print("═" * 76)
print(f"  OVERALL: {total_p} passed  |  {total_e} expected-fail  |  {total_f} unexpected-fail")
print("═" * 76)
sys.exit(1 if total_f > 0 else 0)
