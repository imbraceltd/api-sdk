import { HttpTransport } from "../http.js"

export interface ChannelAutomationItem {
  id: string
  name?: string
  active?: boolean
  tags?: { id: string; name: string }[]
  [key: string]: unknown
}

export class WorkflowsResource {
  /**
   * @param backend - backend base URL (`{gateway}/v1/backend`)
   * Note: channel automation routes respond on v2/backend.
   */
  constructor(
    private readonly http: HttpTransport,
    private readonly backend: string,
  ) {}

  private get v2() {
    return this.backend.replace("/v1/", "/v2/")
  }

  async listChannelAutomation(params?: { channelType?: string }): Promise<{ data: ChannelAutomationItem[] }> {
    const url = new URL(`${this.v2}/workflows/channel_automation`)
    if (params?.channelType) url.searchParams.set("channelType", params.channelType)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }
}
