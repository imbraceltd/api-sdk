import { HttpTransport } from "../http.js"

export class OrganizationsResource {
  /**
   * @param base - platform base URL (gateway/platform)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }
  private get v2() { return `${this.base}/v2` }

  async list(params?: { limit?: number; skip?: number; is_active?: boolean }) {
    const url = new URL(`${this.v2}/organizations`)
    if (params?.limit)  url.searchParams.set("limit",     String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.is_active !== undefined) url.searchParams.set("is_active", String(params.is_active))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listAll(params?: { is_active?: boolean }) {
    const url = new URL(`${this.v2}/organizations/_all`)
    if (params?.is_active !== undefined) url.searchParams.set("is_active", String(params.is_active))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async create(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/organizations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
