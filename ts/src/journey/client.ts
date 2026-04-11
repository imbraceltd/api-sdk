import { TokenManager } from "../core/auth/token-manager.js"
import { HttpTransport } from "../core/http.js"
import { WorkflowResource } from "./resources/workflow.js"
import { AiAssistantResource } from "./resources/ai-assistant.js"
import { AppsResource } from "./resources/apps.js"
import { JourneyBoardsResource } from "./resources/boards.js"
import { JourneyChannelResource } from "./resources/channel.js"

export interface JourneyClientConfig {
  tempToken: string
  baseUrl: string
  timeout?: number
}

export class JourneyClient {
  private readonly http: HttpTransport

  public readonly workflow: WorkflowResource
  public readonly aiAssistant: AiAssistantResource
  public readonly apps: AppsResource
  public readonly boards: JourneyBoardsResource
  public readonly channel: JourneyChannelResource

  constructor(opts: JourneyClientConfig) {
    const base = opts.baseUrl.replace(/\/$/, "")
    this.http = new HttpTransport({
      apiKey: opts.tempToken,
      timeout: opts.timeout ?? 30000,
      tokenManager: new TokenManager(),
      tokenHeader: "x-temp-token",
    })

    this.workflow = new WorkflowResource(this.http, base)
    this.aiAssistant = new AiAssistantResource(this.http, base)
    this.apps = new AppsResource(this.http, base)
    this.boards = new JourneyBoardsResource(this.http, base)
    this.channel = new JourneyChannelResource(this.http, base)
  }
}
