import { HttpTransport } from "../../core/http.js"

export class ContactsResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/v1/backend/contacts` }

  async list(params?: { limit?: number; skip?: number }) {
    const url = new URL(this.url)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async search(query: string) {
    const url = new URL(`${this.url}/_search`)
    url.searchParams.set("q", query)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async update(contactId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.url}/${contactId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getConversations(contactId: string, params?: { channelTypes?: string }) {
    const url = new URL(`${this.url}/${contactId}/conversations`)
    if (params?.channelTypes) url.searchParams.set("channel_types", params.channelTypes)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  // Notifications
  async listNotifications(params?: { limit?: number; skip?: number }) {
    const url = new URL(`${this.base}/v1/backend/notifications`)
    if (params?.limit) url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async markNotificationsRead(notificationIds: string[]) {
    return this.http.getFetch()(`${this.base}/v1/backend/notifications/read`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notification_id: notificationIds }),
    }).then(r => r.json())
  }

  async dismissNotification(notificationId: string) {
    return this.http.getFetch()(`${this.base}/v1/backend/notifications/dismiss`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notification_id: notificationId }),
    }).then(r => r.json())
  }

  async dismissAllNotifications() {
    return this.http.getFetch()(`${this.base}/v1/backend/notifications/dismiss/all`, {
      method: "DELETE",
    }).then(r => r.json())
  }
}
