import { HttpTransport } from "../http.js"

export class TeamsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async list(params?: { type?: string; limit?: number; skip?: number; q?: string }) {
    const url = new URL(`${this.base}/v2/backend/teams`)
    if (params?.type) url.searchParams.set("type", params.type)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.q) url.searchParams.set("q", params.q)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listMy() {
    return this.http.getFetch()(`${this.base}/v2/backend/teams/my`, { method: "GET" }).then(r => r.json())
  }

  async listAll() {
    return this.http.getFetch()(`${this.base}/v1/backend/teams/all`, { method: "GET" }).then(r => r.json())
  }

  async create(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/v1/backend/teams`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(teamId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/v2/backend/teams/${teamId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(teamId: string) {
    return this.http.getFetch()(`${this.base}/v2/backend/teams/${teamId}`, { method: "DELETE" }).then(r => r.json())
  }

  async addUsers(teamId: string, userIds: string[]) {
    return this.http.getFetch()(`${this.base}/v2/backend/teams/_add_users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ team_id: teamId, user_ids: userIds }),
    }).then(r => r.json())
  }

  async removeUsers(userIds: string[]) {
    return this.http.getFetch()(`${this.base}/v2/backend/teams/_remove_users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_ids: userIds }),
    }).then(r => r.json())
  }

  async getUsers(teamId: string) {
    return this.http.getFetch()(`${this.base}/v1/backend/team/${teamId}/users`, { method: "GET" }).then(r => r.json())
  }
}
