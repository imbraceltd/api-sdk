import time
from utils.utils import client, run_test_section, log_result

def test_agent():
    print("\n🚀 Testing Agent Templates and Use Cases...")

    state = {"template_id": None, "use_case_id": None}

    # 1. Templates
    def templates_ops():
        templates = client.agent.list()
        log_result("Templates Count", len(templates))

        created = client.agent.create({
            "assistant": {
                "name": f"SDK Test Agent {int(time.time())}",
                "instructions": "You are a test agent.",
                "model": "gpt-4o-mini"
            },
            "usecase": {
                "title": f"SDK Test UseCase {int(time.time())}",
                "category": "Test"
            }
        })
        state["template_id"] = created.get("_id") or created.get("id")
        log_result("Template Created", state["template_id"])

        if state["template_id"]:
            client.agent.get(state["template_id"])
            client.agent.update(state["template_id"], {
                "assistant": {"instructions": "Updated instructions"}
            })
            log_result("Template Ops Verified", True)

            client.agent.delete(state["template_id"])
            log_result("Template Deleted", True)
    run_test_section("Templates Ops", templates_ops)

    # 2. Use Cases
    def use_cases_ops():
        use_cases = client.agent.list_use_cases()
        log_result("UseCases Count", len(use_cases))

        created = client.agent.create_use_case({
            "name": f"SDK Custom UC {int(time.time())}",
            "description": "Test description"
        })
        state["use_case_id"] = created.get("_id") or created.get("id")
        log_result("UseCase Created", state["use_case_id"])

        if state["use_case_id"]:
            client.agent.get_use_case(state["use_case_id"])
            client.agent.update_use_case(state["use_case_id"], {
                "description": "Updated UC description"
            })
            log_result("UseCase Ops Verified", True)

            client.agent.delete_use_case(state["use_case_id"])
            log_result("UseCase Deleted", True)
    run_test_section("Use Cases Ops", use_cases_ops)

    print("\n✅ Agent Resource Testing Completed.")

if __name__ == "__main__":
    test_agent()
