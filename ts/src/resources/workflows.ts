import { HttpTransport } from "../http.js"

// ─── Workflow interfaces ──────────────────────────────────────────────────────

export interface N8nWorkflow {
  id: string
  name: string
  active?: boolean
  nodes?: unknown[]
  connections?: unknown
  [key: string]: unknown
}

export interface N8nWorkflowListResponse {
  data: N8nWorkflow[]
  [key: string]: unknown
}

export interface CreateWorkflowInput {
  name: string
  nodes?: unknown[]
  connections?: unknown
  [key: string]: unknown
}

export interface UpdateWorkflowInput {
  name?: string
  active?: boolean
  nodes?: unknown[]
  connections?: unknown
  [key: string]: unknown
}

export interface ChannelAutomationItem {
  _id: string
  name?: string
  channel_type?: string
  [key: string]: unknown
}

// ─── Credential interfaces ────────────────────────────────────────────────────

export interface WorkflowCredential {
  id: string
  name: string
  type: string
  [key: string]: unknown
}

export interface CreateCredentialInput {
  name: string
  type: string
  data?: Record<string, unknown>
  [key: string]: unknown
}

export interface UpdateCredentialInput {
  name?: string
  data?: Record<string, unknown>
  [key: string]: unknown
}

export interface ChannelCredential {
  _id: string
  type?: string
  name?: string
  [key: string]: unknown
}

export interface UpdateChannelCredentialInput {
  [key: string]: unknown
}

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

  // ─── Channel automation (channel-service)

  async listChannelAutomation(params?: { channelType?: string }): Promise<ChannelAutomationItem[]> {
    const url = new URL(`${this.chV1}/workflows/channel_automation`)
    if (params?.channelType) url.searchParams.set("channelType", params.channelType)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ─── n8n workflows (platform)

  async list(params?: Record<string, string>): Promise<N8nWorkflowListResponse> {
    const url = new URL(`${this.plV1}/workflows`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(workflowId: string): Promise<N8nWorkflow> {
    return this.http.getFetch()(`${this.plV1}/n8n/workflows/${workflowId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: CreateWorkflowInput): Promise<N8nWorkflow> {
    return this.http.getFetch()(`${this.plV1}/n8n/workflows`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(workflowId: string, body: UpdateWorkflowInput): Promise<N8nWorkflow> {
    return this.http.getFetch()(`${this.plV1}/n8n/workflows/${workflowId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(workflowId: string): Promise<void> {
    await this.http.getFetch()(`${this.plV1}/n8n/workflows/${workflowId}`, { method: "DELETE" })
  }

  async getNew(): Promise<N8nWorkflow> {
    return this.http.getFetch()(`${this.plV1}/n8n/workflows/new`, { method: "GET" }).then(r => r.json())
  }

  // ─── Credentials

  async listCredentials(): Promise<WorkflowCredential[]> {
    return this.http.getFetch()(`${this.plV1}/credentials`, { method: "GET" }).then(r => r.json())
  }

  async getCredential(credentialId: string): Promise<WorkflowCredential> {
    const url = new URL(`${this.plV1}/n8n/credentials/${credentialId}`)
    url.searchParams.set("includeData", "true")
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async createCredential(body: CreateCredentialInput): Promise<WorkflowCredential> {
    return this.http.getFetch()(`${this.plV1}/n8n/credentials`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateCredential(credentialId: string, body: UpdateCredentialInput): Promise<WorkflowCredential> {
    return this.http.getFetch()(`${this.plV1}/n8n/credentials/${credentialId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteCredential(credentialId: string): Promise<void> {
    await this.http.getFetch()(`${this.plV1}/n8n/credentials/${credentialId}`, { method: "DELETE" })
  }

  // ─── Channel credentials (channel-service)

  async getChannelCredential(credentialId: string): Promise<ChannelCredential> {
    return this.http.getFetch()(`${this.chV1}/channels/credentials/${credentialId}`, { method: "GET" }).then(r => r.json())
  }

  async updateChannelCredential(credentialId: string, body: UpdateChannelCredentialInput): Promise<ChannelCredential> {
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
