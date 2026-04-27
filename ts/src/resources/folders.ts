import { HttpTransport } from "../http.js"

export interface Folder {
  _id: string
  name?: string
  parent_id?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export interface FolderListResponse {
  data: Folder[]
  total?: number
  [key: string]: unknown
}

export class FoldersResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get foldersBase() { return `${this.base.replace(/\/$/, "")}/folders` }

  async search(params?: Record<string, string>): Promise<FolderListResponse> {
    const url = new URL(`${this.foldersBase}/search`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(folderId: string): Promise<Folder> {
    return this.http.getFetch()(`${this.foldersBase}/${folderId}`, { method: "GET" }).then(r => r.json())
  }

  async getContents(folderId: string): Promise<Record<string, unknown>> {
    return this.http.getFetch()(`${this.foldersBase}/${folderId}/contents`, { method: "GET" }).then(r => r.json())
  }

  async create(body: Record<string, unknown>): Promise<Folder> {
    return this.http.getFetch()(this.foldersBase, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(folderId: string, body: Record<string, unknown>): Promise<Folder> {
    return this.http.getFetch()(`${this.foldersBase}/${folderId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(folderIds: string[]): Promise<Record<string, unknown>> {
    return this.http.getFetch()(`${this.foldersBase}/delete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids: folderIds }),
    }).then(r => r.json())
  }
}
