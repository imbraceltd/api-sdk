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
"""
import os
import pytest

from imbrace import ImbraceClient

# App Gateway — User JWT (từ OTP login)
ACCESS_TOKEN = os.getenv("IMBRACE_ACCESS_TOKEN", "")
# Server Gateway — API key
API_KEY = os.getenv("IMBRACE_API_KEY", "api_f01fa678-1e50-4481-bbc7-1587c4ae9e97")

APP_BASE_URL = os.getenv("IMBRACE_BASE_URL", "https://app-gatewayv2.imbrace.co")
SERVER_BASE_URL = os.getenv("IMBRACE_SERVER_BASE_URL", "https://app-gatewayv2.imbrace.co")
ORG_ID = os.getenv("IMBRACE_ORG_ID", "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd")

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
    result = app_client.app.teams.list()
    assert isinstance(result, dict)


def test_list_my_teams(app_client):
    result = app_client.app.teams.list_my()
    assert isinstance(result, dict)


def test_list_contacts(app_client):
    result = app_client.app.contacts.list(limit=5)
    assert isinstance(result, dict)


def test_get_views_count(app_client):
    result = app_client.app.conversations.get_views_count()
    assert isinstance(result, dict)


def test_list_messages(app_client):
    result = app_client.app.messages.list(limit=5)
    assert isinstance(result, dict)


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
    import os
    user_id = os.getenv("IMBRACE_USER_ID", "")
    if not user_id:
        pytest.skip("IMBRACE_USER_ID not set")
    result = server_client.server.schedule.list(ORG_ID, user_id)
    assert isinstance(result, dict)
