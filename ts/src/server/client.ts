import { TokenManager } from "../core/auth/token-manager.js"
import { HttpTransport } from "../core/http.js"
import { ServerBoardsResource } from "./resources/boards.js"
import { AiAgentResource } from "./resources/ai-agent.js"
import { CategoriesResource } from "./resources/categories.js"
import { ScheduleResource } from "./resources/schedule.js"
import { PlatformResource } from "./resources/platform.js"
import { MarketplaceResource } from "./resources/marketplace.js"
import { ChannelServerResource } from "./resources/channel.js"
import { ConversationServerResource } from "./resources/conversation.js"

export interface ServerGatewayConfig {
  apiKey: string
  baseUrl: string
  timeout?: number
}

export class ServerGatewayClient {
  private readonly http: HttpTransport

  public readonly boards: ServerBoardsResource
  public readonly aiAgent: AiAgentResource
  public readonly categories: CategoriesResource
  public readonly schedule: ScheduleResource
  public readonly marketplace: MarketplaceResource
  public readonly platform: PlatformResource
  public readonly channel: ChannelServerResource
  public readonly conversation: ConversationServerResource

  constructor(opts: ServerGatewayConfig) {
    const base = opts.baseUrl.replace(/\/$/, "")
    this.http = new HttpTransport({
      apiKey: opts.apiKey,
      timeout: opts.timeout ?? 30000,
      tokenManager: new TokenManager(),
      tokenHeader: "x-access-token",
    })

    this.boards = new ServerBoardsResource(this.http, base)
    this.aiAgent = new AiAgentResource(this.http, base)
    this.categories = new CategoriesResource(this.http, base)
    this.schedule = new ScheduleResource(this.http, base)
    this.marketplace = new MarketplaceResource(this.http, base)
    this.platform = new PlatformResource(this.http, base)
    this.channel = new ChannelServerResource(this.http, base)
    this.conversation = new ConversationServerResource(this.http, base)
  }
}
