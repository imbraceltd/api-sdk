import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { OrganizationsResource } from "../../../src/resources/organizations.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new OrganizationsResource(http, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } })
  )
}

describe("OrganizationsResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  it("list() calls GET /v2/organizations", async () => {
    mockFetch({ data: [{ _id: "org_1", name: "Acme" }] })
    await makeResource().list()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/v2/organizations")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("list() includes limit and skip params", async () => {
    mockFetch({ data: [] })
    await makeResource().list({ limit: 10, skip: 20 })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("limit")).toBe("10")
    expect(url.searchParams.get("skip")).toBe("20")
  })

  it("list() includes skip=0 when explicitly provided", async () => {
    mockFetch({ data: [] })
    await makeResource().list({ skip: 0 })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("skip")).toBe("0")
  })

  it("sends x-api-key header", async () => {
    mockFetch({})
    await makeResource().list()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-api-key")).toBe("test_key")
  })

})
