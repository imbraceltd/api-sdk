import { type Environment, type EnvironmentPreset, ENVIRONMENTS } from './environments.js'

export interface ServiceUrls {
  /** Gateway fallback — used for health, license, and endpoints not yet migrated to a microservice */
  gateway: string
  /** channel-service — version (v1/v2/v3) appended per method */
  channelService: string
  /** platform — version (v1/v2) appended per method */
  platform: string
  /** ips/v1 — gateway/ips/v1 for all environments */
  ips: string
  /** data-board — no version prefix; paths are used directly (KnowledgeHub folders/files/drive) */
  dataBoard: string
  /** /v1/backend — board CRUD, items, fields, search, segmentation */
  backend: string
  /** ai — version (v2/v3) appended per method */
  ai: string
  /** marketplaces/v1 — standalone marketplace service */
  marketplaces: string
  /** file-service — /v1/file-service */
  fileService: string
  /** message-suggestion — /v1/message-suggestion */
  messageSuggestion: string
  /** predict — /predict */
  predict: string
  /** activepieces — /activepieces */
  activepieces: string
}


export function resolveServiceUrls(
  env: Environment | EnvironmentPreset,
  overrides?: Partial<ServiceUrls>,
): ServiceUrls {
  const preset: EnvironmentPreset =
    typeof env === 'string' ? ENVIRONMENTS[env] : env
  const gw    = preset.gateway.replace(/\/$/, '')
  const hosts = preset.serviceHosts ?? {}
  
  // v2 services check: if environment is 'prodv2' or gateway is app-gatewayv2
  const isV2 = env === 'prodv2' || gw.includes('app-gatewayv2')

  const resolved: ServiceUrls = {
    gateway:           gw,
    channelService:    `${gw}/channel-service`,
    platform:          `${gw}/platform`,
    ips:               `${(hosts.ips ?? gw).replace(/\/$/, '')}/ips/v1`,
    dataBoard:         `${gw}/data-board`,
    backend:           isV2 ? `${gw}/v2/backend` : `${gw}/v1/backend`,
    ai:                gw,
    marketplaces:      `${gw}/v2/backend/marketplaces`,
    fileService:       isV2 ? `${gw}/v2/backend/file-service` : `${gw}/v1/backend/file-service`,
    messageSuggestion: `${gw}/v1/message-suggestion`,
    predict:           `${gw}/predict`,
    activepieces:      `${gw}/activepieces`,
  }

  return { ...resolved, ...overrides }
}
