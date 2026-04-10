import { HttpTransport } from "../http.js"

export class MessagesResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/v1/backend/conversation_messages` }

  async list(params?: { limit?: number; skip?: number }) {
    const url = new URL(this.url)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
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
    return this.http.getFetch()(this.url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
