import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { BoardsResource } from "../../../src/resources/boards.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

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

  it("list() calls GET /boards", async () => {
    mockFetch({ data: [{ id: "b_1", name: "CRM" }] })
    const res = await makeResource().list()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/boards")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
    expect(res.data[0].name).toBe("CRM")
  })

  it("get() calls GET /boards/:id", async () => {
    mockFetch({ id: "b_1" })
    await makeResource().get("b_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/boards/b_1")
  })

  it("create() calls POST /boards with body", async () => {
    mockFetch({ id: "b_new", name: "My Board" })
    const res = await makeResource().create({ name: "My Board", description: "Test" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/boards")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
    const body = JSON.parse(vi.mocked(globalThis.fetch).mock.calls[0][1]?.body as string)
    expect(body.name).toBe("My Board")
    expect(res.id).toBe("b_new")
  })

  it("delete() calls DELETE /boards/:id", async () => {
    mockFetch({ success: true })
    await makeResource().delete("b_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/boards/b_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("DELETE")
  })

  it("listItems() calls GET /boards/:id/items", async () => {
    mockFetch({ data: [{ id: "bi_1" }] })
    const res = await makeResource().listItems("b_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/boards/b_1/items")
    expect(res.data.length).toBe(1)
  })

  it("createItem() calls POST /boards/:id/items", async () => {
    mockFetch({ id: "bi_new" })
    await makeResource().createItem("b_1", { fields: [{ key: "name", value: "Test" }] })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/boards/b_1/items")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("deleteItem() calls DELETE /boards/:id/items/:itemId", async () => {
    mockFetch({})
    await makeResource().deleteItem("b_1", "bi_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/boards/b_1/items/bi_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("DELETE")
  })
})
