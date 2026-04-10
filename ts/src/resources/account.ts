import { HttpTransport } from "../http.js"

export class AccountResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async getAccount() {
    return this.http.getFetch()(`${this.base}/v1/backend/account`, { method: "GET" }).then(r => r.json())
  }
}
