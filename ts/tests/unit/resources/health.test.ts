import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { HealthResource } from "../../../src/app/resources/health.js"
import { HttpTransport } from "../../../src/core/http.js"
import { TokenManager } from "../../../src/core/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new HealthResource(http, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } })
  )
}

describe("HealthResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  it("check() calls GET /global/health", async () => {
    mockFetch({ status: "ok" })
    await makeResource().check()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/global/health")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("check() returns response data", async () => {
    mockFetch({ status: "ok", uptime: 12345 })
    const res = await makeResource().check()
    expect(res.status).toBe("ok")
    expect(res.uptime).toBe(12345)
  })

  it("sends x-access-token header", async () => {
    mockFetch({ status: "ok" })
    await makeResource().check()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-access-token")).toBe("test_key")
  })
})
