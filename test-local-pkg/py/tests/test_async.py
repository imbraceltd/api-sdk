import asyncio
import os
import sys
import time
from typing import Callable, Any
from utils.utils import base_url, access_token, api_key, organization_id, log_result
from imbrace import AsyncImbraceClient

async def run_async_test_section(name: str, fn: Callable[[], Any]):
    print(f"\n--- [TEST] {name} ---")
    try:
        start = time.time()
        result = await fn()
        end = time.time()
        print(f"✅ Passed ({(end - start) * 1000:.0f}ms)")
        return result
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        print(f"❌ Failed: {str(e)}")
        if status_code in (404, 500, 501, 502):
            print(f"   ⚠️ Skipping section due to {status_code} (Endpoint might not exist on this environment)")
            return
        raise e

async def test_async():
    print("\n🚀 Testing Async Imbrace Client...")

    async with AsyncImbraceClient(
        api_key=None if access_token else api_key,
        access_token=access_token,
        base_url=base_url,
        organization_id=organization_id,
    ) as client:
        
        # 1. Parallel Requests
        async def parallel_ops():
            results = await asyncio.gather(
                client.platform.get_me(),
                client.marketplace.list_products(),
                client.chat_ai.list_models(),
            )
            log_result("Me", results[0])
            log_result("Products Count", len(results[1].get("data", [])))
            log_result("Models Count", len(results[2]))
        
        await run_async_test_section("Async Parallel Requests", parallel_ops)

        # 2. Async Chat
        async def async_chat():
            res = await client.chat_ai.chat({
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": "Say 'async-ready' if you hear me."}]
            })
            log_result("Chat Response", res["choices"][0]["message"]["content"])
        
        await run_async_test_section("Async Chat", async_chat)

    print("\n✅ Async Resource Testing Completed.")

def run_async_tests():
    asyncio.run(test_async())

if __name__ == "__main__":
    run_async_tests()
