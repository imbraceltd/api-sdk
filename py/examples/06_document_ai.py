"""
Document AI example — runs against prodv2 gateway.
Usage: python examples/06_document_ai.py
"""

import os
import json
from imbrace import ImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c8c27f3b-e147-4735-b641-61e8d3706692")
GATEWAY      = os.environ.get("IMBRACE_GATEWAY_URL",  "https://app-gatewayv2.imbrace.co")
ORG_ID       = os.environ.get("IMBRACE_ORG_ID",       "org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c")

# Small Chinese VAT invoice image — publicly accessible on prodv2
TEST_IMAGE_URL = "https://app-gatewayv2.imbrace.co/files/download/118615471-5b33f600-b7f3-11eb-94a1-78e635e66558.png"

client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY, organization_id=ORG_ID)

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
# List providers (document AI model source)
# ─────────────────────────────────────────────────────────────────────────────

print("\n[1] List document AI providers")
vision_model = None
try:
    providers = client.chat_ai.list_document_models()
    all_models = [m for p in providers for m in p.get("models", [])]
    vision_models = [m for m in all_models if m.get("is_vision_available") and "image" not in m["name"]]
    # prefer gpt-4o for document reading
    vision_model = next((m["name"] for m in vision_models if m["name"] == "gpt-4o"), None) \
        or next((m["name"] for m in vision_models if m["name"].startswith("gpt-4")), None) \
        or (vision_models[0]["name"] if vision_models else None)
    ok("list_document_models()", f"{len(providers)} providers, {len(all_models)} models, {len(vision_models)} vision-capable")
except Exception as e:
    fail("list_document_models()", e)

# ─────────────────────────────────────────────────────────────────────────────
# Process document — vision model from provider
# ─────────────────────────────────────────────────────────────────────────────

print("\n[2] Process document with vision model from provider")
if not vision_model:
    skip("process_document()", "no vision-capable model found in configured providers")
else:
    try:
        res = client.chat_ai.process_document(
            model_name=vision_model,
            url=TEST_IMAGE_URL,
            organization_id=ORG_ID,
        )
        if not res.get("success"):
            raise Exception(json.dumps(res))
        keys = list(res.get("data", {}).keys())
        ok(f"process_document() {vision_model}", f"extracted keys: {', '.join(keys)}")
    except Exception as e:
        fail(f"process_document() {vision_model}", e)

# ─────────────────────────────────────────────────────────────────────────────

client.close()
print(f"\n{'─' * 55}")
print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
if failed > 0:
    raise SystemExit(1)
