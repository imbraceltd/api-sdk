import { HttpTransport } from "../http.js"

export class AgentResource {
  private readonly templates: string
  private readonly useCases: string

  /**
   * @param http     - HTTP transport
   * @param base     - marketplaces service base URL (gateway/marketplaces)
   * @param gateway  - App Gateway root URL
   */
  constructor(
    private readonly http: HttpTransport,
    base: string,
    gateway: string,
  ) {
    this.templates = `${base.replace(/\/$/, "")}/v1/market-places/templates`
    this.useCases  = `${gateway.replace(/\/$/, "")}/v3/marketplaces/use-cases`
  }

  // ── Marketplace Templates ────────────────────────────────────────────────

  async list() {
    return this.http.getFetch()(this.templates, { method: "GET" }).then(r => r.json())
  }

  async get(templateId: string) {
    return this.http.getFetch()(`${this.templates}/${templateId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: {
    assistant: Record<string, unknown>
    usecase: Record<string, unknown>
  }) {
    return this.http.getFetch()(`${this.templates}/custom`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(templateId: string, body: {
    assistant?: Record<string, unknown>
    usecase?: Record<string, unknown>
  }) {
    return this.http.getFetch()(`${this.templates}/${templateId}/custom`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(templateId: string) {
    return this.http.getFetch()(`${this.templates}/${templateId}`, { method: "DELETE" }).then(r => r.json())
  }

  // ── Use-cases ────────────────────────────────────────────────────────────

  async listUseCases() {
    return this.http.getFetch()(this.useCases, { method: "GET" }).then(r => r.json())
  }

  async getUseCase(useCaseId: string) {
    return this.http.getFetch()(`${this.useCases}/${useCaseId}`, { method: "GET" }).then(r => r.json())
  }

  async createUseCase(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.useCases}/v2/custom`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateUseCase(useCaseId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.useCases}/${useCaseId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteUseCase(useCaseId: string) {
    return this.http.getFetch()(`${this.useCases}/${useCaseId}`, { method: "DELETE" }).then(r => r.json())
  }
}
