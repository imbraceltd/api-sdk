import { HttpTransport } from "../http.js"

export interface DataFile {
  _id: string
  name?: string
  path?: string
  size?: number
  mime_type?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export interface DataFileListResponse {
  data: DataFile[]
  total?: number
  [key: string]: unknown
}

export interface DeleteDataFilesInput {
  ids: string[]
  [key: string]: unknown
}

export class DataFilesResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get filesBase() { return `${this.base.replace(/\/$/, "")}/files` }

  async search(params?: Record<string, string>): Promise<DataFileListResponse> {
    const url = new URL(`${this.filesBase}/search`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(fileId: string): Promise<DataFile> {
    return this.http.getFetch()(`${this.filesBase}/${fileId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: Record<string, unknown>): Promise<DataFile> {
    return this.http.getFetch()(this.filesBase, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(fileId: string, body: Record<string, unknown>): Promise<DataFile> {
    return this.http.getFetch()(`${this.filesBase}/${fileId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(fileIds: string[]): Promise<Record<string, unknown>> {
    return this.http.getFetch()(`${this.filesBase}/delete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids: fileIds }),
    }).then(r => r.json())
  }

  async upload(formData: FormData): Promise<DataFile> {
    return this.http.getFetch()(`${this.filesBase}/upload`, {
      method: "POST",
      body: formData,
    }).then(r => r.json())
  }

  async download(fileId: string): Promise<Response> {
    return this.http.getFetch()(`${this.filesBase}/${fileId}/download`, { method: "GET" })
  }
}
