import { HttpTransport } from "../http.js"

export class CampaignResource {
  /**
   * @param base - channel-service base URL (gateway/channel-service)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }

  // ─── Campaigns ───────────────────────────────────────────────────────────────

  async list(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/campaign`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(campaignId: string) {
    return this.http.getFetch()(`${this.v1}/campaign/${campaignId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/campaign`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(campaignId: string): Promise<void> {
    await this.http.getFetch()(`${this.v1}/campaign/${campaignId}`, { method: "DELETE" })
  }

  // ─── Touchpoints ─────────────────────────────────────────────────────────────

  async listTouchpoints(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/touchpoints`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getTouchpoint(touchpointId: string) {
    return this.http.getFetch()(`${this.v1}/touchpoints/${touchpointId}`, { method: "GET" }).then(r => r.json())
  }

  async createTouchpoint(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/touchpoints`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateTouchpoint(touchpointId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/touchpoints/${touchpointId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteTouchpoint(touchpointId: string): Promise<void> {
    await this.http.getFetch()(`${this.v1}/touchpoints/${touchpointId}`, { method: "DELETE" })
  }

  async validateTouchpoint(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/touchpoints/_validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
