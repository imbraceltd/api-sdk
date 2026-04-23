import { HttpTransport } from "../http.js"
import { randomUUID } from "crypto"

function buildQuery(params: Record<string, string | number | boolean | undefined>): string {
  const qs = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined) qs.set(k, String(v))
  }
  const s = qs.toString()
  return s ? `?${s}` : ""
}

export class AiAgentResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get orgId(): string | undefined {
    return this.http.organizationId
  }

  // --- System ---

  async getConfig(): Promise<any> {
    return this.http.getFetch()(`${this.base}/config`).then(r => r.json())
  }

  async getHealth(detailed?: boolean): Promise<any> {
    return this.http.getFetch()(`${this.base}/health${buildQuery({ detailed })}`).then(r => r.json())
  }

  async getVersion(): Promise<any> {
    return this.http.getFetch()(`${this.base}/version`).then(r => r.json())
  }

  // --- Chat v1 ---

  async listChats(params?: { organization_id?: string; user_id?: string; limit?: number }): Promise<any> {
    const p = { organization_id: this.orgId, ...params }
    return this.http.getFetch()(`${this.base}/chat${buildQuery(p)}`).then(r => r.json())
  }

  async getChat(id: string, includeMessages?: boolean): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat/${id}${buildQuery({ include_messages: includeMessages })}`).then(r => r.json())
  }

  async deleteChat(id: string, params?: { organization_id?: string; user_id?: string }): Promise<any> {
    const p = { organization_id: this.orgId, ...params }
    return this.http.getFetch()(`${this.base}/chat/${id}${buildQuery(p)}`, { method: "DELETE" }).then(r => r.json())
  }

  // --- Chat v2 (streaming — returns raw Response for SSE consumption) ---

  async streamChat(body: {
    assistant_id: string
    messages: any[]
    id?: string
    organization_id?: string
    user_id?: string
    [key: string]: unknown
  }): Promise<Response> {
    let userId = body.user_id
    if (!userId) {
      const res = await this.http.getFetch()(`${this.base}/chat-client/auth/user`, { method: "POST" })
      const data = await res.json()
      userId = data.id
    }
    const payload = {
      organization_id: this.orgId,
      id: body.id ?? randomUUID(),
      ...body,
      user_id: userId,
    }
    return this.http.getFetch()(`${this.base}/v2/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  }

  // --- Sub-agent chat v2 ---

  async streamSubAgentChat(body: {
    assistant_id: string
    organization_id?: string
    session_id: string
    chat_id: string
    messages: any[]
    [key: string]: unknown
  }): Promise<Response> {
    const payload = { organization_id: this.orgId, ...body }
    return this.http.getFetch()(`${this.base}/v2/sub-agent-chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  }

  async getSubAgentHistory(params: { session_id: string; chat_id: string }): Promise<any> {
    return this.http.getFetch()(`${this.base}/v2/sub-agent-chat/history${buildQuery(params)}`).then(r => r.json())
  }

  // --- Prompt suggestions ---

  async getAgentPromptSuggestion(assistantId: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat/get-agent-prompt-suggestion${buildQuery({ assistant_id: assistantId })}`).then(r => r.json())
  }

  // --- Embeddings / files ---

  async processEmbedding(body: { fileId: string; options?: Record<string, unknown> }): Promise<any> {
    return this.http.getFetch()(`${this.base}/embedding/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async listEmbeddingFiles(params?: Record<string, string | number>): Promise<any> {
    return this.http.getFetch()(`${this.base}/embedding/files${buildQuery(params ?? {})}`).then(r => r.json())
  }

  async getEmbeddingFile(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/embedding/files/${id}`).then(r => r.json())
  }

  async previewEmbeddingFile(params?: Record<string, string>): Promise<any> {
    return this.http.getFetch()(`${this.base}/embedding/files/preview${buildQuery(params ?? {})}`).then(r => r.json())
  }

  async updateEmbeddingFileStatus(id: string, status: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/embedding/files/${id}/status`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    }).then(r => r.json())
  }

  async deleteEmbeddingFile(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/embedding/files/${id}`, { method: "DELETE" }).then(r => r.json())
  }

  async classifyFile(params?: Record<string, string>): Promise<any> {
    return this.http.getFetch()(`${this.base}/embedding/classify${buildQuery(params ?? {})}`).then(r => r.json())
  }

  // --- Data Board ---

  async suggestFieldTypes(body: { fields: { name: string; samples?: unknown[] }[] }): Promise<any> {
    return this.http.getFetch()(`${this.base}/data-board/suggest-field-types`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // --- Parquet ---

  async generateParquet(body: { data: any[]; fileName?: string; folderName?: string }): Promise<any> {
    return this.http.getFetch()(`${this.base}/parquet/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async listParquetFiles(): Promise<any> {
    return this.http.getFetch()(`${this.base}/parquet/files`).then(r => r.json())
  }

  async deleteParquetFile(fileName: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/parquet/${encodeURIComponent(fileName)}`, { method: "DELETE" }).then(r => r.json())
  }

  // --- Trace (Tempo) ---

  async getTraces(params?: { service?: string; limit?: number; timeRange?: number; orgId?: string; details?: boolean }): Promise<any> {
    return this.http.getFetch()(`${this.base}/trace/traces${buildQuery(params ?? {})}`).then(r => r.json())
  }

  async getTrace(traceId: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/trace/traces/${traceId}`).then(r => r.json())
  }

  async getTraceServices(): Promise<any> {
    return this.http.getFetch()(`${this.base}/trace/services`).then(r => r.json())
  }

  async getTraceTags(): Promise<any> {
    return this.http.getFetch()(`${this.base}/trace/tags`).then(r => r.json())
  }

  async getTraceTagValues(tagName: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/trace/tags/${tagName}/values`).then(r => r.json())
  }

  async searchTraceQL(q: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/trace/search/traceql${buildQuery({ q })}`).then(r => r.json())
  }

  // --- Chat Client — Auth ---

  async verifyChatClientCredentials(body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/auth/verify-credentials`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async registerChatClient(body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getChatClientUser(body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/auth/user`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // --- Chat Client — Chats ---

  async createClientChat(body: {
    id: string
    assistantId: string
    organizationId: string
    userId: string
    selectedVisibilityType: string
    message: { id: string; role: string; content: string; createdAt: string; parts: { type: string; text: string }[] }
    [key: string]: unknown
  }): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/chats`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async listClientChats(params?: { limit?: number; starting_after?: string; ending_before?: string; organization_id?: string }): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/chats${buildQuery(params ?? {})}`).then(r => r.json())
  }

  async deleteAllClientChats(params?: { organization_id?: string }): Promise<any> {
    const p = { organization_id: this.orgId, ...params }
    return this.http.getFetch()(`${this.base}/chat-client/chats${buildQuery(p)}`, { method: "DELETE" }).then(r => r.json())
  }

  async getClientChat(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/chats/${id}`).then(r => r.json())
  }

  async updateClientChat(id: string, body: { assistantId?: string; visibility?: string }): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/chats/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteClientChat(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/chats/${id}`, { method: "DELETE" }).then(r => r.json())
  }

  /** Returns raw Response — consume as SSE stream. */
  async streamClientChatStatus(id: string): Promise<Response> {
    return this.http.getFetch()(`${this.base}/chat-client/chats/${id}/status/stream`)
  }

  async generateClientChatTitle(chatId: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/chats/${chatId}/title`, { method: "POST" }).then(r => r.json())
  }

  // --- Chat Client — Messages ---

  async persistClientMessage(body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async listClientMessages(chatId: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/chats/${chatId}/messages`).then(r => r.json())
  }

  async deleteTrailingMessages(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/messages/${id}/trailing`, { method: "DELETE" }).then(r => r.json())
  }

  // --- Chat Client — Votes ---

  async getVotes(chatId: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/chats/${chatId}/votes`).then(r => r.json())
  }

  async updateVote(body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/votes`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // --- Chat Client — Documents ---

  async createDocument(body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/documents`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getDocumentLatestByKind(params?: Record<string, string>): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/documents/latest-by-kind${buildQuery(params ?? {})}`).then(r => r.json())
  }

  async getDocument(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/documents/${id}`).then(r => r.json())
  }

  async getDocumentLatest(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/documents/${id}/latest`).then(r => r.json())
  }

  async getDocumentPublic(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/documents/${id}/public`).then(r => r.json())
  }

  async deleteDocument(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/documents/${id}`, { method: "DELETE" }).then(r => r.json())
  }

  async getDocumentSuggestions(documentId: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/chat-client/documents/${documentId}/suggestions`).then(r => r.json())
  }

  // --- Admin Guides ---

  async listAdminGuides(): Promise<any> {
    return this.http.getFetch()(`${this.base}/admin/guides`).then(r => r.json())
  }

  /** Returns raw Response — pipe to a file or consume directly (PDF stream). */
  async getAdminGuide(filename: string): Promise<Response> {
    return this.http.getFetch()(`${this.base}/admin/guides/${encodeURIComponent(filename)}`)
  }
}
