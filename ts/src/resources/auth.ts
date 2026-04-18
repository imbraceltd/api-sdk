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
  /**
   * @param base - platform base URL (gateway/platform)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }

  // ─── Third-party token ───────────────────────────────────────────────────────

  async getThirdPartyToken(expirationDays: number = 10): Promise<ThirdPartyTokenResponse> {
    // Requires active access token. "thrid" is a backend typo — preserved intentionally.
    const gatewayBase = this.base.replace(/\/platform$/, "")
    return this.http
      .getFetch()(`${gatewayBase}/private/backend/v1/thrid_party_token`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expirationDays }),
      })
      .then((r) => r.json())
  }

  // ─── Login ───────────────────────────────────────────────────────────────────

  async signinEmailRequest(email: string): Promise<void> {
    await this.http.getFetch()(`${this.v1}/login/_signin_email_request`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    })
  }

  async signinWithEmail(email: string, otp: string): Promise<{ token: string; email: string; expired_at: string }> {
    return this.http.getFetch()(`${this.v1}/login/_signin_with_email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, otp }),
    }).then(r => r.json())
  }

  async signIn(body: { email: string; password: string }) {
    return this.http.getFetch()(`${this.v1}/login/sign_in`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async signUp(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/login/sign_up`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async forgotPassword(email: string) {
    const url = new URL(`${this.v1}/login/forget`)
    url.searchParams.set("email", email)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async resetPassword(body: { token: string; password: string }) {
    return this.http.getFetch()(`${this.v1}/login/forget/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getLoginProviders() {
    return this.http.getFetch()(`${this.v1}/login/providers`, { method: "GET" }).then(r => r.json())
  }

  async signinSSO(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/sso/login-success`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Access token ────────────────────────────────────────────────────────────

  async exchangeAccessToken(body: {
    token: string
    organization_id: string
  }): Promise<{ access_token: string }> {
    return this.http.getFetch()(`${this.v1}/access/_exchange_access_token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async exchangeAccessTokenWithToken(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/access/_exchange_access_token_with_access_token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async signinWithIdentity(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/access/_signin_with_identity`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Sign-up verification ────────────────────────────────────────────────────

  async verifySignUpCheck(email: string) {
    const url = new URL(`${this.v1}/login/sign_up/verify/check`)
    url.searchParams.set("email", email)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async resendVerificationEmail(email: string) {
    const url = new URL(`${this.v1}/login/sign_up/verify/resend`)
    url.searchParams.set("email", email)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async uploadSignUpPhoto(body: FormData) {
    return this.http.getFetch()(`${this.v1}/login/sign_in/file_up_load`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  // ─── SSO / Azure AD ──────────────────────────────────────────────────────────

  async getAzureGroups() {
    return this.http.getFetch()(`${this.v1}/sso/azure_ad/groups/all`, { method: "GET" }).then(r => r.json())
  }

  // ─── OIDC Role Mappings ──────────────────────────────────────────────────────

  async listOidcRoleMappings() {
    return this.http.getFetch()(`${this.v1}/oidc_role_mappings`, { method: "GET" }).then(r => r.json())
  }

  async createOidcRoleMapping(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/oidc_role_mappings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async bulkUpdateOidcRoleMappings(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/oidc_role_mappings/bulk`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Identity ────────────────────────────────────────────────────────────────

  async signupWithGoogle(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/identity/_signup_google`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async signinWithGoogle(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/identity_access/_signin_google`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async signupWithEmail(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/identity/_signup_email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async signinWithEmailIdentity(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/identity_access/_signin_email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── AWS Marketplace ─────────────────────────────────────────────────────────

  async resolveAwsMarketplaceCustomer(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/aws_marketplace/resolve-customer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
