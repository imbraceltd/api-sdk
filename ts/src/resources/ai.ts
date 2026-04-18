import { HttpTransport } from "../http.js"
import type { Completion, Embedding, CompletionInput, EmbeddingInput, StreamChunk } from "../types/index.js"

export class AiResource {
  /**
   * @param base - Fully resolved AI base URL (gateway/ai)
   *   Version (v2/v3) được thêm trong từng method.
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v2() { return `${this.base}/v2` }
  private get v3() { return `${this.base}/v3` }

  // ─── Completions / Embeddings ────────────────────────────────────────────────

  async complete(input: CompletionInput): Promise<Completion> {
    return this.http.getFetch()(`${this.v3}/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...input, stream: false }),
    }).then(r => r.json())
  }

  async *stream(input: Omit<CompletionInput, "stream">): AsyncGenerator<StreamChunk> {
    const res = await this.http.getFetch()(`${this.v3}/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
      },
      body: JSON.stringify({ ...input, stream: true }),
    })

    if (!res.body) throw new Error("No response body for streaming")

    const reader  = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer    = ""

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

  async embed(input: EmbeddingInput): Promise<Embedding> {
    return this.http.getFetch()(`${this.v3}/embeddings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
    }).then(r => r.json())
  }

  // ─── Assistants ──────────────────────────────────────────────────────────────

  async listAssistants() {
    return this.http.getFetch()(`${this.v3}/accounts/assistants`, { method: "GET" }).then(r => r.json())
  }

  async getAssistant(assistantId: string) {
    return this.http.getFetch()(`${this.v3}/assistants/${assistantId}`, { method: "GET" }).then(r => r.json())
  }

  async checkAssistantName(name: string) {
    const url = new URL(`${this.v3}/assistants/check-name`)
    url.searchParams.set("name", name)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listAgents() {
    return this.http.getFetch()(`${this.v3}/assistants/agents`, { method: "GET" }).then(r => r.json())
  }

  async patchInstructions(assistantId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/assistants/${assistantId}/instructions`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Assistant Apps ──────────────────────────────────────────────────────────

  async createAssistantApp(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/assistant_apps`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateAssistantApp(assistantId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/assistant_apps/${assistantId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteAssistantApp(assistantId: string): Promise<void> {
    await this.http.getFetch()(`${this.v3}/assistant_apps/${assistantId}`, { method: "DELETE" })
  }

  async updateAssistantWorkflow(assistantId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/assistant_apps/${assistantId}/workflow`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── RAG Files ───────────────────────────────────────────────────────────────

  async listRagFiles() {
    return this.http.getFetch()(`${this.v3}/rag/files`, { method: "GET" }).then(r => r.json())
  }

  async getRagFile(fileId: string) {
    return this.http.getFetch()(`${this.v3}/rag/files/${fileId}`, { method: "GET" }).then(r => r.json())
  }

  async uploadRagFile(body: FormData) {
    return this.http.getFetch()(`${this.v3}/rag/files`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async deleteRagFile(fileId: string): Promise<void> {
    await this.http.getFetch()(`${this.v3}/rag/files/${fileId}`, { method: "DELETE" })
  }

  // ─── Guardrails ──────────────────────────────────────────────────────────────

  async listGuardrails() {
    return this.http.getFetch()(`${this.v3}/guardrail/all`, { method: "GET" }).then(r => r.json())
  }

  async getGuardrail(guardrailId: string) {
    return this.http.getFetch()(`${this.v3}/guardrail/${guardrailId}`, { method: "GET" }).then(r => r.json())
  }

  async createGuardrail(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/guardrail/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateGuardrail(guardrailId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/guardrail/update/${guardrailId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteGuardrail(guardrailId: string): Promise<void> {
    await this.http.getFetch()(`${this.v3}/guardrail/delete/${guardrailId}`, { method: "DELETE" })
  }

  // ─── Guardrail Providers ─────────────────────────────────────────────────────

  async listGuardrailProviders() {
    return this.http.getFetch()(`${this.v3}/guardrail-providers`, { method: "GET" }).then(r => r.json())
  }

  async getGuardrailProvider(providerId: string) {
    return this.http.getFetch()(`${this.v3}/guardrail-providers/${providerId}`, { method: "GET" }).then(r => r.json())
  }

  async createGuardrailProvider(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/guardrail-providers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateGuardrailProvider(providerId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/guardrail-providers/${providerId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteGuardrailProvider(providerId: string): Promise<void> {
    await this.http.getFetch()(`${this.v3}/guardrail-providers/${providerId}`, { method: "DELETE" })
  }

  async testGuardrailProvider(providerId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/guardrail-providers/${providerId}/test`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getGuardrailProviderModels(providerId: string) {
    return this.http.getFetch()(`${this.v3}/guardrail-providers/${providerId}/models`, { method: "GET" }).then(r => r.json())
  }

  // ─── Custom Providers ────────────────────────────────────────────────────────

  async listProviders() {
    return this.http.getFetch()(`${this.v3}/providers`, { method: "GET" }).then(r => r.json())
  }

  async createProvider(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/providers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateProvider(providerId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/providers/${providerId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteProvider(providerId: string): Promise<void> {
    await this.http.getFetch()(`${this.v3}/providers/${providerId}`, { method: "DELETE" })
  }

  async refreshProviderModels(providerId: string) {
    return this.http.getFetch()(`${this.v3}/providers/${providerId}/models/refresh`, {
      method: "POST",
    }).then(r => r.json())
  }

  async getLlmModels() {
    return this.http.getFetch()(`${this.v3}/workflow-agent/models`, { method: "GET" }).then(r => r.json())
  }

  async verifyToolServer(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v3}/configs/tool_servers/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Financial Documents (v2) ────────────────────────────────────────────────

  async getFinancialDoc(docId: string, params?: { page?: number; limit?: number }) {
    const url = new URL(`${this.v2}/financial_documents/${docId}`)
    if (params?.page)  url.searchParams.set("page",  String(params.page))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async updateFinancialDoc(docId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/financial_documents/${docId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteFinancialDoc(docId: string): Promise<void> {
    await this.http.getFetch()(`${this.v2}/financial_documents/${docId}`, { method: "DELETE" })
  }

  async suggestFinancialFix(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/financial_documents/suggest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async fixFinancialDoc(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/financial_documents/fix`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async resetFinancialDoc(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/financial_documents/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getFinancialDocErrorFiles(fileId: string) {
    return this.http.getFetch()(`${this.v2}/financial_documents/errors-files/${fileId}`, { method: "GET" }).then(r => r.json())
  }

  async getFinancialReport(reportId: string, params?: { page?: number; limit?: number }) {
    const url = new URL(`${this.v2}/financial_documents/reports/${reportId}`)
    if (params?.page)  url.searchParams.set("page",  String(params.page))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async updateFinancialReport(reportId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/financial_documents/reports/${reportId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteFinancialReport(reportId: string): Promise<void> {
    await this.http.getFetch()(`${this.v2}/financial_documents/reports/${reportId}`, { method: "DELETE" })
  }
}
