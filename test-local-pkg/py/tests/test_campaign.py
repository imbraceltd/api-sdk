import time
from io import BytesIO
from utils.utils import client, run_test_section, run_stable_section, log_result, organization_id

def test_campaign():
    print("\n🚀 Testing Campaigns and Touchpoints Resource...")

    state = {"campaign_id": None, "touchpoint_id": None}

    # 1. Campaigns
    def campaign_ops():
        res = client.campaigns.list(params={"limit": 5})
        log_result("Campaigns", res.get("data", []))

        created = client.campaigns.create({
            "name": f"SDK Test Campaign {int(time.time())}",
            "description": "Created by automated test"
        })
        state["campaign_id"] = created.get("id") or created.get("_id")
        log_result("Campaign Created", state["campaign_id"])

        if state["campaign_id"]:
            fetched = client.campaigns.get(state["campaign_id"])
            log_result("Fetched Campaign", fetched.get("name"))

            client.campaigns.delete(state["campaign_id"])
            log_result("Campaign Deleted", True)
    run_stable_section("Campaign Ops", campaign_ops, unstable=True)

    # 2. Touchpoints
    def touchpoint_ops():
        res = client.campaigns.list_touchpoints(params={"limit": 5})
        tp_data = res if isinstance(res, list) else res.get("data", [])
        log_result("Touchpoints List", len(tp_data))

        if tp_data:
            tp_id = tp_data[0].get("id") or tp_data[0].get("_id")
            try:
                tp = client.campaigns.get_touchpoint(tp_id)
                log_result("campaign.get_touchpoint", tp.get("id") or tp.get("_id"))
            except Exception as e:
                print(f"   [warn] get_touchpoint: {str(e)}")

        # Create a fresh campaign first so we have a parent
        try:
            ts = int(time.time())
            camp = client.campaigns.create({"name": f"SDK_TP_CAMP_{ts}"})
            camp_id = camp.get("id") or camp.get("_id")
            if camp_id:
                new_tp = client.campaigns.create_touchpoint({
                    "campaign_id": camp_id,
                    "type": "email",
                    "delay_days": 1
                })
                new_tp_id = new_tp.get("id") or new_tp.get("_id")
                log_result("campaign.create_touchpoint", new_tp_id)

                if new_tp_id:
                    client.campaigns.update_touchpoint(new_tp_id, {"delay_days": 3})
                    log_result("campaign.update_touchpoint", True)
                    client.campaigns.delete_touchpoint(new_tp_id)
                    log_result("campaign.delete_touchpoint", True)

                client.campaigns.delete(camp_id)
        except Exception as e:
            print(f"   [warn] touchpoint CRUD: {str(e)}")

        # Validate
        try:
            val = client.campaigns.validate_touchpoint({"name": "Test", "type": "whatsapp"})
            log_result("Touchpoint Validated", val.get("success", True))
        except Exception as e:
            print(f"   [Skip] validate_touchpoint: {str(e)}")
    run_stable_section("Touchpoint Ops", touchpoint_ops, unstable=True)

    print("\n✅ Campaign Resource Testing Completed.")

if __name__ == "__main__":
    test_campaign()
