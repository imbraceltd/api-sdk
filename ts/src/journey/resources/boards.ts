import { HttpTransport } from "../../core/http.js"

export class JourneyBoardsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/journeys/v1/board` }

  async list() {
    return this.http.getFetch()(this.url, { method: "GET" }).then(r => r.json())
  }

  async create(body: {
    name: string
    description?: string
    workflow_id?: string
    team_ids?: string[]
  }) {
    return this.http.getFetch()(this.url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(boardId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.url}/${boardId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(boardId: string) {
    return this.http.getFetch()(`${this.url}/${boardId}`, { method: "DELETE" }).then(r => r.json())
  }
}
