import { HttpTransport } from "../../core/http.js"

export class ScheduleResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async list(organizationId: string, userId: string, eventType?: string) {
    const url = new URL(`${this.base}/3rd/organization/${organizationId}/users/${userId}/schedulers`)
    if (eventType) url.searchParams.set("event_type", eventType)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }
}
