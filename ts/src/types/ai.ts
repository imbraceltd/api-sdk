/**
 * Base entity with standard ID and timestamps.
 */
export interface BaseEntity {
  _id: string
  created_at?: string
  updated_at?: string
}

/**
 * Generic list response for AI resources.
 */
export interface AiListResponse<T> {
  data: T[]
  total?: number
}

/**
 * Base interface for AI resources to ensure consistency and re-usability.
 */
export interface AiBaseResource extends BaseEntity {
  name: string
  [key: string]: unknown
}

/**
 * AI Roles for completions and streaming.
 */
export enum AiRole {
  System = "system",
  User = "user",
  Assistant = "assistant",
  Tool = "tool",
}

/**
 * AI Operational Modes.
 */
export enum AiMode {
  Standard = "standard",
  Advanced = "advanced",
}

/**
 * AI Resource Status.
 */
export enum AiStatus {
  Active = "active",
  Inactive = "inactive",
  Pending = "pending",
  Processing = "processing",
  Completed = "completed",
  Error = "error",
}

/**
 * AI Completion Finish Reasons.
 */
export enum AiFinishReason {
  Stop = "stop",
  Length = "length",
  ContentFilter = "content_filter",
  ToolCalls = "tool_calls",
  FunctionCall = "function_call",
}

/**
 * AI Agent Types.
 */
export enum AiAgentType {
  Conversational = "conversational",
  Workflow = "workflow",
  Assistant = "assistant",
  Agent = "agent",
}

// ─── Completions / Embeddings ────────────────────────────────────────────────

export interface CompletionInput {
  model: string
  messages: { role: AiRole | string; content: string }[]
  temperature?: number
  maxTokens?: number
  metadata?: Record<string, unknown>
  stream?: boolean
}

export interface Completion {
  id: string
  object: string
  model: string
  choices: {
    index: number
    message: { role: AiRole | string; content: string }
    finish_reason: AiFinishReason | string
  }[]
  usage?: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }
}

export interface StreamChunk {
  id: string
  object: string
  model: string
  choices: {
    index: number
    delta: { role?: AiRole | string; content?: string }
    finish_reason: AiFinishReason | string | null
  }[]
}

export interface EmbeddingInput {
  model: string
  input: string[]
}

export interface Embedding {
  object: string
  model: string
  data: { object: string; embedding: number[]; index: number }[]
  usage: { prompt_tokens: number; total_tokens: number }
}

// ─── AI Assistants ─────────────────────────────────────────────────────────

export interface Assistant extends AiBaseResource {
  description?: string
  instructions?: string
  model?: string
  mode?: AiMode | string
  model_id?: string
  provider_id?: string
  show_thinking_process?: boolean
  streaming?: boolean
  channel?: string
  channel_id?: string
  teams?: string | string[]
  categories?: number[]
  guardrail_id?: string
  personality_and_role?: string
  core_task?: string
  agent_type?: AiAgentType | string
  sub_agents?: Record<string, unknown>[]
  team_leads?: Record<string, unknown>[]
  is_orchestrator?: boolean
  preload_information?: string
  tone_and_style?: string
  response_length?: string
  list_of_banned_words?: string
  files?: Record<string, unknown> | string[]
  selected_board_id?: string
  folder_ids?: string[]
  default_folder_id?: string
  board_ids?: string[]
  knowledge_hubs?: string[]
  workflow_functions?: Record<string, unknown>[]
  temperature?: number
  use_memory?: boolean
  tool_server?: Record<string, unknown>
  enable_echart?: boolean
  top_k_relevant_results?: number
  top_k?: number
}

export interface AssistantListResponse extends AiListResponse<Assistant> {}

export interface AssistantNameCheckResponse {
  available: boolean
  name: string
}

export interface PatchInstructionsInput {
  instructions: string
  [key: string]: unknown
}

// ─── Assistant Apps ────────────────────────────────────────────────────────

export interface AssistantApp extends AiBaseResource {
  assistant_id?: string
  mode?: AiMode | string
  model_id?: string
  provider_id?: string
  instructions?: string
  agent_type?: AiAgentType | string
  workflow?: Record<string, unknown>
}

export interface AssistantAppListResponse extends AiListResponse<AssistantApp> {}

export interface CreateAssistantAppInput {
  name: string
  assistant_id?: string
  mode?: AiMode | string
  model_id?: string
  provider_id?: string
  instructions?: string
  agent_type?: AiAgentType | string
  [key: string]: unknown
}

export interface UpdateAssistantAppInput {
  name?: string
  mode?: AiMode | string
  model_id?: string
  provider_id?: string
  instructions?: string
  agent_type?: AiAgentType | string
  [key: string]: unknown
}

export interface UpdateAssistantWorkflowInput {
  workflow: Record<string, unknown>
  [key: string]: unknown
}

// ─── RAG Files ─────────────────────────────────────────────────────────────

export interface RagFile extends BaseEntity {
  name: string
  size?: number
  status?: AiStatus | string
}

export interface RagFileListResponse extends AiListResponse<RagFile> {}

// ─── Guardrails ────────────────────────────────────────────────────────────

export interface Guardrail extends AiBaseResource {
  type?: string
  config?: Record<string, unknown>
}

export interface GuardrailListResponse extends AiListResponse<Guardrail> {}

export interface CreateGuardrailInput {
  name: string
  type?: string
  config?: Record<string, unknown>
  [key: string]: unknown
}

export interface UpdateGuardrailInput {
  name?: string
  config?: Record<string, unknown>
  [key: string]: unknown
}

// ─── Guardrail Providers ───────────────────────────────────────────────────

export interface GuardrailProvider extends AiBaseResource {
  type?: string
  config?: Record<string, unknown>
}

export interface GuardrailProviderListResponse extends AiListResponse<GuardrailProvider> {}

export interface CreateGuardrailProviderInput {
  name: string
  type?: string
  config?: Record<string, unknown>
  [key: string]: unknown
}

export interface UpdateGuardrailProviderInput {
  name?: string
  config?: Record<string, unknown>
  [key: string]: unknown
}

export interface TestGuardrailProviderInput {
  prompt?: string
  [key: string]: unknown
}

export interface GuardrailProviderModelsResponse {
  models: Array<{ id: string; name: string; [key: string]: unknown }>
}

// ─── AI Providers ──────────────────────────────────────────────────────────

export interface AiProvider extends AiBaseResource {
  type?: string
  api_key?: string
  base_url?: string
}

export interface AiProviderListResponse extends AiListResponse<AiProvider> {}

export interface CreateAiProviderInput {
  name: string
  type?: string
  api_key?: string
  base_url?: string
  [key: string]: unknown
}

export interface UpdateAiProviderInput {
  name?: string
  api_key?: string
  base_url?: string
  [key: string]: unknown
}

export interface LlmModelsResponse {
  models: Array<{
    id: string
    name: string
    provider?: string
    [key: string]: unknown
  }>
}

export interface VerifyToolServerInput {
  url: string
  [key: string]: unknown
}

export interface VerifyToolServerResponse {
  success: boolean
  tools?: Array<{ name: string; description?: string; [key: string]: unknown }>
  [key: string]: unknown
}

// ─── Financial Documents ──────────────────────────────────────────────────

export interface FinancialDoc extends BaseEntity {
  name?: string
  status?: AiStatus | string
  pages?: Record<string, unknown>[]
}

export interface UpdateFinancialDocInput {
  [key: string]: unknown
}

export interface FinancialFixInput {
  doc_id?: string
  [key: string]: unknown
}

export interface FinancialErrorFilesResponse {
  files?: Record<string, unknown>[]
  [key: string]: unknown
}

export interface FinancialReport extends BaseEntity {
  name?: string
  status?: AiStatus | string
}

export interface UpdateFinancialReportInput {
  [key: string]: unknown
}
