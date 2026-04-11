import { HttpTransport } from "../../core/http.js"
import type { Product, Order, CreateOrderInput, OrderStatus, PagedResponse } from "../../types/index.js"

export class MarketplaceResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/marketplace` }

  // ─── Products ───────────────────────────────────────────────────────────────
  async listProducts(params?: {
    page?: number
    limit?: number
    category?: string
    search?: string
  }): Promise<PagedResponse<Product>> {
    const url = new URL(`${this.url}/products`)
    if (params?.page) url.searchParams.set("page", String(params.page))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.category) url.searchParams.set("category", params.category)
    if (params?.search) url.searchParams.set("search", params.search)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getProduct(productId: string): Promise<Product> {
    return this.http.getFetch()(`${this.url}/products/${productId}`, { method: "GET" }).then(r => r.json())
  }

  async createProduct(body: Partial<Product>): Promise<Product> {
    return this.http.getFetch()(`${this.url}/products`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateProduct(productId: string, body: Partial<Product>): Promise<Product> {
    return this.http.getFetch()(`${this.url}/products/${productId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteProduct(productId: string): Promise<void> {
    await this.http.getFetch()(`${this.url}/products/${productId}`, { method: "DELETE" })
  }

  // ─── Orders ─────────────────────────────────────────────────────────────────
  async listOrders(params?: { page?: number; limit?: number; status?: OrderStatus }): Promise<PagedResponse<Order>> {
    const url = new URL(`${this.url}/orders`)
    if (params?.page) url.searchParams.set("page", String(params.page))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.status) url.searchParams.set("status", params.status)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getOrder(orderId: string): Promise<Order> {
    return this.http.getFetch()(`${this.url}/orders/${orderId}`, { method: "GET" }).then(r => r.json())
  }

  async createOrder(body: CreateOrderInput): Promise<Order> {
    return this.http.getFetch()(`${this.url}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order> {
    return this.http.getFetch()(`${this.url}/orders/${orderId}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    }).then(r => r.json())
  }
}
