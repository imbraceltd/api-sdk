import { HttpTransport } from "../http.js"
import type { Product, Order, CreateOrderInput, OrderStatus, PagedResponse } from "../types/index.js"

export interface EmailTemplate {
  _id: string
  name?: string
  subject?: string
  body?: string
  [key: string]: unknown
}

export interface CreateEmailTemplateInput {
  name: string
  subject?: string
  body?: string
  [key: string]: unknown
}

export interface ChannelWorkflowInput {
  channel_id?: string
  workflow_id?: string
  [key: string]: unknown
}

export interface ChannelWorkflowResponse {
  success: boolean
  [key: string]: unknown
}

export interface InstallFromJsonInput {
  template?: Record<string, unknown>
  [key: string]: unknown
}

export interface InstallFromJsonResponse {
  success: boolean
  [key: string]: unknown
}

export interface MarketplaceFileDetails {
  _id: string
  name?: string
  url?: string
  [key: string]: unknown
}

export interface MarketplaceFileUploadResponse {
  url: string
  file_id?: string
  [key: string]: unknown
}

export interface MarketplaceCategory {
  _id: string
  name: string
  [key: string]: unknown
}

export class MarketplaceResource {
  /**
   * @param base    - Marketplaces v2 base URL (gateway/v2/backend/marketplaces)
   * @param gateway - Gateway root URL (to construct /v1/marketplaces)
   */
  constructor(
    private readonly http: HttpTransport,
    private readonly base: string,
    private readonly gateway: string,
  ) {}

  private get marketplacesV2() { return this.base.replace(/\/$/, "") }
  private get legacyV1()       { 
    const gw = this.gateway.replace(/\/$/, "")
    return `${gw}/v1/marketplaces/market-places/templates` 
  }

  async listUseCaseTemplates(): Promise<{ _id: string; name?: string; [key: string]: unknown }[]> {
    return this.http.getFetch()(`${this.marketplacesV2}/templates`, { method: "GET" }).then(r => r.json())
  }

  async installFromJson(body: InstallFromJsonInput): Promise<InstallFromJsonResponse> {
    return this.http.getFetch()(`${this.marketplacesV2}/templates/v2/custom`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async listProducts(params?: {
    page?: number
    limit?: number
    category?: string
    search?: string
  }): Promise<PagedResponse<Product>> {
    const url = new URL(`${this.marketplacesV2}/products`)
    if (params?.page)     url.searchParams.set("page",     String(params.page))
    if (params?.limit)    url.searchParams.set("limit",    String(params.limit))
    if (params?.category) url.searchParams.set("category", params.category)
    if (params?.search)   url.searchParams.set("search",   params.search)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getProduct(productId: string): Promise<Product> {
    return this.http.getFetch()(`${this.marketplacesV2}/products/${productId}`, { method: "GET" }).then(r => r.json())
  }

  async installProduct(productId: string): Promise<Order> {
    return this.http.getFetch()(`${this.marketplacesV2}/installations/${productId}`, {
      method: "POST",
    }).then(r => r.json())
  }

  async createOrder(body: CreateOrderInput): Promise<Order> {
    return this.http.getFetch()(`${this.marketplacesV2}/installations/${body.product_id ?? ""}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async listOrders(params?: { page?: number; limit?: number; status?: OrderStatus }): Promise<PagedResponse<Order>> {
    const url = new URL(`${this.marketplacesV2}/orders`)
    if (params?.page)   url.searchParams.set("page",   String(params.page))
    if (params?.limit)  url.searchParams.set("limit",  String(params.limit))
    if (params?.status) url.searchParams.set("status", params.status)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getOrder(orderId: string): Promise<Order> {
    return this.http.getFetch()(`${this.marketplacesV2}/orders/${orderId}`, { method: "GET" }).then(r => r.json())
  }

  async updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order> {
    return this.http.getFetch()(`${this.marketplacesV2}/orders/${orderId}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    }).then(r => r.json())
  }

  async uploadFile(body: FormData): Promise<MarketplaceFileUploadResponse> {
    return this.http.getFetch()(`${this.marketplacesV2}/files`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async deleteFile(fileId: string): Promise<void> {
    await this.http.getFetch()(`${this.marketplacesV2}/files/${fileId}`, { method: "DELETE" })
  }

  async getFileDetails(fileId: string): Promise<MarketplaceFileDetails> {
    return this.http.getFetch()(`${this.marketplacesV2}/file-details/${fileId}`, { method: "GET" }).then(r => r.json())
  }

  async listEmailTemplates(params?: Record<string, string>): Promise<EmailTemplate[]> {
    const url = new URL(`${this.marketplacesV2}/email-templates/search`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async createEmailTemplate(body: CreateEmailTemplateInput): Promise<EmailTemplate> {
    return this.http.getFetch()(`${this.marketplacesV2}/email-templates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async postChannelWorkflows(body: ChannelWorkflowInput): Promise<ChannelWorkflowResponse> {
    return this.http.getFetch()(`${this.marketplacesV2}/channel-workflows`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async downloadMarketPlaceFile(shortPath: string): Promise<Response> {
    return this.http.getFetch()(`${this.marketplacesV2}/download/${shortPath}`, { method: "GET" })
  }

  async listCategories(params?: Record<string, string>): Promise<MarketplaceCategory[]> {
    const url = new URL(`${this.marketplacesV2}/categories`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }
}
