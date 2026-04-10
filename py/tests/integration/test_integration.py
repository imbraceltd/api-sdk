"""
Integration tests — require a valid IMBRACE_API_KEY in the environment.

Run with:
    IMBRACE_API_KEY=api_xxx pytest py/tests/test_integration.py -v -m integration

Get a new API key:
    POST https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token
    Body: {"expirationDays": 10}
    Header: x-access-token: <existing_key>
"""
import os
import pytest

from imbrace import ImbraceClient

API_KEY = os.getenv("IMBRACE_API_KEY", "")
BASE_URL = os.getenv("IMBRACE_BASE_URL", "https://app-gatewayv2.imbrace.co")
ORG_ID = os.getenv("IMBRACE_ORG_ID", "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd")

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def client():
    if not API_KEY:
        pytest.skip("IMBRACE_API_KEY not set")
    c = ImbraceClient(api_key=API_KEY, base_url=BASE_URL)
    yield c
    c.close()


# ── Account ──────────────────────────────────────────────────────────────────

def test_get_account(client):
    result = client.account.get()
    assert "id" in result or "_id" in result or "data" in result


# ── Channels ─────────────────────────────────────────────────────────────────

def test_list_channels(client):
    result = client.channel.list(type="web")
    assert isinstance(result, dict)


# ── Agents (Templates) ───────────────────────────────────────────────────────

def test_list_agents(client):
    result = client.agent.list()
    assert isinstance(result, dict)


# ── Teams ─────────────────────────────────────────────────────────────────────

def test_list_teams(client):
    result = client.teams.list()
    assert isinstance(result, dict)


def test_list_my_teams(client):
    result = client.teams.list_my()
    assert isinstance(result, dict)


# ── Contacts ─────────────────────────────────────────────────────────────────

def test_list_contacts(client):
    result = client.contacts.list(limit=5)
    assert isinstance(result, dict)


# ── Conversations ─────────────────────────────────────────────────────────────

def test_get_views_count(client):
    result = client.conversations.get_views_count()
    assert isinstance(result, dict)


# ── Messages ─────────────────────────────────────────────────────────────────

def test_list_messages(client):
    result = client.messages.list(limit=5)
    assert isinstance(result, dict)


# ── Boards ────────────────────────────────────────────────────────────────────

def test_list_boards(client):
    result = client.boards.list()
    assert isinstance(result, dict)


# ── Settings ─────────────────────────────────────────────────────────────────

def test_list_users(client):
    result = client.settings.list_users(limit=5)
    assert isinstance(result, dict)


def test_list_message_templates(client):
    result = client.settings.list_message_templates()
    assert isinstance(result, dict)
