import { HttpTransport } from "../http.js"

export class AccountResource {
  /**
   * @param base - platform base URL (gateway/platform)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }

  async getAccount() {
    return this.http.getFetch()(`${this.v1}/account`, { method: "GET" }).then(r => r.json())
  }

  async updateAccount(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/account`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async uploadAvatar(body: FormData) {
    return this.http.getFetch()(`${this.v1}/account/_fileupload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }
}
