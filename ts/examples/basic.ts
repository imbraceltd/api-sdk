// Imbrace TS SDK — Basic usage with real Imbrace Gateway
import { ImbraceClient, extractApiKey } from "../src/index.js"

// Initialize client with explicit API Key
const client = new ImbraceClient({
  apiKey: process.env.IMBRACE_API_KEY, // Explicitly pass from env if desired
})

// Or --- Option 2: From the auth endpoint response ---
// const authResponse = await fetch("https://app-gatewayv2.imbrace.co/auth/key")
//   .then(r => r.json())
// const client = new ImbraceClient({
//   apiKey: extractApiKey(authResponse), // gets authResponse.apiKey.apiKey
// })

// Optional: verify server is reachable first
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
