"""
Document AI test against installed `imbrace` pip package.

Usage:
    pip install ../py/dist/imbrace-X.Y.Z.tar.gz   # local build
    # OR: pip install imbrace                       # from PyPI

    IMBRACE_ACCESS_TOKEN=acc_... \
    IMBRACE_FIN_FILE_ID=fin_xxx \
    PYTHONIOENCODING=utf-8 \
    python tests/test_document_ai.py
"""
import os
import asyncio
from imbrace import ImbraceClient
from imbrace.async_client import AsyncImbraceClient

ACCESS_TOKEN = os.environ["IMBRACE_ACCESS_TOKEN"]
GATEWAY      = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")
FILE_ID      = os.environ.get("IMBRACE_FIN_FILE_ID")
REPORT_ID    = os.environ.get("IMBRACE_FIN_REPORT_ID")

passed = failed = skipped = 0


def ok(label, detail=""):
    global passed
    print(f"  [OK] {label}{('  -> ' + str(detail)[:100]) if detail else ''}")
    passed += 1


def fail(label, err):
    global failed
    print(f"  [FAIL] {label}: {err}")
    failed += 1


def skip(label, reason):
    global skipped
    print(f"  [SKIP] {label} ({reason})")
    skipped += 1


def expect_404(label, fn):
    try:
        fn()
        fail(label, "200 (unexpected — should 404)")
    except Exception as e:
        msg = str(e)
        if "404" in msg or "not found" in msg.lower():
            ok(label, "404 — endpoint reachable, ID not found")
        elif "401" in msg or "403" in msg:
            fail(label, f"auth error: {msg[:80]}")
        else:
            fail(label, e)


def test_sync():
    print("\n--- Sync ---")
    client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)
    d = client.document_ai

    # URL routing smoke
    expect_404("get_file (fake)",   lambda: d.get_file("FAKE_FILE_ID_ROUTING_CHECK"))
    expect_404("get_report (fake)", lambda: d.get_report("FAKE_REPORT_ID_ROUTING_CHECK"))
    expect_404("list_errors (fake)", lambda: d.list_errors("FAKE_FILE_ID_ROUTING_CHECK"))

    # Real CRUD
    if FILE_ID:
        try:
            res = d.get_file(FILE_ID, page=1, limit=5)
            pagination = (res or {}).get("importedFile", {}).get("pagination") or \
                         (res or {}).get("report", {}).get("pagination")
            ok("get_file (real)", f"pagination={pagination}")
        except Exception as e:
            fail("get_file (real)", e)

        try:
            errs = d.list_errors(FILE_ID, limit=10)
            lst = errs if isinstance(errs, list) else (errs or {}).get("data", [])
            ok("list_errors (real)", f"{len(lst)} errors")
        except Exception as e:
            fail("list_errors (real)", e)
    else:
        skip("get_file (real)", "no IMBRACE_FIN_FILE_ID")
        skip("list_errors (real)", "no IMBRACE_FIN_FILE_ID")

    if REPORT_ID:
        try:
            res = d.get_report(REPORT_ID, page=1, limit=5)
            data = (res or {}).get("data", [])
            ok("get_report (real)", f"rows={len(data) if isinstance(data, list) else 'n/a'}")
        except Exception as e:
            fail("get_report (real)", e)
    else:
        skip("get_report (real)", "no IMBRACE_FIN_REPORT_ID")


async def test_async():
    print("\n--- Async ---")
    async with AsyncImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY) as client:
        d = client.document_ai
        try:
            await d.get_file("FAKE_ASYNC_ROUTING")
            fail("async get_file (fake)", "200 unexpected")
        except Exception as e:
            msg = str(e)
            if "404" in msg or "not found" in msg.lower():
                ok("async get_file (fake)", "404 — reachable")
            else:
                fail("async get_file (fake)", e)


if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())
    print(f"\n{'-' * 55}")
    print(f"  {passed} passed | {failed} failed | {skipped} skipped")
    if failed > 0:
        raise SystemExit(1)
