import { HttpTransport } from "../http.js"

export class WorkflowsResource {
  /**
   * @param channelBase  - channel-service base URL (gateway/channel-service)
   * @param platformBase - platform base URL (gateway/platform)
   */
  constructor(
    private readonly http: HttpTransport,
    private readonly channelBase: string,
    private readonly platformBase: string,
  ) {}

  private get chV1() { return `${this.channelBase}/v1` }
  private get plV1() { return `${this.platformBase}/v1` }

  // ─── Channel automation (channel-service) ────────────────────────────────────

  async listChannelAutomation(params?: { channelType?: string }) {
    const url = new URL(`${this.chV1}/workflows/channel_automation`)
    if (params?.channelType) url.searchParams.set("channelType", params.channelType)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ─── n8n workflows (platform) ────────────────────────────────────────────────

  async list(params?: Record<string, string>) {
    const url = new URL(`${this.plV1}/workflows`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(workflowId: string) {
    return this.http.getFetch()(`${this.plV1}/n8n/workflows/${workflowId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.plV1}/n8n/workflows`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(workflowId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.plV1}/n8n/workflows/${workflowId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(workflowId: string): Promise<void> {
    await this.http.getFetch()(`${this.plV1}/n8n/workflows/${workflowId}`, { method: "DELETE" })
  }

  async getNew() {
    return this.http.getFetch()(`${this.plV1}/n8n/workflows/new`, { method: "GET" }).then(r => r.json())
  }

  // ─── Credentials ─────────────────────────────────────────────────────────────

  async listCredentials() {
    return this.http.getFetch()(`${this.plV1}/credentials`, { method: "GET" }).then(r => r.json())
  }

  async getCredential(credentialId: string) {
    const url = new URL(`${this.plV1}/n8n/credentials/${credentialId}`)
    url.searchParams.set("includeData", "true")
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async createCredential(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.plV1}/n8n/credentials`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateCredential(credentialId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.plV1}/n8n/credentials/${credentialId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteCredential(credentialId: string): Promise<void> {
    await this.http.getFetch()(`${this.plV1}/n8n/credentials/${credentialId}`, { method: "DELETE" })
  }

  // ─── Channel credentials (channel-service) ───────────────────────────────────

  async getChannelCredential(credentialId: string) {
    return this.http.getFetch()(`${this.chV1}/channels/credentials/${credentialId}`, { method: "GET" }).then(r => r.json())
  }

  async updateChannelCredential(credentialId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.chV1}/channels/credentials/${credentialId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteChannelCredential(credentialId: string): Promise<void> {
    await this.http.getFetch()(`${this.chV1}/channels/credentials/${credentialId}`, { method: "DELETE" })
  }
}
