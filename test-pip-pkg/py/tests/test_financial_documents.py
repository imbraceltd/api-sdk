"""
Financial Documents test against installed `imbrace` pip package.

Usage:
    pip install ../py/dist/imbrace-X.Y.Z.whl   # local build
    # OR: pip install imbrace                    # from PyPI

    # Reads from .env if present, or use env vars directly:
    IMBRACE_ACCESS_TOKEN=acc_... \
    IMBRACE_ORGANIZATION_ID=org_... \
    PYTHONIOENCODING=utf-8 \
    python tests/test_financial_documents.py
"""
import os
import asyncio
from pathlib import Path
from imbrace import ImbraceClient
from imbrace.async_client import AsyncImbraceClient
from imbrace.resources.financial_documents import FinancialDocumentsNotDeployedError

# Optional: load .env from this folder if present
try:
    from dotenv import load_dotenv  # type: ignore[import-not-found]
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

try:
    ACCESS_TOKEN: str = os.environ["IMBRACE_ACCESS_TOKEN"]
    ORG_ID:       str = os.environ["IMBRACE_ORGANIZATION_ID"]
except KeyError as e:
    raise SystemExit(f"Required env var not set: {e}")

GATEWAY = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")

passed = failed = 0
not_deployed_count = 0

DUMMY_FILE_ID = "041b3f82-041a-44b5-bfa8-714389688d5e"
DUMMY_REPORT_ID = "041b3f82-041a-44b5-bfa8-714389688d5e"


def ok(label, detail=""):
    global passed
    print(f"  [OK] {label}{('  -> ' + str(detail)[:120]) if detail else ''}")
    passed += 1


def not_deployed(label):
    global passed, not_deployed_count
    print(f"  [NOT DEPLOYED] {label} - Financial Management module unavailable on this gateway")
    passed += 1
    not_deployed_count += 1


def fail(label, err):
    global failed
    print(f"  [FAIL] {label}: {err}")
    failed += 1


def run_expect_not_deployed(label, fn):
    """Run fn — pass if it raises FinancialDocumentsNotDeployedError."""
    try:
        fn()
        fail(label, "no error raised — backend deployed?")
    except FinancialDocumentsNotDeployedError:
        not_deployed(label)
    except Exception as e:
        fail(label, str(e)[:120])


async def arun_expect_not_deployed(label, fn):
    try:
        await fn()
        fail(label, "no error raised — backend deployed?")
    except FinancialDocumentsNotDeployedError:
        not_deployed(label)
    except Exception as e:
        fail(label, str(e)[:120])


# ─────────────────────────────────────────────────────────────────────────────
# SYNC
# ─────────────────────────────────────────────────────────────────────────────

def test_sync():
    print("\n--- Sync ---")
    client = ImbraceClient(
        access_token=ACCESS_TOKEN,
        organization_id=ORG_ID,
        gateway=GATEWAY,
    )

    # Preflight: chat_ai.process_document — extraction (production-ready)
    print("\n  -- Preflight: chat_ai.process_document (one-shot extraction) --")
    try:
        res = client.chat_ai.process_document(
            model_name="gpt-4o",
            url="https://app-gatewayv2.imbrace.co/files/download/118615471-5b33f600-b7f3-11eb-94a1-78e635e66558.png",
            organization_id=ORG_ID,
        )
        keys = list((res or {}).get("data", {}).keys())
        ok("chat_ai.process_document (real image)", f"success={res.get('success')} keys={keys[:5]}")
    except Exception as e:
        fail("chat_ai.process_document (real image)", str(e)[:120])

    # Financial workflow — should throw FinancialDocumentsNotDeployedError
    f = client.financial_documents
    print("\n  -- Financial workflow (experimental) --")
    run_expect_not_deployed("get_file",      lambda: f.get_file(DUMMY_FILE_ID))
    run_expect_not_deployed("get_report",    lambda: f.get_report(DUMMY_REPORT_ID))
    run_expect_not_deployed("list_errors",   lambda: f.list_errors(DUMMY_FILE_ID))
    run_expect_not_deployed("suggest",       lambda: f.suggest({"file_id": DUMMY_FILE_ID}))
    run_expect_not_deployed("fix",           lambda: f.fix({"file_id": DUMMY_FILE_ID}))
    run_expect_not_deployed("reset",         lambda: f.reset())
    run_expect_not_deployed("update_file",   lambda: f.update_file(DUMMY_FILE_ID, {"name": "x"}))
    run_expect_not_deployed("update_report", lambda: f.update_report(DUMMY_REPORT_ID, {"status": "x"}))
    run_expect_not_deployed("delete_file",   lambda: f.delete_file(DUMMY_FILE_ID))
    run_expect_not_deployed("delete_report", lambda: f.delete_report(DUMMY_REPORT_ID))


# ─────────────────────────────────────────────────────────────────────────────
# ASYNC
# ─────────────────────────────────────────────────────────────────────────────

async def test_async():
    print("\n--- Async ---")
    async with AsyncImbraceClient(
        access_token=ACCESS_TOKEN,
        organization_id=ORG_ID,
        gateway=GATEWAY,
    ) as client:
        # Preflight: async chat_ai.process_document
        print("\n  -- Preflight: async chat_ai.process_document --")
        try:
            res = await client.chat_ai.process_document(
                model_name="gpt-4o",
                url="https://app-gatewayv2.imbrace.co/files/download/118615471-5b33f600-b7f3-11eb-94a1-78e635e66558.png",
                organization_id=ORG_ID,
            )
            keys = list((res or {}).get("data", {}).keys())
            ok("async chat_ai.process_document", f"success={res.get('success')} keys={keys[:5]}")
        except Exception as e:
            fail("async chat_ai.process_document", str(e)[:120])

        f = client.financial_documents
        print("\n  -- Financial workflow async (experimental) --")
        await arun_expect_not_deployed("async get_file",      lambda: f.get_file(DUMMY_FILE_ID))
        await arun_expect_not_deployed("async get_report",    lambda: f.get_report(DUMMY_REPORT_ID))
        await arun_expect_not_deployed("async list_errors",   lambda: f.list_errors(DUMMY_FILE_ID))
        await arun_expect_not_deployed("async suggest",       lambda: f.suggest({"file_id": DUMMY_FILE_ID}))
        await arun_expect_not_deployed("async fix",           lambda: f.fix({"file_id": DUMMY_FILE_ID}))
        await arun_expect_not_deployed("async reset",         lambda: f.reset())
        await arun_expect_not_deployed("async update_file",   lambda: f.update_file(DUMMY_FILE_ID, {"name": "x"}))
        await arun_expect_not_deployed("async update_report", lambda: f.update_report(DUMMY_REPORT_ID, {"status": "x"}))
        await arun_expect_not_deployed("async delete_file",   lambda: f.delete_file(DUMMY_FILE_ID))
        await arun_expect_not_deployed("async delete_report", lambda: f.delete_report(DUMMY_REPORT_ID))


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())
    print(f"\n{'-' * 55}")
    print(f"  {passed} passed | {failed} failed")
    if not_deployed_count > 0:
        print(f"  ({not_deployed_count} financial workflow methods NOT DEPLOYED — backend module pending)")
    if failed > 0:
        raise SystemExit(1)
