import { HttpTransport } from "../http.js"

export interface ThirdPartyTokenResponse {
  apiKey: {
    _id: string
    apiKey: string
    organization_id: string
    user_id: string
    is_active: boolean
    expired_at: string
    created_at: string
    updated_at: string
    is_temp: boolean
  }
  expires_in: number
}

export class AuthResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async getThirdPartyToken(expirationDays: number = 10): Promise<ThirdPartyTokenResponse> {
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

  async signinWithEmail(email: string, otp: string): Promise<{ token: string; email: string; expired_at: string }> {
    return this.http.getFetch()(`${this.base}/v1/login/_signin_with_email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, otp }),
    }).then(r => r.json())
  }

  async exchangeAccessToken(loginToken: string, organizationId: string): Promise<{ access_token: string }> {
    return this.http.getFetch()(`${this.base}/v1/backend/access/_exchange_access_token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: loginToken, organization_id: organizationId }),
    }).then(r => r.json())
  }
}
