import { HttpTransport } from "../http.js"

export interface FileModel {
  id: string
  user_id: string
  filename: string
  path?: string
  meta: {
    name: string
    content_type: string
    size: number
    data?: Record<string, unknown>
    virtual?: boolean
    [key: string]: unknown
  }
  data?: {
    content?: string
    [key: string]: unknown
  }
  created_at: number
  updated_at: number
}

export class FileServiceResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  /** Upload a file. */
  async uploadFile(
    body: FormData,
    opts?: { process?: boolean },
  ): Promise<FileModel> {
    const url = new URL(`${this.base}/`)
    if (opts?.process === false) url.searchParams.set("process", "false")
    return this.http.getFetch()(url, { method: "POST", body }).then(r => r.json())
  }

  /** Upload a file for a specific agent. */
  async uploadAgentFile(
    agentId: string,
    file: File,
    isRag = true,
  ): Promise<{ message: string; result: unknown }> {
    const form = new FormData()
    form.append("agent_id", agentId)
    form.append("file", file)
    form.append("is_rag", String(isRag))
    return this.http.getFetch()(`${this.base}/agent`, { method: "POST", body: form }).then(r => r.json())
  }

  /** Extract/embed a PDF file (no auth required). */
  async extractFile(file: File): Promise<{ message: string; result: unknown }> {
    const form = new FormData()
    form.append("file", file)
    return this.http.getFetch()(`${this.base}/extract`, { method: "POST", body: form }).then(r => r.json())
  }

  /** List all files accessible to the current user. */
  async listFiles(opts?: { content?: boolean }): Promise<FileModel[]> {
    const url = new URL(`${this.base}/`)
    if (opts?.content === false) url.searchParams.set("content", "false")
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  /** Search files by filename pattern (supports wildcards like *.txt). */
  async searchFiles(filename: string, opts?: { content?: boolean }): Promise<FileModel[]> {
    const url = new URL(`${this.base}/search`)
    url.searchParams.set("filename", filename)
    if (opts?.content === false) url.searchParams.set("content", "false")
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  /** Delete all files (admin only). */
  async deleteAllFiles(): Promise<{ message: string }> {
    return this.http.getFetch()(`${this.base}/all`, { method: "DELETE" }).then(r => r.json())
  }

  /** Get file metadata by ID. */
  async getFile(id: string): Promise<FileModel> {
    return this.http.getFetch()(`${this.base}/${id}`, { method: "GET" }).then(r => r.json())
  }

  /** Download file binary content. Pass attachment=true to force download header. */
  async downloadFile(id: string, opts?: { attachment?: boolean }): Promise<Response> {
    const url = new URL(`${this.base}/${id}/content`)
    if (opts?.attachment) url.searchParams.set("attachment", "true")
    return this.http.getFetch()(url, { method: "GET" })
  }

  /** Download file binary content by name. */
  async downloadFileByName(id: string, fileName: string): Promise<Response> {
    return this.http.getFetch()(`${this.base}/${id}/content/${encodeURIComponent(fileName)}`, { method: "GET" })
  }

  /** Get the HTML-rendered content of a file. */
  async getFileHtmlContent(id: string): Promise<Response> {
    return this.http.getFetch()(`${this.base}/${id}/content/html`, { method: "GET" })
  }

  /** Get the extracted text content of a file. */
  async getFileDataContent(id: string): Promise<{ content: string }> {
    return this.http.getFetch()(`${this.base}/${id}/data/content`, { method: "GET" }).then(r => r.json())
  }

  /** Update the extracted text content of a file. */
  async updateFileDataContent(id: string, content: string): Promise<{ content: string }> {
    return this.http.getFetch()(`${this.base}/${id}/data/content/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    }).then(r => r.json())
  }

  /** Delete a file by ID. */
  async deleteFile(id: string): Promise<{ message: string }> {
    return this.http.getFetch()(`${this.base}/${id}`, { method: "DELETE" }).then(r => r.json())
  }

  /** Build the public download URL for a file (no auth required). */
  getPublicDownloadUrl(id: string): string {
    const gatewayBase = this.base.replace(/\/(v1|v2)\/backend\/file-service$/, "").replace(/\/v1\/file-service$/, "")
    return `${gatewayBase}/files/download/${id}`
  }
}
