import time
from utils.utils import client, run_test_section, log_result

def test_platform():
    print("\n🚀 Testing Platform, Organizations, and Teams...")

    state = {"user_id": None, "team_id": None}

    # 1. Users
    def users_ops():
        me = client.platform.get_me()
        state["user_id"] = me.get("_id") or me.get("id")
        log_result("Me", me)

        users = client.platform.list_users(limit=5)
        log_result("Users Count", len(users.get("data", [])))
    run_test_section("Users Ops", users_ops)

    # 2. Organizations
    run_test_section("platform.list_orgs", lambda: log_result("Orgs Count", len(client.platform.list_orgs(limit=5).get("data", []))))

    # 3. Teams
    def teams_ops():
        team = client.teams.create({
            "name": f"SDK Test Team {int(time.time())}",
            "description": "Created by automated test"
        })
        state["team_id"] = team.get("_id") or team.get("id")
        log_result("Team Created", state["team_id"])

        if state["team_id"]:
            client.teams.update(state["team_id"], {"description": "Updated description"})
            log_result("Team Updated", True)

            client.teams.delete(state["team_id"])
            log_result("Team Deleted", True)
    run_test_section("Teams Ops", teams_ops)

    # 4. System / Apps
    run_test_section("platform.list_apps", lambda: log_result("Apps Count", len(client.platform.list_apps().get("data", []))))

    print("\n✅ Platform Resource Testing Completed.")

if __name__ == "__main__":
    test_platform()
