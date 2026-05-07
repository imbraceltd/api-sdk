import { HttpTransport } from "../http.js"

// ── Channel automation interfaces ─────────────────────────────────────────────

export interface ChannelAutomationItem {
  id: string
  name?: string
  active?: boolean
  tags?: { id: string; name: string }[]
  [key: string]: unknown
}

// ── Workflow flow / runs / folders / connections / pieces / MCP / tables ──────

export interface ApPage<T> {
  data: T[]
  next: string | null
  previous: string | null
}

export interface Flow {
  id: string
  created: string
  updated: string
  projectId: string
  externalId: string
  status: 'ENABLED' | 'DISABLED'
  operationStatus: string
  version: FlowVersion
}

export interface FlowVersion {
  id: string
  created: string
  updated: string
  flowId: string
  displayName: string
  trigger: Record<string, unknown>
  steps?: Record<string, unknown>
  valid?: boolean
}

export interface FlowRun {
  id: string
  created: string
  updated: string
  projectId: string
  flowId: string
  flowVersionId: string
  status: 'RUNNING' | 'SUCCEEDED' | 'FAILED' | 'TIMEOUT' | 'PAUSED' | 'STOPPED'
  environment: 'PRODUCTION' | 'TESTING'
  startTime?: string
  finishTime?: string
  failParentOnFailure: boolean
  tags?: string[]
  [key: string]: unknown
}

export interface WorkflowFolder {
  id: string
  created: string
  updated: string
  displayName: string
  projectId: string
}

export interface AppConnection {
  id: string
  created: string
  updated: string
  externalId: string
  displayName: string
  pieceName: string
  projectId: string
  type: 'SECRET_TEXT' | 'OAUTH2' | 'CLOUD_OAUTH2' | 'PLATFORM_OAUTH2' | 'BASIC_AUTH' | 'CUSTOM_AUTH'
  [key: string]: unknown
}

export interface Piece {
  id: string
  name: string
  displayName: string
  description: string
  logoUrl: string
  version: string
  categories: string[]
  actions: number
  triggers: number
  authors: string[]
  [key: string]: unknown
}

export interface McpServer {
  id: string
  created: string
  updated: string
  projectId: string
  name?: string
  [key: string]: unknown
}

export interface UserInvitation {
  id: string
  created: string
  updated: string
  email: string
  type: 'PLATFORM' | 'PROJECT'
  status: string
  [key: string]: unknown
}

export interface WorkflowTable {
  id: string
  created: string
  updated: string
  name: string
  projectId: string
  [key: string]: unknown
}

export interface WorkflowRecord {
  id: string
  created: string
  updated: string
  tableId: string
  cells: Record<string, unknown>
  [key: string]: unknown
}

export interface TriggerRunStatus {
  pieces: Record<string, {
    dailyStats: Record<string, { success: number; failure: number }>
  }>
}

// ── List params ───────────────────────────────────────────────────────────────

export interface ListParams {
  limit?: number
  cursor?: string
}

export interface FlowListParams extends ListParams {
  projectId?: string
  folderId?: string
  status?: 'ENABLED' | 'DISABLED'
}

export interface RunListParams extends ListParams {
  flowId?: string
  status?: FlowRun['status']
  projectId?: string
  tags?: string[]
  createdAfter?: string
  createdBefore?: string
}

export interface ConnectionListParams extends ListParams {
  projectId?: string
  pieceName?: string
}

export interface InvitationListParams extends ListParams {
  type: 'PLATFORM' | 'PROJECT'
  projectId?: string
  [key: string]: unknown
}

export interface RecordListParams {
  tableId: string
  limit?: number
  cursor?: string
  [key: string]: unknown
}

// ── Resource ──────────────────────────────────────────────────────────────────

export class WorkflowsResource {
  private readonly apBase: string

  /**
   * @param backend - backend base URL (`{gateway}/v1/backend`).
   *   Channel automation routes respond on v2/backend.
   * @param apBase  - workflow engine base URL (`{gateway}/activepieces`)
   *   for flows, runs, folders, connections, pieces, MCP servers, tables.
   */
  constructor(
    private readonly http: HttpTransport,
    private readonly backend: string,
    apBase: string,
  ) {
    this.apBase = apBase.replace(/\/$/, '')
  }

  private get v2() {
    return this.backend.replace("/v1/", "/v2/")
  }

  private apUrl(path: string, params?: Record<string, string | number | boolean | undefined>) {
    const u = new URL(`${this.apBase}${path}`)
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        if (v !== undefined && v !== null && v !== '') u.searchParams.set(k, String(v))
      }
    }
    return u.toString()
  }

  private apFetch<T>(url: string, init?: RequestInit): Promise<T> {
    return this.http.getFetch()(url, init).then(r => {
      if (r.status === 204 || r.headers.get('content-length') === '0') return undefined as T
      return r.json() as T
    })
  }

  // ── Channel automation ─────────────────────────────────────────────────────

  async listChannelAutomation(params?: { channelType?: string }): Promise<{ data: ChannelAutomationItem[] }> {
    const url = new URL(`${this.v2}/workflows/channel_automation`)
    if (params?.channelType) url.searchParams.set("channelType", params.channelType)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ── Flows ──────────────────────────────────────────────────────────────────

  listFlows(params?: FlowListParams): Promise<ApPage<Flow>> {
    return this.apFetch(this.apUrl('/v1/flows', params as Record<string, string>))
  }

  getFlow(flowId: string): Promise<Flow> {
    return this.apFetch(this.apUrl(`/v1/flows/${flowId}`))
  }

  createFlow(body: { displayName: string; projectId: string }): Promise<Flow> {
    return this.apFetch(this.apUrl('/v1/flows'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  deleteFlow(flowId: string): Promise<void> {
    return this.apFetch(this.apUrl(`/v1/flows/${flowId}`), { method: 'DELETE' })
  }

  applyFlowOperation(flowId: string, body: Record<string, unknown>): Promise<Flow> {
    return this.apFetch(this.apUrl(`/v1/flows/${flowId}`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  triggerFlow(flowId: string, payload?: Record<string, unknown>): Promise<unknown> {
    return this.apFetch(this.apUrl(`/v1/webhooks/${flowId}`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload ?? {}),
    })
  }

  triggerFlowSync(flowId: string, payload?: Record<string, unknown>): Promise<unknown> {
    return this.apFetch(this.apUrl(`/v1/webhooks/${flowId}/sync`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload ?? {}),
    })
  }

  // ── Flow Runs ──────────────────────────────────────────────────────────────

  listRuns(params?: RunListParams): Promise<ApPage<FlowRun>> {
    return this.apFetch(this.apUrl('/v1/flow-runs', params as Record<string, string>))
  }

  getRun(runId: string): Promise<FlowRun> {
    return this.apFetch(this.apUrl(`/v1/flow-runs/${runId}`))
  }

  // ── Folders ────────────────────────────────────────────────────────────────

  listFolders(params?: ListParams): Promise<ApPage<WorkflowFolder>> {
    return this.apFetch(this.apUrl('/v1/folders', params as Record<string, string>))
  }

  getFolder(folderId: string): Promise<WorkflowFolder> {
    return this.apFetch(this.apUrl(`/v1/folders/${folderId}`))
  }

  createFolder(body: { displayName: string; projectId: string }): Promise<WorkflowFolder> {
    return this.apFetch(this.apUrl('/v1/folders'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  updateFolder(folderId: string, body: { displayName: string }): Promise<WorkflowFolder> {
    return this.apFetch(this.apUrl(`/v1/folders/${folderId}`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  deleteFolder(folderId: string): Promise<void> {
    return this.apFetch(this.apUrl(`/v1/folders/${folderId}`), { method: 'DELETE' })
  }

  // ── App Connections ────────────────────────────────────────────────────────

  listConnections(params?: ConnectionListParams): Promise<ApPage<AppConnection>> {
    return this.apFetch(this.apUrl('/v1/app-connections', params as Record<string, string>))
  }

  getConnection(connectionId: string): Promise<AppConnection> {
    return this.apFetch(this.apUrl(`/v1/app-connections/${connectionId}`))
  }

  upsertConnection(body: Record<string, unknown>): Promise<AppConnection> {
    return this.apFetch(this.apUrl('/v1/app-connections'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  deleteConnection(connectionId: string): Promise<void> {
    return this.apFetch(this.apUrl(`/v1/app-connections/${connectionId}`), { method: 'DELETE' })
  }

  // ── Pieces ─────────────────────────────────────────────────────────────────

  listPieces(params?: ListParams): Promise<Piece[]> {
    return this.apFetch(this.apUrl('/v1/pieces', params as Record<string, string>))
  }

  // ── Triggers ───────────────────────────────────────────────────────────────

  getTriggerRunStatus(): Promise<TriggerRunStatus> {
    return this.apFetch(this.apUrl('/v1/trigger-runs/status'))
  }

  testTrigger(body: Record<string, unknown>): Promise<unknown> {
    return this.apFetch(this.apUrl('/v1/test-trigger'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  // ── Tables & Records ───────────────────────────────────────────────────────

  listTables(params?: ListParams): Promise<ApPage<WorkflowTable>> {
    return this.apFetch(this.apUrl('/v1/tables', params as Record<string, string>))
  }

  getTable(tableId: string): Promise<WorkflowTable> {
    return this.apFetch(this.apUrl(`/v1/tables/${tableId}`))
  }

  listRecords(params: RecordListParams): Promise<ApPage<WorkflowRecord>> {
    return this.apFetch(this.apUrl('/v1/records', params as Record<string, string>))
  }

  // ── MCP Servers ────────────────────────────────────────────────────────────

  listMcpServers(projectId: string): Promise<ApPage<McpServer>> {
    return this.apFetch(this.apUrl('/v1/mcp-servers', { projectId }))
  }

  getMcpServer(mcpServerId: string): Promise<McpServer> {
    return this.apFetch(this.apUrl(`/v1/mcp-servers/${mcpServerId}`))
  }

  createMcpServer(body: Record<string, unknown>): Promise<McpServer> {
    return this.apFetch(this.apUrl('/v1/mcp-servers'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  deleteMcpServer(mcpServerId: string): Promise<void> {
    return this.apFetch(this.apUrl(`/v1/mcp-servers/${mcpServerId}`), { method: 'DELETE' })
  }

  rotateMcpToken(mcpServerId: string): Promise<McpServer> {
    return this.apFetch(this.apUrl(`/v1/mcp-servers/${mcpServerId}/rotate`), { method: 'POST' })
  }

  // ── User Invitations ───────────────────────────────────────────────────────

  listInvitations(params: InvitationListParams): Promise<ApPage<UserInvitation>> {
    return this.apFetch(this.apUrl('/v1/user-invitations', params as Record<string, string>))
  }

  deleteInvitation(invitationId: string): Promise<void> {
    return this.apFetch(this.apUrl(`/v1/user-invitations/${invitationId}`), { method: 'DELETE' })
  }
}
