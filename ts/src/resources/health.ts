import { HttpTransport } from "../http.js"

export class HealthResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async check() {
    return this.http.getFetch()(`${this.base}/`, { method: "GET" })
      .then(res => res.json())
  }
}
