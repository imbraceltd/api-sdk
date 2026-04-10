import { HttpTransport } from "../http.js"
import type { IpsProfile, Identity, PagedResponse } from "../types/index.js"

export class IpsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/ips` }

  // ─── Profiles ───────────────────────────────────────────────────────────────
  async getProfile(userId: string): Promise<IpsProfile> {
    return this.http.getFetch()(`${this.url}/profiles/${userId}`, { method: "GET" }).then(r => r.json())
  }

  async getMyProfile(): Promise<IpsProfile> {
    return this.http.getFetch()(`${this.url}/profiles/me`, { method: "GET" }).then(r => r.json())
  }

  async updateProfile(userId: string, body: Partial<IpsProfile>): Promise<IpsProfile> {
    return this.http.getFetch()(`${this.url}/profiles/${userId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async searchProfiles(query: string, params?: { page?: number; limit?: number }): Promise<PagedResponse<IpsProfile>> {
    const url = new URL(`${this.url}/profiles`)
    url.searchParams.set("q", query)
    if (params?.page) url.searchParams.set("page", String(params.page))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ─── Follow ─────────────────────────────────────────────────────────────────
  async follow(targetUserId: string): Promise<void> {
    await this.http.getFetch()(`${this.url}/profiles/${targetUserId}/follow`, { method: "POST" })
  }

  async unfollow(targetUserId: string): Promise<void> {
    await this.http.getFetch()(`${this.url}/profiles/${targetUserId}/follow`, { method: "DELETE" })
  }

  async getFollowers(userId: string, params?: { page?: number; limit?: number }): Promise<PagedResponse<IpsProfile>> {
    const url = new URL(`${this.url}/profiles/${userId}/followers`)
    if (params?.page) url.searchParams.set("page", String(params.page))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getFollowing(userId: string, params?: { page?: number; limit?: number }): Promise<PagedResponse<IpsProfile>> {
    const url = new URL(`${this.url}/profiles/${userId}/following`)
    if (params?.page) url.searchParams.set("page", String(params.page))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ─── Identities ─────────────────────────────────────────────────────────────
  async listIdentities(userId: string): Promise<Identity[]> {
    return this.http.getFetch()(`${this.url}/identities/${userId}`, { method: "GET" }).then(r => r.json())
  }

  async unlinkIdentity(userId: string, provider: string): Promise<void> {
    await this.http.getFetch()(`${this.url}/identities/${userId}/${provider}`, { method: "DELETE" })
  }
}
