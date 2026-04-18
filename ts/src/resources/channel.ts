import { HttpTransport } from "../http.js"

export class ChannelResource {
  /**
   * @param base - channel-service base URL (gateway/channel-service)
   *   Version (v1/v2/v3) thêm trong từng method.
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }
  private get v2() { return `${this.base}/v2` }
  private get v3() { return `${this.base}/v3` }

  // ─── Channels ────────────────────────────────────────────────────────────────

  async list(params?: { type?: string }) {
    const url = new URL(`${this.v1}/channels`)
    if (params?.type) url.searchParams.set("type", params.type)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(channelId: string) {
    return this.http.getFetch()(`${this.v1}/channels/${channelId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(channelId: string, body: { active?: boolean; config?: Record<string, unknown> }) {
    return this.http.getFetch()(`${this.v1}/channels/${channelId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(channelId: string) {
    return this.http.getFetch()(`${this.v1}/channels/${channelId}`, { method: "DELETE" }).then(r => r.json())
  }

  async deleteV3(channelId: string) {
    return this.http.getFetch()(`${this.v3}/channels/${channelId}`, { method: "DELETE" }).then(r => r.json())
  }

  async getCount() {
    return this.http.getFetch()(`${this.v1}/channels/_count`, { method: "GET" }).then(r => r.json())
  }

  async getConvCount(params?: { view?: string; teamId?: string }) {
    const url = new URL(`${this.v1}/channels/_conv_count`)
    if (params?.view)   url.searchParams.set("view",    params.view)
    if (params?.teamId) url.searchParams.set("team_id", params.teamId)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async replace(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels/_replace`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Channel type creators ───────────────────────────────────────────────────

  async createWeb(body: { name: string }) {
    return this.http.getFetch()(`${this.v1}/channels/_web`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async createWebV3(body: { name: string }) {
    return this.http.getFetch()(`${this.v3}/channels/_web`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getFacebookPages(credentialId: string) {
    return this.http.getFetch()(`${this.v1}/channels/_facebook/credential/${credentialId}`, { method: "GET" }).then(r => r.json())
  }

  async createFacebook(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/channels/_facebook`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateFacebook(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/channels/_facebook`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async createInstagram(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels/_instagram`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async createInstagramV2(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels/_instagramV2`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async createEmail(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels/_email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async createWechat(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels/_wechat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async createLine(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels/_line`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async createWhatsApp(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels/_whatsapp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async createWhatsAppV2(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/channels/_whatsapp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async createWhatsAppV3(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/channels/_whatsapp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateWhatsApp(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/channels/_whatsapp`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Channel credentials & workflows ────────────────────────────────────────

  async getCredential(credentialId: string) {
    return this.http.getFetch()(`${this.v1}/channels/credentials/${credentialId}`, { method: "GET" }).then(r => r.json())
  }

  async updateCredential(credentialId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels/credentials/${credentialId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteCredential(credentialId: string): Promise<void> {
    await this.http.getFetch()(`${this.v1}/channels/credentials/${credentialId}`, { method: "DELETE" })
  }

  async updateChannelWorkflow(workflowId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/channels/workflows/${workflowId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteChannelWorkflow(workflowId: string): Promise<void> {
    await this.http.getFetch()(`${this.v1}/channels/workflows/${workflowId}`, { method: "DELETE" })
  }

  // ─── Assign ──────────────────────────────────────────────────────────────────

  async listAssignableTeams() {
    return this.http.getFetch()(`${this.v1}/assign/teams/all`, { method: "GET" }).then(r => r.json())
  }

  async listTeamObservers(teamId: string) {
    return this.http.getFetch()(`${this.v1}/assign/team/${teamId}/observers`, { method: "GET" }).then(r => r.json())
  }
}
