import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { BoardsResource } from "../../../src/app/resources/boards.js"
import { HttpTransport } from "../../../src/core/http.js"
import { TokenManager } from "../../../src/core/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new BoardsResource(http, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } })
  )
}

describe("BoardsResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  it("list() calls GET /v1/backend/board", async () => {
    mockFetch({ data: [{ id: "b_1", name: "CRM" }] })
    const res = await makeResource().list()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/board")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
    expect(res.data[0].name).toBe("CRM")
  })

  it("get() calls GET /v1/backend/board/:id", async () => {
    mockFetch({ id: "b_1" })
    await makeResource().get("b_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/board/b_1")
  })

  it("create() calls POST /v1/backend/board with body", async () => {
    mockFetch({ id: "b_new", name: "My Board" })
    const res = await makeResource().create({ name: "My Board", description: "Test" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/board")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
    const body = JSON.parse(vi.mocked(globalThis.fetch).mock.calls[0][1]?.body as string)
    expect(body.name).toBe("My Board")
    expect(res.id).toBe("b_new")
  })

  it("delete() calls DELETE /v1/backend/board/:id", async () => {
    mockFetch({ success: true })
    await makeResource().delete("b_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/board/b_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("DELETE")
  })

  it("listItems() calls GET /v1/backend/board/:id/board_items", async () => {
    mockFetch({ data: [{ id: "bi_1" }] })
    const res = await makeResource().listItems("b_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/board/b_1/board_items")
    expect(res.data.length).toBe(1)
  })

  it("createItem() calls POST /v1/backend/board/:id/board_items", async () => {
    mockFetch({ id: "bi_new" })
    await makeResource().createItem("b_1", { fields: [{ key: "name", value: "Test" }] })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/board/b_1/board_items")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("deleteItem() calls DELETE /v1/backend/board/:id/board_items/:itemId", async () => {
    mockFetch({})
    await makeResource().deleteItem("b_1", "bi_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/v1/backend/board/b_1/board_items/bi_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("DELETE")
  })
})
