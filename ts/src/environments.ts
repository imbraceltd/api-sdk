export type Environment = 'develop' | 'sandbox' | 'stable'

export interface EnvironmentPreset {
  gateway: string
  /** Per-service host overrides (khi service có dedicated host riêng, không qua gateway) */
  serviceHosts?: {
    /** IPS service — dev dùng ips.dev.imbrace.lan trực tiếp */
    ips?: string
    /** Data Board service — dev dùng data-board.dev.imbrace.lan trực tiếp */
    dataBoard?: string
  }
}

export const ENVIRONMENTS: Record<Environment, EnvironmentPreset> = {
  develop: {
    gateway: 'https://app-gateway.dev.imbrace.co',
    serviceHosts: {
      ips:       'http://ips.dev.imbrace.lan',
      dataBoard: 'http://data-board.dev.imbrace.lan',
    },
  },
  sandbox: {
    gateway: 'https://app-gateway.sandbox.imbrace.co',
  },
  stable: {
    gateway: 'https://app-gateway.imbrace.co',
  },
}
