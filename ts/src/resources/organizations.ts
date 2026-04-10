import { HttpTransport } from "../http.js"

export class OrganizationsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async list(params?: { limit?: number; skip?: number }) {
    const url = new URL(`${this.base}/v2/backend/organizations`)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }
}
