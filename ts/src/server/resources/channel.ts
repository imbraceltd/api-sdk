import { HttpTransport } from "../../core/http.js"

export class ChannelServerResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async get(channelId: string) {
    return this.http.getFetch()(`${this.base}/3rd/channels/${channelId}`, {
      method: "GET",
    }).then(r => r.json())
  }

  async getByOrg(organizationId: string, channelId: string) {
    return this.http.getFetch()(
      `${this.base}/3rd/organization/${organizationId}/channels/${channelId}`,
      { method: "GET" }
    ).then(r => r.json())
  }
}
