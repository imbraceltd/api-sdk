import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { DocumentAIResource } from "../../../src/resources/document-ai.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"
const FIN = "/v2/ai/financial_documents"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new DocumentAIResource(http, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } })
  )
}

function getCalledUrl(): URL {
  return new URL(vi.mocked(globalThis.fetch).mock.calls[0][0] as URL)
}

function getCalledInit() {
  return vi.mocked(globalThis.fetch).mock.calls[0][1]!
}

describe("DocumentAIResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  describe("getFile()", () => {
    it("GETs /v2/ai/financial_documents/{id}", async () => {
      mockFetch({ message: "ok" })
      await makeResource().getFile("file_123")
      expect(getCalledUrl().pathname).toBe(`${FIN}/file_123`)
      expect(getCalledInit().method).toBe("GET")
    })

    it("includes page and limit params", async () => {
      mockFetch({})
      await makeResource().getFile("file_123", { page: 2, limit: 10 })
      const url = getCalledUrl()
      expect(url.searchParams.get("page")).toBe("2")
      expect(url.searchParams.get("limit")).toBe("10")
    })
  })

  describe("getReport()", () => {
    it("GETs /v2/ai/financial_documents/reports/{id}", async () => {
      mockFetch({ data: [] })
      await makeResource().getReport("rep_456", { page: 1, limit: 5 })
      expect(getCalledUrl().pathname).toBe(`${FIN}/reports/rep_456`)
    })
  })

  describe("listErrors()", () => {
    it("GETs /errors-files/{fileId} with default limit=-1", async () => {
      mockFetch({ data: [] })
      await makeResource().listErrors("file_123")
      const url = getCalledUrl()
      expect(url.pathname).toBe(`${FIN}/errors-files/file_123`)
      expect(url.searchParams.get("limit")).toBe("-1")
    })

    it("respects custom limit", async () => {
      mockFetch({})
      await makeResource().listErrors("file_123", { limit: 50 })
      expect(getCalledUrl().searchParams.get("limit")).toBe("50")
    })
  })

  describe("suggest() / fix() / reset()", () => {
    it("POST suggest", async () => {
      mockFetch({})
      await makeResource().suggest({ file_id: "f1" })
      expect(getCalledUrl().pathname).toBe(`${FIN}/suggest`)
      expect(getCalledInit().method).toBe("POST")
      expect(JSON.parse(getCalledInit().body as string)).toEqual({ file_id: "f1" })
    })

    it("POST fix", async () => {
      mockFetch({})
      await makeResource().fix({ file_id: "f1", fixes: [] })
      expect(getCalledUrl().pathname).toBe(`${FIN}/fix`)
    })

    it("POST reset (with empty body)", async () => {
      mockFetch({})
      await makeResource().reset()
      expect(getCalledUrl().pathname).toBe(`${FIN}/reset`)
      expect(JSON.parse(getCalledInit().body as string)).toEqual({})
    })
  })

  describe("updateFile() / updateReport()", () => {
    it("PUT /v2/ai/financial_documents/{id}", async () => {
      mockFetch({})
      await makeResource().updateFile("file_123", { name: "new" })
      expect(getCalledUrl().pathname).toBe(`${FIN}/file_123`)
      expect(getCalledInit().method).toBe("PUT")
    })

    it("PUT /v2/ai/financial_documents/reports/{id}", async () => {
      mockFetch({})
      await makeResource().updateReport("rep_456", { status: "approved" })
      expect(getCalledUrl().pathname).toBe(`${FIN}/reports/rep_456`)
      expect(getCalledInit().method).toBe("PUT")
    })
  })

  describe("deleteFile() / deleteReport()", () => {
    it("DELETE file", async () => {
      mockFetch({})
      await makeResource().deleteFile("file_123")
      expect(getCalledUrl().pathname).toBe(`${FIN}/file_123`)
      expect(getCalledInit().method).toBe("DELETE")
    })

    it("DELETE report", async () => {
      mockFetch({})
      await makeResource().deleteReport("rep_456")
      expect(getCalledUrl().pathname).toBe(`${FIN}/reports/rep_456`)
      expect(getCalledInit().method).toBe("DELETE")
    })
  })

  describe("auth header", () => {
    it("sends x-api-key", async () => {
      mockFetch({})
      await makeResource().getFile("f1")
      const headers = new Headers(getCalledInit().headers as HeadersInit)
      expect(headers.get("x-api-key")).toBe("test_key")
    })
  })
})
