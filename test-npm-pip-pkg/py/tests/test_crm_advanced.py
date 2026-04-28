import time
from utils.utils import client, run_test_section, log_result

def test_crm_advanced():
    print("\n🚀 STARTING: CRM ADVANCED & RELATIONS TEST (PY)")

    state = {"contact_id": None, "conversation_id": None, "board1": None, "board2": None}

    # 1. Contacts Advanced
    def contacts_advanced():
        res = client.contacts.list(limit=1)
        data = res.get("data", [])
        if data:
            state["contact_id"] = data[0].get("_id") or data[0].get("id")
            log_result("Using Contact", state["contact_id"])

            comments = client.contacts.get_comments(state["contact_id"])
            log_result("Contact Comments", len(comments))

            activities = client.contacts.get_activities(state["contact_id"])
            log_result("Contact Activities", len(activities))

            files = client.contacts.get_files(state["contact_id"])
            log_result("Contact Files", len(files))

            convs = client.contacts.get_conversations(state["contact_id"])
            log_result("Contact Conversations", len(convs))
            if convs:
                state["conversation_id"] = convs[0].get("_id") or convs[0].get("id")
        else:
            print("   ⚠️ No contacts found.")
    run_test_section("Contacts Advanced", contacts_advanced)

    # 2. Board Relations
    def board_relations():
        ts = int(time.time())
        b1 = client.boards.create(name=f"SDK Parent Board {ts}")
        b2 = client.boards.create(name=f"SDK Related Board {ts}")
        state["board1"] = b1.get("_id") or b1.get("id")
        state["board2"] = b2.get("_id") or b2.get("id")

        if state["board1"] and state["board2"]:
            # Logic to link items would go here
            log_result("Boards Created for Relation Test", f"{state['board1']}, {state['board2']}")

            # Cleanup boards
            client.boards.delete(state["board1"])
            client.boards.delete(state["board2"])
            print("   Boards deleted.")
    run_test_section("Board Relations", board_relations)

    print("\n✅ CRM Advanced Test Completed.")

if __name__ == "__main__":
    test_crm_advanced()
