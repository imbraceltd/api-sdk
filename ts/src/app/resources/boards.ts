import { HttpTransport } from "../../core/http.js"

export class BoardsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/v1/backend/board` }

  async list(params?: { limit?: number; skip?: number }) {
    const url = new URL(this.url)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(boardId: string) {
    return this.http.getFetch()(`${this.url}/${boardId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: { name: string; description?: string }) {
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

  async listItems(boardId: string, params?: { limit?: number; skip?: number }) {
    const url = new URL(`${this.url}/${boardId}/board_items`)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getItem(boardId: string, itemId: string) {
    return this.http.getFetch()(`${this.url}/${boardId}/board_items/${itemId}`, { method: "GET" }).then(r => r.json())
  }

  async createItem(boardId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.url}/${boardId}/board_items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateItem(boardId: string, itemId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.url}/${boardId}/board_items/${itemId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteItem(boardId: string, itemId: string) {
    return this.http.getFetch()(`${this.url}/${boardId}/board_items/${itemId}`, { method: "DELETE" }).then(r => r.json())
  }

  async search(boardId: string, body: { q?: string; limit?: number; offset?: number }) {
    return this.http.getFetch()(`${this.base}/v1/backend/meilisearch/${boardId}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async exportCsv(boardId: string) {
    return this.http.getFetch()(`${this.url}/${boardId}/export_csv`, { method: "GET" }).then(r => r.text())
  }
}
