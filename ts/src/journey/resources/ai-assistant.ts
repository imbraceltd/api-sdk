import { HttpTransport } from "../../core/http.js"

export class AiAssistantResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/journeys/v2/ai/assistants` }

  async list(params?: { limit?: number; sort?: string }) {
    const url = new URL(this.url)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.sort) url.searchParams.set("sort", params.sort)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async create(body: {
    name: string
    description?: string
    instructions?: string
    file_ids?: string[]
    metadata?: Record<string, string>
  }) {
    return this.http.getFetch()(this.url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(assistantId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.url}/${assistantId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(assistantId: string) {
    return this.http.getFetch()(`${this.url}/${assistantId}`, { method: "DELETE" }).then(r => r.json())
  }
}
