# -*- coding: utf-8 -*-
"""
Probe script — điều tra 10 skipped tests và tìm hướng khắc phục.

Chạy: python scripts/probe_skipped.py

Skips cần điều tra:
  [1]  test_get_views_count      — tìm valid type value
  [2]  test_list_messages        — tìm conversation_id có quyền
  [3]  test_health_check         — tìm health endpoint đúng
  [4]  test_list_organizations   — kiểm tra quyền account
  [5]  test_list_workflows       — kiểm tra endpoint + env
  [6]  test_list_channel_automation — kiểm tra endpoint + env
  [7]  test_conversations_search — kiểm tra meilisearch availability
  [8]  test_conversations_fetch  — kiểm tra meilisearch availability
  [9]  test_server_boards_search — probe timeout / index
  [10] test_server_ai_agent      — kiểm tra assistant + timeout

Env vars được cập nhật:
  IMBRACE_USER_ID, IMBRACE_BOARD_ID, IMBRACE_CHANNEL_ID,
  IMBRACE_CONVERSATION_ID, IMBRACE_ASSISTANT_ID
"""
import os
import sys
import httpx
from pathlib import Path
from dotenv import load_dotenv, set_key

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

from imbrace import ImbraceClient
from imbrace.core.exceptions import AuthError, ApiError

ACCESS_TOKEN    = os.getenv("IMBRACE_ACCESS_TOKEN", "")
API_KEY         = os.getenv("IMBRACE_API_KEY", "")
BASE_URL        = os.getenv("IMBRACE_BASE_URL", "https://app-gatewayv2.imbrace.co")
ORG_ID          = os.getenv("IMBRACE_ORG_ID", "")
BOARD_ID        = os.getenv("IMBRACE_BOARD_ID", "")
CHANNEL_ID      = os.getenv("IMBRACE_CHANNEL_ID", "")
CONVERSATION_ID = os.getenv("IMBRACE_CONVERSATION_ID", "")
ASSISTANT_ID    = os.getenv("IMBRACE_ASSISTANT_ID", "")
ENV_FILE        = Path(__file__).parent.parent / ".env"

if not ACCESS_TOKEN:
    print("ERROR: IMBRACE_ACCESS_TOKEN chưa set. Chạy get_access_token.py trước.")
    sys.exit(1)

app    = ImbraceClient(app_access_token=ACCESS_TOKEN, app_base_url=BASE_URL)
server = ImbraceClient(server_api_key=API_KEY, server_base_url=BASE_URL) if API_KEY else None


def _extract_id(obj: dict) -> str | None:
    return obj.get("_id") or obj.get("id") or obj.get("public_id")


def _first_item(data) -> dict | None:
    if isinstance(data, list):
        return data[0] if data else None
    if isinstance(data, dict):
        items = data.get("data") or data.get("items") or data.get("results") or []
        if isinstance(items, list) and items:
            return items[0]
        if isinstance(items, dict):
            return items
    return None


def save(key: str, value: str):
    set_key(str(ENV_FILE), key, value)
    print(f"    ✓ Saved {key}={value[:50]}{'...' if len(value) > 50 else ''}")


def _raw_get(path: str, params: dict | None = None, timeout: float = 10) -> httpx.Response | None:
    try:
        return httpx.get(
            f"{BASE_URL}{path}",
            headers={"x-access-token": ACCESS_TOKEN},
            params=params or {},
            timeout=timeout,
        )
    except Exception as e:
        print(f"    ERROR: {e}")
        return None


def _raw_post(path: str, body: dict, timeout: float = 10, api_key: bool = False) -> httpx.Response | None:
    token = API_KEY if api_key else ACCESS_TOKEN
    try:
        return httpx.post(
            f"{BASE_URL}{path}",
            headers={"x-access-token": token, "Content-Type": "application/json"},
            json=body,
            timeout=timeout,
        )
    except httpx.TimeoutException:
        print(f"    TIMEOUT after {timeout}s")
        return None
    except Exception as e:
        print(f"    ERROR: {e}")
        return None


print("=" * 70)
print(f"BASE_URL : {BASE_URL}")
print(f"ORG_ID   : {ORG_ID}")
print(f"BOARD_ID : {BOARD_ID or '(not set)'}")
print(f"ASSISTANT: {ASSISTANT_ID or '(not set)'}")
print("=" * 70)


# ─── [1] test_get_views_count — tìm valid type value ─────────────────────────
print("\n[1] SKIP: test_get_views_count — probe valid type values")
ALL_TYPES = [
    "mine", "team", "unassigned", "assigned", "all",
    "business_unit_id", "open", "closed", "pending", "resolved",
    "snoozed", "inbox", "spam", "trash", "overdue", "soon_to_be",
]
found_type = None
for t in ALL_TYPES:
    resp = _raw_get("/v2/backend/team_conversations/_views_count", {"type": t})
    if resp and resp.status_code < 300:
        print(f"    ✓ type={t!r} → OK: {str(resp.json())[:80]}")
        found_type = t
        break
    else:
        code = resp.status_code if resp else "ERR"
        body = resp.text[:60] if resp else ""
        print(f"    ✗ type={t!r} → {code} {body}")

if found_type:
    print(f"\n  → FIX: cập nhật test dùng type={found_type!r}")
else:
    print("\n  → RESULT: không có type nào hợp lệ — endpoint cần quyền đặc biệt hoặc sai env")


# ─── [2] test_list_messages — tìm conversation_id có quyền ───────────────────
print("\n[2] SKIP: test_list_messages — probe message endpoint với conversation_id")
conv_id = CONVERSATION_ID

# thử lấy conversation_id nếu chưa có
if not conv_id:
    resp = _raw_get("/v2/backend/team_conversations", {"limit": 1})
    if resp and resp.status_code < 300:
        item = _first_item(resp.json())
        conv_id = _extract_id(item) if item else None
        if conv_id:
            save("IMBRACE_CONVERSATION_ID", conv_id)

if conv_id:
    # thử list messages của conversation cụ thể
    resp = _raw_get(f"/v2/backend/team_conversations/{conv_id}/messages", {"limit": 1})
    if resp:
        print(f"    /v2/backend/team_conversations/{{id}}/messages → {resp.status_code}: {resp.text[:100]}")
    # thử endpoint khác
    resp2 = _raw_get("/v2/backend/messages", {"limit": 1, "conversation_id": conv_id})
    if resp2:
        print(f"    /v2/backend/messages?conversation_id → {resp2.status_code}: {resp2.text[:100]}")
else:
    print("    WARN: không có conversation_id để probe")

resp3 = _raw_get("/v2/backend/messages", {"limit": 1})
if resp3:
    print(f"    /v2/backend/messages (no conv_id) → {resp3.status_code}: {resp3.text[:80]}")

print("  → FIX: cập nhật test_list_messages để truyền conversation_id nếu endpoint yêu cầu")


# ─── [3] test_health_check — tìm health endpoint đúng ────────────────────────
print("\n[3] SKIP: test_health_check — probe health endpoint variations")
health_paths = [
    "/global/health",
    "/health",
    "/api/health",
    "/v1/health",
    "/v1/backend/health",
    "/ping",
    "/status",
]
found_health = None
for path in health_paths:
    resp = _raw_get(path)
    if resp:
        print(f"    {path} → {resp.status_code}: {resp.text[:60]}")
        if resp.status_code < 300:
            found_health = path
            break
    else:
        print(f"    {path} → ERROR")

if found_health:
    print(f"\n  → FIX: đổi health.py endpoint thành {found_health!r}")
else:
    print("\n  → RESULT: không tìm được health endpoint — cần hỏi Dan hoặc bỏ test này")


# ─── [4] test_list_organizations — kiểm tra quyền account ────────────────────
print("\n[4] SKIP: test_list_organizations — kiểm tra role / quyền account")
try:
    account = app.app.account.get()
    item = _first_item(account) or account
    user_id = _extract_id(item)
    role    = item.get("role") or item.get("roles") or item.get("type") or "(không có field role)"
    print(f"    user_id : {user_id}")
    print(f"    role    : {role}")
    print(f"    raw keys: {list(item.keys())[:15]}")
    if user_id:
        save("IMBRACE_USER_ID", user_id)
except Exception as e:
    print(f"    ERROR: {e}")

resp = _raw_get("/v2/backend/organizations", {"limit": 1})
if resp:
    print(f"    GET /v2/backend/organizations → {resp.status_code}: {resp.text[:100]}")
    if resp.status_code < 300:
        print("  → FIX: endpoint OK nhưng test đang catch AuthError — cần thêm ApiError hoặc bỏ catch")
    elif resp.status_code in (401, 403):
        print("  → RESULT: cần account admin — dùng token khác hoặc bỏ test")
    else:
        print(f"  → RESULT: lỗi {resp.status_code} — kiểm tra endpoint")


# ─── [5+6] test_list_workflows + test_list_channel_automation — probe endpoint ─
print("\n[5+6] SKIP: test_list_workflows / test_list_channel_automation — probe endpoint")
for path, label in [
    ("/v1/backend/workflows", "workflows.list"),
    ("/v1/backend/workflows/channel_automation", "workflows.list_channel_automation"),
    ("/v2/backend/workflows", "workflows v2"),
    ("/v3/backend/workflows", "workflows v3"),
]:
    resp = _raw_get(path)
    if resp:
        print(f"    {label} [{path}] → {resp.status_code}: {resp.text[:80]}")

print("  → FIX: nếu tất cả đều 404/500 thì endpoint không khả dụng trên env này")
print("         thử đổi IMBRACE_BASE_URL sang app-gateway.dev.imbrace.co")


# ─── [7+8] test_conversations_search + fetch — probe meilisearch ─────────────
print("\n[7+8] SKIP: test_conversations_search / fetch — probe meilisearch")
# thử org_id hiện tại
resp = _raw_post(f"/v1/backend/meilisearch/{ORG_ID}/search", {"limit": 1})
if resp:
    print(f"    meilisearch search [{ORG_ID}] → {resp.status_code}: {resp.text[:100]}")
    if resp.status_code < 300:
        print("  → FIX: endpoint OK — cập nhật test truyền đúng ORG_ID")
    elif resp.status_code == 404:
        print("  → RESULT: org này chưa được index trên Meilisearch")
        print("             thử với org khác hoặc env prod")

# probe fetch
resp2 = _raw_post(f"/v1/backend/meilisearch/{ORG_ID}/fetch", {"filter": "", "limit": 1})
if resp2:
    print(f"    meilisearch fetch [{ORG_ID}] → {resp2.status_code}: {resp2.text[:100]}")


# ─── [9] test_server_boards_search — probe timeout / index ───────────────────
print(f"\n[9] SKIP: test_server_boards_search — probe board search timeout (BOARD_ID={BOARD_ID or 'not set'})")
if server and BOARD_ID:
    # thử với timeout ngắn trước để xem có response không
    for t in [5, 15, 30]:
        print(f"    Thử timeout={t}s ...")
        resp = None
        try:
            resp = httpx.post(
                f"{BASE_URL}/3rd/board_search/{BOARD_ID}/search",
                headers={"x-access-token": API_KEY},
                json={"limit": 1, "matchingStrategy": "last", "offset": 0},
                timeout=t,
            )
        except httpx.TimeoutException:
            print(f"    → TIMEOUT sau {t}s")
            continue
        except Exception as e:
            print(f"    → ERROR: {e}")
            break
        print(f"    → {resp.status_code}: {resp.text[:100]}")
        if resp.status_code < 300:
            print(f"  → FIX: tăng timeout trong HttpTransport lên >={t}s")
        break
    else:
        print("  → RESULT: endpoint luôn timeout — board này chưa có data indexing hoặc meilisearch chậm")
        print("             thử BOARD_ID khác có data thực sự")
else:
    print("    SKIP: cần API_KEY và BOARD_ID")


# ─── [10] test_server_ai_agent_answer_question — probe assistant + timeout ────
print(f"\n[10] SKIP: test_server_ai_agent_answer_question — probe assistant (ASSISTANT_ID={ASSISTANT_ID or 'not set'})")

# thử lấy assistant_id mới từ agent list
print("    Probe AI Agent list (/v2/backend/templates) ...")
try:
    result = app.app.agent.list()
    items_raw = result.get("data") or result.get("items") or (result if isinstance(result, list) else [])
    agents = items_raw if isinstance(items_raw, list) else [items_raw]
    print(f"    Tìm thấy {len(agents)} agents")
    for ag in agents[:5]:
        aid = ag.get("assistant_id") if isinstance(ag, dict) else None
        name = (ag.get("title") or ag.get("name") or "") if isinstance(ag, dict) else ""
        print(f"      assistant_id={aid!r} name={name!r}")
    # save cái đầu tiên có assistant_id
    for ag in agents:
        if isinstance(ag, dict) and ag.get("assistant_id"):
            save("IMBRACE_ASSISTANT_ID", ag["assistant_id"])
            ASSISTANT_ID = ag["assistant_id"]
            break
except (AuthError, ApiError) as e:
    print(f"    SKIP: {e}")
except Exception as e:
    print(f"    ERROR: {e}")

# thử call AI với timeout tăng dần
if server and ASSISTANT_ID:
    for t in [10, 30]:
        print(f"    Thử answer_question timeout={t}s ...")
        try:
            resp = httpx.post(
                f"{BASE_URL}/3rd/ai-service/rag/answer_question",
                headers={"x-access-token": API_KEY, "Content-Type": "application/json"},
                json={"text": "Hello", "assistant_id": ASSISTANT_ID,
                      "instructions": "", "role": "user", "streaming": False},
                timeout=t,
            )
            print(f"    → {resp.status_code}: {resp.text[:120]}")
            if resp.status_code < 300:
                print(f"  → FIX: tăng timeout trong HttpTransport lên >={t}s")
            break
        except httpx.TimeoutException:
            print(f"    → TIMEOUT sau {t}s")
        except Exception as e:
            print(f"    → ERROR: {e}")
            break
    else:
        print("  → RESULT: AI endpoint luôn timeout — assistant_id này chưa có RAG data")
        print("             cần ASSISTANT_ID có data đã index, hoặc hỏi Dan")
else:
    print("    SKIP: cần API_KEY và ASSISTANT_ID")


# ─── Summary ──────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY — hướng khắc phục:")
print("  [1] get_views_count  : xem type nào OK ở trên, cập nhật test")
print("  [2] list_messages    : truyền conversation_id vào messages.list()")
print("  [3] health_check     : xem path nào OK ở trên, sửa health.py")
print("  [4] list_orgs        : cần admin token hoặc skip test này")
print("  [5+6] workflows      : đổi BASE_URL → app-gateway.dev.imbrace.co")
print("  [7+8] conv search    : đổi BASE_URL → app-gateway.dev.imbrace.co")
print("  [9] server search    : tăng timeout hoặc dùng board có index data")
print("  [10] ai_agent        : dùng assistant_id có RAG data + tăng timeout")
print("=" * 70)

app.close()
if server:
    server.close()
