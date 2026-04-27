import { HttpTransport } from "../http.js"

export interface ChannelAutomationItem {
  id: string
  name?: string
  active?: boolean
  tags?: { id: string; name: string }[]
  [key: string]: unknown
}

export interface N8nWorkflow {
  id: string
  name?: string
  active?: boolean
  [key: string]: unknown
}

export interface N8nCredential {
  id: string
  name?: string
  type?: string
  [key: string]: unknown
}

export class WorkflowsResource {
  /**
   * @param backend - backend base URL (`{gateway}/v1/backend`)
   * Note: channel automation routes respond on v2/backend.
   */
  constructor(
    private readonly http: HttpTransport,
    private readonly backend: string,
  ) {}

  private get v2() {
    return this.backend.replace("/v1/", "/v2/")
  }

  async listChannelAutomation(params?: { channelType?: string }): Promise<{ data: ChannelAutomationItem[] }> {
    const url = new URL(`${this.v2}/workflows/channel_automation`)
    if (params?.channelType) url.searchParams.set("channelType", params.channelType)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ─── n8n Workflows ────────────────────────────────────────────────────────

  async listN8n(): Promise<N8nWorkflow[]> {
    return this.http.getFetch()(`${this.backend}/n8n/workflows`, { method: "GET" }).then(r => r.json())
  }

  async getN8n(workflowId: string): Promise<N8nWorkflow> {
    return this.http.getFetch()(`${this.backend}/n8n/workflows/${workflowId}`, { method: "GET" }).then(r => r.json())
  }

  async createN8n(body: Record<string, unknown>): Promise<N8nWorkflow> {
    return this.http.getFetch()(`${this.backend}/workflow`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateN8n(workflowId: string, body: Record<string, unknown>): Promise<N8nWorkflow> {
    return this.http.getFetch()(`${this.backend}/workflow/${workflowId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async listN8nCredentials(): Promise<N8nCredential[]> {
    return this.http.getFetch()(`${this.backend}/n8n/credentials`, { method: "GET" }).then(r => r.json())
  }

  async updateN8nCredential(credentialId: string, body: Record<string, unknown>): Promise<N8nCredential> {
    return this.http.getFetch()(`${this.backend}/workflow/credentials/${credentialId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getProcessedCredentialTypes(): Promise<unknown> {
    return this.http.getFetch()(`${this.backend}/workflow/processed-credential-types`, { method: "GET" }).then(r => r.json())
  }
}
