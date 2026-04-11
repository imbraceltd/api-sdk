import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { ImbraceClient, createImbraceClient } from "../../src/client.js"

describe("ImbraceClient", () => {
  let originalEnv: NodeJS.ProcessEnv

  beforeEach(() => {
    originalEnv = { ...process.env }
    delete process.env.IMBRACE_API_KEY
    delete process.env.IMBRACE_BASE_URL
    delete process.env.IMBRACE_TEMP_TOKEN
  })

  afterEach(() => {
    process.env = originalEnv
  })

  it("initialises all 3 gateways", () => {
    const client = new ImbraceClient({ serverApiKey: "key" })
    expect(client.app).toBeDefined()
    expect(client.server).toBeDefined()
    expect(client.journey).toBeDefined()
  })

  it("app gateway has all resources", () => {
    const client = new ImbraceClient({ appApiKey: "key" })
    expect(client.app.auth).toBeDefined()
    expect(client.app.account).toBeDefined()
    expect(client.app.agent).toBeDefined()
    expect(client.app.ai).toBeDefined()
    expect(client.app.boards).toBeDefined()
    expect(client.app.channel).toBeDefined()
    expect(client.app.contacts).toBeDefined()
    expect(client.app.conversations).toBeDefined()
    expect(client.app.health).toBeDefined()
    expect(client.app.messages).toBeDefined()
    expect(client.app.organizations).toBeDefined()
    expect(client.app.sessions).toBeDefined()
    expect(client.app.settings).toBeDefined()
    expect(client.app.teams).toBeDefined()
    expect(client.app.workflows).toBeDefined()
  })

  it("server gateway has all resources", () => {
    const client = new ImbraceClient({ serverApiKey: "key" })
    expect(client.server.boards).toBeDefined()
    expect(client.server.aiAgent).toBeDefined()
    expect(client.server.categories).toBeDefined()
    expect(client.server.schedule).toBeDefined()
    expect(client.server.marketplace).toBeDefined()
  })

  it("journey gateway has all resources", () => {
    const client = new ImbraceClient({ journeyTempToken: "tok" })
    expect(client.journey.workflow).toBeDefined()
    expect(client.journey.aiAssistant).toBeDefined()
    expect(client.journey.apps).toBeDefined()
    expect(client.journey.boards).toBeDefined()
  })

  it("reads IMBRACE_API_KEY from env for server gateway", () => {
    process.env.IMBRACE_API_KEY = "env_key"
    const client = new ImbraceClient()
    expect(client.server).toBeDefined()
  })

  it("reads IMBRACE_BASE_URL from env", () => {
    process.env.IMBRACE_BASE_URL = "https://staging.imbrace.co"
    const client = new ImbraceClient()
    expect(client.app).toBeDefined()
  })

  it("setAccessToken updates app token manager", () => {
    const client = new ImbraceClient({ appApiKey: "key" })
    client.app.setAccessToken("tok_new")
    expect(client.app.tokenManager.getToken()).toBe("tok_new")
  })

  it("clearAccessToken removes token", () => {
    const client = new ImbraceClient({ appAccessToken: "tok_old" })
    client.app.clearAccessToken()
    expect(client.app.tokenManager.getToken()).toBeUndefined()
  })

  it("createImbraceClient returns an ImbraceClient", () => {
    const client = createImbraceClient({ serverApiKey: "key" })
    expect(client).toBeInstanceOf(ImbraceClient)
  })
})
