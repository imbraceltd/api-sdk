# iMBrace SDK — Official Documentation

> Multi-language SDK (TypeScript & Python) for the iMBrace platform.
> Provides a unified, typed interface for authentication, resources, and error handling.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Architecture](#architecture)
6. [Resources](#resources)
   - [Health](#health)
   - [Sessions](#sessions)
   - [Messages](#messages)
   - [Agent](#agent)
   - [AI](#ai)
   - [Marketplace](#marketplace)
   - [Platform](#platform)
   - [Channel](#channel)
   - [IPS](#ips)
7. [Error Handling](#error-handling)
8. [Authentication](#authentication)
9. [TypeScript API Reference](#typescript-api-reference)
10. [Python API Reference](#python-api-reference)
11. [Roadmap](#roadmap)

---

## Overview

iMBrace SDK abstracts all HTTP communication with the iMBrace Gateway. Instead of manually building requests, developers call typed methods organized by domain.

```
Developer Code
    └── ImbraceClient
            ├── HttpTransport  (auth headers, retry, timeout, error mapping)
            └── Resources      (sessions, messages, agent, ai, ...)
                    └── iMBrace Gateway API
```

**Supported languages:** TypeScript (Node.js ≥ 18 / browser) · Python 3.9+

**Default base URL:** `https://app-gatewayv2.imbrace.co`

---

## Installation

### TypeScript

```bash
npm install @imbrace/sdk
```

### Python

```bash
pip install imbrace
```

---

## Quick Start

### TypeScript

```ts
import { ImbraceClient } from "@imbrace/sdk"

const client = new ImbraceClient({
  apiKey: process.env.IMBRACE_API_KEY,
})

await client.init() // optional health check on startup

const agents = await client.agent.listAgents({ page: 1, limit: 10 })
console.log(agents.data)
```

### Python (sync)

```python
from imbrace import ImbraceClient

# reads IMBRACE_API_KEY from env automatically
client = ImbraceClient()

agents = client.agent.list_agents(page=1, limit=10)
print(agents["data"])
```

### Python (async)

```python
from imbrace import AsyncImbraceClient
import asyncio

async def main():
    client = AsyncImbraceClient()
    agents = await client.agent.list_agents(page=1, limit=10)
    print(agents["data"])

asyncio.run(main())
```

---

## Configuration

| Option | TypeScript key | Python key | Env variable | Default |
|---|---|---|---|---|
| API key | `apiKey` | `api_key` | `IMBRACE_API_KEY` | — |
| Access token | `accessToken` | `access_token` | — | — |
| Base URL | `baseUrl` | `base_url` | `IMBRACE_BASE_URL` | `https://app-gatewayv2.imbrace.co` |
| Timeout | `timeout` | `timeout` | — | 30 000 ms / 30 s |
| Health check on init | `checkHealth` | `check_health` | — | `false` |

Both SDKs automatically read `IMBRACE_API_KEY` and `IMBRACE_BASE_URL` from environment variables if the options are not passed explicitly.

### TypeScript example

```ts
const client = new ImbraceClient({
  apiKey: "sk_xxx",
  baseUrl: "https://staging-gateway.imbrace.co",
  timeout: 10_000,
  checkHealth: true,
})
```

### Python example

```python
client = ImbraceClient(
    api_key="sk_xxx",
    base_url="https://staging-gateway.imbrace.co",
    timeout=10,
    check_health=True,
)
```

---

## Architecture

```
sdk/
├── ts/src/
│   ├── client.ts              # ImbraceClient — entry point
│   ├── http.ts                # HttpTransport — retry, timeout, auth headers
│   ├── errors.ts              # ImbraceError, AuthError, ApiError, NetworkError
│   ├── auth/
│   │   └── token-manager.ts   # Thread-safe token storage
│   ├── types/
│   │   └── index.ts           # All shared types & interfaces
│   └── resources/
│       ├── health.ts
│       ├── sessions.ts
│       ├── messages.ts
│       ├── agent.ts
│       ├── ai.ts
│       ├── marketplace.ts
│       ├── platform.ts
│       ├── channel.ts
│       └── ips.ts
└── py/src/imbrace/
    ├── client.py              # ImbraceClient (sync)
    ├── async_client.py        # AsyncImbraceClient
    ├── http.py                # HttpTransport
    ├── exceptions.py          # AuthError, ApiError, NetworkError
    ├── auth/token_manager.py
    ├── types/                 # Typed dicts per domain
    └── resources/             # One file per domain
```

### HttpTransport behaviour

| Behaviour | Detail |
|---|---|
| Auth headers | Injects `X-Api-Key` and/or `Authorization: Bearer <token>` on every request |
| Timeout | Every request is wrapped in an `AbortController`; throws `NetworkError` when exceeded |
| Retry | Up to **2 retries** on `429` or `≥ 500` responses, exponential backoff: 2 s → 4 s |
| Error mapping | `401/403` → `AuthError` · other HTTP errors → `ApiError` · connection/timeout → `NetworkError` |

### Request flow

```
client.agent.listAgents()
  → AgentResource builds URL + query params
  → calls HttpTransport.getFetch()(url, init)
  → HttpTransport injects X-Api-Key / Authorization header
  → HTTP request with AbortController timeout
  → on 429 / 5xx: sleep → retry (max 2)
  → on 401/403: throw AuthError
  → on success: return r.json()
```

---

## Resources

All resources are accessed via `client.<resource>.<method>()`.

---

### Health

Ping the gateway to verify it is reachable.

```ts
// TypeScript
await client.health.check()
```

```python
# Python
client.health.check()
```

---

### Sessions

Manage conversation sessions.

| Method | TypeScript | Python |
|---|---|---|
| List sessions | `client.sessions.list(params?)` | `client.sessions.list(...)` |
| Get session | `client.sessions.get(sessionId, params?)` | `client.sessions.get(session_id, ...)` |
| Create session | `client.sessions.create(body)` | `client.sessions.create(body)` |
| Delete session | `client.sessions.delete(sessionId)` | `client.sessions.delete(session_id)` |

**Params for `list` / `get`:**

| Param | Type | Description |
|---|---|---|
| `directory` | `string` | Filter by directory path |
| `workspace` | `string` | Filter by workspace ID |

```ts
// TypeScript
const session = await client.sessions.create({ directory: "/my-project" })
const list    = await client.sessions.list({ workspace: "default" })
await client.sessions.delete(session.id)
```

---

### Messages

Manage messages within a session.

| Method | TypeScript | Python |
|---|---|---|
| List messages | `client.messages.list(sessionId, params?)` | `client.messages.list(session_id, ...)` |
| Get message | `client.messages.get(sessionId, messageId)` | `client.messages.get(session_id, message_id)` |
| Send message | `client.messages.send(sessionId, body)` | `client.messages.send(session_id, body)` |
| Delete message | `client.messages.delete(sessionId, messageId)` | `client.messages.delete(session_id, message_id)` |

```ts
// TypeScript
const msg = await client.messages.send(sessionId, {
  role: "user",
  parts: [{ type: "text", text: "Hello world" }],
})
```

**Message types:**

```ts
interface Message {
  id: string
  sessionId: string
  role: "user" | "assistant"
  time: { created: number; completed?: number }
  parts: Array<TextPart | FilePart>
  metadata?: Record<string, unknown>
}
```

---

### Agent

Full CRUD for agents and their run lifecycle.

**Agent methods:**

| Method | Description |
|---|---|
| `listAgents(params?)` | Paginated list (`page`, `limit`) |
| `getAgent(agentId)` | Get agent by ID |
| `createAgent(body)` | Create a new agent |
| `updateAgent(agentId, body)` | Partial update (PATCH) |
| `deleteAgent(agentId)` | Delete agent |

**Run methods:**

| Method | Description |
|---|---|
| `runAgent(agentId, input, sessionId?)` | Start an agent run |
| `getRun(runId)` | Get run status and output |
| `listRuns(params?)` | Filter by `agentId`, `status`, pagination |
| `cancelRun(runId)` | Cancel a running job |

**AgentStatus values:** `"idle"` · `"running"` · `"paused"` · `"completed"` · `"failed"` · `"cancelled"`

```ts
// TypeScript
const agent = await client.agent.createAgent({
  name: "Support Bot",
  model: "gpt-4o",
  systemPrompt: "You are a helpful assistant.",
})

const run = await client.agent.runAgent(
  agent.id,
  { query: "How do I reset my password?" },
)
console.log(run.status) // "running"

// Poll until done
const result = await client.agent.getRun(run.id)
console.log(result.output)
```

```python
# Python
agent = client.agent.create_agent(name="Support Bot", model="gpt-4o")
run   = client.agent.run_agent(agent["id"], input={"query": "Hello"})
```

---

### AI

Text completions (streaming + non-streaming) and embeddings.

| Method | Description |
|---|---|
| `complete(input)` | Non-streaming completion — returns full response |
| `stream(input)` | SSE streaming — returns `AsyncGenerator<StreamChunk>` (TypeScript) |
| `embed(input)` | Generate vector embeddings |

**CompletionInput:**

```ts
interface CompletionInput {
  model: string
  messages: Array<{ role: "system" | "user" | "assistant"; content: string }>
  temperature?: number      // default: model default
  maxTokens?: number
  stream?: boolean          // set automatically by complete() / stream()
  metadata?: Record<string, unknown>
}
```

```ts
// TypeScript — non-streaming
const result = await client.ai.complete({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Summarise this text..." }],
  temperature: 0.7,
  maxTokens: 512,
})
console.log(result.choices[0].message.content)
console.log(result.usage?.totalTokens)

// TypeScript — streaming (SSE)
for await (const chunk of client.ai.stream({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Tell me a joke" }],
})) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "")
}

// TypeScript — embeddings
const emb = await client.ai.embed({
  model: "text-embedding-3-small",
  input: ["Hello", "World"],
})
console.log(emb.data[0].embedding) // number[]
```

```python
# Python
result = client.ai.complete(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
)
print(result["choices"][0]["message"]["content"])
```

---

### Marketplace

Manage products and orders.

**Product methods:**

| Method | Description |
|---|---|
| `listProducts(params?)` | Filter by `category`, `search`; paginate |
| `getProduct(productId)` | Get product by ID |
| `createProduct(body)` | Create product |
| `updateProduct(productId, body)` | Partial update |
| `deleteProduct(productId)` | Delete product |

**Order methods:**

| Method | Description |
|---|---|
| `listOrders(params?)` | Filter by `status`; paginate |
| `getOrder(orderId)` | Get order by ID |
| `createOrder(body)` | Place an order |
| `updateOrderStatus(orderId, status)` | Update order status |

**OrderStatus values:** `"pending"` · `"confirmed"` · `"processing"` · `"shipped"` · `"delivered"` · `"cancelled"` · `"refunded"`

```ts
// TypeScript
const products = await client.marketplace.listProducts({
  category: "electronics",
  page: 1,
  limit: 20,
})

const order = await client.marketplace.createOrder({
  items: [{ productId: "prod_123", quantity: 2 }],
  shippingAddress: { city: "Hanoi", country: "VN" },
  notes: "Please gift wrap",
})

await client.marketplace.updateOrderStatus(order.id, "confirmed")
```

---

### Platform

Manage users, organizations, and permissions.

**User methods:**

| Method | Description |
|---|---|
| `listUsers(params?)` | Search by `search`; paginate |
| `getUser(userId)` | Get user by ID |
| `getMe()` | Get the authenticated user |
| `updateUser(userId, body)` | Update user fields |
| `deleteUser(userId)` | Delete user |

**Organization methods:**

| Method | Description |
|---|---|
| `listOrgs(params?)` | Paginate organizations |
| `getOrg(orgId)` | Get org by ID |
| `createOrg(body)` | Create organization |
| `updateOrg(orgId, body)` | Partial update |
| `deleteOrg(orgId)` | Delete organization |

**Permission methods:**

| Method | Description |
|---|---|
| `listPermissions(userId)` | Get all permissions for a user |
| `grantPermission(userId, resource, action)` | Grant `read`/`write`/`delete`/`admin` |
| `revokePermission(userId, permissionId)` | Revoke permission by ID |

```ts
// TypeScript
const me = await client.platform.getMe()
await client.platform.grantPermission(me.id, "marketplace", "write")

const org = await client.platform.createOrg({ name: "Acme Corp", plan: "pro" })
```

---

### Channel

Channels, conversations, and messaging.

**Channel methods:**

| Method | Description |
|---|---|
| `listChannels(params?)` | Filter by `type`; paginate |
| `getChannel(channelId)` | Get channel by ID |
| `createChannel(body)` | Create channel |
| `updateChannel(channelId, body)` | Partial update |
| `deleteChannel(channelId)` | Delete channel |
| `addParticipants(channelId, userIds)` | Add members to channel |
| `removeParticipant(channelId, userId)` | Remove a member |

**ChannelType values:** `"direct"` · `"group"` · `"broadcast"` · `"support"`

**Conversation methods:**

| Method | Description |
|---|---|
| `listConversations(channelId, params?)` | List conversations in a channel |
| `getConversation(conversationId)` | Get conversation by ID |

**Message methods:**

| Method | Description |
|---|---|
| `listMessages(conversationId, params?)` | Paginate messages |
| `sendMessage(conversationId, body)` | Send a message |
| `deleteMessage(conversationId, messageId)` | Delete a message |
| `markRead(conversationId)` | Mark conversation as read |

```ts
// TypeScript
const ch = await client.channel.createChannel({ name: "General", type: "group" })
await client.channel.addParticipants(ch.id, ["user_1", "user_2"])

const conversations = await client.channel.listConversations(ch.id)

await client.channel.sendMessage(conversations.data[0].id, {
  content: "Hello team!",
  type: "text",
})

await client.channel.markRead(conversations.data[0].id)
```

---

### IPS

Identity and Profile System — profiles, follow graph, and linked OAuth identities.

**Profile methods:**

| Method | Description |
|---|---|
| `getProfile(userId)` | Get profile by user ID |
| `getMyProfile()` | Get authenticated user's profile |
| `updateProfile(userId, body)` | Update profile fields |
| `searchProfiles(query, params?)` | Search public profiles |

**Follow methods:**

| Method | Description |
|---|---|
| `follow(targetUserId)` | Follow a user |
| `unfollow(targetUserId)` | Unfollow a user |
| `getFollowers(userId, params?)` | Get followers list (paginated) |
| `getFollowing(userId, params?)` | Get following list (paginated) |

**Identity methods:**

| Method | Description |
|---|---|
| `listIdentities(userId)` | List linked OAuth providers |
| `unlinkIdentity(userId, provider)` | Remove a linked provider |

```ts
// TypeScript
const profile = await client.ips.getMyProfile()
await client.ips.follow("user_456")

const followers = await client.ips.getFollowers(profile.userId, { limit: 50 })

// Search other users
const results = await client.ips.searchProfiles("phong", { page: 1, limit: 10 })
```

---

## Error Handling

All SDK errors extend `ImbraceError`. Catch specific types for precise handling.

### TypeScript

```ts
import { AuthError, ApiError, NetworkError } from "@imbrace/sdk"

try {
  await client.agent.listAgents()
} catch (e) {
  if (e instanceof AuthError) {
    // 401 or 403 — refresh token or re-authenticate
    console.error("Authentication failed:", e.message)
  } else if (e instanceof ApiError) {
    // 4xx / 5xx after retries are exhausted
    console.error(`API error ${e.statusCode}:`, e.message)
  } else if (e instanceof NetworkError) {
    // timeout or connection failure
    console.error("Network error:", e.message)
  }
}
```

### Python

```python
from imbrace.exceptions import AuthError, ApiError, NetworkError

try:
    client.agent.list_agents()
except AuthError as e:
    print("Auth failed:", e)
except ApiError as e:
    print(f"API error {e.status_code}:", e)
except NetworkError as e:
    print("Network error:", e)
```

### Error class reference

| Class | Trigger | Extra fields |
|---|---|---|
| `AuthError` | HTTP 401 or 403 | — |
| `ApiError` | HTTP 4xx / 5xx (after retries) | `.statusCode` (TS) / `.status_code` (Python) |
| `NetworkError` | Timeout, abort, or connection failure | — |

---

## Authentication

iMBrace supports two auth modes — you can use either or both simultaneously.

### API Key (server-side)

```ts
const client = new ImbraceClient({ apiKey: "sk_live_xxx" })
```

Header sent: `X-Api-Key: sk_live_xxx`

### Access Token (OAuth / user session)

```ts
const client = new ImbraceClient({ accessToken: "eyJ..." })

// Update token at runtime (e.g. after OAuth refresh)
client.setAccessToken(newToken)

// Remove token
client.clearAccessToken()
```

Header sent: `Authorization: Bearer eyJ...`

### Python context manager (auto-close connection)

```python
with ImbraceClient(api_key="sk_xxx") as client:
    result = client.agent.list_agents()
# HTTP session closed automatically
```

---

## TypeScript API Reference

### `ImbraceClient`

```ts
new ImbraceClient(opts?: ImbraceClientConfig)
```

**Resources:**

| Property | Type | Domain |
|---|---|---|
| `client.health` | `HealthResource` | Gateway health |
| `client.sessions` | `SessionsResource` | Sessions |
| `client.messages` | `MessagesResource` | Messages |
| `client.agent` | `AgentResource` | Agents & runs |
| `client.ai` | `AiResource` | Completions & embeddings |
| `client.marketplace` | `MarketplaceResource` | Products & orders |
| `client.platform` | `PlatformResource` | Users, orgs, permissions |
| `client.channel` | `ChannelResource` | Channels & messaging |
| `client.ips` | `IpsResource` | Profiles & follow graph |

**Methods:**

| Method | Description |
|---|---|
| `client.init()` | Run health check if `checkHealth: true` |
| `client.setAccessToken(token)` | Update Bearer token at runtime |
| `client.clearAccessToken()` | Remove Bearer token |

**`createImbraceClient(config?)`** — factory function, equivalent to `new ImbraceClient(config)`.

---

## Python API Reference

### `ImbraceClient` (sync)

```python
ImbraceClient(
    base_url=None,
    access_token=None,
    api_key=None,
    timeout=30,        # seconds
    check_health=False,
)
```

### `AsyncImbraceClient` (async)

```python
AsyncImbraceClient(
    base_url=None,
    access_token=None,
    api_key=None,
    timeout=30,
    check_health=False,
)
```

### Method name mapping (TypeScript → Python)

| TypeScript | Python |
|---|---|
| `listAgents()` | `list_agents()` |
| `createAgent()` | `create_agent()` |
| `runAgent()` | `run_agent()` |
| `getMe()` | `get_me()` |
| `listProducts()` | `list_products()` |
| `updateOrderStatus()` | `update_order_status()` |
| `addParticipants()` | `add_participants()` |
| `getFollowers()` | `get_followers()` |
| `unlinkIdentity()` | `unlink_identity()` |

---

## Roadmap

- [ ] Base resource class (reduce boilerplate across resources)
- [ ] Unified error codes between Python and TypeScript
- [ ] Pagination auto-iterator (`for item in client.agent.iter_agents()`)
- [ ] Webhook signature verification
- [ ] Configurable retry strategy (custom delays, max retries)
- [ ] Request ID tracing header
- [ ] WebSocket / real-time event support
- [ ] File upload (multipart/form-data)
