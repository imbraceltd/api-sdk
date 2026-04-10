import { HttpTransport } from "../http.js"
import type { User, Organization, Permission, PagedResponse } from "../types/index.js"

export class PlatformResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/platform` }

  // ─── Users ──────────────────────────────────────────────────────────────────
  async listUsers(params?: { page?: number; limit?: number; search?: string }): Promise<PagedResponse<User>> {
    const url = new URL(`${this.url}/users`)
    if (params?.page) url.searchParams.set("page", String(params.page))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.search) url.searchParams.set("search", params.search)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getUser(userId: string): Promise<User> {
    return this.http.getFetch()(`${this.url}/users/${userId}`, { method: "GET" }).then(r => r.json())
  }

  async getMe(): Promise<User> {
    return this.http.getFetch()(`${this.url}/users/me`, { method: "GET" }).then(r => r.json())
  }

  async updateUser(userId: string, body: Partial<User>): Promise<User> {
    return this.http.getFetch()(`${this.url}/users/${userId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteUser(userId: string): Promise<void> {
    await this.http.getFetch()(`${this.url}/users/${userId}`, { method: "DELETE" })
  }

  // ─── Organizations ──────────────────────────────────────────────────────────
  async listOrgs(params?: { page?: number; limit?: number }): Promise<PagedResponse<Organization>> {
    const url = new URL(`${this.url}/organizations`)
    if (params?.page) url.searchParams.set("page", String(params.page))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getOrg(orgId: string): Promise<Organization> {
    return this.http.getFetch()(`${this.url}/organizations/${orgId}`, { method: "GET" }).then(r => r.json())
  }

  async createOrg(body: Partial<Organization>): Promise<Organization> {
    return this.http.getFetch()(`${this.url}/organizations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateOrg(orgId: string, body: Partial<Organization>): Promise<Organization> {
    return this.http.getFetch()(`${this.url}/organizations/${orgId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteOrg(orgId: string): Promise<void> {
    await this.http.getFetch()(`${this.url}/organizations/${orgId}`, { method: "DELETE" })
  }

  // ─── Permissions ────────────────────────────────────────────────────────────
  async listPermissions(userId: string): Promise<Permission[]> {
    return this.http.getFetch()(`${this.url}/users/${userId}/permissions`, { method: "GET" }).then(r => r.json())
  }

  async grantPermission(userId: string, resource: string, action: Permission["action"]): Promise<Permission> {
    return this.http.getFetch()(`${this.url}/users/${userId}/permissions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resource, action }),
    }).then(r => r.json())
  }

  async revokePermission(userId: string, permissionId: string): Promise<void> {
    await this.http.getFetch()(`${this.url}/users/${userId}/permissions/${permissionId}`, { method: "DELETE" })
  }
}
