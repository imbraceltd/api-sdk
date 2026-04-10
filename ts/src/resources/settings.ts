import { HttpTransport } from "../http.js"

export class SettingsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  // Message templates
  async listMessageTemplates(params?: { businessUnitId?: string; limit?: number; skip?: number }) {
    const url = new URL(`${this.base}/v2/backend/message_templates`)
    if (params?.businessUnitId) url.searchParams.set("business_unit_id", params.businessUnitId)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async createMessageTemplate(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/v1/backend/message_templates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteMessageTemplate(templateId: string) {
    return this.http.getFetch()(`${this.base}/v1/backend/message_templates/${templateId}`, { method: "DELETE" }).then(r => r.json())
  }

  // Users
  async listUsers(params?: { skip?: number; limit?: number; search?: string; roles?: string; status?: string }) {
    const url = new URL(`${this.base}/v1/backend/users`)
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.search) url.searchParams.set("search", params.search)
    if (params?.roles) url.searchParams.set("roles", params.roles)
    if (params?.status) url.searchParams.set("status", params.status)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getUserRolesCount() {
    return this.http.getFetch()(`${this.base}/v1/backend/users/_roles_count`, { method: "GET" }).then(r => r.json())
  }

  async bulkInviteUsers(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/v1/backend/users/_bulk_invite`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
