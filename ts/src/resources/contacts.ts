import { HttpTransport } from "../http.js"

export class ContactsResource {
  /**
   * @param base - channel-service base URL (gateway/channel-service)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get v1() { return `${this.base}/v1` }

  // ─── Contacts ────────────────────────────────────────────────────────────────

  async list(params?: { limit?: number; skip?: number; sort?: string }) {
    const url = new URL(`${this.v1}/contacts`)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params?.sort)   url.searchParams.set("sort",  params.sort)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(contactId: string) {
    return this.http.getFetch()(`${this.v1}/contacts/${contactId}`, { method: "GET" }).then(r => r.json())
  }

  async update(contactId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.v1}/contacts/${contactId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async search(params: { q: string; limit?: number; skip?: number; sort?: string; type?: string }) {
    const url = new URL(`${this.v1}/contacts/_search`)
    url.searchParams.set("q", params.q)
    if (params.limit)  url.searchParams.set("limit", String(params.limit))
    if (params.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    if (params.sort)   url.searchParams.set("sort",  params.sort)
    if (params.type)   url.searchParams.set("type",  params.type)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async exportCsv(params?: { sort?: string }) {
    const url = new URL(`${this.v1}/contacts/_export_csv`)
    if (params?.sort) url.searchParams.set("sort", params.sort)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.text())
  }

  async getConversations(contactId: string, params?: { channelTypes?: string }) {
    const url = new URL(`${this.v1}/contacts/${contactId}/conversations`)
    if (params?.channelTypes) url.searchParams.set("channel_types", params.channelTypes)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getComments(contactId: string, params?: {
    channelType?: string
    skip?: number
    limit?: number
  }) {
    const url = new URL(`${this.v1}/contacts/${contactId}/comments`)
    if (params?.channelType) url.searchParams.set("channel_types", params.channelType)
    if (params?.skip !== undefined) url.searchParams.set("skip",  String(params.skip))
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getFiles(contactId: string) {
    return this.http.getFetch()(`${this.v1}/contact/${contactId}/files`, { method: "GET" }).then(r => r.json())
  }

  async getActivities(conversationId: string) {
    return this.http.getFetch()(`${this.v1}/conversations_activities/${conversationId}`, { method: "GET" }).then(r => r.json())
  }

  async uploadAvatar(body: FormData) {
    return this.http.getFetch()(`${this.v1}/contacts/_fileupload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  // ─── Notifications (moved to channel-service) ────────────────────────────────

  async listNotifications(params?: { limit?: number; skip?: number }) {
    const url = new URL(`${this.v1}/notifications`)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async markNotificationsRead(notificationIds: string[]) {
    return this.http.getFetch()(`${this.v1}/notifications/read`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notification_id: notificationIds }),
    }).then(r => r.json())
  }

  async dismissNotification(notificationId: string) {
    return this.http.getFetch()(`${this.v1}/notifications/dismiss`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notification_id: notificationId }),
    }).then(r => r.json())
  }

  async dismissAllNotifications() {
    return this.http.getFetch()(`${this.v1}/notifications/dismiss/all`, {
      method: "DELETE",
    }).then(r => r.json())
  }
}
