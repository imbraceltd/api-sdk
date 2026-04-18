import { type Environment, type EnvironmentPreset, ENVIRONMENTS } from './environments.js'

export interface ServiceUrls {
  /** Gateway fallback — dùng cho health, license, và các endpoint chưa migrate */
  gateway: string
  /** channel-service — version (v1/v2/v3) thêm trong từng method */
  channelService: string
  /** platform — version (v1/v2) thêm trong từng method */
  platform: string
  /** ips/v1 — develop: ips.dev.imbrace.lan/ips/v1, các env khác: gateway/ips/v1 */
  ips: string
  /** data-board — không có version prefix, path trực tiếp */
  dataBoard: string
  /** ai — version (v2/v3) thêm trong từng method */
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
