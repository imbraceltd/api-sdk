"""Verify renamed AI Agent methods work end-to-end against real backend."""
import time
from imbrace import ImbraceClient

ACCESS_TOKEN = "acc_c8c27f3b-e147-4735-b641-61e8d3706692"
GATEWAY = "https://app-gatewayv2.imbrace.co"

client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)

ts = int(time.time() * 1000)
created_id = None


def step(label, fn):
    try:
        r = fn()
        s = str(r)[:140] if r is not None else ""
        print(f"✓ {label}: {s}")
        return r
    except Exception as e:
        print(f"✗ {label}: {e}")
        return None


print(f"\n── chat_ai AI Agent CRUD lifecycle (ts={ts}) ──")

created = step("create_ai_agent", lambda: client.chat_ai.create_ai_agent({
    "name":          f"SDK_PY_RENAME_TEST_{ts}",
    "workflow_name": f"sdk_py_rename_test_{ts}",
    "provider_id":   "system",
    "model_id":      "gpt-4o",
    "description":   "rename verification — auto-deleted",
}))
if created:
    created_id = created.get("id") or created.get("_id")

if created_id:
    step("get_ai_agent", lambda: client.chat_ai.get_ai_agent(created_id))

    def _list_check():
        lst = client.chat_ai.list_ai_agents()
        found = any((a.get("id") or a.get("_id")) == created_id for a in lst)
        return {"found": found, "total": len(lst)}
    step("list_ai_agents (contains new)", _list_check)

    step("update_ai_agent_instructions", lambda: client.chat_ai.update_ai_agent_instructions(
        created_id, "Updated instructions.",
    ))

    step("update_ai_agent (rename)", lambda: client.chat_ai.update_ai_agent(created_id, {
        "name":          f"SDK_PY_RENAME_TEST_{ts}_renamed",
        "workflow_name": f"sdk_py_rename_test_{ts}",
    }))

    step("delete_ai_agent", lambda: client.chat_ai.delete_ai_agent(created_id))

print("\nDone.")
