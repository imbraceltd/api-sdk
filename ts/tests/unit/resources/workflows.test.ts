import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { WorkflowsResource } from "../../../src/resources/workflows.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

const BACKEND = "https://app-gatewayv2.imbrace.co/v1/backend"
const WORKFLOW_ENGINE = "https://app-gatewayv2.imbrace.co/activepieces"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new WorkflowsResource(http, BACKEND, WORKFLOW_ENGINE)
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

  it("listChannelAutomation() calls GET /v2/backend/workflows/channel_automation", async () => {
    mockFetch({ data: [] })
    await makeResource().listChannelAutomation()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/v2/backend/workflows/channel_automation")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("listChannelAutomation() includes channelType param", async () => {
    mockFetch({ data: [] })
    await makeResource().listChannelAutomation({ channelType: "whatsapp" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("channelType")).toBe("whatsapp")
  })

  it("sends x-api-key header", async () => {
    mockFetch({})
    await makeResource().listChannelAutomation()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-api-key")).toBe("test_key")
  })
})
