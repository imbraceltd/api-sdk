import { HttpTransport } from "../http.js"
import type { AgentTemplate } from "../types/index.js"

// ─── Agent / use-case interfaces  

export interface AgentAssistantInput {
  name?: string
  description?: string
  model?: string
  instructions?: string
  [key: string]: unknown
}

export interface AgentUseCaseInput {
  name?: string
  description?: string
  category?: string
  [key: string]: unknown
}

export interface CreateAgentInput {
  assistant: AgentAssistantInput
  usecase: AgentUseCaseInput
}

export interface UpdateAgentInput {
  assistant?: AgentAssistantInput
  usecase?: AgentUseCaseInput
}

export interface DeleteAgentResponse {
  success: boolean
  [key: string]: unknown
}

export interface UseCase {
  _id: string
  name?: string
  description?: string
  category?: string
  [key: string]: unknown
}

export interface CreateUseCaseInput {
  name: string
  description?: string
  category?: string
  assistant_id?: string
  [key: string]: unknown
}

export interface UpdateUseCaseInput {
  name?: string
  description?: string
  category?: string
  [key: string]: unknown
}

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
  ) {
    const backendV2 = base.replace(/\/marketplaces\/?$/, "").replace(/\/$/, "")
    this.templates = `${backendV2}/templates`
    this.useCases  = `${backendV2}/templates` // In new-frontend, use-cases are also under /templates
  }

  // ── Marketplace Templates   

  async list(): Promise<AgentTemplate[]> {
    return this.http.getFetch()(this.templates, { method: "GET" }).then(r => r.json())
  }

  async get(templateId: string): Promise<{ data: AgentTemplate }> {
    return this.http.getFetch()(`${this.templates}/${templateId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: CreateAgentInput): Promise<AgentTemplate> {
    return this.http.getFetch()(`${this.templates}/custom`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(templateId: string, body: UpdateAgentInput): Promise<AgentTemplate> {
    return this.http.getFetch()(`${this.templates}/${templateId}/custom`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(templateId: string): Promise<DeleteAgentResponse> {
    return this.http.getFetch()(`${this.templates}/${templateId}`, { method: "DELETE" }).then(r => r.json())
  }

  // ── Use-cases   

  async listUseCases(): Promise<UseCase[]> {
    return this.http.getFetch()(this.useCases, { method: "GET" }).then(r => r.json())
  }

  async getUseCase(useCaseId: string): Promise<UseCase> {
    return this.http.getFetch()(`${this.useCases}/${useCaseId}`, { method: "GET" }).then(r => r.json())
  }

  async createUseCase(body: CreateUseCaseInput): Promise<UseCase> {
    return this.http.getFetch()(`${this.useCases}/v2/custom`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateUseCase(useCaseId: string, body: UpdateUseCaseInput): Promise<UseCase> {
    return this.http.getFetch()(`${this.useCases}/${useCaseId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteUseCase(useCaseId: string): Promise<DeleteAgentResponse> {
    return this.http.getFetch()(`${this.useCases}/${useCaseId}`, { method: "DELETE" }).then(r => r.json())
  }
}
