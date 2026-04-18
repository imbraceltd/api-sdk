import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { WorkflowsResource } from "../../../src/resources/workflows.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

const CHANNEL_BASE  = "https://app-gateway.dev.imbrace.co/channel-service"
const PLATFORM_BASE = "https://app-gateway.dev.imbrace.co/platform"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new WorkflowsResource(http, CHANNEL_BASE, PLATFORM_BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } })
  )
}

describe("WorkflowsResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  // ─── Channel automation ──────────────────────────────────────────────────────

  it("listChannelAutomation() calls GET /channel-service/v1/workflows/channel_automation", async () => {
    mockFetch({ data: [] })
    await makeResource().listChannelAutomation()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/channel-service/v1/workflows/channel_automation")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("listChannelAutomation() includes channelType param", async () => {
    mockFetch({ data: [] })
    await makeResource().listChannelAutomation({ channelType: "whatsapp" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("channelType")).toBe("whatsapp")
  })

  // ─── n8n workflows (platform) ────────────────────────────────────────────────

  it("list() calls GET /platform/v1/workflows", async () => {
    mockFetch({ data: [] })
    await makeResource().list()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/platform/v1/workflows")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("get() calls GET /platform/v1/n8n/workflows/:id", async () => {
    mockFetch({ id: "n8n_1", name: "N8n Flow" })
    const res = await makeResource().get("n8n_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/platform/v1/n8n/workflows/n8n_1")
    expect(res.name).toBe("N8n Flow")
  })

  it("create() calls POST /platform/v1/n8n/workflows", async () => {
    mockFetch({ id: "n8n_new" })
    await makeResource().create({ name: "New N8n Flow" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/platform/v1/n8n/workflows")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("update() calls PATCH /platform/v1/n8n/workflows/:id", async () => {
    mockFetch({ id: "n8n_1" })
    await makeResource().update("n8n_1", { name: "Updated" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/platform/v1/n8n/workflows/n8n_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("PATCH")
  })

  it("sends x-api-key header", async () => {
    mockFetch({})
    await makeResource().list()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-api-key")).toBe("test_key")
  })

})
