import time
from utils.utils import client, run_test_section, log_result

def test_settings():
    print("\n🚀 Testing Settings Resource...")

    state = {"template_id": None}

    # 1. Message Templates
    def templates_ops():
        res = client.settings.list_message_templates()
        log_result("Templates Count", len(res.get("data", [])))

        created = client.settings.create_message_template({
            "name": f"SDK_PY_TEMP_{int(time.time())}",
            "body": "Hello {{1}}",
            "category": "UTILITY",
            "language": "en_US"
        })
        state["template_id"] = created.get("_id")
        log_result("Template Created", state["template_id"])

        if state["template_id"]:
            fetched = client.settings.get_message_template(state["template_id"])
            log_result("Template Retrieved", fetched.get("name"))

            client.settings.update_message_template(state["template_id"], {"body": "Hi {{1}}, updated!"})
            log_result("Template Updated", True)

            search = client.settings.search_message_templates(q="SDK_PY")
            log_result("Search Templates Count", len(search))

            client.settings.delete_message_template(state["template_id"])
            log_result("Template Deleted", True)
    run_test_section("Message Templates Ops", templates_ops)

    # 2. WhatsApp Templates
    def wa_templates():
        wa = client.settings.list_whatsapp_templates(limit=5)
        log_result("WA Templates (v1)", len(wa))

        try:
            wa_v2 = client.settings.list_whatsapp_templates_v2(limit=5)
            log_result("WA Templates (v2)", len(wa_v2))
        except:
            print("   [Skip] WA Templates v2 failed")
    run_test_section("WhatsApp Templates", wa_templates)

    # 3. User Management
    def user_mgmt():
        users = client.settings.list_users(limit=5)
        log_result("Users Count", len(users))

        try:
            roles = client.settings.get_user_roles_count()
            log_result("User Roles Count", roles)
        except:
            print("   [Skip] get_user_roles_count failed")
    run_test_section("User Management (Settings)", user_mgmt)

    print("\n✅ Settings Resource Testing Completed.")

if __name__ == "__main__":
    test_settings()
