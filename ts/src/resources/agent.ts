import { HttpTransport } from "../http.js"

export class AgentResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/v2/backend/templates` }

  async list() {
    return this.http.getFetch()(this.url, { method: "GET" }).then(r => r.json())
  }

  async get(templateId: string) {
    return this.http.getFetch()(`${this.url}/${templateId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: {
    assistant: Record<string, unknown>
    usecase: Record<string, unknown>
  }) {
    return this.http.getFetch()(`${this.url}/custom`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(templateId: string, body: {
    assistant?: Record<string, unknown>
    usecase?: Record<string, unknown>
  }) {
    return this.http.getFetch()(`${this.url}/${templateId}/custom`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(templateId: string) {
    return this.http.getFetch()(`${this.url}/${templateId}`, { method: "DELETE" }).then(r => r.json())
  }
}
