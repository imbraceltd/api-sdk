import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { MarketplaceResource } from "../../../src/resources/marketplace.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new MarketplaceResource(http, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } })
  )
}

describe("MarketplaceResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  // ─── Products ───────────────────────────────────────────────────────────────

  it("listProducts() calls GET /marketplace/products", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().listProducts()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/marketplace/products")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("listProducts() includes filter params", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().listProducts({ page: 1, limit: 20, category: "tools", search: "sdk" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("page")).toBe("1")
    expect(url.searchParams.get("limit")).toBe("20")
    expect(url.searchParams.get("category")).toBe("tools")
    expect(url.searchParams.get("search")).toBe("sdk")
  })

  it("getProduct() calls GET /marketplace/products/:id", async () => {
    mockFetch({ _id: "prod_1", name: "Widget" })
    const res = await makeResource().getProduct("prod_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplace/products/prod_1")
    expect(res.name).toBe("Widget")
  })

  it("createProduct() calls POST /marketplace/products", async () => {
    mockFetch({ _id: "prod_new", name: "New Widget" })
    await makeResource().createProduct({ name: "New Widget" } as any)
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplace/products")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("updateProduct() calls PATCH /marketplace/products/:id", async () => {
    mockFetch({ _id: "prod_1", name: "Updated" })
    await makeResource().updateProduct("prod_1", { name: "Updated" } as any)
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplace/products/prod_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("PATCH")
  })

  it("deleteProduct() calls DELETE /marketplace/products/:id", async () => {
    mockFetch({})
    await makeResource().deleteProduct("prod_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplace/products/prod_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("DELETE")
  })

  // ─── Orders ─────────────────────────────────────────────────────────────────

  it("listOrders() calls GET /marketplace/orders", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().listOrders()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/marketplace/orders")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("listOrders() includes status filter", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().listOrders({ status: "pending" as any })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("status")).toBe("pending")
  })

  it("getOrder() calls GET /marketplace/orders/:id", async () => {
    mockFetch({ _id: "ord_1", status: "paid" })
    const res = await makeResource().getOrder("ord_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplace/orders/ord_1")
    expect(res.status).toBe("paid")
  })

  it("createOrder() calls POST /marketplace/orders", async () => {
    mockFetch({ _id: "ord_new" })
    await makeResource().createOrder({ productId: "prod_1", quantity: 1 } as any)
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplace/orders")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("updateOrderStatus() calls PATCH /marketplace/orders/:id/status", async () => {
    mockFetch({ _id: "ord_1", status: "shipped" })
    await makeResource().updateOrderStatus("ord_1", "shipped" as any)
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplace/orders/ord_1/status")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("PATCH")
  })

  it("sends x-access-token header", async () => {
    mockFetch({ data: [] })
    await makeResource().listProducts()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-access-token")).toBe("test_key")
  })
})
