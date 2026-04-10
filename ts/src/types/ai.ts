export interface CompletionInput {
  model: string
  messages: { role: string; content: string }[]
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
    message: { role: string; content: string }
    finish_reason: string
  }[]
  usage?: { prompt_tokens: number; completion_tokens: number; total_tokens: number }
}

export interface StreamChunk {
  id: string
  object: string
  model: string
  choices: {
    index: number
    delta: { role?: string; content?: string }
    finish_reason: string | null
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
