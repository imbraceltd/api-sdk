import { HttpTransport } from "../http.js"

// ─── AI Agents ────────────────────────────────────────────────────────────────

export interface AiAgent {
  id: string
  name: string
  description?: string
  model?: string
  instructions?: string
  [key: string]: unknown
}

export interface CreateAiAgentInput {
  name: string
  workflow_name: string
  /**
   * The provider this AI agent chats through. Use `"system"` to delegate to
   * the org's default LLM provider; pass a specific provider UUID to pin one.
   */
  provider_id: string
  /**
   * The model name. With `provider_id: "system"` use a model name (e.g.
   * `"gpt-4o"`) or the literal `"Default"` to fall back to the system default.
   * For a custom provider, pass that provider's model id.
   */
  model_id: string
  description?: string
  /** @deprecated legacy field — chat orchestrator type, leave unset. */
  model?: string
  instructions?: string
  [key: string]: unknown
}

// ─── Document AI ──────────────────────────────────────────────────────────────

export interface DocumentAIInput {
  modelName: string
  url: string
  organizationId: string
  boardId?: string
  language?: string
  additionalInstructions?: string
  additionalDocumentInstructions?: string
  processModelName?: string
  fileUrlToFill?: string
  tools?: Record<string, unknown>[]
  utc?: number
  chunkSize?: number
  maxConcurrent?: number
  maxRetries?: number
  useEnhancedProcessing?: boolean
}

export interface DocumentAIResponse {
  success: boolean
  data: Record<string, unknown> & { filledPdfUrl?: string }
}

/**
 * Imbrace-specific endpoints exposed by the chat-ai service. The
 * upstream OpenWebUI surface (chats, files list/upload, audio, knowledge,
 * folders, prompts, tools, models) is intentionally not wrapped here:
 * those endpoints require an OpenWebUI session JWT (issued only by the
 * OpenWebUI login flow) and reject `x-api-key` / `x-access-token` auth.
 *
 * What this resource covers:
 *   • Agent file upload and content extraction
 *   • Document AI (vision-model document processing) and provider listing
 *   • Imbrace AI agents (`/accounts/assistants`, `/assistant_apps`, …)
 */
export class ChatAiResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  // ─── Files (Imbrace additions on top of OpenWebUI) ──────────────────────────

  /** Upload an agent-specific file. Endpoint: /ai/v3/files/agent */
  async uploadAgentFile(body: FormData): Promise<unknown> {
    return this.http.getFetch()(`${this.base}/files/agent`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  /** Extract content from an uploaded file (PDF/etc). Endpoint: /ai/v3/files/extract */
  async extractFile(body: FormData): Promise<unknown> {
    return this.http.getFetch()(`${this.base}/files/extract`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  // ─── Document AI ──────────────────────────────────────────────────────────

  /** Process a document with a vision model and extract structured data. Endpoint: /ai/v3/document/ */
  async processDocument(body: DocumentAIInput): Promise<DocumentAIResponse> {
    return this.http.getFetch()(`${this.base}/document/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /** List LLM providers configured for the org — these are the models available for document AI. Endpoint: /ai/v3/providers */
  async listDocumentModels(): Promise<unknown[]> {
    return this.http.getFetch()(`${this.base}/providers`, { method: "GET" }).then(r => r.json())
  }

  // ─── AI Agents ─────────────────────────────────────────────────────────────

  async listAiAgents(): Promise<AiAgent[]> {
    return this.http.getFetch()(`${this.base}/accounts/assistants`, { method: "GET" }).then(r => r.json())
  }

  async getAiAgent(id: string): Promise<AiAgent> {
    return this.http.getFetch()(`${this.base}/assistants/${id}`, { method: "GET" }).then(r => r.json())
  }

  async createAiAgent(body: CreateAiAgentInput): Promise<AiAgent> {
    if (!body?.provider_id || !body?.model_id) {
      throw new Error(
        "createAiAgent: provider_id and model_id are required. " +
        "Use { provider_id: \"system\", model_id: \"gpt-4o\" } for the system default, " +
        "or pass a custom provider's UUID and model name.",
      )
    }
    return this.http.getFetch()(`${this.base}/assistant_apps`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateAiAgent(id: string, body: Partial<CreateAiAgentInput>): Promise<AiAgent> {
    return this.http.getFetch()(`${this.base}/assistant_apps/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteAiAgent(id: string): Promise<boolean> {
    const r = await this.http.getFetch()(`${this.base}/assistant_apps/${id}`, { method: "DELETE" })
    return r.ok
  }

  async updateAiAgentInstructions(id: string, instructions: string): Promise<AiAgent> {
    return this.http.getFetch()(`${this.base}/assistants/${id}/instructions`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ instructions }),
    }).then(r => r.json())
  }

  async listAiAgentSubAgents(): Promise<unknown[]> {
    return this.http.getFetch()(`${this.base}/assistants/agents`, { method: "GET" }).then(r => r.json())
  }
}
