import { HttpTransport } from "../http.js"

// ── Interfaces ────────────────────────────────────────────────────────────────

export interface PaginationMeta {
  total: string | number
  page: number
  limit: number
  total_pages: number
  [key: string]: unknown
}

export interface FinancialFileDetail {
  message?: string
  importedFile?: {
    data: Record<string, unknown>[]
    pagination: PaginationMeta
  }
  report?: {
    data: Record<string, unknown>[]
    pagination: PaginationMeta
  }
  [key: string]: unknown
}

export interface FinancialReportDetail {
  data: Record<string, unknown>[]
  pagination: PaginationMeta
  [key: string]: unknown
}

export interface FinancialFileError {
  _id?: string
  file_id?: string
  row?: number
  column?: string
  message?: string
  [key: string]: unknown
}

export interface FinancialErrorListResponse {
  data: FinancialFileError[]
  total?: number
  [key: string]: unknown
}

export interface SuggestInput {
  file_id?: string
  errors?: Record<string, unknown>[]
  [key: string]: unknown
}

export interface SuggestResponse {
  suggestions?: Record<string, unknown>[]
  [key: string]: unknown
}

export interface FixInput {
  file_id?: string
  fixes?: Record<string, unknown>[]
  [key: string]: unknown
}

export interface FixResponse {
  success?: boolean
  fixed?: number
  [key: string]: unknown
}

export interface ResetInput {
  file_id?: string
  [key: string]: unknown
}

export interface ResetResponse {
  success?: boolean
  [key: string]: unknown
}

export interface UpdateFileInput {
  [key: string]: unknown
}

export interface UpdateReportInput {
  [key: string]: unknown
}

// ── Resource ──────────────────────────────────────────────────────────────────

export class DocumentAIResource {
  /**
   * @param base - AI service base URL (gateway root). Methods append `/v2/ai/financial_documents/...`.
   *   This matches the path `/v2/ai/financial_documents/*` that the new-frontend UI calls.
   */
  constructor(
    private readonly http: HttpTransport,
    private readonly base: string,
  ) {}

  private get v2() {
    return `${this.base.replace(/\/$/, "")}/v2/ai/financial_documents`
  }

  // ── File / Report detail (paginated) ───────────────────────────────────────

  async getFile(id: string, params?: { page?: number; limit?: number }): Promise<FinancialFileDetail> {
    const url = new URL(`${this.v2}/${id}`)
    if (params?.page !== undefined) url.searchParams.set("page", String(params.page))
    if (params?.limit !== undefined) url.searchParams.set("limit", String(params.limit))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getReport(id: string, params?: { page?: number; limit?: number }): Promise<FinancialReportDetail> {
    const url = new URL(`${this.v2}/reports/${id}`)
    if (params?.page !== undefined) url.searchParams.set("page", String(params.page))
    if (params?.limit !== undefined) url.searchParams.set("limit", String(params.limit))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ── Errors ─────────────────────────────────────────────────────────────────

  async listErrors(fileId: string, params?: { limit?: number }): Promise<FinancialErrorListResponse> {
    const url = new URL(`${this.v2}/errors-files/${fileId}`)
    url.searchParams.set("limit", String(params?.limit ?? -1))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ── Suggest / Fix / Reset ──────────────────────────────────────────────────

  async suggest(body: SuggestInput): Promise<SuggestResponse> {
    return this.http.getFetch()(`${this.v2}/suggest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async fix(body: FixInput): Promise<FixResponse> {
    return this.http.getFetch()(`${this.v2}/fix`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async reset(body?: ResetInput): Promise<ResetResponse> {
    return this.http.getFetch()(`${this.v2}/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body ?? {}),
    }).then(r => r.json())
  }

  // ── Update ─────────────────────────────────────────────────────────────────

  async updateFile(id: string, body: UpdateFileInput): Promise<FinancialFileDetail> {
    return this.http.getFetch()(`${this.v2}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateReport(id: string, body: UpdateReportInput): Promise<FinancialReportDetail> {
    return this.http.getFetch()(`${this.v2}/reports/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ── Delete ─────────────────────────────────────────────────────────────────

  async deleteFile(id: string): Promise<void> {
    await this.http.getFetch()(`${this.v2}/${id}`, { method: "DELETE" })
  }

  async deleteReport(id: string): Promise<void> {
    await this.http.getFetch()(`${this.v2}/reports/${id}`, { method: "DELETE" })
  }
}
