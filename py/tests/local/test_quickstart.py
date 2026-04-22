"""
Quickstart test — simple surface check against prodv2.
Usage: python tests/local/test_quickstart.py
"""
import os
import json
from imbrace import ImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c10f483f-0e45-4966-a275-2fb0356365e7")
GATEWAY      = os.environ.get("IMBRACE_GATEWAY_URL",  "https://app-gatewayv2.imbrace.co")

client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)

def test(name, fn):
    try:
        res = fn()
        print(f"✓ {name}: {json.dumps(res)[:120]}")
    except Exception as e:
        print(f"✗ {name}: {e}")

if __name__ == "__main__":
    test("boards.list",         lambda: client.boards.list(limit=3))
    test("contacts.list",       lambda: client.contacts.list(limit=3))
    test("chat_ai.list_models", lambda: client.chat_ai.list_models())
    test("ai_agent.list_embedding_files", lambda: client.ai_agent.list_embedding_files())
    test("conversations.get_outstanding", lambda: client.conversations.get_outstanding(business_unit_id="any", limit=3))
