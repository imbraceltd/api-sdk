import { HttpTransport } from "../../core/http.js"

export interface JourneyChannelCreateBody {
  business_unit_id: string
  name: string
  icon_url?: string
  primary_color?: string
  secondary_color?: string
  description?: string
  welcome_message?: string
  fallback_url?: string
}

export interface JourneyChannelUpdateBody {
  name?: string
  icon_url?: string
  primary_color?: string
  secondary_color?: string
  description?: string
  welcome_message?: string
  fallback_url?: string
}

export class JourneyChannelResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  private get url() { return `${this.base}/journeys/v1/channels` }

  async create(body: JourneyChannelCreateBody) {
    return this.http.getFetch()(this.url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(channelId: string, body: JourneyChannelUpdateBody) {
    return this.http.getFetch()(`${this.url}/${channelId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(channelId: string) {
    return this.http.getFetch()(`${this.url}/${channelId}`, {
      method: "DELETE",
    }).then(r => r.json())
  }
}
