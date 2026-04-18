import { HttpTransport } from "../http.js"

export class MessagesResource {
  /**
   * @param base - channel-service base URL (gateway/channel-service)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }

  async list(params?: {
    type?: string
    q?: string
    limit?: number
    skip?: number
  }) {
    const url = new URL(`${this.v1}/conversation_messages`)
    if (params?.type)   url.searchParams.set("type",  params.type)
    if (params?.q)      url.searchParams.set("q",     params.q)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async send(body: {
    type: "text" | "image" | "quick_reply" | "file" | "pdf"
    text?: string
    url?: string
    caption?: string
    title?: string
    payload?: string
  }) {
    return this.http.getFetch()(`${this.v1}/conversation_messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async uploadFile(body: FormData) {
    return this.http.getFetch()(`${this.v1}/conversation_messages/_fileupload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async addComment(convId: string, messageId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/conversations/${convId}/conversation_messages/${messageId}/comments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateComment(convId: string, commentId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/conversations/${convId}/comments/${commentId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteComment(convId: string, commentId: string): Promise<void> {
    await this.http.getFetch()(`${this.v1}/conversations/${convId}/comments/${commentId}`, { method: "DELETE" })
  }

  async pin(convId: string, messageId: string) {
    const url = new URL(`${this.v1}/conversations/${convId}/conversation_messages/${messageId}`)
    url.searchParams.set("action", "pin")
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async unpin(convId: string, messageId: string) {
    const url = new URL(`${this.v1}/conversations/${convId}/conversation_messages/${messageId}`)
    url.searchParams.set("action", "unpin")
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getIndex(conversationId: string, messageId: string) {
    return this.http.getFetch()(
      `${this.v1}/conversations/${conversationId}/conversation_messages/${messageId}/_index`,
      { method: "GET" }
    ).then(r => r.json())
  }
}
