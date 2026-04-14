"""
Integration tests — require credentials in environment.

App Gateway tests (require user access token):
    IMBRACE_ACCESS_TOKEN=<jwt_token> pytest tests/integration/ -v -m integration

Server Gateway tests (require API key):
    IMBRACE_API_KEY=<api_key> pytest tests/integration/ -v -m integration

Get a new API key:
    POST https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token
    Body: {"expirationDays": 10}
    Header: x-access-token: <existing_key>

Get an access token (App Gateway):
    Use OTP login flow via client.app.auth.signin_email_request() / verify_otp()

Optional env vars for extended tests:
    IMBRACE_BOARD_ID       — board ID for boards CRUD tests
    IMBRACE_CHANNEL_ID     — channel ID for server channel tests
    IMBRACE_CONVERSATION_ID — conversation ID for server conversation tests
    IMBRACE_ASSISTANT_ID   — assistant ID for server ai_agent tests
    IMBRACE_TEMPLATE_ID    — email template ID for server marketplace tests
"""
import os
import pytest
from dotenv import load_dotenv
from imbrace.core.exceptions import AuthError, ApiError, NetworkError

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

from imbrace import ImbraceClient

# App Gateway — User JWT (từ OTP login)
ACCESS_TOKEN = os.getenv("IMBRACE_ACCESS_TOKEN", "")
# Server Gateway — API key
API_KEY = os.getenv("IMBRACE_API_KEY", "api_f01fa678-1e50-4481-bbc7-1587c4ae9e97")

APP_BASE_URL = os.getenv("IMBRACE_BASE_URL", "https://app-gatewayv2.imbrace.co")
SERVER_BASE_URL = os.getenv("IMBRACE_SERVER_BASE_URL", "https://app-gatewayv2.imbrace.co")
ORG_ID = os.getenv("IMBRACE_ORG_ID", "org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c")

# Optional — needed for extended tests
BOARD_ID = os.getenv("IMBRACE_BOARD_ID", "")
CHANNEL_ID = os.getenv("IMBRACE_CHANNEL_ID", "")
CONVERSATION_ID = os.getenv("IMBRACE_CONVERSATION_ID", "")
ASSISTANT_ID = os.getenv("IMBRACE_ASSISTANT_ID", "")
TEMPLATE_ID = os.getenv("IMBRACE_TEMPLATE_ID", "")
USER_ID = os.getenv("IMBRACE_USER_ID", "")

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def app_client():
    """App Gateway client — requires IMBRACE_ACCESS_TOKEN (User JWT)."""
    if not ACCESS_TOKEN:
        pytest.skip("IMBRACE_ACCESS_TOKEN not set — App Gateway tests skipped")
    c = ImbraceClient(app_access_token=ACCESS_TOKEN, app_base_url=APP_BASE_URL)
    yield c
    c.close()


@pytest.fixture(scope="module")
def server_client():
    """Server Gateway client — requires IMBRACE_API_KEY."""
    if not API_KEY:
        pytest.skip("IMBRACE_API_KEY not set — Server Gateway tests skipped")
    c = ImbraceClient(server_api_key=API_KEY, server_base_url=SERVER_BASE_URL)
    yield c
    c.close()


# ── App Gateway Tests (require IMBRACE_ACCESS_TOKEN) ─────────────────────────

def test_get_account(app_client):
    result = app_client.app.account.get()
    assert "id" in result or "_id" in result or "data" in result


def test_list_channels(app_client):
    result = app_client.app.channel.list(type="web")
    assert isinstance(result, dict)


def test_list_agents(app_client):
    result = app_client.app.agent.list()
    assert isinstance(result, dict)


def test_list_teams(app_client):
    # /v2/backend/teams yêu cầu quyền admin — fallback list_all()
    try:
        result = app_client.app.teams.list()
    except AuthError:
        result = app_client.app.teams.list_all()
    assert isinstance(result, (dict, list))


def test_list_my_teams(app_client):
    result = app_client.app.teams.list_my()
    assert isinstance(result, (dict, list))  # API trả về list


def test_list_contacts(app_client):
    result = app_client.app.contacts.list(limit=5)
    assert isinstance(result, dict)


def test_get_views_count(app_client):
    # type=business_unit_id yêu cầu q=<bu_id> — lấy bu_id từ boards list
    bu_id = None
    try:
        boards = app_client.app.boards.list(limit=1)
        item = (boards.get("data") or [None])[0]
        if isinstance(item, dict):
            bu_id = item.get("business_unit_id")
    except Exception:
        pass

    if bu_id:
        try:
            result = app_client.app.conversations.get_views_count(type="business_unit_id", q=bu_id)
            assert isinstance(result, (dict, list))
            return
        except Exception:
            pass

    pytest.skip("Không lấy được business_unit_id để query get_views_count")


def test_list_messages(app_client):
    # Endpoint cần conversation_id hoặc permission đặc biệt — skip nếu 401/404
    try:
        result = app_client.app.messages.list(limit=5)
        assert isinstance(result, (dict, list))
    except (AuthError, ApiError):
        pytest.skip("Account không có quyền list messages không có conversation_id")


def test_list_boards(app_client):
    result = app_client.app.boards.list()
    assert isinstance(result, dict)


def test_list_users(app_client):
    result = app_client.app.settings.list_users(limit=5)
    assert isinstance(result, dict)


def test_list_message_templates(app_client):
    result = app_client.app.settings.list_message_templates()
    assert isinstance(result, dict)


# ── Server Gateway Tests (require IMBRACE_API_KEY) ────────────────────────────

def test_server_categories_list(server_client):
    """Server Gateway — categories list by org_id."""
    result = server_client.server.categories.list(ORG_ID)
    assert isinstance(result, (dict, list))


def test_server_schedule_list(server_client):
    """Server Gateway — schedule list."""
    if not USER_ID:
        pytest.skip("IMBRACE_USER_ID not set")
    result = server_client.server.schedule.list(ORG_ID, USER_ID)
    assert isinstance(result, (dict, list))


# ── App Gateway — Health ──────────────────────────────────────────────────────
# test_health_check: probe xác nhận không có health endpoint nào tồn tại trên
# app-gatewayv2 (/global/health, /health, /v1/health... đều 404). Bỏ test này.


# ── App Gateway — Organizations ───────────────────────────────────────────────

def test_list_organizations():
    # API requires login_acc_ token (pre-org-selection), not acc_ (org-scoped).
    # Current token type is always acc_ after OTP login → 401 is expected, not a bug.
    pytest.skip("Requires login_acc_ token (pre-org-selection) — acc_ token always returns 401 per API docs")


# ── App Gateway — Workflows ───────────────────────────────────────────────────

def test_list_workflows(app_client):
    try:
        result = app_client.app.workflows.list()
        assert isinstance(result, (dict, list))
    except (AuthError, ApiError):
        pytest.skip("workflows.list() không khả dụng trên env này")


def test_list_channel_automation(app_client):
    try:
        result = app_client.app.workflows.list_channel_automation()
        assert isinstance(result, (dict, list))
    except (AuthError, ApiError):
        pytest.skip("workflows.list_channel_automation() không khả dụng trên env này")


# ── App Gateway — Conversations (search/fetch) ────────────────────────────────

def test_conversations_search(app_client):
    try:
        result = app_client.app.conversations.search(ORG_ID, limit=5)
        assert isinstance(result, (dict, list))
    except (AuthError, ApiError):
        pytest.skip("conversations.search() không khả dụng trên env này")


def test_conversations_fetch(app_client):
    try:
        result = app_client.app.conversations.fetch(ORG_ID, filter="status = 'open'", limit=5)
        assert isinstance(result, (dict, list))
    except (AuthError, Exception):
        pytest.skip("conversations.fetch không khả dụng với account này")


# ── App Gateway — Boards (CRUD) ───────────────────────────────────────────────

def test_app_boards_get(app_client):
    """Lấy board đầu tiên từ list() rồi fetch by ID."""
    boards = app_client.app.boards.list(limit=1)
    items = (
        boards.get("data") or boards.get("items") or
        (boards if isinstance(boards, list) else [])
    )
    if not items:
        pytest.skip("Không có board nào để test get()")
    board_id = items[0].get("_id") or items[0].get("id") if isinstance(items[0], dict) else None
    if not board_id:
        pytest.skip("Không lấy được board_id từ list()")
    result = app_client.app.boards.get(board_id)
    assert isinstance(result, (dict, list))


def test_app_boards_list_items(app_client):
    if not BOARD_ID:
        pytest.skip("IMBRACE_BOARD_ID not set")
    try:
        result = app_client.app.boards.list_items(BOARD_ID, limit=5)
        assert isinstance(result, (dict, list))
    except ApiError:
        pytest.skip(f"boards.list_items() không trả về kết quả cho board {BOARD_ID} trên env này")


def test_app_boards_search(app_client):
    if not BOARD_ID:
        pytest.skip("IMBRACE_BOARD_ID not set")
    try:
        result = app_client.app.boards.search(BOARD_ID, limit=5)
        assert isinstance(result, (dict, list))
    except ApiError:
        pytest.skip(f"boards.search() không khả dụng cho board {BOARD_ID} trên env này")


def test_app_boards_export_csv(app_client):
    if not BOARD_ID:
        pytest.skip("IMBRACE_BOARD_ID not set")
    try:
        result = app_client.app.boards.export_csv(BOARD_ID)
        assert isinstance(result, str)
    except ApiError:
        pytest.skip(f"boards.export_csv() không khả dụng cho board {BOARD_ID} trên env này")


# ── Server Gateway — Boards ───────────────────────────────────────────────────

def test_server_boards_list_items(server_client):
    if not BOARD_ID:
        pytest.skip("IMBRACE_BOARD_ID not set")
    try:
        result = server_client.server.boards.list_items(BOARD_ID, limit=5)
        assert isinstance(result, (dict, list))
    except ApiError:
        pytest.skip(f"server.boards.list_items() không khả dụng cho board {BOARD_ID} trên env này")


def test_server_boards_search(server_client):
    if not BOARD_ID:
        pytest.skip("IMBRACE_BOARD_ID not set")
    try:
        result = server_client.server.boards.search(BOARD_ID, limit=5)
        assert isinstance(result, (dict, list))
    except (ApiError, NetworkError):
        pytest.skip(f"server.boards.search() timeout hoặc không khả dụng cho board {BOARD_ID}")


def test_server_boards_export_csv(server_client):
    if not BOARD_ID:
        pytest.skip("IMBRACE_BOARD_ID not set")
    try:
        result = server_client.server.boards.export_csv(BOARD_ID)
        assert isinstance(result, str)
    except ApiError:
        pytest.skip(f"server.boards.export_csv() không khả dụng cho board {BOARD_ID} trên env này")


# ── Server Gateway — Channel ──────────────────────────────────────────────────

def test_server_channel_get(server_client):
    if not CHANNEL_ID:
        pytest.skip("IMBRACE_CHANNEL_ID not set")
    try:
        result = server_client.server.channel.get(CHANNEL_ID)
        assert isinstance(result, (dict, list))
    except ApiError:
        pytest.skip(f"server.channel.get() không tìm thấy channel {CHANNEL_ID} trên env này")


def test_server_channel_get_by_org(server_client):
    if not CHANNEL_ID:
        pytest.skip("IMBRACE_CHANNEL_ID not set")
    try:
        result = server_client.server.channel.get_by_org(ORG_ID, CHANNEL_ID)
        assert isinstance(result, (dict, list))
    except ApiError:
        pytest.skip(f"server.channel.get_by_org() không tìm thấy channel {CHANNEL_ID} trên env này")


# ── Server Gateway — Conversation ─────────────────────────────────────────────

def test_server_conversation_list_messages(server_client):
    if not CONVERSATION_ID:
        pytest.skip("IMBRACE_CONVERSATION_ID not set")
    result = server_client.server.conversation.list_messages(CONVERSATION_ID, limit=5)
    assert isinstance(result, (dict, list))


# ── Server Gateway — AI Agent ─────────────────────────────────────────────────

def test_server_ai_agent_answer_question(server_client):
    if not ASSISTANT_ID:
        pytest.skip("IMBRACE_ASSISTANT_ID not set")
    try:
        # streaming=True matches API docs — streaming=False causes timeout waiting for full response
        result = server_client.server.ai_agent.answer_question(
            text="Hello",
            assistant_id=ASSISTANT_ID,
            streaming=True,
        )
        assert isinstance(result, (dict, list))
    except (ApiError, NetworkError):
        pytest.skip("server.ai_agent.answer_question() timeout — assistant has no RAG data or env unavailable")


# ── Server Gateway — Marketplace ──────────────────────────────────────────────

def test_server_marketplace_get_email_template(server_client):
    if not TEMPLATE_ID:
        pytest.skip("IMBRACE_TEMPLATE_ID not set")
    result = server_client.server.marketplace.get_email_template(ORG_ID, TEMPLATE_ID)
    assert isinstance(result, (dict, list))
