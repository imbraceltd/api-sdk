import sys
import os

# Add parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import client, base_url, access_token, api_key
from tests.test_full_flow_guide import test_full_flow_guide
from tests.test_ai_agent import test_ai_agent
from tests.test_chat_ai import test_chat_ai
from tests.test_activepieces import test_activepieces
from tests.test_boards import test_boards
from tests.test_crm import test_crm
from tests.test_platform import test_platform
from tests.test_agent import test_agent
from tests.test_marketplace import test_marketplace
from tests.test_settings import test_settings
from tests.test_frontend_sdk import test_frontend_sdk
from tests.test_multi_agent import test_multi_agent
from tests.test_crm_advanced import test_crm_advanced
from tests.test_error_paths import test_error_paths
from tests.test_async import run_async_tests
from tests.test_campaign import test_campaign
from tests.test_ai_raw import test_ai_raw
from tests.test_file_service import test_file_service
from tests.test_misc import test_misc
from tests.test_multimedia_ai import test_multimedia_ai
from tests.test_auth import test_auth
from tests.test_account import test_account
from tests.test_channel import test_channel
from tests.test_resources import test_resources
from tests.test_ai_extended import test_ai_extended
from tests.test_chat_ai_extended import test_chat_ai_extended

def run_all_tests():
    print("================================================")
    print("   IMBRACE SDK COMPREHENSIVE TEST SUITE (PY)")
    print("================================================")
    print(f"Target: {base_url}")
    print(f"Mode:   {'Access Token' if access_token else 'API Key'}")
    print("================================================")

    modules = [
        {"name": "Platform", "fn": test_platform},
        {"name": "Agent", "fn": test_agent},
        {"name": "Marketplace", "fn": test_marketplace},
        {"name": "AiAgent", "fn": test_ai_agent},
        {"name": "ChatAi", "fn": test_chat_ai},
        {"name": "Activepieces", "fn": test_activepieces},
        {"name": "Boards", "fn": test_boards},
        {"name": "CRM", "fn": test_crm},
        {"name": "Full Flow Guide", "fn": test_full_flow_guide},
        {"name": "Frontend SDK", "fn": test_frontend_sdk},
        {"name": "Multi-Agent", "fn": test_multi_agent},
        {"name": "CRM Advanced", "fn": test_crm_advanced},
        {"name": "Multimedia AI", "fn": test_multimedia_ai},
        {"name": "Settings", "fn": test_settings},
        {"name": "Campaign", "fn": test_campaign},
        {"name": "AI Raw", "fn": test_ai_raw},
        {"name": "File Service", "fn": test_file_service},
        {"name": "Misc", "fn": test_misc},
        {"name": "Error Paths", "fn": test_error_paths},
        {"name": "Async Client", "fn": run_async_tests},
        {"name": "Auth Methods", "fn": test_auth},
        {"name": "Account", "fn": test_account},
        {"name": "Channel", "fn": test_channel},
        {"name": "Resources (misc)", "fn": test_resources},
        {"name": "AI Extended", "fn": test_ai_extended},
        {"name": "Chat AI Extended", "fn": test_chat_ai_extended},
    ]

    passed = 0
    failed = 0

    for mod in modules:
        try:
            mod["fn"]()
            passed += 1
        except Exception as e:
            print(f"\n❌ MODULE [{mod['name']}] FAILED: {str(e)}")
            failed += 1

    print("\n" + "=" * 48)
    print(f"   TEST SUITE SUMMARY")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print("=" * 48)

    if failed > 0:
        print("\n⚠️ SOME MODULES FAILED. Please check the logs above.")
        sys.exit(1)
    else:
        print("\n🎉 ALL TEST MODULES FINISHED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_tests()
