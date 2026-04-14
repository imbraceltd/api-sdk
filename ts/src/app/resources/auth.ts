import { HttpTransport } from "../../core/http.js"

export class AuthResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async getThirdPartyToken(expirationDays = 10) {
    return this.http.getFetch()(`${this.base}/private/backend/v1/thrid_party_token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ expirationDays }),
    }).then(r => r.json())
  }

  async signinEmailRequest(email: string): Promise<void> {
    await this.http.getFetch()(`${this.base}/v1/backend/login/_signin_email_request`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    })
  }

  async signinWithEmail(email: string, otp: string) {
    return this.http.getFetch()(`${this.base}/v1/backend/login/_signin_with_email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, otp }),
    }).then(r => r.json())
  }

  async exchangeAccessToken(loginToken: string, organizationId: string) {
    return this.http.getFetch()(`${this.base}/v1/backend/access/_exchange_access_token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: loginToken, organization_id: organizationId }),
    }).then(r => r.json())
  }
}
