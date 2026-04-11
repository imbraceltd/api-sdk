import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { HttpTransport } from "../../src/core/http.js"
import { TokenManager } from "../../src/core/auth/token-manager.js"
import { AuthError, ApiError, NetworkError } from "../../src/core/errors.js"

const BASE = "https://app-gatewayv2.imbrace.co"

function makeTransport(opts: { apiKey?: string; token?: string } = {}) {
  const tokenManager = new TokenManager(opts.token)
  return new HttpTransport({ apiKey: opts.apiKey, timeout: 5000, tokenManager })
}

describe("HttpTransport", () => {
  let originalFetch: typeof fetch

  beforeEach(() => {
    originalFetch = globalThis.fetch
    vi.useFakeTimers()
  })

  afterEach(() => {
    globalThis.fetch = originalFetch
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it("sets X-Api-Key header when apiKey provided", async () => {
    const transport = makeTransport({ apiKey: "key_test" })
    const capturedHeaders: Record<string, string> = {}

    globalThis.fetch = vi.fn().mockImplementation(async (_input: RequestInfo | URL, init?: RequestInit) => {
      const h = init?.headers as Headers
      h.forEach((v, k) => { capturedHeaders[k] = v })
      return new Response(JSON.stringify({ ok: true }), { status: 200 })
    })

    await transport.getFetch()(BASE + "/health", { method: "GET" })
    expect(capturedHeaders["x-access-token"]).toBe("key_test")
  })

  it("sets x-access-token header when token set", async () => {
    const transport = makeTransport({ token: "tok_test" })
    const capturedHeaders: Record<string, string> = {}

    globalThis.fetch = vi.fn().mockImplementation(async (_input: RequestInfo | URL, init?: RequestInit) => {
      const h = init?.headers as Headers
      h.forEach((v, k) => { capturedHeaders[k] = v })
      return new Response("{}", { status: 200 })
    })

    await transport.getFetch()(BASE + "/health", { method: "GET" })
    expect(capturedHeaders["x-access-token"]).toBe("tok_test")
  })

  it("does not set Authorization header when no token", async () => {
    const transport = makeTransport()
    const capturedHeaders: Record<string, string> = {}

    globalThis.fetch = vi.fn().mockImplementation(async (_input: RequestInfo | URL, init?: RequestInit) => {
      const h = init?.headers as Headers
      h.forEach((v, k) => { capturedHeaders[k] = v })
      return new Response("{}", { status: 200 })
    })

    await transport.getFetch()(BASE + "/health", { method: "GET" })
    expect(capturedHeaders["authorization"]).toBeUndefined()
  })

  it("throws AuthError on 401", async () => {
    const transport = makeTransport()
    globalThis.fetch = vi.fn().mockResolvedValue(new Response("Unauthorized", { status: 401 }))

    await expect(transport.getFetch()(BASE + "/session")).rejects.toBeInstanceOf(AuthError)
  })

  it("throws AuthError on 403", async () => {
    const transport = makeTransport()
    globalThis.fetch = vi.fn().mockResolvedValue(new Response("Forbidden", { status: 403 }))

    await expect(transport.getFetch()(BASE + "/session")).rejects.toBeInstanceOf(AuthError)
  })

  it("throws ApiError on 404", async () => {
    const transport = makeTransport()
    globalThis.fetch = vi.fn().mockResolvedValue(
      new Response("Not Found", { status: 404 })
    )

    await expect(transport.getFetch()(BASE + "/missing")).rejects.toBeInstanceOf(ApiError)
  })

  it("retries on 500 and throws after max retries", async () => {
    const transport = makeTransport()
    const fetchMock = vi.fn().mockResolvedValue(new Response("Server Error", { status: 500 }))
    globalThis.fetch = fetchMock

    // Attach rejection handler before advancing timers to avoid unhandled rejection warning
    const captured = transport.getFetch()(BASE + "/session").catch((e: unknown) => e)
    await vi.runAllTimersAsync()

    const err = await captured
    expect(err).toBeInstanceOf(ApiError)
    // 1 initial + 2 retries = 3 total calls
    expect(fetchMock).toHaveBeenCalledTimes(3)
  })

  it("throws NetworkError when fetch throws", async () => {
    const transport = makeTransport()
    globalThis.fetch = vi.fn().mockRejectedValue(new TypeError("Failed to fetch"))

    const captured = transport.getFetch()(BASE + "/session").catch((e: unknown) => e)
    await vi.runAllTimersAsync()

    const err = await captured
    expect(err).toBeInstanceOf(NetworkError)
  })

  it("returns response on 200", async () => {
    const transport = makeTransport()
    globalThis.fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify({ status: "ok" }), { status: 200 }))

    const res = await transport.getFetch()(BASE + "/health")
    const data = await res.json()
    expect(data.status).toBe("ok")
  })
})
