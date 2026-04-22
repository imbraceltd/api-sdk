"""
Stream chat test — token streaming from AiAgent.
Usage: python tests/local/test_stream_chat.py
"""
import os
import sys
import json
from imbrace import ImbraceClient

ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN", "acc_c10f483f-0e45-4966-a275-2fb0356365e7")
GATEWAY      = os.environ.get("IMBRACE_GATEWAY_URL",  "https://app-gatewayv2.imbrace.co")
ASSISTANT_ID = os.environ.get("IMBRACE_ASSISTANT_ID", "a5ffe364-c136-40a0-aa49-84866e4d8485")
ORG_ID       = os.environ.get("IMBRACE_ORG_ID",       "org_6d4ae4f2-f75c-4324-9269-c3fec12078cc")

client = ImbraceClient(access_token=ACCESS_TOKEN, gateway=GATEWAY)

def test_stream():
    print("Testing stream_chat (token streaming)...")
    
    resp = client.ai_agent.stream_chat({
        "assistant_id": ASSISTANT_ID,
        "organization_id": ORG_ID,
        "messages": [{"role": "user", "content": "Say hello in one sentence."}],
    })

    print(f"Status: {resp.status_code}")
    
    token_count = 0
    for line in resp.iter_lines():
        if line:
            line_str = line.decode("utf-8")
            if line_str.startswith("data: ") and line_str != "data: [DONE]":
                try:
                    event = json.loads(line_str[6:])
                    if event.get("type") == "text-delta":
                        sys.stdout.write(event.get("delta", ""))
                        sys.stdout.flush()
                        token_count += 1
                except:
                    pass
    
    print(f"\n\n✓ {token_count} text-delta chunks received")

if __name__ == "__main__":
    test_stream()
