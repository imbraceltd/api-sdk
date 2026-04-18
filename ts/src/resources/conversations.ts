import { HttpTransport } from "../http.js"

export class ConversationsResource {
  /**
   * @param base - channel-service base URL (gateway/channel-service)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }
  private get v2() { return `${this.base}/v2` }

  // ─── Team Conversations ──────────────────────────────────────────────────────

  async list(params?: {
    type?: string
    q?: string
    limit?: number
    skip?: number
    sort?: string
  }) {
    const url = new URL(`${this.v2}/team_conversations`)
    if (params?.type)   url.searchParams.set("type",  params.type)
    if (params?.q)      url.searchParams.set("q",     params.q)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.sort)   url.searchParams.set("sort",  params.sort)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(convId: string) {
    return this.http.getFetch()(`${this.v1}/team_conversations/${convId}`, { method: "GET" }).then(r => r.json())
  }

  async getByConversationId(conversationId: string) {
    const url = new URL(`${this.v1}/team_conversations`)
    url.searchParams.set("type", "conversation_id")
    url.searchParams.set("q",    conversationId)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async search(params: { businessUnitId: string; q: string; limit?: number; skip?: number }) {
    const url = new URL(`${this.v1}/team_conversations/_search`)
    url.searchParams.set("business_unit_id", params.businessUnitId)
    url.searchParams.set("type",             "text")
    url.searchParams.set("q",               params.q)
    if (params.limit) url.searchParams.set("limit", String(params.limit))
    if (params.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getViewsCount(params?: { type?: string; q?: string }) {
    const url = new URL(`${this.v2}/team_conversations/_views_count`)
    if (params?.type) url.searchParams.set("type", params.type)
    if (params?.q)    url.searchParams.set("q",    params.q)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getOutstanding(params: { businessUnitId: string; limit?: number; skip?: number }) {
    const url = new URL(`${this.v1}/team_conversations/_outstanding`)
    url.searchParams.set("type", "business_unit_id")
    url.searchParams.set("q",    params.businessUnitId)
    if (params.limit) url.searchParams.set("limit", String(params.limit))
    if (params.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async join(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/team_conversations/_join`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async leave(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/team_conversations/_leave`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateStatus(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/team_conversations/_update_status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateName(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/team_conversations/_update_name`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async initVideoCall(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/team_conversations/_init_jaas_conference`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async assignTeamMember(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/team_conversations/assign_team_member`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async removeTeamMember(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/team_conversations/remove_team_member`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getInvitableUsers(teamConvId: string) {
    return this.http.getFetch()(`${this.v1}/team_conversations/${teamConvId}/users`, { method: "GET" }).then(r => r.json())
  }

  // ─── Single Conversation ─────────────────────────────────────────────────────

  async getConversation(conversationId: string) {
    return this.http.getFetch()(`${this.v1}/conversations/${conversationId}`, { method: "GET" }).then(r => r.json())
  }

  // ─── Create standalone conversation ─────────────────────────────────────────

  async create(body?: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/conversations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body ?? {}),
    }).then(r => r.json())
  }

  async joinRequest(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/team_conversations/_join_request`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
