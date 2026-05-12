"""Regression tests for the 9 bug fixes in SDK v1.0.5 (commit ffb3708).

Auth: API Key.

Each section pins one fix from ``fix/sdk-bugs-v1.0.5``. If a regression
sneaks back in, the corresponding step fails with a concrete reason
(not just "backend 400") so it's easy to map back to the offending fix.

  1. document_ai.create_full  — board type "General" (not "DocumentAI"),
                                 schema_fields added one-by-one,
                                 workflow_name default present.
  2. document_ai.update_agent — partial body auto-merges with existing.
  3. ai_agent.suggest_field_types — wire body uses ``file_urls``, not ``fields``.
  4. workflows.list_mcp_servers — project_id arg is optional (auto-resolves).
  5. boards.create_field — returns the new field (not the full Board).
  6. boards.update_item — caller can pass create_item-shape ``fields:[...]``.
  7. boards.create_folder — defaults source_type + parent_folder_id.
  8. workflows.list_invitations — type annotation is ``Literal["PLATFORM","PROJECT"]``.

Creates real resources on the org and cleans up after itself.
"""
from __future__ import annotations
import inspect
import json
import os
import sys
import time
import typing
from typing import Any

from dotenv import load_dotenv

load_dotenv()

from imbrace import ImbraceClient

API_KEY        = os.environ.get("IMBRACE_API_KEY")
ORG_ID         = os.environ.get("IMBRACE_ORGANIZATION_ID")
GATEWAY        = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")
SAMPLE_DOC_URL = os.environ.get("IMBRACE_SAMPLE_DOC_URL", "")
MODEL_ID       = os.environ.get("IMBRACE_DOC_MODEL_ID", "qwen3.5-27b")
PROVIDER_ID    = os.environ.get("IMBRACE_DOC_PROVIDER_ID", "c95e63ad-3c48-4b6a-8ed1-49cf8408088d")

if not API_KEY or not ORG_ID:
    print("Missing IMBRACE_API_KEY or IMBRACE_ORGANIZATION_ID")
    sys.exit(1)

client = ImbraceClient(api_key=API_KEY, organization_id=ORG_ID, gateway=GATEWAY, timeout=60)

passed = 0
failed = 0
skipped_n = 0
failures: list[str] = []
cleanup_board_ids: list[str] = []
cleanup_agent_ids: list[str] = []
cleanup_folder_ids: list[str] = []


def step(label: str, fn, expect_fail: bool = False) -> None:
    global passed, failed
    sys.stdout.write(f"  - {label} ... ")
    sys.stdout.flush()
    try:
        t0 = time.time()
        result = fn()
        dt = int((time.time() - t0) * 1000)
        summary = json.dumps(result, default=str)[:160] if result is not None else ""
        if expect_fail:
            print(f"unexpected pass [{dt}ms]: {summary}")
            failed += 1
            failures.append(f"{label} -> unexpected pass")
        else:
            print(f"OK [{dt}ms] {summary}")
            passed += 1
    except Exception as e:
        detail = str(e)[:300]
        if expect_fail:
            print(f"OK (expected fail [{detail[:120]}])")
            passed += 1
        else:
            print(f"FAIL {detail}")
            failed += 1
            failures.append(f"{label} -> {detail}")


def skip(label: str, reason: str) -> None:
    global skipped_n
    print(f"  - {label}  SKIP: {reason}")
    skipped_n += 1


def section(title: str) -> None:
    print(f"\n== {title} ==")


def _assert(cond: Any, msg: str) -> None:
    if not cond:
        raise AssertionError(f"assertion failed: {msg}")


print(f"\n=== v1.0.5 regression - auth: API KEY (PyPI imbrace) ===")
print(f"gateway={GATEWAY}")
print(f"org={ORG_ID}")

stamp = int(time.time() * 1000)

# ── Fix #1 + #9 — document_ai.create_full ───────────────────────────────────
# Pre-fix: board type "DocumentAI" was rejected by backend enum + adding
# schema_fields at create-time conflicted with auto-Name field's is_identifier.
# (workflow_name default was already present in Py — covered for TS too.)
section("Fix #1+#9: document_ai.create_full (General board, fields one-by-one)")
full_result: dict | None = None


def _create_full() -> dict:
    global full_result
    full_result = client.document_ai.create_full(
        name=f"sdk-regress-docfull-{stamp}",
        description="regression v1.0.5 - auto-cleanup",
        instructions="Extract invoice fields. Return JSON.",
        schema_fields=[
            {"name": "invoice_number", "label": "Invoice Number", "type": "ShortText"},
            {"name": "total",          "label": "Total",          "type": "Number"},
        ],
        model_id=MODEL_ID,
        provider_id=PROVIDER_ID,
        extra_ai_agent={"agent_type": "agent"},
    )
    if full_result.get("board_id"):    cleanup_board_ids.append(full_result["board_id"])
    if full_result.get("ai_agent_id"): cleanup_agent_ids.append(full_result["ai_agent_id"])
    return {
        "board_id":    full_result.get("board_id"),
        "ai_agent_id": full_result.get("ai_agent_id"),
        "usecase_id":  full_result.get("usecase_id"),
    }


step("create_full succeeds end-to-end with 2 schema_fields", _create_full)

if full_result and full_result.get("board_id"):
    board_id = full_result["board_id"]

    def _board_type_general() -> dict:
        board = client.boards.get(board_id)
        _assert(board.get("type") == "General",
                f"expected type 'General', got {board.get('type')!r}")
        return {"type": board.get("type")}
    step("created board has type='General' (not 'DocumentAI')", _board_type_general)

    def _board_has_schema_fields() -> dict:
        board = client.boards.get(board_id)
        names = {f.get("name") for f in board.get("fields", [])}
        _assert("invoice_number" in names, "missing field 'invoice_number'")
        _assert("total" in names,          "missing field 'total'")
        return {"fieldNames": sorted(n for n in names if n)}
    step("created board contains both schema_fields", _board_has_schema_fields)
else:
    skip("created board has type='General'",    "create_full did not return a board_id")
    skip("created board contains schema_fields", "create_full did not return a board_id")

# ── Fix #2 — document_ai.update_agent (auto-merge partial body) ─────────────
# Pre-fix: PUT /assistant_apps/{id} is full-replacement at the backend,
# so partial body would 400 for missing required fields (name, workflow_name).
# Post-fix: SDK auto-fetches existing agent + merges body before PUT.
section("Fix #2: document_ai.update_agent (partial body auto-merges with existing)")
partial_agent_id: str | None = None
partial_agent_name = f"sdk-regress-partial-{stamp}"


def _create_agent_fixture() -> dict:
    global partial_agent_id
    r = client.document_ai.create_agent(
        name=partial_agent_name,
        instructions="Extract any visible field. Return JSON.",
        model_id=MODEL_ID,
        provider_id=PROVIDER_ID,
        schema={"invoice_number": {"type": "string"}},
        description="regression fixture - pre-update",
    )
    partial_agent_id = r.get("_id") or r.get("id")
    if partial_agent_id:
        cleanup_agent_ids.append(partial_agent_id)
    return {"id": partial_agent_id, "name": r.get("name")}


step("create_agent fixture", _create_agent_fixture)

if partial_agent_id:
    def _update_agent_partial() -> dict:
        r = client.document_ai.update_agent(
            partial_agent_id, {"description": "regression fixture - post-update"},
        )
        return {"id": r.get("_id") or r.get("id"), "description": r.get("description")}
    step("update_agent with ONLY {description} succeeds (auto-merge)", _update_agent_partial)

    def _check_post_update() -> dict:
        a = client.document_ai.get_agent(partial_agent_id)
        _assert(a.get("name") == partial_agent_name,
                f"expected name {partial_agent_name!r}, got {a.get('name')!r}")
        _assert(a.get("description") == "regression fixture - post-update",
                f"expected new description, got {a.get('description')!r}")
        return {"name": a.get("name"), "description": a.get("description")}
    step("post-update agent retains original name (merge preserved other fields)", _check_post_update)

    step(
        "update_agent merge_mode='replace' with partial body should fail (opt-out works)",
        lambda: client.document_ai.update_agent(
            partial_agent_id,
            {"description": "this body is intentionally incomplete"},
            merge_mode="replace",
        ),
        expect_fail=True,
    )
else:
    skip("update_agent auto-merge tests", "create_agent fixture did not return an id")

# ── Fix #3 — ai_agent.suggest_field_types ───────────────────────────────────
# Pre-fix: SDK sent {fields:[...]} body, backend expected {file_urls:[...]} → 400.
# Post-fix: SDK signature is suggest_field_types(file_urls=[...]) sending file_urls.
# We also assert the keyword-arg signature, which is enough on its own to
# detect a revert (callers that pass `fields=` will TypeError).
section("Fix #3: ai_agent.suggest_field_types (signature uses file_urls)")


def _signature_check() -> dict:
    sig = inspect.signature(client.ai_agent.suggest_field_types)
    params = list(sig.parameters)
    _assert("file_urls" in params,
            f"expected 'file_urls' param; got {params!r} (looks like signature reverted to 'fields')")
    _assert("fields" not in params,
            f"old 'fields' param still present in signature: {params!r}")
    return {"params": params}


step("suggest_field_types signature uses file_urls (not fields)", _signature_check)

if not SAMPLE_DOC_URL:
    skip("suggest_field_types runtime call", "set IMBRACE_SAMPLE_DOC_URL to a public PDF/image to enable")
else:
    step("suggest_field_types(file_urls=[...]) is accepted by backend",
         lambda: client.ai_agent.suggest_field_types(file_urls=[SAMPLE_DOC_URL]))

# ── Fix #4 — workflows.list_mcp_servers (project_id optional) ───────────────
# Pre-fix: signature was list_mcp_servers(project_id: str) — missing arg = TypeError.
# Post-fix: arg is optional; SDK auto-resolves via resolve_project_id().
section("Fix #4: workflows.list_mcp_servers (project_id optional, auto-resolved)")
step("list_mcp_servers() (no arg) auto-resolves project_id",
     lambda: client.workflows.list_mcp_servers())
step("list_mcp_servers() second call uses cached project_id (no error)",
     lambda: client.workflows.list_mcp_servers())

# ── Fix #5 — boards.create_field returns the new field (not Board) ──────────
# Pre-fix: backend returns the whole Board from POST /board/{id}/board_fields,
# SDK returned that verbatim. Caller's `result["name"]` was the BOARD name.
# Post-fix: SDK extracts the just-added field from board.fields[] by name.
section("Fix #5: boards.create_field returns the new field (not full Board)")
regress_board_name = f"sdk-regress-board-{stamp}"
regress_board_id: str | None = None


def _create_regress_board() -> dict:
    global regress_board_id
    r = client.boards.create(
        name=regress_board_name, description="regression v1.0.5",
        type="General", show_id=False,
    )
    regress_board_id = r.get("_id") or r.get("id")
    if regress_board_id:
        cleanup_board_ids.append(regress_board_id)
    return {"id": regress_board_id, "name": r.get("name"), "type": r.get("type")}


step("create regression board fixture", _create_regress_board)

if regress_board_id:
    field_name = f"regress_field_{stamp}"

    def _create_field_returns_field() -> dict:
        r = client.boards.create_field(regress_board_id, {"name": field_name, "type": "ShortText"})
        _assert(r.get("name") == field_name,
                f"expected field name {field_name!r}, got {r.get('name')!r} "
                f"(smells like Board not BoardField)")
        _assert(r.get("type") != "General",
                f"result type='General' suggests Board leaked through")
        _assert(not isinstance(r.get("fields"), list),
                f"result has .fields[] array - looks like the whole Board was returned")
        return {"name": r.get("name"), "type": r.get("type"), "id": r.get("_id") or r.get("id")}

    step("create_field returns the new field, not the parent board", _create_field_returns_field)

    # ── Fix #6 — boards.update_item auto-translates fields shape ────────────
    section("Fix #6: boards.update_item accepts create_item-shape fields[]")
    id_field_id: str | None = None
    regress_item_id: str | None = None

    def _find_id_field() -> dict:
        global id_field_id
        board = client.boards.get(regress_board_id)
        id_f = next((f for f in board.get("fields", []) if f.get("is_identifier")), None)
        id_field_id = id_f.get("_id") if id_f else None
        return {"id_field_id": id_field_id, "id_field_name": (id_f or {}).get("name")}

    step("locate identifier field on regression board", _find_id_field)

    if id_field_id:
        def _create_item_fixture() -> dict:
            global regress_item_id
            r = client.boards.create_item(regress_board_id, {
                "fields": [{"board_field_id": id_field_id, "value": "regress-initial"}],
            })
            regress_item_id = r.get("_id") or r.get("id")
            return {"id": regress_item_id}

        step("create_item fixture", _create_item_fixture)

        if regress_item_id:
            step(
                "update_item({fields:[{board_field_id,value}]}) succeeds (auto-translated to data[])",
                lambda: client.boards.update_item(regress_board_id, regress_item_id, {
                    "fields": [{"board_field_id": id_field_id, "value": "regress-updated"}],
                }),
            )

            def _verify_update_applied() -> dict:
                it = client.boards.get_item(regress_board_id, regress_item_id)
                raw = json.dumps(it, default=str).lower()
                _assert("regress-updated" in raw,
                        f"item should contain 'regress-updated' after update; got {raw[:200]}")
                return {"ok": True}
            step("post-update item reflects new value", _verify_update_applied)

            step(
                "update_item raw wire shape {fields:[], data:[...]} still passes through",
                lambda: client.boards.update_item(regress_board_id, regress_item_id, {
                    "fields": [],
                    "data":   [{"key": id_field_id, "value": "regress-rewire"}],
                }),
            )
        else:
            skip("update_item regression checks", "create_item fixture did not return an id")
    else:
        skip("update_item regression checks", "no identifier field found on regression board")
else:
    skip("create_field / update_item regression checks", "regression board fixture create failed")

# ── Fix #7 — boards.create_folder defaults source_type + parent_folder_id ───
# Pre-fix: omitting either field 400'd at the backend (enum / null reject).
# Post-fix: SDK auto-fills source_type:"upload" + parent_folder_id:"root".
section("Fix #7: boards.create_folder defaults source_type + parent_folder_id")


def _create_folder_minimal() -> dict:
    r = client.boards.create_folder({
        "name": f"sdk-regress-folder-{stamp}",
        "organization_id": ORG_ID,
    })
    folder_id = r.get("_id") or r.get("id")
    if folder_id:
        cleanup_folder_ids.append(folder_id)
    return {"id": folder_id, "name": r.get("name")}


step("create_folder({name}) only - no source_type/parent_folder_id - succeeds", _create_folder_minimal)

# ── Fix #8 — workflows.list_invitations Literal hint ────────────────────────
# Pre-fix: ``type: str`` (any string accepted at the type level).
# Post-fix: ``type: Literal["PLATFORM", "PROJECT"]`` matching TS signature.
section("Fix #8: workflows.list_invitations type hint is Literal['PLATFORM','PROJECT']")


def _check_literal_hint() -> dict:
    sig = inspect.signature(client.workflows.list_invitations)
    type_param = sig.parameters.get("type")
    _assert(type_param is not None, "list_invitations has no 'type' parameter")
    ann = type_param.annotation
    origin = typing.get_origin(ann)
    args = typing.get_args(ann)
    _assert(origin is typing.Literal,
            f"expected Literal[...] annotation; got origin={origin!r} annotation={ann!r}")
    _assert(set(args) == {"PLATFORM", "PROJECT"},
            f"expected Literal values {{'PLATFORM','PROJECT'}}; got {set(args)!r}")
    return {"annotation": str(ann)}


step("list_invitations type annotation is Literal['PLATFORM','PROJECT']", _check_literal_hint)
# Runtime smoke (best-effort — backend may reject if no project / wrong context)
step("list_invitations('PLATFORM') runtime call is accepted",
     lambda: client.workflows.list_invitations(type="PLATFORM", limit=1))

# ── Cleanup ─────────────────────────────────────────────────────────────────
section("Cleanup")
for aid in cleanup_agent_ids:
    step(f"delete_agent({aid})", lambda _id=aid: (
        client.document_ai.delete_agent(_id) or {"deleted": _id}
    ))
for bid in cleanup_board_ids:
    step(f"boards.delete({bid})", lambda _id=bid: (
        client.boards.delete(_id) or {"deleted": _id}
    ))
for fid in cleanup_folder_ids:
    step(f"boards.delete_folders([{fid}])",
         lambda _id=fid: client.boards.delete_folders([_id]))

# ── Summary ─────────────────────────────────────────────────────────────────
print(f"\n=== Summary ===")
print(f"pass={passed}  fail={failed}  skip={skipped_n}")
if failures:
    print("Failures:")
    for f in failures:
        print(f"  - {f}")
sys.exit(1 if failed > 0 else 0)
