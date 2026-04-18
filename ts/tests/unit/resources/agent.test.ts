import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { AgentResource } from "../../../src/resources/agent.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

// base = gateway/marketplaces
const BASE = "https://app-gatewayv2.imbrace.co/marketplaces"
const TEMPLATES = `${BASE}/market-places/templates`

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new AgentResource(http, BASE, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } })
  )
}

describe("AgentResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  it("list() calls GET /marketplaces/v1/market-places/templates", async () => {
    mockFetch({ data: [{ _id: "uc_1", title: "Agent A" }] })
    await makeResource().list()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplaces/v1/market-places/templates")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("get() calls GET /marketplaces/v1/market-places/templates/:id", async () => {
    mockFetch({ data: { _id: "uc_1", title: "Agent A" } })
    const res = await makeResource().get("uc_1")
    expect(res.data.title).toBe("Agent A")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplaces/v1/market-places/templates/uc_1")
  })

  it("create() calls POST /marketplaces/v1/market-places/templates/custom", async () => {
    mockFetch({ data: { _id: "uc_new", title: "Test Agent" } })
    await makeResource().create({ assistant: { name: "Test Agent" }, usecase: { title: "Test Agent" } })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplaces/v1/market-places/templates/custom")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("update() calls PATCH /marketplaces/v1/market-places/templates/:id/custom", async () => {
    mockFetch({ data: { _id: "uc_1" } })
    await makeResource().update("uc_1", { usecase: { title: "Updated" } })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplaces/v1/market-places/templates/uc_1/custom")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("PATCH")
  })

  it("delete() calls DELETE /marketplaces/v1/market-places/templates/:id", async () => {
    mockFetch({})
    await makeResource().delete("uc_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplaces/v1/market-places/templates/uc_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("DELETE")
  })

  it("sends x-api-key header", async () => {
    mockFetch({})
    await makeResource().list()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-api-key")).toBe("test_key")
  })
})
