import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { WorkflowsResource } from "../../../src/app/resources/workflows.js"
import { HttpTransport } from "../../../src/core/http.js"
import { TokenManager } from "../../../src/core/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new WorkflowsResource(http, BASE)
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

  // ─── Workflows ───────────────────────────────────────────────────────────────

  it("list() calls GET /v1/backend/workflows", async () => {
    mockFetch({ data: [] })
    await makeResource().list()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/v1/backend/workflows")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("list() includes tag param", async () => {
    mockFetch({ data: [] })
    await makeResource().list({ tag: "automation" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("tag")).toBe("automation")
  })

  it("listChannelAutomation() calls GET /v1/backend/workflows/channel_automation", async () => {
    mockFetch({ data: [] })
    await makeResource().listChannelAutomation()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/v1/backend/workflows/channel_automation")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("listChannelAutomation() includes channelType param", async () => {
    mockFetch({ data: [] })
    await makeResource().listChannelAutomation("whatsapp")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("channelType")).toBe("whatsapp")
  })

  it("create() calls POST /v1/backend/workflow", async () => {
    mockFetch({ _id: "wf_new" })
    await makeResource().create({ name: "My Workflow" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/workflow")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("update() calls PATCH /v1/backend/workflow/:id", async () => {
    mockFetch({ _id: "wf_1" })
    await makeResource().update("wf_1", { name: "Updated" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/workflow/wf_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("PATCH")
  })

  // ─── N8n workflows ───────────────────────────────────────────────────────────

  it("listN8n() calls GET /v1/backend/n8n/workflows", async () => {
    mockFetch({ data: [] })
    await makeResource().listN8n()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/n8n/workflows")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("getN8n() calls GET /v1/backend/n8n/workflows/:id", async () => {
    mockFetch({ id: "n8n_1", name: "N8n Flow" })
    const res = await makeResource().getN8n("n8n_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/n8n/workflows/n8n_1")
    expect(res.name).toBe("N8n Flow")
  })

  it("createN8n() calls POST /v1/backend/n8n/workflows", async () => {
    mockFetch({ id: "n8n_new" })
    await makeResource().createN8n({ name: "New N8n Flow" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/n8n/workflows")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("sends x-access-token header", async () => {
    mockFetch({ data: [] })
    await makeResource().list()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-access-token")).toBe("test_key")
  })
})
