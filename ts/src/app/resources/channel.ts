import { HttpTransport } from "../../core/http.js"

export class ChannelResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/v1/backend/channels` }

  async list(params?: { type?: string }) {
    const url = new URL(this.url)
    if (params?.type) url.searchParams.set("type", params.type)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getCount() {
    return this.http.getFetch()(`${this.url}/_count`, { method: "GET" }).then(r => r.json())
  }

  async get(channelId: string) {
    return this.http.getFetch()(`${this.url}/${channelId}`, { method: "GET" }).then(r => r.json())
  }

  async createWeb(body: { name: string }) {
    return this.http.getFetch()(`${this.base}/v3/backend/channels/_web`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(channelId: string, body: { active?: boolean; config?: Record<string, unknown> }) {
    return this.http.getFetch()(`${this.url}/${channelId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(channelId: string) {
    return this.http.getFetch()(`${this.url}/${channelId}`, { method: "DELETE" }).then(r => r.json())
  }

  async getConvCount(params?: { view?: string; teamId?: string }) {
    const url = new URL(`${this.url}/_conv_count`)
    if (params?.view) url.searchParams.set("view", params.view)
    if (params?.teamId) url.searchParams.set("team_id", params.teamId)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }
}
