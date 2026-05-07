import { HttpTransport } from "../http.js"
import type { Account } from "../types/index.js"

export class AccountResource {
  constructor(
    private readonly http: HttpTransport,
    private readonly base: string,
    /**
     * Legacy backend base (e.g. `${gw}/v1/backend`). When provided together with
     * `legacy=true`, account routes resolve to /v1/backend/account instead of
     * /platform/v1/account (the platform microservice is not deployed on prodv2).
     */
    private readonly legacyBase?: string,
    private readonly legacy?: boolean,
  ) {}

  private get v1() { return `${this.base}/v1` }

  /** Returns the path for /account. Routes to legacy /v1/backend/account on prodv2/stable. */
  private accountPath(): string {
    return this.legacy && this.legacyBase
      ? `${this.legacyBase}/account`
      : `${this.v1}/account`
  }

  async getAccount(): Promise<Account> {
    return this.http.getFetch()(this.accountPath(), { method: "GET" }).then(r => r.json())
  }

  async updateAccount(body: Partial<Account>): Promise<Account> {
    return this.http.getFetch()(this.accountPath(), {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async uploadAvatar(body: FormData): Promise<{ url: string }> {
    const base = this.legacy && this.legacyBase ? this.legacyBase : this.v1
    return this.http.getFetch()(`${base}/account/_fileupload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }
}
