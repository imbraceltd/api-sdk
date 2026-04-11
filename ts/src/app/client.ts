import { TokenManager } from "../core/auth/token-manager.js"
import { HttpTransport } from "../core/http.js"
import { AuthResource } from "./resources/auth.js"
import { BoardsResource } from "./resources/boards.js"
import { AgentResource } from "./resources/agent.js"
import { AiResource } from "./resources/ai.js"
import { ChannelResource } from "./resources/channel.js"
import { ConversationsResource } from "./resources/conversations.js"
import { MessagesResource } from "./resources/messages.js"
import { ContactsResource } from "./resources/contacts.js"
import { TeamsResource } from "./resources/teams.js"
import { WorkflowsResource } from "./resources/workflows.js"
import { SettingsResource } from "./resources/settings.js"
import { HealthResource } from "./resources/health.js"
import { AccountResource } from "./resources/account.js"
import { OrganizationsResource } from "./resources/organizations.js"
import { SessionsResource } from "./resources/sessions.js"
import { IpsResource } from "./resources/ips.js"

export interface AppGatewayConfig {
  baseUrl: string
  accessToken?: string
  apiKey?: string
  timeout?: number
}

export class AppGatewayClient {
  private readonly tokenManager: TokenManager
  private readonly http: HttpTransport

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
  public readonly sessions: SessionsResource
  public readonly ips: IpsResource

  constructor(opts: AppGatewayConfig) {
    const base = opts.baseUrl.replace(/\/$/, "")
    this.tokenManager = new TokenManager(opts.accessToken)
    this.http = new HttpTransport({
      apiKey: opts.apiKey,
      timeout: opts.timeout ?? 30000,
      tokenManager: this.tokenManager,
      tokenHeader: "x-access-token",
    })

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
    this.sessions = new SessionsResource(this.http, base)
    this.ips = new IpsResource(this.http, base)
  }

  setAccessToken(token: string) { this.tokenManager.setToken(token) }
  clearAccessToken() { this.tokenManager.clear() }
}
