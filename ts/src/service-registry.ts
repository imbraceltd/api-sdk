import { type Environment, type EnvironmentPreset, ENVIRONMENTS } from './environments.js'

export interface ServiceUrls {
  /** Gateway fallback — used for health, license, and endpoints not yet migrated to a microservice */
  gateway: string
  /** channel-service — version (v1/v2/v3) appended per method */
  channelService: string
  /** platform — version (v1/v2) appended per method */
  platform: string
  /** ips/v1 — develop: ips.dev.imbrace.lan/ips/v1, other envs: gateway/ips/v1 */
  ips: string
  /** data-board — no version prefix; paths are used directly */
  dataBoard: string
  /** ai — version (v2/v3) appended per method */
  ai: string
  /** marketplaces/v1 — standalone marketplace service */
  marketplaces: string
}

export function resolveServiceUrls(
  env: Environment | EnvironmentPreset,
  overrides?: Partial<ServiceUrls>,
): ServiceUrls {
  const preset: EnvironmentPreset =
    typeof env === 'string' ? ENVIRONMENTS[env] : env
  const gw    = preset.gateway.replace(/\/$/, '')
  const hosts = preset.serviceHosts ?? {}

  const resolved: ServiceUrls = {
    gateway:        gw,
    channelService: `${gw}/channel-service`,
    platform:       `${gw}/platform`,
    ips:            `${(hosts.ips ?? gw).replace(/\/$/, '')}/ips/v1`,
    dataBoard:      `${(hosts.dataBoard ?? gw).replace(/\/$/, '')}/data-board`,
    ai:             `${gw}/ai`,
    marketplaces:   `${gw}/marketplaces`,
  }

  return { ...resolved, ...overrides }
}
