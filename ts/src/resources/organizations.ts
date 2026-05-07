import { HttpTransport } from "../http.js"
import type { Organization, PagedResponse } from "../types/index.js"

export interface CreateOrganizationInput {
  name: string
  plan?: string
  is_active?: boolean
  [key: string]: unknown
}

export class OrganizationsResource {
  constructor(
    private readonly http: HttpTransport,
    private readonly base: string,
    /** Gateway URL. Used to build legacy /v1/backend and /v2/backend paths. */
    private readonly gateway?: string,
    /** When true, route through legacy backend (platform service not deployed on prodv2). */
    private readonly legacy?: boolean,
  ) {}

  private get v1() {
    return this.legacy && this.gateway ? `${this.gateway}/v1/backend` : `${this.base}/v1`
  }
  private get v2() {
    return this.legacy && this.gateway ? `${this.gateway}/v2/backend` : `${this.base}/v2`
  }

  async list(params?: { limit?: number; skip?: number; is_active?: boolean }): Promise<PagedResponse<Organization>> {
    // Legacy backend has no paged /v2/backend/organizations — fall through to /_all
    if (this.legacy && this.gateway) {
      const all = await this.listAll({ is_active: params?.is_active })
      return { data: all, total: all.length, page: 1, limit: all.length }
    }
    const url = new URL(`${this.v2}/organizations`)
    if (params?.limit)  url.searchParams.set("limit",     String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.is_active !== undefined) url.searchParams.set("is_active", String(params.is_active))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listAll(params?: { is_active?: boolean }): Promise<Organization[]> {
    const url = new URL(`${this.v2}/organizations/_all`)
    if (params?.is_active !== undefined) url.searchParams.set("is_active", String(params.is_active))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json()).then((res: unknown) => {
      // Legacy backend wraps results in {object_name, data}
      if (res && typeof res === "object" && "data" in (res as Record<string, unknown>)) {
        return (res as { data: Organization[] }).data
      }
      return res as Organization[]
    })
  }

  async create(body: CreateOrganizationInput): Promise<Organization> {
    return this.http.getFetch()(`${this.v1}/organizations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
