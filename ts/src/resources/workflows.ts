import { HttpTransport } from "../http.js"

export class WorkflowsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async list(params?: { tag?: string }) {
    const url = new URL(`${this.base}/v1/backend/workflows`)
    if (params?.tag) url.searchParams.set("tag", params.tag)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listChannelAutomation(channelType?: string) {
    const url = new URL(`${this.base}/v1/backend/workflows/channel_automation`)
    if (channelType) url.searchParams.set("channelType", channelType)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async create(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/v1/backend/workflow`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(workflowId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/v1/backend/workflow/${workflowId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // n8n workflows
  async listN8n() {
    return this.http.getFetch()(`${this.base}/v1/backend/n8n/workflows`, { method: "GET" }).then(r => r.json())
  }

  async getN8n(id: string) {
    return this.http.getFetch()(`${this.base}/v1/backend/n8n/workflows/${id}`, { method: "GET" }).then(r => r.json())
  }

  async createN8n(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/v1/backend/n8n/workflows`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
