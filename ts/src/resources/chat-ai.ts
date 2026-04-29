import { HttpTransport } from "../http.js"

export interface ChatAiModel {
  id: string
  name: string
  [key: string]: unknown
}

export interface ChatAiResponse {
  id: string
  choices: any[]
  [key: string]: unknown
}

export interface ChatAiChat {
  id: string
  title: string
  updated_at: number
  created_at: number
  [key: string]: unknown
}

export interface ChatAiFile {
  id: string
  filename: string
  meta: Record<string, unknown>
  [key: string]: unknown
}

export interface ChatAiKnowledge {
  id: string
  name: string
  description?: string
  data?: Record<string, any>
  [key: string]: unknown
}

export interface Assistant {
  id: string
  name: string
  description?: string
  model?: string
  instructions?: string
  [key: string]: unknown
}

export interface CreateAssistantInput {
  name: string
  workflow_name: string
  /**
   * The provider this assistant chats through. Use `"system"` to delegate to
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

export class ChatAiResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  /**
   * Get available models from chat-ai (aiv2)
   * Endpoint: /ai/v3/models
   */
  async listModels(): Promise<{ data: ChatAiModel[] }> {
    return this.http.getFetch()(`${this.base}/models`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Create chat completion (aiv2)
   * Endpoint: /ai/v3/openai/chat/completions
   */
  async chat(body: any): Promise<ChatAiResponse> {
    return this.http.getFetch()(`${this.base}/openai/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // --- Chats ---

  /**
   * List user chats
   * Endpoint: /ai/v3/chats/
   */
  async listChats(): Promise<ChatAiChat[]> {
    return this.http.getFetch()(`${this.base}/chats/`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Get chat by ID
   * Endpoint: /ai/v3/chats/:id
   */
  async getChat(id: string): Promise<ChatAiChat> {
    return this.http.getFetch()(`${this.base}/chats/${id}`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Create new chat
   * Endpoint: /ai/v3/chats/new
   */
  async createChat(body: any): Promise<ChatAiChat> {
    return this.http.getFetch()(`${this.base}/chats/new`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /**
   * Delete chat by ID
   * Endpoint: /ai/v3/chats/:id
   */
  async deleteChat(id: string): Promise<boolean> {
    return this.http.getFetch()(`${this.base}/chats/${id}`, { method: "DELETE" }).then(r => r.json())
  }

  // --- Files ---

  /**
   * List uploaded files
   * Endpoint: /ai/v3/files/
   */
  async listFiles(): Promise<ChatAiFile[]> {
    return this.http.getFetch()(`${this.base}/files/`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Upload file
   * Endpoint: /ai/v3/files/
   */
  async uploadFile(body: FormData): Promise<ChatAiFile> {
    return this.http.getFetch()(`${this.base}/files/`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  /**
   * Upload agent specific file
   * Endpoint: /ai/v3/files/agent
   */
  async uploadAgentFile(body: FormData): Promise<any> {
    return this.http.getFetch()(`${this.base}/files/agent`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  /**
   * Extract file content (PDF/etc)
   * Endpoint: /ai/v3/files/extract
   */
  async extractFile(body: FormData): Promise<any> {
    return this.http.getFetch()(`${this.base}/files/extract`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  /**
   * Get file data content
   * Endpoint: /ai/v3/files/:id/data/content
   */
  async getFileData(id: string): Promise<{ content: string }> {
    return this.http.getFetch()(`${this.base}/files/${id}/data/content`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Update file data content
   * Endpoint: /ai/v3/files/:id/data/content/update
   */
  async updateFileData(id: string, content: string): Promise<{ content: string }> {
    return this.http.getFetch()(`${this.base}/files/${id}/data/content/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    }).then(r => r.json())
  }

  /**
   * Delete file by ID
   * Endpoint: /ai/v3/files/:id
   */
  async deleteFile(id: string): Promise<boolean> {
    return this.http.getFetch()(`${this.base}/files/${id}`, { method: "DELETE" }).then(r => r.json())
  }

  // --- Audio ---

  /**
   * Transcribe audio to text
   * Endpoint: /ai/v3/audio/transcriptions
   */
  async transcribe(body: FormData): Promise<{ text: string }> {
    return this.http.getFetch()(`${this.base}/audio/transcriptions`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  /**
   * Generate speech from text
   * Endpoint: /ai/v3/audio/speech
   */
  async speech(body: any): Promise<Response> {
    return this.http.getFetch()(`${this.base}/audio/speech`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })
  }

  // --- Knowledge ---

  /**
   * List knowledge bases
   * Endpoint: /ai/v3/knowledge/
   */
  async listKnowledge(): Promise<ChatAiKnowledge[]> {
    return this.http.getFetch()(`${this.base}/knowledge/`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Get knowledge base by ID
   * Endpoint: /ai/v3/knowledge/:id
   */
  async getKnowledge(id: string): Promise<ChatAiKnowledge> {
    return this.http.getFetch()(`${this.base}/knowledge/${id}`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Create new knowledge base
   * Endpoint: /ai/v3/knowledge/create
   */
  async createKnowledge(body: any): Promise<ChatAiKnowledge> {
    return this.http.getFetch()(`${this.base}/knowledge/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /**
   * Delete knowledge base by ID
   * Endpoint: /ai/v3/knowledge/:id/delete
   */
  async deleteKnowledge(id: string): Promise<boolean> {
    return this.http.getFetch()(`${this.base}/knowledge/${id}/delete`, { method: "DELETE" }).then(r => r.json())
  }

  // --- Folders ---

  /**
   * List chat folders
   * Endpoint: /ai/v3/folders/
   */
  async listFolders(): Promise<any[]> {
    return this.http.getFetch()(`${this.base}/folders/`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Create chat folder
   * Endpoint: /ai/v3/folders/
   */
  async createFolder(name: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/folders/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }).then(r => r.json())
  }

  /**
   * Update folder name
   * Endpoint: /ai/v3/folders/:id/update
   */
  async updateFolder(id: string, name: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/folders/${id}/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }).then(r => r.json())
  }

  /**
   * Delete folder
   * Endpoint: /ai/v3/folders/:id
   */
  async deleteFolder(id: string): Promise<boolean> {
    return this.http.getFetch()(`${this.base}/folders/${id}`, { method: "DELETE" }).then(r => r.json())
  }

  // --- Prompts ---

  /**
   * List custom prompts
   * Endpoint: /ai/v3/prompts/
   */
  async listPrompts(): Promise<any[]> {
    return this.http.getFetch()(`${this.base}/prompts/`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Create custom prompt
   * Endpoint: /ai/v3/prompts/create
   */
  async createPrompt(body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/prompts/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /**
   * Get prompt by command
   * Endpoint: /ai/v3/prompts/command/:command
   */
  async getPrompt(command: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/prompts/command/${command}`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Update prompt by command
   * Endpoint: /ai/v3/prompts/command/:command/update
   */
  async updatePrompt(command: string, body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/prompts/command/${command}/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /**
   * Delete prompt by command
   * Endpoint: /ai/v3/prompts/command/:command/delete
   */
  async deletePrompt(command: string): Promise<boolean> {
    return this.http.getFetch()(`${this.base}/prompts/command/${command}/delete`, { method: "DELETE" }).then(r => r.json())
  }

  // --- Tools ---

  /**
   * List custom tools
   * Endpoint: /ai/v3/tools/
   */
  async listTools(): Promise<any[]> {
    return this.http.getFetch()(`${this.base}/tools/`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Create custom tool
   * Endpoint: /ai/v3/tools/create
   */
  async createTool(body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/tools/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /**
   * Get tool by ID
   * Endpoint: /ai/v3/tools/id/:id
   */
  async getTool(id: string): Promise<any> {
    return this.http.getFetch()(`${this.base}/tools/id/${id}`, { method: "GET" }).then(r => r.json())
  }

  /**
   * Update tool by ID
   * Endpoint: /ai/v3/tools/id/:id/update
   */
  async updateTool(id: string, body: any): Promise<any> {
    return this.http.getFetch()(`${this.base}/tools/id/${id}/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /**
   * Delete tool by ID
   * Endpoint: /ai/v3/tools/id/:id/delete
   */
  async deleteTool(id: string): Promise<boolean> {
    return this.http.getFetch()(`${this.base}/tools/id/${id}/delete`, { method: "DELETE" }).then(r => r.json())
  }

  // --- Document AI ---

  /**
   * Process a document with a vision model and extract structured data.
   * Endpoint: /ai/v3/document/
   */
  async processDocument(body: DocumentAIInput): Promise<DocumentAIResponse> {
    return this.http.getFetch()(`${this.base}/document/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /**
   * List LLM providers configured by the user — these are the models available for document AI.
   * Endpoint: /ai/v3/providers
   */
  async listDocumentModels(): Promise<any[]> {
    return this.http.getFetch()(`${this.base}/providers`, { method: "GET" }).then(r => r.json())
  }

  // ─── Assistants ───────────────────────────────────────────────────────────

  async listAssistants(): Promise<Assistant[]> {
    return this.http.getFetch()(`${this.base}/accounts/assistants`, { method: "GET" }).then(r => r.json())
  }

  async getAssistant(id: string): Promise<Assistant> {
    return this.http.getFetch()(`${this.base}/assistants/${id}`, { method: "GET" }).then(r => r.json())
  }

  async createAssistant(body: CreateAssistantInput): Promise<Assistant> {
    if (!body?.provider_id || !body?.model_id) {
      throw new Error(
        "createAssistant: provider_id and model_id are required. " +
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

  async updateAssistant(id: string, body: Partial<CreateAssistantInput>): Promise<Assistant> {
    return this.http.getFetch()(`${this.base}/assistant_apps/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteAssistant(id: string): Promise<boolean> {
    const r = await this.http.getFetch()(`${this.base}/assistant_apps/${id}`, { method: "DELETE" })
    return r.ok
  }

  async updateAssistantInstructions(id: string, instructions: string): Promise<Assistant> {
    return this.http.getFetch()(`${this.base}/assistants/${id}/instructions`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ instructions }),
    }).then(r => r.json())
  }

  async listAssistantAgents(): Promise<any[]> {
    return this.http.getFetch()(`${this.base}/assistants/agents`, { method: "GET" }).then(r => r.json())
  }
}
