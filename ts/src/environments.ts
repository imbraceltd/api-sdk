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
  },
  prodv2: {
    gateway: 'https://app-gatewayv2.imbrace.co',
  },
}
