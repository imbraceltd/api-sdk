import { HttpTransport } from "../http.js"

// ── Interfaces ────────────────────────────────────────────────────────────────

export interface PaginationMeta {
  total?: string | number
  page?: number
  limit?: number
  total_pages?: number
  [key: string]: unknown
}

export interface FinancialFileDetail {
  message?: string
  importedFile?: { data: Record<string, unknown>[]; pagination: PaginationMeta }
  report?: { data: Record<string, unknown>[]; pagination: PaginationMeta }
  [key: string]: unknown
}

export interface FinancialReportDetail {
  data: Record<string, unknown>[]
  pagination?: PaginationMeta
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

export interface UpdateFileInput { [key: string]: unknown }
export interface UpdateReportInput { [key: string]: unknown }

// ── Error ─────────────────────────────────────────────────────────────────────

/**
 * Thrown when a Financial Documents endpoint returns the FastAPI default
 * "Not Found" 404 — meaning the route is not registered on the gateway.
 *
 * Distinct from "ID not found" (which has a custom error message).
 */
export class FinancialDocumentsNotDeployedError extends Error {
  constructor(public readonly endpoint: string) {
    super(
      `Financial Documents endpoint "${endpoint}" is not deployed on this gateway. ` +
      `These methods (getFile/getReport/listErrors/suggest/fix/reset/update*/delete*) ` +
      `belong to a backend module that may not be exposed on every iMBRACE environment. ` +
      `Contact the iMBRACE backend team or use a gateway URL that fronts the Financial ` +
      `Management module.`
    )
    this.name = "FinancialDocumentsNotDeployedError"
  }
}

async function withNotDeployedCheck<T>(endpoint: string, fn: () => Promise<T>): Promise<T> {
  try {
    return await fn()
  } catch (e: any) {
    const msg = String(e?.message ?? "")
    if (msg.includes("[404]") && msg.includes('"detail":"Not Found"')) {
      throw new FinancialDocumentsNotDeployedError(endpoint)
    }
    throw e
  }
}

// ── Resource ──────────────────────────────────────────────────────────────────

/**
 * Financial Documents — multi-step review/correction workflow for documents
 * extracted via {@link ChatAiResource.processDocument}.
 *
 * All methods route to `/v2/ai/financial_documents/*`.
 *
 * **@experimental**: requires the Financial Management backend module to be
 * deployed on your gateway. If not deployed, calls throw
 * {@link FinancialDocumentsNotDeployedError} with a clear message.
 *
 * For one-shot extraction, use {@link ChatAiResource.processDocument} instead.
 */
export class FinancialDocumentsResource {
  /**
   * @param base - AI service base URL (gateway root).
   *   All methods append `/v2/ai/financial_documents/...`.
   */
  constructor(
    private readonly http: HttpTransport,
    private readonly base: string,
  ) {}

  private get v2() { return `${this.base.replace(/\/$/, "")}/v2/ai/financial_documents` }

  // ── File / Report detail (paginated) — @experimental ───────────────────────

  /** @experimental */
  async getFile(id: string, params?: { page?: number; limit?: number }): Promise<FinancialFileDetail> {
    const url = new URL(`${this.v2}/${id}`)
    if (params?.page  !== undefined) url.searchParams.set("page",  String(params.page))
    if (params?.limit !== undefined) url.searchParams.set("limit", String(params.limit))
    return withNotDeployedCheck(`GET ${url.pathname}`, async () =>
      this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
    )
  }

  /** @experimental */
  async getReport(id: string, params?: { page?: number; limit?: number }): Promise<FinancialReportDetail> {
    const url = new URL(`${this.v2}/reports/${id}`)
    if (params?.page  !== undefined) url.searchParams.set("page",  String(params.page))
    if (params?.limit !== undefined) url.searchParams.set("limit", String(params.limit))
    return withNotDeployedCheck(`GET ${url.pathname}`, async () =>
      this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
    )
  }

  // ── Errors — @experimental ─────────────────────────────────────────────────

  /** @experimental */
  async listErrors(fileId: string, params?: { limit?: number }): Promise<FinancialErrorListResponse> {
    const url = new URL(`${this.v2}/errors-files/${fileId}`)
    url.searchParams.set("limit", String(params?.limit ?? -1))
    return withNotDeployedCheck(`GET ${url.pathname}`, async () =>
      this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
    )
  }

  // ── Suggest / Fix / Reset — @experimental ──────────────────────────────────

  /** @experimental */
  async suggest(body: SuggestInput): Promise<SuggestResponse> {
    return withNotDeployedCheck("POST /v2/ai/financial_documents/suggest", async () =>
      this.http.getFetch()(`${this.v2}/suggest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }).then(r => r.json())
    )
  }

  /** @experimental */
  async fix(body: FixInput): Promise<FixResponse> {
    return withNotDeployedCheck("POST /v2/ai/financial_documents/fix", async () =>
      this.http.getFetch()(`${this.v2}/fix`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }).then(r => r.json())
    )
  }

  /** @experimental */
  async reset(body?: ResetInput): Promise<ResetResponse> {
    return withNotDeployedCheck("POST /v2/ai/financial_documents/reset", async () =>
      this.http.getFetch()(`${this.v2}/reset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body ?? {}),
      }).then(r => r.json())
    )
  }

  // ── Update — @experimental ─────────────────────────────────────────────────

  /** @experimental */
  async updateFile(id: string, body: UpdateFileInput): Promise<FinancialFileDetail> {
    return withNotDeployedCheck(`PUT /v2/ai/financial_documents/${id}`, async () =>
      this.http.getFetch()(`${this.v2}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }).then(r => r.json())
    )
  }

  /** @experimental */
  async updateReport(id: string, body: UpdateReportInput): Promise<FinancialReportDetail> {
    return withNotDeployedCheck(`PUT /v2/ai/financial_documents/reports/${id}`, async () =>
      this.http.getFetch()(`${this.v2}/reports/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }).then(r => r.json())
    )
  }

  // ── Delete — @experimental ─────────────────────────────────────────────────

  /** @experimental */
  async deleteFile(id: string): Promise<void> {
    await withNotDeployedCheck(`DELETE /v2/ai/financial_documents/${id}`, async () => {
      await this.http.getFetch()(`${this.v2}/${id}`, { method: "DELETE" })
    })
  }

  /** @experimental */
  async deleteReport(id: string): Promise<void> {
    await withNotDeployedCheck(`DELETE /v2/ai/financial_documents/reports/${id}`, async () => {
      await this.http.getFetch()(`${this.v2}/reports/${id}`, { method: "DELETE" })
    })
  }
}
