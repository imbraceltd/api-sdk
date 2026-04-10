// Imbrace TS SDK — Basic usage với Imbrace Gateway thực
import { ImbraceClient, extractApiKey } from "../src/index.js"

// --- Cách 1: Dùng thẳng API Key string ---
const client = new ImbraceClient({
  apiKey: process.env.IMBRACE_API_KEY,
  // baseUrl mặc định: https://app-gatewayv2.imbrace.co
})

// Hoặc --- Cách 2: Từ response của auth endpoint ---
// const authResponse = await fetch("https://app-gatewayv2.imbrace.co/auth/key")
//   .then(r => r.json())
// const client = new ImbraceClient({
//   apiKey: extractApiKey(authResponse), // lấy authResponse.apiKey.apiKey
// })

// Optional: verify server is reachable trước
await client.init()

// List all sessions
const sessions = await client.sessions.list()
console.log("Sessions:", sessions)

// Create a session and send a prompt
const session = await client.sessions.create({ directory: process.cwd() })
const response = await client.messages.send(session.id, {
  parts: [{ type: "text", text: "Hello, Imbrace!" }],
  directory: process.cwd(),
})

console.log("Response:", response)
