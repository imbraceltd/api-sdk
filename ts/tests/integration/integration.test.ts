/**
 * Integration tests — require a valid IMBRACE_API_KEY in the environment.
 *
 * Run with:
 *   IMBRACE_API_KEY=api_xxx npx vitest run src/__tests__/integration.test.ts
 *
 * Get a new API key:
 *   POST https://app-gatewayv2.imbrace.co/private/backend/v1/thrid_party_token
 *   Body: {"expirationDays": 10}
 *   Header: x-access-token: <existing_key>
 */
import { config } from "dotenv"
import { describe, it, expect, beforeAll } from "vitest"
import { ImbraceClient } from "../../src/client.js"

config({ path: new URL("../../.env", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1") })

const API_KEY = process.env.IMBRACE_API_KEY ?? ""
const BASE_URL = process.env.IMBRACE_BASE_URL ?? "https://app-gatewayv2.imbrace.co"
const ORG_ID = process.env.IMBRACE_ORG_ID ?? "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd"

let client: ImbraceClient

beforeAll(() => {
  if (!API_KEY) {
    console.warn("IMBRACE_API_KEY not set — skipping integration tests")
  }
  client = new ImbraceClient({ apiKey: API_KEY, baseUrl: BASE_URL })
})

function skipIfNoKey() {
  if (!API_KEY) return true
  return false
}

// ── Account ──────────────────────────────────────────────────────────────────

describe("Account (integration)", () => {
  it("getAccount() returns account data", async () => {
    if (skipIfNoKey()) return
    const result = await client.account.getAccount()
    expect(result).toBeDefined()
  })
})

// ── Channels ─────────────────────────────────────────────────────────────────

describe("Channels (integration)", () => {
  it("list() returns channel list", async () => {
    if (skipIfNoKey()) return
    const result = await client.channel.list()
    expect(result).toBeDefined()
  })
})

// ── Agents ───────────────────────────────────────────────────────────────────

describe("Agent (integration)", () => {
  it("list() returns templates", async () => {
    if (skipIfNoKey()) return
    const result = await client.agent.list()
    expect(result).toBeDefined()
  })
})

// ── Teams ─────────────────────────────────────────────────────────────────────

describe("Teams (integration)", () => {
  it("list() returns teams", async () => {
    if (skipIfNoKey()) return
    const result = await client.teams.list()
    expect(result).toBeDefined()
  })

  it("listMy() returns user teams", async () => {
    if (skipIfNoKey()) return
    const result = await client.teams.listMy()
    expect(result).toBeDefined()
  })
})

// ── Contacts ─────────────────────────────────────────────────────────────────

describe("Contacts (integration)", () => {
  it("list() returns contacts", async () => {
    if (skipIfNoKey()) return
    const result = await client.contacts.list({ limit: 5 })
    expect(result).toBeDefined()
  })
})

// ── Conversations ─────────────────────────────────────────────────────────────

describe("Conversations (integration)", () => {
  it("getViewsCount() returns counts", async () => {
    if (skipIfNoKey()) return
    const result = await client.conversations.getViewsCount()
    expect(result).toBeDefined()
  })
})

// ── Messages ─────────────────────────────────────────────────────────────────

describe("Messages (integration)", () => {
  it("list() returns messages", async () => {
    if (skipIfNoKey()) return
    const result = await client.messages.list({ limit: 5 })
    expect(result).toBeDefined()
  })
})

// ── Boards ────────────────────────────────────────────────────────────────────

describe("Boards (integration)", () => {
  it("list() returns boards", async () => {
    if (skipIfNoKey()) return
    const result = await client.boards.list()
    expect(result).toBeDefined()
  })
})

// ── Settings ─────────────────────────────────────────────────────────────────

describe("Settings (integration)", () => {
  it("listUsers() returns users", async () => {
    if (skipIfNoKey()) return
    const result = await client.settings.listUsers({ limit: 5 })
    expect(result).toBeDefined()
  })

  it("listMessageTemplates() returns templates", async () => {
    if (skipIfNoKey()) return
    const result = await client.settings.listMessageTemplates()
    expect(result).toBeDefined()
  })
})
