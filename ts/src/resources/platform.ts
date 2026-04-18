import { HttpTransport } from "../http.js"
import type { User, Organization, Permission, PagedResponse } from "../types/index.js"

export class PlatformResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }
  private get v2() { return `${this.base}/v2` }

  // ─── Users ──────────────────────────────────────────────────────────────────

  async listUsers(params?: {
    page?: number
    limit?: number
    skip?: number
    search?: string
    roles?: string
    sort?: string
    status?: string
  }): Promise<PagedResponse<User>> {
    const url = new URL(`${this.v1}/users`)
    if (params?.page)   url.searchParams.set("page",   String(params.page))
    if (params?.limit)  url.searchParams.set("limit",  String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.search) url.searchParams.set("search", params.search)
    if (params?.roles)  url.searchParams.set("roles",  params.roles)
    if (params?.sort)   url.searchParams.set("sort",   params.sort)
    if (params?.status) url.searchParams.set("status", params.status)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getUser(userId: string): Promise<User> {
    return this.http.getFetch()(`${this.v1}/users/${userId}`, { method: "GET" }).then(r => r.json())
  }

  async getMe(): Promise<User> {
    return this.http.getFetch()(`${this.v1}/users/me`, { method: "GET" }).then(r => r.json())
  }

  async updateUser(userId: string, body: Partial<User>): Promise<User> {
    return this.http.getFetch()(`${this.v1}/users/${userId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async changeRole(body: { user_id: string; role: string }) {
    return this.http.getFetch()(`${this.v1}/users/_change_role`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async archiveUser(body: { user_id: string }) {
    return this.http.getFetch()(`${this.v1}/users/_archive`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async reactivateUser(body: { user_id: string }) {
    return this.http.getFetch()(`${this.v1}/users/_reactivate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async bulkInvite(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/users/_bulk_invite`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getUserWorkflows(userId: string) {
    return this.http.getFetch()(`${this.v1}/users/${userId}/workflows`, { method: "GET" }).then(r => r.json())
  }

  // ─── Organizations ──────────────────────────────────────────────────────────

  async listOrgs(params?: {
    limit?: number
    skip?: number
    is_active?: boolean
  }): Promise<PagedResponse<Organization>> {
    const url = new URL(`${this.v2}/organizations`)
    if (params?.limit)  url.searchParams.set("limit",     String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.is_active !== undefined) url.searchParams.set("is_active", String(params.is_active))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listAllOrgs(params?: { is_active?: boolean }): Promise<Organization[]> {
    const url = new URL(`${this.v2}/organizations/_all`)
    if (params?.is_active !== undefined) url.searchParams.set("is_active", String(params.is_active))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async createOrg(body: Partial<Organization>): Promise<Organization> {
    return this.http.getFetch()(`${this.v1}/organizations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Teams ──────────────────────────────────────────────────────────────────

  async listTeams(params?: { type?: string; limit?: number; skip?: number; q?: string }) {
    const url = new URL(`${this.v2}/teams`)
    if (params?.type)   url.searchParams.set("type",  params.type)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.q)      url.searchParams.set("q",     params.q)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getMyTeams() {
    return this.http.getFetch()(`${this.v2}/teams/my`, { method: "GET" }).then(r => r.json())
  }

  async createTeam(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/teams`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateTeam(teamId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/teams/${teamId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteTeam(teamId: string) {
    return this.http.getFetch()(`${this.v2}/teams/${teamId}`, { method: "DELETE" }).then(r => r.json())
  }

  async addTeamUsers(body: { team_id: string; user_ids: string[] }) {
    return this.http.getFetch()(`${this.v2}/teams/_add_users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async removeTeamUsers(body: { user_ids: string[] }) {
    return this.http.getFetch()(`${this.v2}/teams/_remove_users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getTeamWorkflows(teamId: string) {
    return this.http.getFetch()(`${this.v1}/teams/${teamId}/workflows`, { method: "GET" }).then(r => r.json())
  }

  // ─── Permissions ────────────────────────────────────────────────────────────

  async listPermissions(userId: string): Promise<Permission[]> {
    return this.http.getFetch()(`${this.v1}/users/${userId}/permissions`, { method: "GET" }).then(r => r.json())
  }

  async grantPermission(userId: string, resource: string, action: Permission["action"]): Promise<Permission> {
    return this.http.getFetch()(`${this.v1}/users/${userId}/permissions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resource, action }),
    }).then(r => r.json())
  }

  async revokePermission(userId: string, permissionId: string): Promise<void> {
    await this.http.getFetch()(`${this.v1}/users/${userId}/permissions/${permissionId}`, { method: "DELETE" })
  }

  // ─── Credentials / n8n ──────────────────────────────────────────────────────

  async listCredentials() {
    return this.http.getFetch()(`${this.v1}/credentials`, { method: "GET" }).then(r => r.json())
  }

  async getCredentialTypes(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/workflow/credential-types`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async n8nLogin() {
    return this.http.getFetch()(`${this.v1}/_n8nlogin`, { method: "GET" }).then(r => r.json())
  }

  async listN8nWorkflows(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/workflows`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getN8nWorkflow(workflowId: string) {
    return this.http.getFetch()(`${this.v1}/n8n/workflows/${workflowId}`, { method: "GET" }).then(r => r.json())
  }

  async createN8nWorkflow(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/n8n/workflows`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateN8nWorkflow(workflowId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/n8n/workflows/${workflowId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteN8nWorkflow(workflowId: string) {
    return this.http.getFetch()(`${this.v1}/n8n/workflows/${workflowId}`, { method: "DELETE" }).then(r => r.json())
  }

  // ─── Knowledge ──────────────────────────────────────────────────────────────

  async listKnowledge() {
    return this.http.getFetch()(`${this.v1}/knowledge`, { method: "GET" }).then(r => r.json())
  }

  async uploadKnowledge(body: FormData) {
    return this.http.getFetch()(`${this.v1}/knowledge/upload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  // ─── Resources ──────────────────────────────────────────────────────────────

  async listResources() {
    return this.http.getFetch()(`${this.v1}/resources`, { method: "GET" }).then(r => r.json())
  }

  // ─── Apps (journeys) ────────────────────────────────────────────────────────

  async listApps() {
    return this.http.getFetch()(`${this.v2}/apps`, { method: "GET" }).then(r => r.json())
  }

  async getApp(appId: string) {
    return this.http.getFetch()(`${this.v2}/apps/${appId}`, { method: "GET" }).then(r => r.json())
  }

  async getMenuSettings() {
    return this.http.getFetch()(`${this.v1}/app/_menu_settings`, { method: "GET" }).then(r => r.json())
  }

  // ─── Contacts v2 ────────────────────────────────────────────────────────────

  async getContactV2(contactId: string) {
    return this.http.getFetch()(`${this.v2}/contacts/${contactId}`, { method: "GET" }).then(r => r.json())
  }

  async updateContactV2(contactId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/contacts/${contactId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Users (thêm) ───────────────────────────────────────────────────────────

  async suspendUser(body: { user_id: string }) {
    return this.http.getFetch()(`${this.v1}/users/_suspend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deactivateUser(body: { user_id: string }) {
    return this.http.getFetch()(`${this.v1}/users/_deactivate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async listAllUsers(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/users/_all`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async uploadUserAvatar(body: FormData) {
    return this.http.getFetch()(`${this.v1}/users/_fileupload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  // ─── Apps (thêm) ────────────────────────────────────────────────────────────

  async updateApp(appId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/apps/${appId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteApp(appId: string): Promise<void> {
    await this.http.getFetch()(`${this.v2}/apps/${appId}`, { method: "DELETE" })
  }

  async activateApp(appId: string) {
    return this.http.getFetch()(`${this.v2}/apps/activate/${appId}`, { method: "PATCH" }).then(r => r.json())
  }

  async deactivateApp(appId: string) {
    return this.http.getFetch()(`${this.v2}/apps/de-activate/${appId}`, { method: "PATCH" }).then(r => r.json())
  }

  async getOrgMembersEmail() {
    return this.http.getFetch()(`${this.v2}/apps/org-members-email`, { method: "GET" }).then(r => r.json())
  }

  async listAppForms() {
    return this.http.getFetch()(`${this.v2}/apps/forms`, { method: "GET" }).then(r => r.json())
  }

  async getAppForm(formId: string) {
    return this.http.getFetch()(`${this.v2}/apps/forms/${formId}`, { method: "GET" }).then(r => r.json())
  }

  // ─── Email Senders ───────────────────────────────────────────────────────────

  async listEmailSenders() {
    return this.http.getFetch()(`${this.v2}/apps/email-senders`, { method: "GET" }).then(r => r.json())
  }

  async createEmailSender(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/apps/email-senders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateEmailSender(senderId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v2}/apps/email-senders/${senderId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteEmailSender(senderId: string): Promise<void> {
    await this.http.getFetch()(`${this.v2}/apps/email-senders/${senderId}`, { method: "DELETE" })
  }

  // ─── Business Units ──────────────────────────────────────────────────────────

  async listBusinessUnits(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/business_units`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ─── Rooms ───────────────────────────────────────────────────────────────────

  async listRooms(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/rooms`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getRoom(roomId: string) {
    return this.http.getFetch()(`${this.v1}/rooms/${roomId}`, { method: "GET" }).then(r => r.json())
  }

  async updateRoom(roomId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/rooms/${roomId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getRoomStatus(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/rooms/_status`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async joinRoom(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/rooms/_join`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getRoomStatusCount() {
    return this.http.getFetch()(`${this.v1}/rooms/_status_count`, { method: "GET" }).then(r => r.json())
  }

  async searchRooms(params: { q: string }) {
    const url = new URL(`${this.v1}/rooms/_search`)
    url.searchParams.set("q", params.q)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // ─── Physical Stores ─────────────────────────────────────────────────────────

  async listStores() {
    return this.http.getFetch()(`${this.v1}/stores`, { method: "GET" }).then(r => r.json())
  }

  async createStore(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/stores/_create_with_fp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateStore(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/stores/_modify_with_fp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getStore(storeId: string) {
    return this.http.getFetch()(`${this.v1}/stores/${storeId}`, { method: "GET" }).then(r => r.json())
  }

  // ─── Facebook (platform) ─────────────────────────────────────────────────────

  async getFacebookPages(params?: { fbUserId?: string }) {
    const url = new URL(`${this.v1}/facebooks`)
    if (params?.fbUserId) url.searchParams.set("fbUserId", params.fbUserId)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async authFacebookPages(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/facebook/_auth_pages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async cancelFacebookPages(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/facebook/_cancel_pages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Mail Channels ───────────────────────────────────────────────────────────

  async createMailChannel(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/mail_channels`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getMailChannel(channelId: string) {
    return this.http.getFetch()(`${this.v1}/mail_channels/${channelId}`, { method: "GET" }).then(r => r.json())
  }

  async initChannel(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/init_channel`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Organizations (thêm) ────────────────────────────────────────────────────

  async createAwsOrg(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/organizations/aws`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Workflows / n8n (thêm) ─────────────────────────────────────────────────

  async listN8nNodeTypes(params?: { onlyLatest?: boolean }) {
    const url = new URL(`${this.v1}/n8n/node-types`)
    if (params?.onlyLatest !== undefined) url.searchParams.set("onlyLatest", String(params.onlyLatest))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getCredentialTypeByName(name: string) {
    return this.http.getFetch()(`${this.v1}/workflow/credential-types/${name}`, { method: "GET" }).then(r => r.json())
  }

  async listProcessedCredentialTypes() {
    return this.http.getFetch()(`${this.v1}/workflow/processed-credential-types`, { method: "GET" }).then(r => r.json())
  }

  async listN8nCredentialTypes() {
    return this.http.getFetch()(`${this.v1}/n8n/credential-types`, { method: "GET" }).then(r => r.json())
  }

  async getCredentialParam(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/workflow/_credentialParam`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getN8nOAuth2AuthUrl(credentialId: string) {
    return this.http.getFetch()(`${this.v1}/n8n/oauth2-credential/auth?id=${credentialId}`, { method: "GET" }).then(r => r.json())
  }

  async getN8nOAuth1AuthUrl(credentialId: string) {
    return this.http.getFetch()(`${this.v1}/n8n/oauth1-credential/auth?id=${credentialId}`, { method: "GET" }).then(r => r.json())
  }

  // ─── Teams (thêm) ────────────────────────────────────────────────────────────

  async updateTeamV1(teamId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/teams/${teamId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async uploadTeamIcon(body: FormData) {
    return this.http.getFetch()(`${this.v1}/teams/_fileupload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async listTeamUsers(params?: Record<string, string>) {
    const url = new URL(`${this.v1}/team_users`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listTeamInvites(version: "v1" | "v2" = "v2") {
    return this.http.getFetch()(`${this.base}/${version}/team_users/_invite_list`, { method: "GET" }).then(r => r.json())
  }

  async listTeamUsersV2(params?: Record<string, string>) {
    const url = new URL(`${this.v2}/team_users`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async acceptTeamJoinRequest(teamId: string, teamUserId: string) {
    return this.http.getFetch()(`${this.v2}/teams/${teamId}/user/${teamUserId}/accept`, {
      method: "POST",
    }).then(r => r.json())
  }

  async getTeamLabels(teamId: string) {
    return this.http.getFetch()(`${this.v1}/teams/${teamId}/team_labels`, { method: "GET" }).then(r => r.json())
  }
}
