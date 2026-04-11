import { HttpTransport } from "../../core/http.js"

export class AppsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/journeys/v2/apps` }

  async submit(appId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.url}/submit/${appId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateSettings(appId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.url}/settings/${appId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
