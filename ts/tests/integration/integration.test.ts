/**
 * Integration tests — require credentials in environment.
 *
 * App Gateway tests (require user access token):
 *   IMBRACE_ACCESS_TOKEN=<jwt> npx vitest run tests/integration
 *
 * Server Gateway tests (require API key):
 *   IMBRACE_API_KEY=<api_key> npx vitest run tests/integration
 *
 * Get a new API key:
 *   POST https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token
 *   Body: {"expirationDays": 10}
 *   Header: x-access-token: <existing_key>
 *
 * Get an access token (App Gateway):
 *   Use OTP login flow via client.app.auth
 */
import { config } from "dotenv"
import { describe, it, expect, beforeAll } from "vitest"
import { ImbraceClient } from "../../src/client.js"

config({ path: new URL("../../.env", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1") })

// App Gateway — User JWT (từ OTP login)
const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN ?? ""
// Server Gateway — API key
const API_KEY = process.env.IMBRACE_API_KEY ?? "api_f01fa678-1e50-4481-bbc7-1587c4ae9e97"

const APP_BASE_URL = process.env.IMBRACE_BASE_URL ?? "https://app-gatewayv2.imbrace.co"
const SERVER_BASE_URL = process.env.IMBRACE_SERVER_BASE_URL ?? "https://app-gatewayv2.imbrace.co"
const ORG_ID = process.env.IMBRACE_ORG_ID ?? "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd"

let appClient: ImbraceClient
let serverClient: ImbraceClient

beforeAll(() => {
  appClient = new ImbraceClient({ appAccessToken: ACCESS_TOKEN, appBaseUrl: APP_BASE_URL })
  serverClient = new ImbraceClient({ serverApiKey: API_KEY, serverBaseUrl: SERVER_BASE_URL })
})

function skipIfNoToken() {
  if (!ACCESS_TOKEN) return true
  return false
}

function skipIfNoKey() {
  if (!API_KEY) return true
  return false
}

// ── App Gateway Tests (require IMBRACE_ACCESS_TOKEN) ─────────────────────────

describe("Account (integration)", () => {
  it("getAccount() returns account data", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.account.getAccount()
    expect(result).toBeDefined()
  })
})

describe("Channels (integration)", () => {
  it("list() returns channel list", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.channel.list()
    expect(result).toBeDefined()
  })
})

describe("Agent (integration)", () => {
  it("list() returns templates", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.agent.list()
    expect(result).toBeDefined()
  })
})

describe("Teams (integration)", () => {
  it("list() returns teams", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.teams.list()
    expect(result).toBeDefined()
  })

  it("listMy() returns user teams", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.teams.listMy()
    expect(result).toBeDefined()
  })
})

describe("Contacts (integration)", () => {
  it("list() returns contacts", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.contacts.list({ limit: 5 })
    expect(result).toBeDefined()
  })
})

describe("Conversations (integration)", () => {
  it("getViewsCount() returns counts", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.conversations.getViewsCount()
    expect(result).toBeDefined()
  })
})

describe("Messages (integration)", () => {
  it("list() returns messages", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.messages.list({ limit: 5 })
    expect(result).toBeDefined()
  })
})

describe("Boards (integration)", () => {
  it("list() returns boards", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.boards.list()
    expect(result).toBeDefined()
  })
})

describe("Settings (integration)", () => {
  it("listUsers() returns users", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.settings.listUsers({ limit: 5 })
    expect(result).toBeDefined()
  })

  it("listMessageTemplates() returns templates", async () => {
    if (skipIfNoToken()) return
    const result = await appClient.app.settings.listMessageTemplates()
    expect(result).toBeDefined()
  })
})

// ── Server Gateway Tests (require IMBRACE_API_KEY) ────────────────────────────

describe("Server Categories (integration)", () => {
  it("list() returns categories by org", async () => {
    if (skipIfNoKey()) return
    const result = await serverClient.server.categories.list(ORG_ID)
    expect(result).toBeDefined()
  })
})
