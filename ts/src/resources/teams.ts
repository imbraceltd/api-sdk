import { HttpTransport } from "../http.js"

export class TeamsResource {
  /**
   * @param base - platform base URL (gateway/platform)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }
  private get v2() { return `${this.base}/v2` }

  async list(params?: { type?: string; limit?: number; skip?: number; q?: string }) {
    const url = new URL(`${this.v2}/teams`)
    if (params?.type)   url.searchParams.set("type",  params.type)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.q)      url.searchParams.set("q",     params.q)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listMy() {
    return this.http.getFetch()(`${this.v2}/teams/my`, { method: "GET" }).then(r => r.json())
  }

  async create(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/teams`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(teamId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/teams/${teamId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(teamId: string): Promise<void> {
    await this.http.getFetch()(`${this.v2}/teams/${teamId}`, { method: "DELETE" })
  }

  async addUsers(body: { team_id: string; user_ids: string[] }) {
    return this.http.getFetch()(`${this.v2}/teams/_add_users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async removeUsers(body: { user_ids: string[] }) {
    return this.http.getFetch()(`${this.v2}/teams/_remove_users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getUsers(teamId: string) {
    return this.http.getFetch()(`${this.v1}/team/${teamId}/users`, { method: "GET" }).then(r => r.json())
  }

  async getWorkflows(teamId: string) {
    return this.http.getFetch()(`${this.v1}/teams/${teamId}/workflows`, { method: "GET" }).then(r => r.json())
  }

  async join(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/teams/_join_team`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async leave(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/teams/_leave`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async requestJoin(teamId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/teams/${teamId}/join_request`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async approveJoinRequest(teamId: string, teamUserId: string) {
    return this.http.getFetch()(`${this.v2}/teams/${teamId}/user/${teamUserId}/approve`, {
      method: "POST",
    }).then(r => r.json())
  }

  async updateUserRole(teamId: string, teamUserId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/teams/${teamId}/user/${teamUserId}/role`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
