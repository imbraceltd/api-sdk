import { describe, it, expect, vi, beforeEach, afterEach } from "vitest"
import { FinancialDocumentsResource, FinancialDocumentsNotDeployedError } from "../../../src/resources/financial-documents.js"
import { HttpTransport } from "../../../src/http.js"
import { TokenManager } from "../../../src/auth/token-manager.js"

const BASE = "https://app-gatewayv2.imbrace.co"
const FIN  = "/v2/ai/financial_documents"

function makeResource() {
  const http = new HttpTransport({ apiKey: "test_key", timeout: 5000, tokenManager: new TokenManager() })
  return new FinancialDocumentsResource(http, BASE)
}

function mockFetch(data: unknown, status = 200) {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(typeof data === "string" ? data : JSON.stringify(data), {
      status,
      headers: { "Content-Type": "application/json" },
    })
  )
}

function getCalledUrl(): string {
  const arg = vi.mocked(globalThis.fetch).mock.calls[0][0]
  return arg instanceof URL ? arg.toString() : String(arg)
}

function getCalledInit() {
  return vi.mocked(globalThis.fetch).mock.calls[0][1]!
}

describe("FinancialDocumentsResource", () => {
  let originalFetch: typeof fetch
  beforeEach(() => { originalFetch = globalThis.fetch })
  afterEach(() => { globalThis.fetch = originalFetch })

  describe("getFile() / getReport()", () => {
    it("GET /v2/ai/financial_documents/{id}", async () => {
      mockFetch({})
      await makeResource().getFile("file_123", { page: 2, limit: 10 })
      const u = new URL(getCalledUrl())
      expect(u.pathname).toBe(`${FIN}/file_123`)
      expect(u.searchParams.get("page")).toBe("2")
      expect(u.searchParams.get("limit")).toBe("10")
    })

    it("GET /reports/{id}", async () => {
      mockFetch({})
      await makeResource().getReport("rep_456")
      expect(new URL(getCalledUrl()).pathname).toBe(`${FIN}/reports/rep_456`)
    })
  })

  describe("listErrors()", () => {
    it("default limit=-1", async () => {
      mockFetch({ data: [] })
      await makeResource().listErrors("file_123")
      expect(new URL(getCalledUrl()).searchParams.get("limit")).toBe("-1")
    })

    it("custom limit", async () => {
      mockFetch({})
      await makeResource().listErrors("file_123", { limit: 50 })
      expect(new URL(getCalledUrl()).searchParams.get("limit")).toBe("50")
    })
  })

  describe("suggest() / fix() / reset()", () => {
    it("POST suggest", async () => {
      mockFetch({})
      await makeResource().suggest({ file_id: "f1" })
      expect(new URL(getCalledUrl()).pathname).toBe(`${FIN}/suggest`)
      expect(getCalledInit().method).toBe("POST")
    })

    it("POST fix", async () => {
      mockFetch({})
      await makeResource().fix({ file_id: "f1" })
      expect(new URL(getCalledUrl()).pathname).toBe(`${FIN}/fix`)
    })

    it("POST reset (empty body if not provided)", async () => {
      mockFetch({})
      await makeResource().reset()
      expect(new URL(getCalledUrl()).pathname).toBe(`${FIN}/reset`)
      expect(JSON.parse(getCalledInit().body as string)).toEqual({})
    })
  })

  describe("updateFile() / updateReport()", () => {
    it("PUT file", async () => {
      mockFetch({})
      await makeResource().updateFile("file_123", { name: "new" })
      expect(getCalledInit().method).toBe("PUT")
    })

    it("PUT report", async () => {
      mockFetch({})
      await makeResource().updateReport("rep_456", { status: "ok" })
      expect(getCalledInit().method).toBe("PUT")
    })
  })

  describe("deleteFile() / deleteReport()", () => {
    it("DELETE file", async () => {
      mockFetch({}, 200)
      await makeResource().deleteFile("file_123")
      expect(getCalledInit().method).toBe("DELETE")
    })

    it("DELETE report", async () => {
      mockFetch({}, 200)
      await makeResource().deleteReport("rep_456")
      expect(getCalledInit().method).toBe("DELETE")
    })
  })

  describe("FinancialDocumentsNotDeployedError", () => {
    it("throws when 404 with FastAPI default 'Not Found' literal", async () => {
      mockFetch('{"detail":"Not Found"}', 404)
      await expect(makeResource().getFile("file_x")).rejects.toThrow(FinancialDocumentsNotDeployedError)
    })

    it("does NOT throw NotDeployedError for custom 404", async () => {
      mockFetch('{"detail":"[ERROR: File not found]"}', 404)
      await expect(makeResource().getFile("file_x")).rejects.not.toThrow(FinancialDocumentsNotDeployedError)
    })

    it("delete_file throws NotDeployedError too", async () => {
      mockFetch('{"detail":"Not Found"}', 404)
      await expect(makeResource().deleteFile("file_x")).rejects.toThrow(FinancialDocumentsNotDeployedError)
    })
  })
})
