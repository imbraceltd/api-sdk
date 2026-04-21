export * from "./errors.js"
export * from "./types/index.js"
export * from "./environments.js"
export * from "./service-registry.js"

import { type Environment, type EnvironmentPreset, ENVIRONMENTS } from "./environments.js"
import { resolveServiceUrls, type ServiceUrls } from "./service-registry.js"
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
import { CampaignResource } from "./resources/campaign.js"
import { OutboundResource } from "./resources/outbound.js"
import { LicenseResource } from "./resources/license.js"
import { ChatAiResource } from "./resources/chat-ai.js"
import { FileServiceResource } from "./resources/file-service.js"
import { MessageSuggestionResource } from "./resources/message-suggestion.js"
import { PredictResource } from "./resources/predict.js"
import { ActivePiecesResource } from "./resources/activepieces.js"

export interface ImbraceClientConfig {
  /**
   * Environment preset.
   * - 'develop'  - app-gateway.dev.imbrace.co
   * - 'sandbox'  - app-gateway.sandbox.imbrace.co
   * - 'stable'   - app-gatewayv2.imbrace.co (default)
   */
  env?: Environment
  /** Override the gateway URL for the selected environment. */
  gateway?: string
  /** Override the base URL for individual services. */
  services?: Partial<ServiceUrls>
  /** API key (server-side) - from POST /private/backend/v1/thrid_party_token */
  apiKey?: string
  /** User access token (client-side OAuth/JWT). */
  accessToken?: string
  /** Sent as x-organization-id on every request. */
  organizationId?: string
  /** Timeout in ms. Default: 30000 */
  timeout?: number
  /** Ping /global/health on init(). Default: false */
  checkHealth?: boolean
}

/** Extract apiKey from the response of the third-party token endpoint. */
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
  public readonly campaign: CampaignResource
  public readonly outbound: OutboundResource
  public readonly license: LicenseResource
  public readonly chatAi: ChatAiResource
  public readonly fileService: FileServiceResource
  public readonly messageSuggestion: MessageSuggestionResource
  public readonly predict: PredictResource
  public readonly activepieces: ActivePiecesResource

  constructor(opts?: ImbraceClientConfig) {
    this.opts = opts ?? {}

    const mergedServices = opts?.services ?? {}

    // -- Resolve environment & service URLs ----------------------------------
    const envName = opts?.env ?? 'stable'
    const gatewayOverride = opts?.gateway

    const basePreset: Environment | EnvironmentPreset = gatewayOverride
      ? { ...ENVIRONMENTS[envName], gateway: gatewayOverride }
      : envName

    const urls = resolveServiceUrls(basePreset, mergedServices)

    const resolvedApiKey = opts?.apiKey

    // -- Warn when no credentials ---------------------------------------------
    if (!resolvedApiKey && !opts?.accessToken) {
      console.warn(
        '[ImbraceClient] No credentials provided. ' +
        'Pass accessToken= (user login) or apiKey= (server-to-server).'
      )
    }

    // -- HTTP Transport -------------------------------------------------------

    this.tokenManager = new TokenManager(opts?.accessToken)
    this.http = new HttpTransport({
      apiKey:         resolvedApiKey,
      timeout:        opts?.timeout ?? 30000,
      tokenManager:   this.tokenManager,
      organizationId: opts?.organizationId,
    })

    // -- Wire resources with per-service base URLs ----------------------------

    // Auth & Account - platform service
    this.auth          = new AuthResource(this.http, urls.platform, urls.gateway)
    this.account       = new AccountResource(this.http, urls.platform)

    // Platform group
    this.platform      = new PlatformResource(this.http, urls.platform, urls.backend)
    this.organizations = new OrganizationsResource(this.http, urls.platform)
    this.teams         = new TeamsResource(this.http, urls.platform, urls.backend)
    this.settings      = new SettingsResource(this.http, urls.channelService, urls.platform)

    // channel-service group
    this.channel       = new ChannelResource(this.http, urls.channelService)
    this.contacts      = new ContactsResource(this.http, urls.channelService)
    this.conversations = new ConversationsResource(this.http, urls.channelService)
    this.messages      = new MessagesResource(this.http, urls.channelService, urls.backend)
    this.categories    = new CategoriesResource(this.http, urls.channelService)

    this.workflows     = new WorkflowsResource(this.http, urls.backend)

    // Dedicated services
    this.boards        = new BoardsResource(this.http, urls.dataBoard, urls.backend)
    this.ips           = new IpsResource(this.http, urls.ips)
    this.ai            = new AiResource(this.http, urls.ai)

    this.marketplace   = new MarketplaceResource(this.http, urls.marketplaces, urls.gateway)

    // Agent templates + use-cases
    this.agent         = new AgentResource(this.http, urls.marketplaces, urls.gateway)

    // Campaign & Outbound - channel-service
    this.campaign      = new CampaignResource(this.http, urls.channelService)
    this.outbound      = new OutboundResource(this.http, urls.channelService)

    // License - gateway root
    this.license       = new LicenseResource(this.http, urls.gateway)

    // Gateway fallback
    this.health        = new HealthResource(this.http, urls.gateway)
    this.sessions      = new SessionsResource(this.http, urls.gateway)
    this.schedule      = new ScheduleResource(this.http, urls.ips)

    // New services
    this.chatAi           = new ChatAiResource(this.http, `${urls.ai}/v3/ai`)
    this.fileService      = new FileServiceResource(this.http, urls.fileService)       
    this.messageSuggestion = new MessageSuggestionResource(this.http, urls.messageSuggestion)
    this.predict          = new PredictResource(this.http, urls.predict)
    this.activepieces      = new ActivePiecesResource(this.http, urls.activepieces)    
    }
  // -- Convenience auth ------------------------------------------------------

  /** Sign in with email/password and store the returned access token. */
  public async login(email: string, password: string): Promise<Record<string, unknown>> {
    const res = await this.auth.signIn({ email, password })
    const token = (res as any).accessToken
      ?? (res as any).token
      ?? (res as any).access_token
    if (typeof token === 'string') this.tokenManager.setToken(token)
    return res as any
  }

  /** Sign in with an OTP (after calling requestOtp) and store the returned access token. */
  public async loginWithOtp(email: string, otp: string): Promise<Record<string, unknown>> {
    const res = await this.auth.signinWithEmail(email, otp)
    const token = (res as any).accessToken
      ?? (res as any).token
      ?? (res as any).access_token
    if (typeof token === 'string') this.tokenManager.setToken(token)
    return res as any
  }

  /** Send an OTP to the given email. Call before loginWithOtp(). */
  public async requestOtp(email: string): Promise<void> {
    await this.auth.signinEmailRequest(email)
  }

  public setAccessToken(token: string): void {
    this.tokenManager.setToken(token)
    this.http.clearApiKey() // Explicit setAccessToken switches off api_key mode
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
