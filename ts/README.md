# Imbrace TypeScript SDK

Official TypeScript/JavaScript SDK for Imbrace. Fully typed. Supports dual authentication: API Key (server-side) and Access Token (client-side).

## Installation

```bash
npm install @imbrace/sdk
# or
yarn add @imbrace/sdk
# or
bun add @imbrace/sdk
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

### Initialize the client

```typescript
import { ImbraceClient } from "@imbrace/sdk"

// Option 1: auto-read from .env (Node.js / server)
const client = new ImbraceClient()

// Option 2: explicit configuration (server-side)
const client = new ImbraceClient({
  apiKey: "sk-xxx...",
  baseUrl: "https://app-gatewayv2.imbrace.co",
  timeout: 30000,
  checkHealth: true,
})

// Option 3: Access Token (browser / client-side)
const client = new ImbraceClient({
  accessToken: "eyJhbGci...",
})

// Update token after OAuth refresh
client.setAccessToken("new-token")
client.clearAccessToken()

// Run health check manually
await client.init()
```

---

## Domain Resources

### Marketplace

```typescript
// Products
const products = await client.marketplace.listProducts({
  category: "electronics",
  page: 1,
  limit: 20,
})
const product = await client.marketplace.getProduct("prod_id")
await client.marketplace.createProduct({ name: "Product A", price: 99 })
await client.marketplace.updateProduct("prod_id", { price: 89 })
await client.marketplace.deleteProduct("prod_id")

// Orders
const orders = await client.marketplace.listOrders({ status: "pending" })
const order = await client.marketplace.getOrder("order_id")
await client.marketplace.createOrder({
  items: [{ productId: "prod_id", quantity: 2 }],
  shippingAddress: { city: "Ho Chi Minh", country: "VN" },
})
await client.marketplace.updateOrderStatus("order_id", "confirmed")
```

### Platform

```typescript
// Users
const me    = await client.platform.getMe()
const users = await client.platform.listUsers({ search: "john" })
const user  = await client.platform.getUser("user_id")
await client.platform.updateUser("user_id", { displayName: "John" })
await client.platform.deleteUser("user_id")

// Organizations
const orgs = await client.platform.listOrgs()
const org  = await client.platform.createOrg({ name: "My Org" })
await client.platform.updateOrg("org_id", { name: "New Name" })

// Permissions
const perms = await client.platform.listPermissions("user_id")
await client.platform.grantPermission("user_id", "flows", "write")
await client.platform.revokePermission("user_id", "perm_id")
```

### Channel

```typescript
// Channels
const channels = await client.channel.listChannels({ type: "group" })
const channel  = await client.channel.createChannel({ name: "general", type: "group" })
await client.channel.addParticipants("channel_id", ["user_1", "user_2"])

// Messages
const msgs = await client.channel.listMessages("conversation_id")
const msg  = await client.channel.sendMessage("conversation_id", {
  content: "Hello!",
  type: "text",
})
await client.channel.markRead("conversation_id")
```

### IPS (Identity and Profile Service)

```typescript
const profile = await client.ips.getMyProfile()
await client.ips.updateProfile("user_id", { bio: "Developer" })
const results = await client.ips.searchProfiles("john doe", { limit: 10 })
await client.ips.follow("target_user_id")
await client.ips.unfollow("target_user_id")
const followers = await client.ips.getFollowers("user_id")
const following = await client.ips.getFollowing("user_id")
const identities = await client.ips.listIdentities("user_id")
```

### Agent

```typescript
const agents = await client.agent.listAgents()
const agent  = await client.agent.createAgent({
  name: "My Agent",
  model: "gpt-4o",
  systemPrompt: "You are helpful.",
})
const run    = await client.agent.runAgent("agent_id", { task: "Analyze data" })
const status = await client.agent.getRun(run.id)
await client.agent.cancelRun(run.id)
```

### AI

```typescript
// Non-streaming completion
const completion = await client.ai.complete({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Hello!" },
  ],
  temperature: 0.7,
  maxTokens: 1000,
})
console.log(completion.choices[0].message.content)

// Streaming completion (AsyncGenerator)
for await (const chunk of client.ai.stream({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Count to 5." }],
})) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "")
}

// Embeddings
const embeddings = await client.ai.embed({
  model: "text-embedding-ada-002",
  input: ["Hello world", "Imbrace SDK"],
})
```

### Sessions and Messages

```typescript
const sessions = await client.sessions.list()
const session  = await client.sessions.create({ directory: "/my/project" })
await client.sessions.delete(session.id)

const messages = await client.messages.list(session.id)
await client.messages.send(session.id, {
  parts: [{ type: "text", text: "Hi!" }],
})
```

---

## Error Handling

```typescript
import { ImbraceClient, AuthError, ApiError, NetworkError } from "@imbrace/sdk"

const client = new ImbraceClient()

try {
  const me = await client.platform.getMe()
} catch (e) {
  if (e instanceof AuthError)    console.error("Invalid API Key or Token")
  if (e instanceof ApiError)     console.error(`[${e.statusCode}] ${e.message}`)
  if (e instanceof NetworkError) console.error("Cannot reach Imbrace Gateway")
}
```

---

## React Integration

```tsx
import { useState, useEffect } from "react"
import { ImbraceClient } from "@imbrace/sdk"
import type { Product } from "@imbrace/sdk"

const client = new ImbraceClient({
  accessToken: localStorage.getItem("imbrace_token") ?? undefined,
})

function ProductList() {
  const [products, setProducts] = useState<Product[]>([])

  useEffect(() => {
    client.marketplace
      .listProducts()
      .then(res => setProducts(res.data))
  }, [])

  return (
    <ul>
      {products.map(p => (
        <li key={p.id}>{p.name} — {p.price} {p.currency}</li>
      ))}
    </ul>
  )
}
```

---

## Build

```bash
npm run build      # compile to dist/
npm run typecheck  # type-check only
npm run test       # run tests
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `IMBRACE_ENV` | No | `stable` | Chọn môi trường (`develop`, `sandbox`, `stable`) |
| `IMBRACE_GATEWAY_URL` | No | — | Ghi đè URL Gateway (ví dụ trỏ về local hoặc custom gateway) |
| `IMBRACE_API_KEY` | Yes* | — | API Key từ Imbrace Gateway (server-side) |

### Configuration Priority
SDK sẽ đọc cấu hình theo thứ tự ưu tiên sau:
1.  **Explicit Options**: Truyền trực tiếp vào `new ImbraceClient({ env: 'sandbox', gateway: '...' })`.
2.  **Environment Variables**: Đọc từ `.env` hoặc hệ thống (`IMBRACE_ENV`, `IMBRACE_GATEWAY_URL`).
3.  **Defaults**: Mặc định là môi trường `stable` với gateway `https://app-gateway.imbrace.co`.

*Or pass `accessToken` for client-side usage.
