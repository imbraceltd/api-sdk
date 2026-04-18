import { HttpTransport } from "../http.js"

export class SettingsResource {
  constructor(
    private readonly http: HttpTransport,
    private readonly channelServiceBase: string,
    private readonly platformBase: string
  ) {}

  // Message templates
  async listMessageTemplates(params?: { businessUnitId?: string; limit?: number; skip?: number }) {
    const url = new URL(`${this.channelServiceBase}/v1/message_templates`)
    if (params?.businessUnitId) url.searchParams.set("type", "business_unit_id")
    if (params?.businessUnitId) url.searchParams.set("q", params.businessUnitId)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async createMessageTemplate(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.channelServiceBase}/v1/message_templates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getMessageTemplate(templateId: string) {
    return this.http.getFetch()(`${this.channelServiceBase}/v1/message_templates/${templateId}`, {
      method: "GET",
    }).then(r => r.json())
  }

  async updateMessageTemplate(templateId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.channelServiceBase}/v1/message_templates/${templateId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteMessageTemplate(templateId: string) {
    return this.http.getFetch()(`${this.channelServiceBase}/v1/message_templates/${templateId}`, {
      method: "DELETE",
    }).then(r => r.json())
  }

  async searchMessageTemplates(params?: Record<string, string>) {
    const url = new URL(`${this.channelServiceBase}/v1/message_templates/_search`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listMessageTemplatesV2(params?: Record<string, string>) {
    const url = new URL(`${this.channelServiceBase}/v2/message_templates`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // WhatsApp Templates
  async listWhatsAppTemplates(params?: Record<string, string>) {
    const url = new URL(`${this.channelServiceBase}/v1/whatsapp_templates`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listWhatsAppTemplatesV2(params?: Record<string, string>) {
    const url = new URL(`${this.channelServiceBase}/v2/whatsapp_templates`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // Users
  async listUsers(params?: { skip?: number; limit?: number; search?: string; roles?: string; status?: string }) {
    const url = new URL(`${this.platformBase}/v1/users`)
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.search) url.searchParams.set("search", params.search)
    if (params?.roles) url.searchParams.set("roles", params.roles)
    if (params?.status) url.searchParams.set("status", params.status)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getUserRolesCount() {
    return this.http.getFetch()(`${this.platformBase}/v1/users/_roles_count`, { method: "GET" }).then(r => r.json())
  }

  async bulkInviteUsers(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.platformBase}/v1/users/_bulk_invite`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
