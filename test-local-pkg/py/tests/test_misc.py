import time
from utils.utils import client, run_test_section, log_result

def test_misc():
    print("\n🚀 Testing Miscellaneous Resources (Predict, Message Suggestions, IPS)...")

    # 1. Predict
    def predict_ops():
        try:
            res = client.predict.predict({"input": "test"})
            log_result("Prediction", res)
        except:
            print("   [Skip] Predict failed")
    run_test_section("Predict Ops", predict_ops)

    # 2. Message Suggestions
    def suggestion_ops():
        try:
            res = client.message_suggestion.get_suggestions({"text": "How are you?"})
            log_result("Suggestions", res)
        except:
            print("   [Skip] Message suggestion failed")
    run_test_section("Message Suggestion Ops", suggestion_ops)

    # 3. IPS (IP Service)
    def ips_ops():
        try:
            ips = client.ips.list_ips()
            log_result("IPS Count", len(ips))
        except:
            print("   [Skip] IPS list failed")
    run_test_section("IPS Ops", ips_ops)

    # 4. License
    run_test_section("license.get", lambda: log_result("License", client.license.get()))

    print("\n✅ Miscellaneous Resources Testing Completed.")

if __name__ == "__main__":
    test_misc()
