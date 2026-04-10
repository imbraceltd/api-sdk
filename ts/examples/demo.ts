/**
 * Imbrace TypeScript SDK — Frontend demo
 * Dùng cho: React, Next.js, Vue, Svelte, hoặc Node.js script
 */
import { ImbraceClient } from "imbrace-ts"

// ── INIT ──────────────────────────────────────────────────────────────────────
// Tự đọc IMBRACE_API_KEY, IMBRACE_BASE_URL từ env
const client = new ImbraceClient({
  // apiKey: process.env.IMBRACE_API_KEY,          // server-side
  // accessToken: "eyJhbGci...",                   // client-side (browser)
  // baseUrl: "https://app-gatewayv2.imbrace.co",  // optional
  checkHealth: true,
})

await client.init()


// ── PLATFORM ─────────────────────────────────────────────────────────────────
const me = await client.platform.getMe()
console.log("👤 Me:", me)

const users = await client.platform.listUsers({ page: 1, limit: 10 })
console.log("👥 Users:", users.data.length)


// ── MARKETPLACE ──────────────────────────────────────────────────────────────
const products = await client.marketplace.listProducts({ category: "electronics", limit: 5 })
console.log("🛒 Products:", products.data.length)

const order = await client.marketplace.createOrder({
  items: [{ productId: "prod_123", quantity: 2 }],
  shippingAddress: { city: "Ho Chi Minh", country: "VN" },
})
console.log("📦 Order:", order.id)


// ── CHANNEL ──────────────────────────────────────────────────────────────────
const channels = await client.channel.listChannels({ type: "group" })
console.log("💬 Channels:", channels.data.length)

// Gửi tin nhắn
const msg = await client.channel.sendMessage("conv_123", {
  content: "Hello from SDK!",
  type: "text",
})
console.log("✉️ Sent:", msg.id)


// ── IPS ──────────────────────────────────────────────────────────────────────
const profile = await client.ips.getMyProfile()
console.log("🪪 Profile:", profile.displayName)

const results = await client.ips.searchProfiles("john", { limit: 5 })
console.log("🔍 Found:", results.data.length)


// ── AGENT ────────────────────────────────────────────────────────────────────
const agents = await client.agent.listAgents()
console.log("🤖 Agents:", agents.data.length)

const run = await client.agent.runAgent("agent_123", {
  task: "Summarize the latest sales report",
})
console.log("▶️ Run:", run.id, run.status)


// ── AI ───────────────────────────────────────────────────────────────────────
// Non-streaming
const completion = await client.ai.complete({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Explain the Imbrace SDK in one sentence." },
  ],
})
console.log("🧠 AI:", completion.choices[0].message.content)

// Streaming (AsyncGenerator)
console.log("🌊 Streaming:")
for await (const chunk of client.ai.stream({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Count from 1 to 5." }],
})) {
  const content = chunk.choices[0]?.delta?.content ?? ""
  process.stdout.write(content)
}
console.log()


// ── Token refresh (client-side OAuth) ────────────────────────────────────────
client.setAccessToken("new-oauth-token-after-refresh")
client.clearAccessToken()
