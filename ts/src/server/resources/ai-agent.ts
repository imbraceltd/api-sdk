import { HttpTransport } from "../../core/http.js"

export class AiAgentResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/3rd/ai-service` }

  async answerQuestion(body: {
    text: string
    assistant_id: string
    thread_id?: string
    instructions?: string
    streaming?: boolean
  }) {
    return this.http.getFetch()(`${this.url}/rag/answer_question`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role: "user", instructions: "", streaming: false, ...body }),
    }).then(r => r.json())
  }

  async getFile(fileId: string) {
    return this.http.getFetch()(`${this.url}/files/${fileId}`, { method: "GET" }).then(r => r.json())
  }

  async deleteFile(fileId: string) {
    return this.http.getFetch()(`${this.url}/rag/files/${fileId}`, { method: "DELETE" }).then(r => r.json())
  }
}
