import { HttpTransport } from "../http.js"

export class CategoriesResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/v1/categories` }

  async list(organizationId: string) {
    const url = new URL(this.url)
    url.searchParams.set("organization_id", organizationId)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(categoryId: string) {
    return this.http.getFetch()(`${this.url}/${categoryId}`, { method: "GET" }).then(r => r.json())
  }

  async create(organizationId: string, body: { name: string; apply_to?: string[]; description?: string }) {
    return this.http.getFetch()(this.url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "organization_id": organizationId },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(organizationId: string, categoryId: string, body: { name?: string; apply_to?: string[]; description?: string }) {
    return this.http.getFetch()(`${this.url}/${categoryId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", "organization_id": organizationId },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(categoryId: string) {
    return this.http.getFetch()(`${this.url}/${categoryId}`, { method: "DELETE" }).then(r => r.json())
  }
}
