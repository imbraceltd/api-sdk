import { HttpTransport } from "../../core/http.js"

export class ConversationServerResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async listMessages(conversationId: string, opts: { limit?: number; skip?: number } = {}) {
    const url = new URL(`${this.base}/3rd/conversations/${conversationId}/messages`)
    if (opts.limit !== undefined) url.searchParams.set("limit", String(opts.limit))
    if (opts.skip !== undefined) url.searchParams.set("skip", String(opts.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }
}
