import { HttpTransport } from "../../core/http.js"
import type { Completion, Embedding, CompletionInput, EmbeddingInput, StreamChunk } from "../../types/index.js"

export class AiResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/ai` }

  /**
   * Full (non-streaming) completion — waits for entire response.
   */
  async complete(input: CompletionInput): Promise<Completion> {
    return this.http.getFetch()(`${this.url}/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...input, stream: false }),
    }).then(r => r.json())
  }

  /**
   * Streaming completion via SSE — returns an AsyncGenerator of StreamChunk.
   *
   * @example
   * for await (const chunk of client.ai.stream({ model: "gpt-4o", messages: [...] })) {
   *   process.stdout.write(chunk.choices[0]?.delta?.content ?? "")
   * }
   */
  async *stream(input: Omit<CompletionInput, "stream">): AsyncGenerator<StreamChunk> {
    const res = await this.http.getFetch()(`${this.url}/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
      },
      body: JSON.stringify({ ...input, stream: true }),
    })

    if (!res.body) throw new Error("No response body for streaming")

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ""

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split("\n")
        buffer = lines.pop() ?? ""

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue
          const data = line.slice(6).trim()
          if (data === "[DONE]") return
          try {
            yield JSON.parse(data) as StreamChunk
          } catch {
            // skip malformed JSON lines
          }
        }
      }
    } finally {
      reader.releaseLock()
    }
  }

  /**
   * Generate embeddings for a list of strings.
   */
  async embed(input: EmbeddingInput): Promise<Embedding> {
    return this.http.getFetch()(`${this.url}/embeddings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
    }).then(r => r.json())
  }
}
