import { HttpTransport } from "../http.js"

export class LicenseResource {
  /**
   * @param base - gateway base URL
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async get() {
    return this.http.getFetch()(`${this.base}/license`, { method: "GET" }).then(r => r.json())
  }

  async activate(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/license`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
