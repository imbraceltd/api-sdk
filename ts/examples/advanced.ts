// Imbrace TS SDK — Advanced usage: events, token refresh, error handling
import { ImbraceClient, AuthError, NetworkError } from "../src/index.js"

const client = new ImbraceClient({
  baseUrl: process.env.IMBRACE_BASE_URL ?? "http://localhost:4096",
  apiKey: process.env.IMBRACE_API_KEY,
  timeout: 60000,
  checkHealth: true,
})

try {
  // Subscribe to global events via gen/ client
  const events = await client.global.event()
  console.log("Connected to event stream:", events)

  // Dynamic token refresh example
  client.setAccessToken("new-token-from-oauth")

  // Cleanup
  await client.global.dispose()
} catch (err) {
  if (err instanceof AuthError) {
    console.error("Auth failed — check your IMBRACE_API_KEY")
  } else if (err instanceof NetworkError) {
    console.error("Server unreachable:", err.message)
  } else {
    throw err
  }
}
