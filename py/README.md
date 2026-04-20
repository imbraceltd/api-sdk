# Imbrace Python SDK

Official Python SDK for Imbrace. Supports dual authentication: API Key (server-side) and Access Token (client-side).

## Installation

```bash
pip install imbrace
```

Development mode (from source):

```bash
cd py
pip install -e ".[dev]"
```

## Configuration

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Open `.env` and set:

```env
IMBRACE_API_KEY=your-api-key-here
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
```

**Where to get the API Key**

Call the Imbrace auth endpoint. The response looks like:

```json
{
  "apiKey": {
    "apiKey": "sk-xxx..."
  }
}
```

The value you need is `response.apiKey.apiKey`.

---

## Quick Start

### Synchronous client

```python
from imbrace import ImbraceClient

# Option 1: auto-read from .env (recommended)
client = ImbraceClient()

# Option 2: explicit configuration
client = ImbraceClient(
    api_key="sk-xxx...",
    base_url="https://app-gatewayv2.imbrace.co",
    timeout=30,
    check_health=True,
)

# Option 3: Access Token (browser / client-side)
client = ImbraceClient(access_token="eyJhbGci...")

# Update token after OAuth refresh
client.set_access_token("new-token")
client.clear_access_token()

client.close()
```

### Asynchronous client (FastAPI / asyncio)

```python
from imbrace import AsyncImbraceClient

async with AsyncImbraceClient() as client:
    me = await client.platform.get_me()
```

---

## Domain Resources

### Marketplace

```python
# Products
client.marketplace.list_products(category="electronics", page=1, limit=20)
client.marketplace.get_product("prod_id")
client.marketplace.create_product({"name": "Product A", "price": 99.0})
client.marketplace.update_product("prod_id", {"price": 89.0})
client.marketplace.delete_product("prod_id")

# Orders
client.marketplace.list_orders(status="pending")
client.marketplace.get_order("order_id")
client.marketplace.create_order({
    "items": [{"product_id": "prod_id", "quantity": 2}],
    "shipping_address": {"city": "Ho Chi Minh", "country": "VN"},
})
client.marketplace.update_order_status("order_id", "confirmed")
```

### Platform

```python
# Users
client.platform.get_me()
client.platform.list_users(search="john", page=1, limit=20)
client.platform.get_user("user_id")
client.platform.update_user("user_id", {"display_name": "John"})
client.platform.delete_user("user_id")

# Organizations
client.platform.list_orgs()
client.platform.create_org({"name": "My Org"})
client.platform.update_org("org_id", {"name": "New Name"})

# Permissions
client.platform.list_permissions("user_id")
client.platform.grant_permission("user_id", "flows", "write")
client.platform.revoke_permission("user_id", "perm_id")
```

### Channel

```python
# Channels
client.channel.list_channels(type="group")
client.channel.create_channel({"name": "general", "type": "group"})
client.channel.add_participants("channel_id", ["user_1", "user_2"])

# Messages
client.channel.list_messages("conversation_id")
client.channel.send_message("conversation_id", "Hello!", type="text")
client.channel.mark_read("conversation_id")
```

### IPS (Identity and Profile Service)

```python
client.ips.get_my_profile()
client.ips.get_profile("user_id")
client.ips.update_profile("user_id", {"bio": "Developer"})
client.ips.search_profiles("john doe", page=1, limit=10)
client.ips.follow("target_user_id")
client.ips.unfollow("target_user_id")
client.ips.get_followers("user_id")
client.ips.get_following("user_id")
client.ips.list_identities("user_id")
```

### Agent

```python
client.agent.list_agents()
client.agent.get_agent("agent_id")
client.agent.create_agent({"name": "My Agent", "model": "gpt-4o"})
client.agent.update_agent("agent_id", {"system_prompt": "You are helpful."})
client.agent.delete_agent("agent_id")
client.agent.run_agent("agent_id", {"task": "Analyze Q1 data"})
client.agent.get_run("run_id")
client.agent.cancel_run("run_id")
```

### AI

```python
# Non-streaming completion
response = client.ai.complete(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
    temperature=0.7,
    max_tokens=1000,
)
print(response["choices"][0]["message"]["content"])

# Streaming completion
for chunk in client.ai.stream(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Count to 5."}],
):
    content = chunk["choices"][0]["delta"].get("content", "")
    print(content, end="", flush=True)

# Embeddings
result = client.ai.embed(
    model="text-embedding-ada-002",
    input=["Hello world", "Imbrace SDK"],
)
```

### Sessions and Messages

```python
client.sessions.list()
session = client.sessions.create(directory="/my/project")
client.sessions.get(session["id"])
client.sessions.delete(session["id"])

client.messages.list(session["id"])
client.messages.send(session["id"], parts=[{"type": "text", "text": "Hi"}])
client.messages.delete(session["id"], "message_id")
```

---

## Error Handling

```python
from imbrace import ImbraceClient, AuthError, ApiError, NetworkError

client = ImbraceClient()

try:
    result = client.platform.get_me()
except AuthError:
    print("Invalid API Key or Access Token")
except ApiError as e:
    print(f"API error {e.status_code}: {e}")
except NetworkError:
    print("Cannot reach Imbrace Gateway")
```

---

## FastAPI Integration

```python
from fastapi import FastAPI, Depends
from imbrace import AsyncImbraceClient

app = FastAPI()

async def get_imbrace():
    async with AsyncImbraceClient() as client:
        yield client

@app.get("/products")
async def list_products(client: AsyncImbraceClient = Depends(get_imbrace)):
    return await client.marketplace.list_products()

@app.post("/ai/chat")
async def chat(message: str, client: AsyncImbraceClient = Depends(get_imbrace)):
    return await client.ai.complete(
        model="gpt-4o",
        messages=[{"role": "user", "content": message}],
    )
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `IMBRACE_ENV` | No | `stable` | Select environment (`develop`, `sandbox`, `stable`) |
| `IMBRACE_GATEWAY_URL` | No | — | Override Gateway URL (e.g., point to local or custom gateway) |
| `IMBRACE_API_KEY` | Yes | — | API Key from Imbrace Gateway |

### Configuration Priority
The SDK will read configuration in the following priority order:
1.  **Explicit Options**: Passed directly into `ImbraceClient(env='sandbox', gateway='...')`.
2.  **Environment Variables**: Read from `.env` (via `python-dotenv`) or system (`IMBRACE_ENV`, `IMBRACE_GATEWAY_URL`).
3.  **Defaults**: Defaults to `stable` environment with gateway `https://app-gateway.imbrace.co`.
