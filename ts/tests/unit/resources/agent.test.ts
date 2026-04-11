import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { AgentResource } from "../../../src/app/resources/agent.js"
import { HttpTransport } from "../../../src/core/http.js"
import { TokenManager } from "../../../src/core/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new AgentResource(http, BASE)
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

  it("list() calls GET /v2/backend/templates", async () => {
    mockFetch({ data: [{ _id: "uc_1", title: "Agent A" }] })
    await makeResource().list()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v2/backend/templates")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("get() calls GET /v2/backend/templates/:id", async () => {
    mockFetch({ data: { _id: "uc_1", title: "Agent A" } })
    const res = await makeResource().get("uc_1")
    expect(res.data.title).toBe("Agent A")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v2/backend/templates/uc_1")
  })

  it("create() calls POST /v2/backend/templates/custom", async () => {
    mockFetch({ data: { _id: "uc_new", title: "Test Agent" } })
    await makeResource().create({ assistant: { name: "Test Agent" }, usecase: { title: "Test Agent" } })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v2/backend/templates/custom")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("update() calls PATCH /v2/backend/templates/:id/custom", async () => {
    mockFetch({ data: { _id: "uc_1" } })
    await makeResource().update("uc_1", { usecase: { title: "Updated" } })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v2/backend/templates/uc_1/custom")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("PATCH")
  })

  it("delete() calls DELETE /v2/backend/templates/:id", async () => {
    mockFetch({})
    await makeResource().delete("uc_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("DELETE")
  })

  it("sends x-access-token header", async () => {
    mockFetch({})
    await makeResource().list()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-access-token")).toBe("test_key")
  })
})
