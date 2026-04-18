import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { MarketplaceResource } from "../../../src/resources/marketplace.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new MarketplaceResource(http, `${BASE}/marketplaces`, `${BASE}/platform`)
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

  it("listProducts() calls GET /platform/v2/marketplaces/products", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().listProducts()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/platform/v2/marketplaces/products")
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

  it("getProduct() calls GET /platform/v2/marketplaces/products/:id", async () => {
    mockFetch({ _id: "prod_1", name: "Widget" })
    const res = await makeResource().getProduct("prod_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/platform/v2/marketplaces/products/prod_1")
    expect(res.name).toBe("Widget")
  })

  it("listUseCaseTemplates() calls GET /marketplaces/v1/market-places/templates", async () => {
    mockFetch({ data: [] })
    await makeResource().listUseCaseTemplates()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/marketplaces/v1/market-places/templates")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("installFromJson() calls POST /marketplaces/v1/market-places/templates/install-from-json", async () => {
    mockFetch({ success: true })
    await makeResource().installFromJson({ name: "Load" })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/marketplaces/v1/market-places/templates/install-from-json")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("installProduct() calls POST /platform/v2/marketplaces/installations/:id", async () => {
    mockFetch({ _id: "ord_new" })
    await makeResource().installProduct("prod_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/platform/v2/marketplaces/installations/prod_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  // ─── Orders ─────────────────────────────────────────────────────────────────

  it("listOrders() calls GET /platform/v2/marketplaces/orders", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().listOrders()
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.pathname).toBe("/platform/v2/marketplaces/orders")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("GET")
  })

  it("listOrders() includes status filter", async () => {
    mockFetch({ data: [], total: 0 })
    await makeResource().listOrders({ status: "pending" as any })
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as URL))
    expect(url.searchParams.get("status")).toBe("pending")
  })

  it("getOrder() calls GET /platform/v2/marketplaces/orders/:id", async () => {
    mockFetch({ _id: "ord_1", status: "paid" })
    const res = await makeResource().getOrder("ord_1")
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/platform/v2/marketplaces/orders/ord_1")
    expect(res.status).toBe("paid")
  })

  it("createOrder() calls POST /platform/v2/marketplaces/installations/:productId", async () => {
    mockFetch({ _id: "ord_new" })
    await makeResource().createOrder({ product_id: "prod_1", quantity: 1 } as any)
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/platform/v2/marketplaces/installations/prod_1")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("POST")
  })

  it("updateOrderStatus() calls PATCH /platform/v2/marketplaces/orders/:id/status", async () => {
    mockFetch({ _id: "ord_1", status: "shipped" })
    await makeResource().updateOrderStatus("ord_1", "shipped" as any)
    const url = new URL((vi.mocked(globalThis.fetch).mock.calls[0][0] as string))
    expect(url.pathname).toBe("/platform/v2/marketplaces/orders/ord_1/status")
    expect(vi.mocked(globalThis.fetch).mock.calls[0][1]?.method).toBe("PATCH")
  })

  it("sends x-api-key header", async () => {
    mockFetch({ data: [] })
    await makeResource().listProducts()
    const headers = new Headers(vi.mocked(globalThis.fetch).mock.calls[0][1]?.headers as HeadersInit)
    expect(headers.get("x-api-key")).toBe("test_key")
  })
})
