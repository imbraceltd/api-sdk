import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { ConversationsResource } from "../../../src/app/resources/conversations.js"
import { HttpTransport } from "../../../src/core/http.js"
import { TokenManager } from "../../../src/core/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"
const ORG_ID = "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new ConversationsResource(http, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } })
  )
}

describe("ConversationsResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  it("getViewsCount() calls GET /v2/backend/team_conversations/_views_count", async () => {
    mockFetch({ all: 975, yours: 293, closed: 61 })
    const res = await makeResource().getViewsCount()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v2/backend/team_conversations/_views_count")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
    expect(res.all).toBe(975)
  })

  it("create() calls POST /v1/backend/conversation", async () => {
    mockFetch({ id: "conv_123", status: "active" })
    const res = await makeResource().create()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/conversation")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
    expect(res.id).toBe("conv_123")
  })

  it("search() calls POST /v1/backend/meilisearch/:orgId/search", async () => {
    mockFetch({ success: true, message: { hits: [], total: 0 } })
    const res = await makeResource().search(ORG_ID, { q: "hello" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe(`/v1/backend/meilisearch/${ORG_ID}/search`)
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
    expect(res.success).toBe(true)
  })

  it("search() sends query body", async () => {
    mockFetch({})
    await makeResource().search(ORG_ID, { q: "test", limit: 20 })
    const body = JSON.parse(vi.mocked(globalThis.fetch).mock.calls[0][1]?.body as string)
    expect(body.q).toBe("test")
    expect(body.limit).toBe(20)
  })
})
