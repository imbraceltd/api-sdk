"""
Imbrace Python SDK — ví dụ sử dụng thực tế (sync)
Chạy: python examples/demo.py
"""
import os
from dotenv import load_dotenv
from imbrace import ImbraceClient

load_dotenv()

# ── INIT ──────────────────────────────────────────────────────────────────────
# Cách 1: đọc tự động từ .env (IMBRACE_API_KEY, IMBRACE_BASE_URL)
client = ImbraceClient(check_health=True)

# Cách 2: truyền tường minh
# client = ImbraceClient(api_key="sk-...", base_url="https://app-gatewayv2.imbrace.co")

# Cách 3: dùng Access Token (client-side auth)
# client = ImbraceClient(access_token="eyJhbGci...")


# ── PLATFORM ──────────────────────────────────────────────────────────────────
me = client.platform.get_me()
print("Me:", me)

users = client.platform.list_users(page=1, limit=10)
print("Users:", users)


# ── MARKETPLACE ───────────────────────────────────────────────────────────────
products = client.marketplace.list_products(category="electronics", limit=5)
print("Products:", products)

# Tạo đơn hàng
order = client.marketplace.create_order({
    "items": [{"product_id": "prod_123", "quantity": 2}],
    "shipping_address": {"city": "Ho Chi Minh", "country": "VN"},
})
print("Order:", order)


# ── CHANNEL ───────────────────────────────────────────────────────────────────
channels = client.channel.list_channels(type="group")
print("Channels:", channels)


# ── IPS ───────────────────────────────────────────────────────────────────────
profile = client.ips.get_my_profile()
print("My Profile:", profile)


# ── AGENT ─────────────────────────────────────────────────────────────────────
agents = client.agent.list_agents()
print("Agents:", agents)


# ── AI ────────────────────────────────────────────────────────────────────────
# Non-streaming
response = client.ai.complete(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain the Imbrace SDK in one sentence."},
    ],
)
print("AI:", response["choices"][0]["message"]["content"])

# Streaming
print("Streaming:")
for chunk in client.ai.stream(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Count from 1 to 5."}],
):
    content = chunk["choices"][0]["delta"].get("content", "")
    print(content, end="", flush=True)
print()

client.close()
