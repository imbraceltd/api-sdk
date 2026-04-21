import { HttpTransport } from "../http.js"

// ── Shared ────────────────────────────────────────────────────────────────────

export interface ApPage<T> {
  data: T[]
  next: string | null
  previous: string | null
}

export interface ApFlow {
  id: string
  created: string
  updated: string
  projectId: string
  externalId: string
  status: 'ENABLED' | 'DISABLED'
  operationStatus: string
  version: ApFlowVersion
}

export interface ApFlowVersion {
  id: string
  created: string
  updated: string
  flowId: string
  displayName: string
  trigger: Record<string, unknown>
  steps?: Record<string, unknown>
  valid?: boolean
}

export interface ApFlowRun {
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

export interface ApFolder {
  id: string
  created: string
  updated: string
  displayName: string
  projectId: string
}

export interface ApAppConnection {
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

export interface ApPiece {
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

export interface ApMcpServer {
  id: string
  created: string
  updated: string
  projectId: string
  name?: string
  [key: string]: unknown
}

export interface ApUserInvitation {
  id: string
  created: string
  updated: string
  email: string
  type: 'PLATFORM' | 'PROJECT'
  status: string
  [key: string]: unknown
}

export interface ApTable {
  id: string
  created: string
  updated: string
  name: string
  projectId: string
  [key: string]: unknown
}

export interface ApRecord {
  id: string
  created: string
  updated: string
  tableId: string
  cells: Record<string, unknown>
  [key: string]: unknown
}

export interface ApTriggerRunStatus {
  pieces: Record<string, {
    dailyStats: Record<string, { success: number; failure: number }>
  }>
}

// ── List params ───────────────────────────────────────────────────────────────

export interface ApListParams {
  limit?: number
  cursor?: string
}

export interface ApFlowListParams extends ApListParams {
  projectId?: string
  folderId?: string
  status?: 'ENABLED' | 'DISABLED'
}

export interface ApRunListParams extends ApListParams {
  flowId?: string
  status?: ApFlowRun['status']
  projectId?: string
  tags?: string[]
  createdAfter?: string
  createdBefore?: string
}

export interface ApConnectionListParams extends ApListParams {
  projectId?: string
  pieceName?: string
}

export interface ApInvitationListParams extends ApListParams {
  type: 'PLATFORM' | 'PROJECT'
  projectId?: string
  [key: string]: unknown
}

export interface ApRecordListParams {
  tableId: string
  limit?: number
  cursor?: string
  [key: string]: unknown
}

// ── Resource ──────────────────────────────────────────────────────────────────

export class ActivePiecesResource {
  private readonly base: string

  constructor(private readonly http: HttpTransport, base: string) {
    this.base = base.replace(/\/$/, '')
  }

  private url(path: string, params?: Record<string, string | number | boolean | undefined>) {
    const u = new URL(`${this.base}${path}`)
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        if (v !== undefined && v !== null && v !== '') u.searchParams.set(k, String(v))
      }
    }
    return u.toString()
  }

  private fetch<T>(url: string, init?: RequestInit): Promise<T> {
    return this.http.getFetch()(url, init).then(r => {
      if (r.status === 204 || r.headers.get('content-length') === '0') return undefined as T
      return r.json() as T
    })
  }

  // ── Flows ──────────────────────────────────────────────────────────────────

  listFlows(params?: ApFlowListParams): Promise<ApPage<ApFlow>> {
    return this.fetch(this.url('/v1/flows', params as Record<string, string>))
  }

  getFlow(flowId: string): Promise<ApFlow> {
    return this.fetch(this.url(`/v1/flows/${flowId}`))
  }

  createFlow(body: { displayName: string; projectId: string }): Promise<ApFlow> {
    return this.fetch(this.url('/v1/flows'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  deleteFlow(flowId: string): Promise<void> {
    return this.fetch(this.url(`/v1/flows/${flowId}`), { method: 'DELETE' })
  }

  applyFlowOperation(flowId: string, body: Record<string, unknown>): Promise<ApFlow> {
    return this.fetch(this.url(`/v1/flows/${flowId}`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  triggerFlow(flowId: string, payload?: Record<string, unknown>): Promise<unknown> {
    return this.fetch(this.url(`/v1/webhooks/${flowId}`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload ?? {}),
    })
  }

  triggerFlowSync(flowId: string, payload?: Record<string, unknown>): Promise<unknown> {
    return this.fetch(this.url(`/v1/webhooks/${flowId}/sync`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload ?? {}),
    })
  }

  // ── Flow Runs ──────────────────────────────────────────────────────────────

  listRuns(params?: ApRunListParams): Promise<ApPage<ApFlowRun>> {
    return this.fetch(this.url('/v1/flow-runs', params as Record<string, string>))
  }

  getRun(runId: string): Promise<ApFlowRun> {
    return this.fetch(this.url(`/v1/flow-runs/${runId}`))
  }

  // ── Folders ────────────────────────────────────────────────────────────────

  listFolders(params?: ApListParams): Promise<ApPage<ApFolder>> {
    return this.fetch(this.url('/v1/folders', params as Record<string, string>))
  }

  getFolder(folderId: string): Promise<ApFolder> {
    return this.fetch(this.url(`/v1/folders/${folderId}`))
  }

  createFolder(body: { displayName: string; projectId: string }): Promise<ApFolder> {
    return this.fetch(this.url('/v1/folders'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  updateFolder(folderId: string, body: { displayName: string }): Promise<ApFolder> {
    return this.fetch(this.url(`/v1/folders/${folderId}`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  deleteFolder(folderId: string): Promise<void> {
    return this.fetch(this.url(`/v1/folders/${folderId}`), { method: 'DELETE' })
  }

  // ── App Connections ────────────────────────────────────────────────────────

  listConnections(params?: ApConnectionListParams): Promise<ApPage<ApAppConnection>> {
    return this.fetch(this.url('/v1/app-connections', params as Record<string, string>))
  }

  getConnection(connectionId: string): Promise<ApAppConnection> {
    return this.fetch(this.url(`/v1/app-connections/${connectionId}`))
  }

  upsertConnection(body: Record<string, unknown>): Promise<ApAppConnection> {
    return this.fetch(this.url('/v1/app-connections'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  deleteConnection(connectionId: string): Promise<void> {
    return this.fetch(this.url(`/v1/app-connections/${connectionId}`), { method: 'DELETE' })
  }

  // ── Pieces ─────────────────────────────────────────────────────────────────

  listPieces(params?: ApListParams): Promise<ApPiece[]> {
    return this.fetch(this.url('/v1/pieces', params as Record<string, string>))
  }

  // ── Triggers ───────────────────────────────────────────────────────────────

  getTriggerRunStatus(): Promise<ApTriggerRunStatus> {
    return this.fetch(this.url('/v1/trigger-runs/status'))
  }

  testTrigger(body: Record<string, unknown>): Promise<unknown> {
    return this.fetch(this.url('/v1/test-trigger'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  // ── Tables & Records ───────────────────────────────────────────────────────

  listTables(params?: ApListParams): Promise<ApPage<ApTable>> {
    return this.fetch(this.url('/v1/tables', params as Record<string, string>))
  }

  getTable(tableId: string): Promise<ApTable> {
    return this.fetch(this.url(`/v1/tables/${tableId}`))
  }

  listRecords(params: ApRecordListParams): Promise<ApPage<ApRecord>> {
    return this.fetch(this.url('/v1/records', params as Record<string, string>))
  }

  // ── MCP Servers ────────────────────────────────────────────────────────────

  listMcpServers(projectId: string): Promise<ApPage<ApMcpServer>> {
    return this.fetch(this.url('/v1/mcp-servers', { projectId }))
  }

  getMcpServer(mcpServerId: string): Promise<ApMcpServer> {
    return this.fetch(this.url(`/v1/mcp-servers/${mcpServerId}`))
  }

  createMcpServer(body: Record<string, unknown>): Promise<ApMcpServer> {
    return this.fetch(this.url('/v1/mcp-servers'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  }

  deleteMcpServer(mcpServerId: string): Promise<void> {
    return this.fetch(this.url(`/v1/mcp-servers/${mcpServerId}`), { method: 'DELETE' })
  }

  rotateMcpToken(mcpServerId: string): Promise<ApMcpServer> {
    return this.fetch(this.url(`/v1/mcp-servers/${mcpServerId}/rotate`), { method: 'POST' })
  }

  // ── User Invitations ───────────────────────────────────────────────────────

  listInvitations(params: ApInvitationListParams): Promise<ApPage<ApUserInvitation>> {
    return this.fetch(this.url('/v1/user-invitations', params as Record<string, string>))
  }

  deleteInvitation(invitationId: string): Promise<void> {
    return this.fetch(this.url(`/v1/user-invitations/${invitationId}`), { method: 'DELETE' })
  }
}
