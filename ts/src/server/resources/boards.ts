import { HttpTransport } from "../../core/http.js"

export interface BoardItem {
  fields: Array<{ board_field_id: string; value: unknown }>
}

export class ServerBoardsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/3rd` }

  async search(boardId: string, body: {
    q?: string
    limit?: number
    offset?: number
    matchingStrategy?: string
  }) {
    return this.http.getFetch()(`${this.url}/board_search/${boardId}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ limit: 20, offset: 0, matchingStrategy: "last", ...body }),
    }).then(r => r.json())
  }

  async listItems(boardId: string, params?: { limit?: number; skip?: number }) {
    const url = new URL(`${this.url}/boards/${boardId}/board_items`)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async createItems(boardId: string, items: BoardItem[]) {
    return this.http.getFetch()(`${this.url}/boards/create/${boardId}/board_items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items }),
    }).then(r => r.json())
  }

  async updateItems(boardId: string, items: Array<{ id: string; fields: BoardItem["fields"] }>) {
    return this.http.getFetch()(`${this.url}/boards/update/${boardId}/board_items`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items }),
    }).then(r => r.json())
  }

  async deleteItems(boardId: string, ids: string[]) {
    return this.http.getFetch()(`${this.url}/boards/delete/${boardId}/board_items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids }),
    }).then(r => r.json())
  }

  async exportCsv(boardId: string) {
    return this.http.getFetch()(`${this.url}/boards/${boardId}/export_csv`, { method: "GET" }).then(r => r.text())
  }
}
