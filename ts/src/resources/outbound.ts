import { HttpTransport } from "../http.js"

export class OutboundResource {
  /**
   * @param base - channel-service base URL (gateway/channel-service)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }

  async sendWhatsApp(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/outbounds/whatsapp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async sendEmail(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/outbounds/email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
