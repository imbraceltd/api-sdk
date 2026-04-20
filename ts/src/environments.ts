export type Environment = 'develop' | 'sandbox' | 'stable'

export interface EnvironmentPreset {
  gateway: string
  /** Per-service host overrides (for services with a dedicated host that bypass the gateway) */
  serviceHosts?: {
    /** IPS service — develop uses ips.dev.imbrace.lan directly */
    ips?: string
    /** Data Board service — develop uses data-board.dev.imbrace.lan directly */
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
    gateway: 'https://app-gateway.imbrace.co',
  },
}
