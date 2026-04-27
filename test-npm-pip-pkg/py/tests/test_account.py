"""
Test: client.account — get(), update()
"""
from utils.utils import client, run_test_section, run_stable_section, log_result

def test_account():
    print("\n[START] Testing Account Resource...")

    def account_ops():
        acc = client.account.get()
        log_result("Account", acc)

        try:
            client.account.update({"timezone": "Asia/Ho_Chi_Minh"})
            log_result("Account Updated", True)
        except Exception as e:
            print(f"   [warn] account.update: {str(e)}")

    run_stable_section("Account get + update", account_ops, unstable=True)

    print("\n[DONE] Account Resource Testing Completed.")

if __name__ == "__main__":
    test_account()
