"""
Document AI resource test — sync + async, runs against prodv2 gateway.
Usage:
    pip install -e ".[dev]"
    python tests/local/test_document_ai.py
"""
import os
import asyncio
from imbrace import ImbraceClient
from imbrace.async_client import AsyncImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c8c27f3b-e147-4735-b641-61e8d3706692")
GATEWAY      = os.environ.get("IMBRACE_GATEWAY_URL",  "https://app-gatewayv2.imbrace.co")
ORG_ID       = os.environ.get("IMBRACE_ORG_ID",       "org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c")

# Small Chinese VAT invoice image
TEST_IMAGE_URL = "https://app-gatewayv2.imbrace.co/files/download/118615471-5b33f600-b7f3-11eb-94a1-78e635e66558.png"

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
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY, organization_id=ORG_ID)
    chat_ai = client.chat_ai

    # [1] List document AI providers
    print("\n[1] List document AI providers")
    vision_model = None
    try:
        providers = chat_ai.list_document_models()
        # unwrap
        lst = providers.get("data", providers) if isinstance(providers, dict) else providers
        lst = lst if isinstance(lst, list) else []
        
        all_models = []
        for p in lst:
            models = p.get("models", [])
            for m in models:
                m["providerName"] = p.get("name")
                all_models.append(m)
        
        vision_models = [m for m in all_models if m.get("is_vision_available") and "image" not in m.get("name", "")]
        
        # prefer gpt-4o
        for m in vision_models:
            if m.get("name") == "gpt-4o":
                vision_model = m.get("name")
                break
        
        if not vision_model:
            for m in vision_models:
                if m.get("name", "").startswith("gpt-4"):
                    vision_model = m.get("name")
                    break
        
        if not vision_model and vision_models:
            vision_model = vision_models[0].get("name")

        ok("list_document_models()", f"{len(lst)} providers, {len(all_models)} models, {len(vision_models)} vision-capable")
    except Exception as e: fail("list_document_models()", e)

    # [2] Process document
    print("\n[2] Process document")
    if not vision_model:
        skip("process_document()", "no vision-capable model found")
    else:
        try:
            res = chat_ai.process_document(
                model_name=vision_model,
                url=TEST_IMAGE_URL,
                organization_id=ORG_ID,
            )
            # Gateway usually returns { success, data: { ... } }
            success = res.get("success")
            data = res.get("data", {})
            if not success:
                raise Exception(str(res))
            keys = list(data.keys())
            ok(f"process_document() {vision_model}", f"extracted keys: {', '.join(keys)}")
        except Exception as e: fail(f"process_document() {vision_model}", e)

# ─────────────────────────────────────────────────────────────────────────────
# Async
# ─────────────────────────────────────────────────────────────────────────────

async def test_async():
    print("\n--- Asynchronous Tests ---")
    async with AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY, organization_id=ORG_ID) as client:
        chat_ai = client.chat_ai
        try:
            res = await chat_ai.list_document_models()
            lst = res.get("data", res) if isinstance(res, dict) else res
            ok("async list_document_models()", f"count={len(lst) if isinstance(lst, list) else '?'}")
        except Exception as e: fail("async list_document_models()", e)

if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())

    print(f"\n{'─' * 55}")
    print(f"  {passed} passed  |  {failed} failed  |  {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
