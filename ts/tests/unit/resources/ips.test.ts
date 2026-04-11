import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { IpsResource } from "../../../src/app/resources/ips.js"
import { HttpTransport } from "../../../src/core/http.js"
import { TokenManager } from "../../../src/core/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new IpsResource(http, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } })
  )
}

describe("IpsResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  // ─── Profiles ───────────────────────────────────────────────────────────────

  it("getProfile() calls GET /ips/profiles/:userId", async () => {
    mockFetch({ _id: "u_1", displayName: "Alice" })
    await makeResource().getProfile("u_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/ips/profiles/u_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("getMyProfile() calls GET /ips/profiles/me", async () => {
    mockFetch({ _id: "me", displayName: "Me" })
    await makeResource().getMyProfile()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/ips/profiles/me")
  })

  it("updateProfile() calls PATCH /ips/profiles/:userId", async () => {
    mockFetch({ _id: "u_1", displayName: "Bob" })
    await makeResource().updateProfile("u_1", { displayName: "Bob" } as any)
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/ips/profiles/u_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("PATCH")
  })

  it("searchProfiles() calls GET /ips/profiles with query param", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().searchProfiles("alice")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/ips/profiles")
    expect(url.searchParams.get("q")).toBe("alice")
  })

  it("searchProfiles() includes pagination params", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().searchProfiles("alice", { page: 2, limit: 10 })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("page")).toBe("2")
    expect(url.searchParams.get("limit")).toBe("10")
  })

  // ─── Follow ─────────────────────────────────────────────────────────────────

  it("follow() calls POST /ips/profiles/:userId/follow", async () => {
    mockFetch({})
    await makeResource().follow("u_2")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/ips/profiles/u_2/follow")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("unfollow() calls DELETE /ips/profiles/:userId/follow", async () => {
    mockFetch({})
    await makeResource().unfollow("u_2")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/ips/profiles/u_2/follow")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("DELETE")
  })

  it("getFollowers() calls GET /ips/profiles/:userId/followers", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().getFollowers("u_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/ips/profiles/u_1/followers")
  })

  it("getFollowing() calls GET /ips/profiles/:userId/following", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().getFollowing("u_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/ips/profiles/u_1/following")
  })

  // ─── Identities ─────────────────────────────────────────────────────────────

  it("listIdentities() calls GET /ips/identities/:userId", async () => {
    mockFetch([{ provider: "google", sub: "sub_1" }])
    await makeResource().listIdentities("u_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/ips/identities/u_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("unlinkIdentity() calls DELETE /ips/identities/:userId/:provider", async () => {
    mockFetch({})
    await makeResource().unlinkIdentity("u_1", "google")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/ips/identities/u_1/google")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("DELETE")
  })

  it("sends x-access-token header", async () => {
    mockFetch({ _id: "u_1" })
    await makeResource().getMyProfile()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-access-token")).toBe("test_key")
  })
})
