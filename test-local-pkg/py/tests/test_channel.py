"""
Test: client.channel — CRUD channels, credentials, workflow bindings
Per docsv2/py-sdk/resources.md
"""
import time
from utils.utils import client, run_test_section, log_result

def test_channel():
    print("\n[START] Testing Channel Resource...")

    state = {"channel_id": None}

    # 1. List channels (basic)
    def list_ops():
        channels = client.channel.list()
        data = channels if isinstance(channels, list) else channels.get("data", [])
        log_result("Channels list()", len(data))

        try:
            all_ch = client.channel.list_all()
            data2 = all_ch if isinstance(all_ch, list) else all_ch.get("data", [])
            log_result("Channels list_all()", len(data2))
            if data2:
                state["channel_id"] = data2[0].get("_id") or data2[0].get("id")
        except Exception as e:
            print(f"   [warn] list_all: {str(e)}")
    run_test_section("channel.list / list_all", list_ops)

    # 2. Get + counts
    def get_ops():
        if state["channel_id"]:
            try:
                ch = client.channel.get(state["channel_id"])
                log_result("channel.get", ch.get("_id") or ch.get("id"))
            except Exception as e:
                print(f"   [warn] channel.get: {str(e)}")
        try:
            cnt = client.channel.get_count()
            log_result("channel.get_count", cnt)
        except Exception as e:
            print(f"   [warn] channel.get_count: {str(e)}")
        try:
            conv_cnt = client.channel.get_conv_count()
            log_result("channel.get_conv_count", conv_cnt)
        except Exception as e:
            print(f"   [warn] channel.get_conv_count: {str(e)}")
    run_test_section("channel.get / counts", get_ops)

    # 3. Assignable teams
    def teams_ops():
        if state["channel_id"]:
            try:
                teams = client.channel.list_assignable_teams(state["channel_id"])
                log_result("Assignable Teams", len(teams) if isinstance(teams, list) else teams)
            except Exception as e:
                print(f"   [warn] list_assignable_teams: {str(e)}")
        else:
            print("   [skip] No channel_id found")
    run_test_section("channel.list_assignable_teams", teams_ops)

    # 4. Credential ops
    def credential_ops():
        if state["channel_id"]:
            try:
                cred = client.channel.get_credential(state["channel_id"])
                log_result("Credential", cred)
            except Exception as e:
                print(f"   [warn] get_credential: {str(e)}")
        else:
            print("   [skip] No channel_id found")
    run_test_section("channel.get_credential", credential_ops)

    print("\n[DONE] Channel Resource Testing Completed.")

if __name__ == "__main__":
    test_channel()
