export * from "./errors.js"
export * from "./types/index.js"

import { TokenManager } from "./auth/token-manager.js"
import { HttpTransport } from "./http.js"
import { AuthResource } from "./resources/auth.js"
import { AccountResource } from "./resources/account.js"
import { OrganizationsResource } from "./resources/organizations.js"
import { AgentResource } from "./resources/agent.js"
import { AiResource } from "./resources/ai.js"
import { ChannelResource } from "./resources/channel.js"
import { ConversationsResource } from "./resources/conversations.js"
import { MessagesResource } from "./resources/messages.js"
import { ContactsResource } from "./resources/contacts.js"
import { TeamsResource } from "./resources/teams.js"
import { WorkflowsResource } from "./resources/workflows.js"
import { BoardsResource } from "./resources/boards.js"
import { SettingsResource } from "./resources/settings.js"
import { HealthResource } from "./resources/health.js"
import { IpsResource } from "./resources/ips.js"
import { MarketplaceResource } from "./resources/marketplace.js"
import { PlatformResource } from "./resources/platform.js"
import { SessionsResource } from "./resources/sessions.js"
import { CategoriesResource } from "./resources/categories.js"
import { ScheduleResource } from "./resources/schedule.js"

export interface ImbraceClientConfig {
  /** API key từ POST /private/backend/v1/thrid_party_token */
  apiKey?: string
  accessToken?: string
  /** Default: https://app-gatewayv2.imbrace.co */
  baseUrl?: string
  /** Timeout in ms. Default: 30000 */
  timeout?: number
  /** Ping /global/health on init(). Default: false */
  checkHealth?: boolean
}

/** Extract apiKey từ response của third-party token endpoint */
export function extractApiKey(res: { apiKey: { apiKey: string } }): string {
  return res.apiKey.apiKey
}

export class ImbraceClient {
  private readonly tokenManager: TokenManager
  private readonly http: HttpTransport
  private readonly opts: ImbraceClientConfig
  private healthChecked = false

  public readonly auth: AuthResource
  public readonly account: AccountResource
  public readonly organizations: OrganizationsResource
  public readonly agent: AgentResource
  public readonly ai: AiResource
  public readonly channel: ChannelResource
  public readonly conversations: ConversationsResource
  public readonly messages: MessagesResource
  public readonly contacts: ContactsResource
  public readonly teams: TeamsResource
  public readonly workflows: WorkflowsResource
  public readonly boards: BoardsResource
  public readonly settings: SettingsResource
  public readonly health: HealthResource
  public readonly ips: IpsResource
  public readonly marketplace: MarketplaceResource
  public readonly platform: PlatformResource
  public readonly sessions: SessionsResource
  public readonly categories: CategoriesResource
  public readonly schedule: ScheduleResource

  constructor(opts?: ImbraceClientConfig) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const env = (globalThis as any).process?.env ?? {}
    const apiKey = opts?.apiKey ?? env.IMBRACE_API_KEY
    const base = (opts?.baseUrl ?? env.IMBRACE_BASE_URL ?? "https://app-gatewayv2.imbrace.co").replace(/\/$/, "")
    const timeout = opts?.timeout ?? 30000

    this.opts = opts ?? {}
    this.tokenManager = new TokenManager(opts?.accessToken)
    this.http = new HttpTransport({ apiKey, timeout, tokenManager: this.tokenManager })

    this.auth = new AuthResource(this.http, base)
    this.account = new AccountResource(this.http, base)
    this.organizations = new OrganizationsResource(this.http, base)
    this.agent = new AgentResource(this.http, base)
    this.ai = new AiResource(this.http, base)
    this.channel = new ChannelResource(this.http, base)
    this.conversations = new ConversationsResource(this.http, base)
    this.messages = new MessagesResource(this.http, base)
    this.contacts = new ContactsResource(this.http, base)
    this.teams = new TeamsResource(this.http, base)
    this.workflows = new WorkflowsResource(this.http, base)
    this.boards = new BoardsResource(this.http, base)
    this.settings = new SettingsResource(this.http, base)
    this.health = new HealthResource(this.http, base)
    this.ips = new IpsResource(this.http, base)
    this.marketplace = new MarketplaceResource(this.http, base)
    this.platform = new PlatformResource(this.http, base)
    this.sessions = new SessionsResource(this.http, base)
    this.categories = new CategoriesResource(this.http, base)
    this.schedule = new ScheduleResource(this.http, base)
  }

  public setAccessToken(token: string): void {
    this.tokenManager.setToken(token)
  }

  public clearAccessToken(): void {
    this.tokenManager.clear()
  }

  public async init(): Promise<void> {
    if (this.opts.checkHealth && !this.healthChecked) {
      await this.health.check()
      this.healthChecked = true
    }
  }
}

export function createImbraceClient(config?: ImbraceClientConfig): ImbraceClient {
  return new ImbraceClient(config)
}
