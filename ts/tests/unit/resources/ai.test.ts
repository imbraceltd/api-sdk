import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { AiResource } from "../../../src/resources/ai.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"
const MESSAGES = [{ role: "user" as const, content: "Hello" }]

function makeResource() {
  const http = new HttpTransport({ timeout: 5000, tokenManager: new TokenManager() })
  return new AiResource(http, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status })
  )
}

describe("AiResource", () => {
  let originalFetch: typeof fetch

  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  describe("complete()", () => {
    it("POSTs to /ai/completions with stream=false", async () => {
      const payload = { id: "cmpl_1", model: "gpt-4o", choices: [] }
      mockFetch(payload)

      const res = await makeResource().complete({ model: "gpt-4o", messages: MESSAGES })
      expect(res.id).toBe("cmpl_1")

      const init = vi.mocked(globalThis.fetch).mock.calls[0][1]!
      expect(init.method).toBe("POST")
      const body = JSON.parse(init.body as string)
      expect(body.stream).toBe(false)
      expect(body.model).toBe("gpt-4o")
    })

    it("passes temperature and maxTokens", async () => {
      mockFetch({ id: "cmpl_2" })
      await makeResource().complete({ model: "gpt-4o", messages: MESSAGES, temperature: 0.5, maxTokens: 256 })
      const body = JSON.parse(vi.mocked(globalThis.fetch).mock.calls[0][1]!.body as string)
      expect(body.temperature).toBe(0.5)
      expect(body.maxTokens).toBe(256)
    })
  })

  describe("embed()", () => {
    it("POSTs to /ai/embeddings", async () => {
      const payload = { model: "text-embedding-3-small", data: [{ index: 0, embedding: [0.1, 0.2] }] }
      mockFetch(payload)

      const res = await makeResource().embed({ model: "text-embedding-3-small", input: ["hello"] })
      expect(res.data[0].embedding).toEqual([0.1, 0.2])

      const init = vi.mocked(globalThis.fetch).mock.calls[0][1]!
      expect(init.method).toBe("POST")
      const body = JSON.parse(init.body as string)
      expect(body.input).toEqual(["hello"])
    })
  })

  describe("stream()", () => {
    it("yields parsed SSE chunks and stops at [DONE]", async () => {
      const chunks = [
        { id: "c1", model: "gpt-4o", choices: [{ index: 0, delta: { content: "Hello" } }] },
        { id: "c2", model: "gpt-4o", choices: [{ index: 0, delta: { content: " world" } }] },
      ]
      const sseBody = chunks.map(c => `data: ${JSON.stringify(c)}`).join("\n") + "\ndata: [DONE]\n"

      const encoder = new TextEncoder()
      const stream = new ReadableStream({
        start(controller) {
          controller.enqueue(encoder.encode(sseBody))
          controller.close()
        },
      })

      globalThis.fetch = vi.fn().mockResolvedValue(new Response(stream, { status: 200 }))

      const collected: unknown[] = []
      for await (const chunk of makeResource().stream({ model: "gpt-4o", messages: MESSAGES })) {
        collected.push(chunk)
      }

      expect(collected).toHaveLength(2)
      expect((collected[0] as typeof chunks[0]).id).toBe("c1")
      expect((collected[1] as typeof chunks[1]).id).toBe("c2")
    })
  })
})
