import { HttpTransport } from "../http.js"
import type { BoardsResource, CreateBoardFieldInput } from "./boards.js"
import type { TemplatesResource, UseCase } from "./templates.js"

// ── Types ─────────────────────────────────────────────────────────────────────

export interface DocumentAIAgent {
  _id?: string
  id?: string
  name: string
  agent_type?: string
  model_id?: string
  provider_id?: string
  instructions?: string
  data_schema?: Record<string, unknown>
  workflow_name?: string
  description?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export interface CreateDocumentAIAgentInput {
  /** Display name shown in UI (e.g. "Receipt Extractor"). */
  name: string
  /** System prompt governing extraction logic. */
  instructions: string
  /** LLM model id (e.g. "gpt-4o" for system provider, or model id of a custom provider). */
  model_id: string
  /** Provider id. Use "system" for org default, or a custom provider UUID. */
  provider_id?: string
  /** Internal workflow name (defaults to "document_extraction"). */
  workflow_name?: string
  /**
   * JSON schema for fields to extract. Stored as `data_schema` on backend.
   * @example { invoice_number: { type: "string" }, total: { type: "number" } }
   */
  schema?: Record<string, unknown>
  description?: string
  [key: string]: unknown
}

export interface UpdateDocumentAIAgentInput {
  name?: string
  instructions?: string
  model_id?: string
  provider_id?: string
  workflow_name?: string
  schema?: Record<string, unknown>
  description?: string
  [key: string]: unknown
}

export interface ProcessDocumentInput {
  /** URL of the PDF/image to extract. */
  url: string
  /** Organization id (sent in body and header). */
  organizationId: string
  /**
   * If provided, agent's `model_id` and `instructions` are looked up and used
   * unless `modelName`/`instructions` are also provided (which override).
   */
  agentId?: string
  /** Override or replace agent's model. Required if `agentId` not provided. */
  modelName?: string
  /** Override or replace agent's instructions. */
  instructions?: string
  boardId?: string
  language?: string
  additionalDocumentInstructions?: string
  utc?: number
  chunkSize?: number
  maxConcurrent?: number
  maxRetries?: number
  useEnhancedProcessing?: boolean
  [key: string]: unknown
}

export interface ProcessDocumentResponse {
  success: boolean
  data: Record<string, unknown> & { filledPdfUrl?: string }
  [key: string]: unknown
}

// ── Resource ──────────────────────────────────────────────────────────────────

/**
 * Document AI — high-level wrapper for the iMBRACE Document AI Agent feature.
 *
 * **What is a Document AI Agent?** A specialized AI Assistant configured to
 * extract structured JSON from unstructured documents (PDFs, images, scanned
 * forms). Each agent has:
 * - a **schema** defining the fields to extract
 * - **instructions** guiding the LLM (business rules, formats)
 * - a **model** + **provider** for the underlying VLM/LLM
 * - optional **workflow** integration for automation
 *
 * Under the hood this resource wraps the AI Assistant CRUD endpoints with
 * `agent_type: "document_ai"` filtering, plus the document processing endpoint
 * `/v3/ai/document/`.
 *
 * @example Create + use an agent
 * ```ts
 * // Setup once
 * const agent = await client.documentAi.createAgent({
 *   name: "Invoice Extractor",
 *   instructions: "Extract invoice fields. Dates as YYYY-MM-DD.",
 *   model_id: "gpt-4o",
 *   schema: {
 *     invoice_number: { type: "string", description: "Invoice ID" },
 *     total:          { type: "number" },
 *     date:           { type: "string", format: "date" },
 *   },
 * })
 *
 * // Use many times
 * const result = await client.documentAi.process({
 *   agentId: agent._id!,
 *   url: "https://example.com/invoice.pdf",
 *   organizationId: "org_xxx",
 * })
 * ```
 */
export interface CreateFullDocumentAIInput {
  /** Display name shown in UI + used as UseCase title and Assistant name. */
  name: string
  /** System prompt governing extraction logic (mapped to assistant `core_task`). */
  instructions: string
  /** Schema fields to extract — embedded in the auto-created board. */
  schemaFields: CreateBoardFieldInput[]
  /** LLM model id (e.g. "qwen3.5:27b", "gpt-4o"). */
  modelId: string
  /** Provider id (UUID of the AI provider). */
  providerId: string
  /** Optional description (used for UseCase short_description + Assistant description). */
  description?: string
  /** Vision model. Defaults to `modelId`. */
  vlmModel?: string
  /** Vision provider id. Defaults to `providerId`. */
  vlmProviderId?: string
  /** Document languages to recognize. Defaults to `["English"]`. */
  sourceLanguages?: string[]
  handwritingSupport?: boolean
  timeOffset?: string
  continueOnFailure?: boolean
  retryTime?: number
  temperature?: number
  demoUrl?: string
  teamIds?: string[]
  /** Override / extend assistant fields (e.g. `workflow_function_call`, `metadata`). */
  extraAssistant?: Record<string, unknown>
}

export interface CreateFullDocumentAIResult {
  board_id: string
  assistant_id?: string
  channel_id?: string
  usecase_id?: string
  usecase: UseCase | Record<string, unknown>
  board: Record<string, unknown>
}

export class DocumentAIResource {
  /**
   * @param http  shared HTTP transport
   * @param aiBase  AI service base ending with `/v3/ai` (same as ChatAI / AI resources)
   * @param deps  Optional cross-resource refs used by `createFull`. Auto-wired by ImbraceClient.
   */
  constructor(
    private readonly http: HttpTransport,
    private readonly aiBase: string,
    private readonly deps?: {
      boards?: BoardsResource
      templates?: TemplatesResource
    },
  ) {}

  private get base() {
    return this.aiBase.replace(/\/$/, "")
  }

  // ── Agent CRUD ─────────────────────────────────────────────────────────────

  /**
   * List AI Assistants. Optional `nameContains` filter (case-insensitive).
   *
   * @param opts.nameContains   case-insensitive name substring filter.
   * @param opts.documentAiOnly  if `true`, return ONLY assistants that have
   *                             the `document_ai` config field populated
   *                             (i.e. created via {@link createFull} or via
   *                             the iMBRACE webapp Document AI flow).
   *
   * Note: in orgs without the Document AI module enabled, backend stores
   * `agent_type: "agent"` for all assistants. With the module enabled,
   * Document AI agents have `agent_type: "document_ai"`. The most reliable
   * marker across orgs is `assistant.document_ai != null`.
   */
  async listAgents(opts?: {
    nameContains?: string
    documentAiOnly?: boolean
  }): Promise<DocumentAIAgent[]> {
    const res: any = await this.http.getFetch()(`${this.base}/accounts/assistants`, { method: "GET" })
      .then(r => r.json())
    let all: DocumentAIAgent[] = Array.isArray(res) ? res : (res?.data ?? [])
    if (opts?.documentAiOnly) {
      all = all.filter(a => (a as any).document_ai != null)
    }
    if (opts?.nameContains) {
      const kw = opts.nameContains.toLowerCase()
      all = all.filter(a => (a.name ?? "").toLowerCase().includes(kw))
    }
    return all
  }

  /** Get a single Document AI Agent by id. */
  async getAgent(agentId: string): Promise<DocumentAIAgent> {
    return this.http.getFetch()(`${this.base}/assistants/${agentId}`, { method: "GET" })
      .then(r => r.json())
  }

  /**
   * Create a Document AI Agent. Wraps `POST /v3/ai/assistant_apps` with
   * `agent_type: "document_ai"`. Pass `schema` to define the extraction fields.
   */
  async createAgent(input: CreateDocumentAIAgentInput): Promise<DocumentAIAgent> {
    const { schema, ...rest } = input
    const body: Record<string, unknown> = {
      ...rest,
      provider_id: input.provider_id ?? "system",
      workflow_name: input.workflow_name ?? "document_extraction",
    }
    if (schema !== undefined) body.data_schema = schema
    return this.http.getFetch()(`${this.base}/assistant_apps`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /** Partial update — wraps `PUT /v3/ai/assistant_apps/{id}`. */
  async updateAgent(agentId: string, input: UpdateDocumentAIAgentInput): Promise<DocumentAIAgent> {
    const { schema, ...rest } = input
    const body: Record<string, unknown> = { ...rest }
    if (schema !== undefined) body.data_schema = schema
    return this.http.getFetch()(`${this.base}/assistant_apps/${agentId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /** Delete an agent. */
  async deleteAgent(agentId: string): Promise<void> {
    await this.http.getFetch()(`${this.base}/assistant_apps/${agentId}`, { method: "DELETE" })
  }

  // ── Process ────────────────────────────────────────────────────────────────

  /**
   * Process a document through a configured agent (or with explicit model/instructions).
   *
   * If `agentId` is given, the agent's `model_id` and `instructions` are loaded
   * unless `modelName`/`instructions` are also passed (which take precedence).
   *
   * Routes to `POST /v3/ai/document/`.
   */
  async process(input: ProcessDocumentInput): Promise<ProcessDocumentResponse> {
    let modelName = input.modelName
    let instructions = input.instructions

    if (input.agentId && (!modelName || !instructions)) {
      const agent = await this.getAgent(input.agentId)
      modelName    = modelName    ?? (agent.model_id as string | undefined)
      instructions = instructions ?? (agent.instructions as string | undefined)
    }

    if (!modelName) {
      throw new Error(
        "documentAi.process: must provide either `agentId` or `modelName`. " +
        "If you passed `agentId` but it has no `model_id` set, pass `modelName` explicitly."
      )
    }

    const reservedKeys = new Set(["url", "organizationId", "agentId", "modelName", "instructions"])
    const body: Record<string, unknown> = {
      modelName,
      url: input.url,
      organizationId: input.organizationId,
    }
    if (instructions) body.additionalInstructions = instructions
    for (const [k, v] of Object.entries(input)) {
      if (!reservedKeys.has(k) && v !== undefined) body[k] = v
    }

    return this.http.getFetch()(`${this.base}/document`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ── Schema auto-learn (provisional) ────────────────────────────────────────

  /**
   * Suggest a JSON schema by analyzing a sample document.
   *
   * **Provisional**: this currently uses `process()` with a meta-prompt asking
   * the vision model to propose a schema. If/when the backend exposes a
   * dedicated endpoint (e.g. `/v3/ai/document/auto-schema`), this method will
   * be updated to call it directly. The signature is stable.
   */
  async suggestSchema(input: {
    url: string
    organizationId: string
    modelName?: string
  }): Promise<ProcessDocumentResponse> {
    const metaPrompt =
      "Analyze this document and propose a JSON schema describing the fields. " +
      "Return ONLY a JSON object where each key is a field name and the value " +
      "is { type: <string|number|boolean|date>, description: <short description> }. " +
      "Example: { \"invoice_number\": { \"type\": \"string\", \"description\": \"Invoice ID\" } }"
    return this.process({
      url: input.url,
      organizationId: input.organizationId,
      modelName: input.modelName ?? "gpt-4o",
      instructions: metaPrompt,
    })
  }

  // ── Orchestrator ───────────────────────────────────────────────────────────

  /**
   * End-to-end Document AI agent creation.
   *
   * Wraps the 2-step flow the iMBRACE webapp performs:
   * 1. Create a board with `type: "DocumentAI"` and `schemaFields` embedded
   *    (the extraction schema container).
   * 2. Create a UseCase + Assistant via {@link TemplatesResource.createCustom},
   *    linking the new board through `assistant.document_ai.board_id`.
   *
   * Returns aggregated ids: `{ board_id, assistant_id, channel_id, usecase_id, usecase, board }`.
   *
   * Defaults: `vlmModel` falls back to `modelId`, `vlmProviderId` to `providerId`,
   * `sourceLanguages` to `["English"]`. Pass `extraAssistant` to override or
   * extend assistant fields (e.g. `workflow_function_call`, `metadata`).
   *
   * @throws {Error} if the resource was constructed without `boards` + `templates`
   *   (typical when constructed manually, not via `ImbraceClient`).
   */
  async createFull(input: CreateFullDocumentAIInput): Promise<CreateFullDocumentAIResult> {
    const boards = this.deps?.boards
    const templates = this.deps?.templates
    if (!boards || !templates) {
      throw new Error(
        "documentAi.createFull requires boards + templates resources. " +
        "These are auto-wired by ImbraceClient. If you constructed " +
        "DocumentAIResource directly, pass { boards, templates } as the third arg."
      )
    }

    const board = await boards.create({
      name: input.name,
      description: input.description,
      type: "DocumentAI",
      fields: input.schemaFields,
      team_ids: input.teamIds ?? [],
      show_id: false,
    })
    const boardId = (board as any)._id ?? (board as any).id
    if (!boardId) {
      throw new Error(`boards.create did not return an _id (got ${JSON.stringify(board)})`)
    }

    const usecase: Record<string, unknown> = {
      title: input.name,
      short_description: input.description ?? "",
      agent_type: "document_ai",
    }
    if (input.demoUrl) usecase.demo_url = input.demoUrl

    const assistant: Record<string, unknown> = {
      name: input.name,
      description: input.description ?? "",
      mode: "advanced",
      model_id: input.modelId,
      provider_id: input.providerId,
      core_task: input.instructions,
      agent_type: "document_ai",
      channel: "web",
      temperature: input.temperature ?? 0.1,
      version: 2,
      document_ai: {
        vlm_provider_id: input.vlmProviderId ?? input.providerId,
        vlm_model: input.vlmModel ?? input.modelId,
        source_languages: input.sourceLanguages ?? ["English"],
        handwriting_support: input.handwritingSupport ?? false,
        board_id: boardId,
        time_offset: input.timeOffset ?? "UTC+00:00",
        continue_on_failure: input.continueOnFailure ?? false,
        retry_time: input.retryTime ?? 2,
      },
      ...(input.extraAssistant ?? {}),
    }

    const res = await templates.createCustom({
      usecase: usecase as any,
      assistant: assistant as any,
    })
    const data = (res?.data ?? res) as any

    return {
      board_id:     boardId,
      assistant_id: data?.assistant_id,
      channel_id:   data?.channel_id,
      usecase_id:   data?._id,
      usecase:      data,
      board:        board as any,
    }
  }
}
