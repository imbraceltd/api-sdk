export * from "./core/errors.js"
export * from "./types/index.js"

import { AppGatewayClient } from "./app/client.js"
import { ServerGatewayClient } from "./server/client.js"
import { JourneyClient } from "./journey/client.js"

export { AppGatewayClient } from "./app/client.js"
export { ServerGatewayClient } from "./server/client.js"
export { JourneyClient } from "./journey/client.js"

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const env = (globalThis as any).process?.env ?? {}

const DEFAULT_BASE_URL = "https://app-gateway.imbrace.co"

export interface ImbraceClientConfig {
  // App Gateway
  appBaseUrl?: string
  appAccessToken?: string
  appApiKey?: string
  // Server Gateway
  serverBaseUrl?: string
  serverApiKey?: string
  // Journey API
  journeyBaseUrl?: string
  journeyTempToken?: string
  // Shared
  timeout?: number
}

export class ImbraceClient {
  public readonly app: AppGatewayClient
  public readonly server: ServerGatewayClient
  public readonly journey: JourneyClient

  constructor(opts?: ImbraceClientConfig) {
    const appBase = (opts?.appBaseUrl ?? env.IMBRACE_BASE_URL ?? DEFAULT_BASE_URL).replace(/\/$/, "")
    const serverBase = (opts?.serverBaseUrl ?? env.IMBRACE_BASE_URL ?? DEFAULT_BASE_URL).replace(/\/$/, "")
    const journeyBase = (opts?.journeyBaseUrl ?? env.IMBRACE_BASE_URL ?? DEFAULT_BASE_URL).replace(/\/$/, "")
    const serverKey = opts?.serverApiKey ?? env.IMBRACE_API_KEY ?? ""
    const journeyToken = opts?.journeyTempToken ?? env.IMBRACE_TEMP_TOKEN ?? ""
    const timeout = opts?.timeout ?? 30000

    this.app = new AppGatewayClient({
      baseUrl: appBase,
      accessToken: opts?.appAccessToken,
      apiKey: opts?.appApiKey,
      timeout,
    })

    this.server = new ServerGatewayClient({
      apiKey: serverKey,
      baseUrl: serverBase,
      timeout,
    })

    this.journey = new JourneyClient({
      tempToken: journeyToken,
      baseUrl: journeyBase,
      timeout,
    })
  }
}

export function createImbraceClient(config?: ImbraceClientConfig): ImbraceClient {
  return new ImbraceClient(config)
}
