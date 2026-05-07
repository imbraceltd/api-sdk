export type Environment = 'develop' | 'sandbox' | 'stable' | 'prodv2'

export interface EnvironmentPreset {
  gateway: string
  /** Per-service host overrides (for services with a dedicated host that bypass the gateway) */
  serviceHosts?: {
    /** Override IPS service host (e.g. for internal direct access). Defaults to gateway/ips/v1. */
    ips?: string
    /** Override Data Board service host. Defaults to gateway/data-board. */
    dataBoard?: string
  }
  /**
   * When true, the platform/account/organizations/teams resources route to
   * `/v1/backend` and `/v2/backend` (legacy paths) instead of `/platform/v1`
   * and `/platform/v2`. The platform microservice is not deployed on prodv2,
   * so prodv2/stable use the legacy backend routes.
   */
  legacyBackend?: boolean
}

export const ENVIRONMENTS: Record<Environment, EnvironmentPreset> = {
  develop: {
    gateway: 'https://app-gateway.dev.imbrace.co',
  },
  sandbox: {
    gateway: 'https://app-gateway.sandbox.imbrace.co',
  },
  stable: {
    gateway: 'https://app-gatewayv2.imbrace.co',
    legacyBackend: true,
  },
  prodv2: {
    gateway: 'https://app-gatewayv2.imbrace.co',
    legacyBackend: true,
  },
}
