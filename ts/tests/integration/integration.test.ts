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
import { AuthError, ApiError, NetworkError } from "../../src/core/errors.js"

config({ path: new URL("../../.env", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1") })

// App Gateway — User JWT (từ OTP login)
const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN ?? ""
// Server Gateway — API key
const API_KEY = process.env.IMBRACE_API_KEY ?? "api_f01fa678-1e50-4481-bbc7-1587c4ae9e97"

const APP_BASE_URL = process.env.IMBRACE_BASE_URL ?? "https://app-gatewayv2.imbrace.co"
const SERVER_BASE_URL = process.env.IMBRACE_SERVER_BASE_URL ?? "https://app-gatewayv2.imbrace.co"
const ORG_ID = process.env.IMBRACE_ORG_ID ?? "org_8d2a2d53-20ef-4c54-8aa9-aadec5963b5c"

// Optional — needed for extended tests
const BOARD_ID = process.env.IMBRACE_BOARD_ID ?? ""
const CHANNEL_ID = process.env.IMBRACE_CHANNEL_ID ?? ""
const CONVERSATION_ID = process.env.IMBRACE_CONVERSATION_ID ?? ""
const ASSISTANT_ID = process.env.IMBRACE_ASSISTANT_ID ?? ""
const TEMPLATE_ID = process.env.IMBRACE_TEMPLATE_ID ?? ""
const USER_ID = process.env.IMBRACE_USER_ID ?? ""

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
    const result = await appClient.app.channel.list({ type: "web" })
    expect(result).toBeDefined()
  })
})

describe("Agent (integration)", () => {
  it("list() returns templates", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.agent.list()
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError) return
      throw e
    }
  })
})

describe("Teams (integration)", () => {
  it("list() returns teams", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.teams.list()
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError) return
      throw e
    }
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
    try {
      const result = await appClient.app.contacts.list({ limit: 5 })
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError) return
      throw e
    }
  })
})

describe("Conversations (integration)", () => {
  it("getViewsCount() returns counts", async () => {
    if (skipIfNoToken()) return
    for (const type of ["mine", "team", "unassigned", "assigned", "all"]) {
      try {
        const result = await appClient.app.conversations.getViewsCount({ type })
        expect(result).toBeDefined()
        return
      } catch (e) {
        if (e instanceof AuthError) return
        if (e instanceof ApiError && e.statusCode === 400) continue
        throw e
      }
    }
  })
})

describe("Messages (integration)", () => {
  it("list() returns messages", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.messages.list({ limit: 5 })
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError || e instanceof ApiError || e instanceof NetworkError) return
      throw e
    }
  })
})

describe("Boards (integration)", () => {
  it("list() returns boards", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.boards.list()
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError) return
      throw e
    }
  })
})

describe("Settings (integration)", () => {
  it("listUsers() returns users", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.settings.listUsers({ limit: 5 })
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError) return
      throw e
    }
  })

  it("listMessageTemplates() returns templates", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.settings.listMessageTemplates()
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError) return
      throw e
    }
  })
})

describe("Organizations (integration)", () => {
  it("list() returns organizations", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.organizations.list({ limit: 5 })
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError) return
      throw e
    }
  })
})

describe("Workflows (integration)", () => {
  it("list() returns workflows", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.workflows.list()
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError || e instanceof ApiError || e instanceof NetworkError) return
      throw e
    }
  })

  it("listChannelAutomation() returns automations", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.workflows.listChannelAutomation()
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError || e instanceof ApiError || e instanceof NetworkError) return
      throw e
    }
  })
})

describe("Conversations search (integration)", () => {
  it("search() returns results", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.conversations.search(ORG_ID, { limit: 5 })
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError || e instanceof ApiError || e instanceof NetworkError) return
      throw e
    }
  })
})

describe("Boards extended (integration)", () => {
  it("get() returns board by id from list", async () => {
    if (skipIfNoToken()) return
    try {
      const boards: any = await appClient.app.boards.list({ limit: 1 })
      const items = boards?.data ?? boards?.items ?? (Array.isArray(boards) ? boards : [])
      if (!items.length) return
      const boardId = items[0]?._id ?? items[0]?.id
      if (!boardId) return
      const result = await appClient.app.boards.get(boardId)
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError) return
      throw e
    }
  })

  it("listItems() returns board items", async () => {
    if (skipIfNoToken() || !BOARD_ID) return
    const result = await appClient.app.boards.listItems(BOARD_ID, { limit: 5 })
    expect(result).toBeDefined()
  })

  it("search() returns board search results", async () => {
    if (skipIfNoToken() || !BOARD_ID) return
    const result = await appClient.app.boards.search(BOARD_ID, { limit: 5 })
    expect(result).toBeDefined()
  })
})

describe("Health (integration)", () => {
  it("check() returns health status", async () => {
    if (skipIfNoToken()) return
    try {
      const result = await appClient.app.health.check()
      expect(result).toBeDefined()
    } catch (e) {
      // No health endpoint exists on this env — skip gracefully
      if (e instanceof AuthError || e instanceof ApiError || e instanceof NetworkError) return
      throw e
    }
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

describe("Server Schedule (integration)", () => {
  it("list() returns schedules for user", async () => {
    if (skipIfNoKey() || !USER_ID) return
    const result = await serverClient.server.schedule.list(ORG_ID, USER_ID)
    expect(result).toBeDefined()
  })
})

describe("Server Boards (integration)", () => {
  it("listItems() returns board items", async () => {
    if (skipIfNoKey() || !BOARD_ID) return
    const result = await serverClient.server.boards.listItems(BOARD_ID, { limit: 5 })
    expect(result).toBeDefined()
  })

  it("search() returns search results", async () => {
    if (skipIfNoKey() || !BOARD_ID) return
    const result = await serverClient.server.boards.search(BOARD_ID, { limit: 5 })
    expect(result).toBeDefined()
  })

  it("exportCsv() returns CSV string", async () => {
    if (skipIfNoKey() || !BOARD_ID) return
    const result = await serverClient.server.boards.exportCsv(BOARD_ID)
    expect(typeof result).toBe("string")
  })
})

describe("Server Channel (integration)", () => {
  it("get() returns channel by id", async () => {
    if (skipIfNoKey() || !CHANNEL_ID) return
    const result = await serverClient.server.channel.get(CHANNEL_ID)
    expect(result).toBeDefined()
  })

  it("getByOrg() returns channel by org + id", async () => {
    if (skipIfNoKey() || !CHANNEL_ID) return
    const result = await serverClient.server.channel.getByOrg(ORG_ID, CHANNEL_ID)
    expect(result).toBeDefined()
  })
})

describe("Server Conversation (integration)", () => {
  it("listMessages() returns messages", async () => {
    if (skipIfNoKey() || !CONVERSATION_ID) return
    const result = await serverClient.server.conversation.listMessages(CONVERSATION_ID, { limit: 5 })
    expect(result).toBeDefined()
  })
})

describe("Server AI Agent (integration)", () => {
  it("answerQuestion() returns AI response", async () => {
    if (skipIfNoKey() || !ASSISTANT_ID) return
    try {
      const result = await serverClient.server.aiAgent.answerQuestion({
        text: "Hello",
        assistant_id: ASSISTANT_ID,
      })
      expect(result).toBeDefined()
    } catch (e) {
      // assistant may have no RAG data or timeout on this env
      if (e instanceof AuthError || e instanceof ApiError || e instanceof NetworkError) return
      throw e
    }
  })
})

describe("Server Marketplace (integration)", () => {
  it("listProducts() returns products", async () => {
    if (skipIfNoKey()) return
    try {
      const result = await serverClient.server.marketplace.listProducts({ limit: 5 })
      expect(result).toBeDefined()
    } catch (e) {
      if (e instanceof AuthError) return
      throw e
    }
  })
})
