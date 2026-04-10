import { HttpTransport } from "../http.js"

export class ConversationsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async getViewsCount(params?: { type?: string; q?: string }) {
    const url = new URL(`${this.base}/v2/backend/team_conversations/_views_count`)
    if (params?.type) url.searchParams.set("type", params.type)
    if (params?.q) url.searchParams.set("q", params.q)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async create() {
    return this.http.getFetch()(`${this.base}/v1/backend/conversation`, {
      method: "POST",
      body: "",
    }).then(r => r.json())
  }

  async search(organizationId: string, body: { q?: string; limit?: number }) {
    return this.http.getFetch()(`${this.base}/v1/backend/meilisearch/${organizationId}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async fetch(organizationId: string, body: { filter: string; limit?: number }) {
    return this.http.getFetch()(`${this.base}/v1/backend/meilisearch/${organizationId}/fetch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
