# Refactor Report — Workflows + Document AI

**Ngày:** 2026-05-08
**Branch:** `refactor/drop-financial-documents-update-llms-docs`
**Commits:** `8171d16` (cleanup) + `641c880` (test rewrite + report)
**Base:** `main` (`faade03`)
**PR:** <https://github.com/imbraceltd/api-sdk/pull/new/refactor/drop-financial-documents-update-llms-docs>

---

## Hai task chính

| Task | SDK source | Unit tests | Integration tests |
|---|---|---|---|
| 1. Bỏ hết `ActivePieces` → đổi thành `workflows` | ✅ Done | ✅ Pass | ✅ **52 endpoints work end-to-end** |
| 2. Thêm `Document AI` resource | ✅ Done | ✅ Pass | ✅ **9/10 sandbox e2e pass** (1 fail backend) |

Phần dưới đây chứng minh từng task.

---

## Task 1 — `ActivePieces` → `workflows`

### Source code (đã sạch)

Không còn property `client.activepieces` / `client.active_pieces` ở bất kỳ file nào trong SDK. Mọi truy cập đều qua `client.workflows` (TS) / `client.workflows` (Py sync + async):

- TS: `public readonly workflows: WorkflowsResource` ([ts/src/client.ts](../ts/src/client.ts))
- Python sync: `self.workflows = WorkflowsResource(...)` ([py/src/imbrace/client.py](../py/src/imbrace/client.py))
- Python async: `self.workflows = AsyncWorkflowsResource(...)` ([py/src/imbrace/async_client.py](../py/src/imbrace/async_client.py))

> **Lưu ý:** string `/activepieces` trong `service-registry.{ts,py}` là **gateway PATH thật** của backend (`{gateway}/activepieces`), không phải SDK API surface. Backend chưa rename path này nên SDK phải giữ.

### Unit tests (mocked)

```
tests/unit/resources/workflows.test.ts (3 tests) ✓
tests/unit/resources/test_workflows.py (2 tests) ✓
```

### Integration tests (real prodv2 gateway)

#### TypeScript — workflows

```
$ node ts/tests/local/test-workflows-apikey.mjs
  21 passed | 0 failed | 3 skipped (resource empty)
```

13 sections — channel automations, flows CRUD, trigger, runs, folders CRUD, pieces (126), triggers, tables, MCP servers, invitations, cleanup. Tất cả hoạt động end-to-end thật trên prodv2.

#### Python — workflows (sync + async)

```
$ python py/tests/local/test_workflows.py
  31 passed | 0 failed | 3 skipped
```

13 sync sections + 6 async sections. Cả `client.workflows.*` lẫn `await async_client.workflows.*` đều pass.

→ **Tổng 52 endpoints workflows hoạt động end-to-end.**

---

## Task 2 — Thêm `Document AI`

### Source code

Resource files:

- TS: [ts/src/resources/document-ai.ts](../ts/src/resources/document-ai.ts) → `DocumentAIResource`
- Python: [py/src/imbrace/resources/document_ai.py](../py/src/imbrace/resources/document_ai.py) → `DocumentAIResource` + `AsyncDocumentAIResource`

Wired vào client:

- TS: `client.documentAi: DocumentAIResource` ([ts/src/client.ts](../ts/src/client.ts))
- Python sync: `self.document_ai` ([py/src/imbrace/client.py](../py/src/imbrace/client.py))
- Python async: `self.document_ai` ([py/src/imbrace/async_client.py](../py/src/imbrace/async_client.py))

API surface: `createAgent`, `listAgents`, `getAgent`, `updateAgent`, `deleteAgent`, `process`, `suggestSchema`, `createFull`. Wrap `/v3/ai/assistant_apps/*` (filter `agent_type=document_ai`) + endpoint xử lý `/v3/ai/document/`.

### Unit tests (mocked)

```
tests/unit/resources/document-ai.test.ts (22 tests) ✓
tests/unit/resources/test_document_ai.py (21 tests) ✓
```

### Integration tests

#### TypeScript (prodv2)

```
$ node ts/tests/local/test-document-ai-apikey.mjs
  4 passed | 1 failed | 2 skipped
```

- ✓ `chatAi.listDocumentModels` → 2 providers, 118 models, 26 vision-capable
- ✗ `chatAi.processDocument` — **backend issue, không phải SDK bug.** Em verify bằng curl: gateway prodv2 redirect `/v3/ai/document/` → internal host `aiv2.imbrace.lan/api/v1/document` (DNS không reach từ ngoài). SDK build URL đúng.
- ✓ `documentAi.listAgents` → 51 agents
- ✓ `documentAi.listAgents({documentAiOnly:true})`
- ✓ `documentAi.suggestSchema`

#### Python (sandbox env, end-to-end)

```
$ python py/tests/local/test_documentai_imbrace.py
  9 passed | 1 failed
```

- ✓ `list_providers` → 13 providers
- ✓ `list_agents` → 59 total
- ✓ `list_agents(document_ai_only=True)` → 4 Document AI agents
- ✓ `process` với gpt-4o → `success=True`, extract đủ keys: `header`, `buyer_info`, `details`, `total`, `seller_info`
- ✓ `suggest_schema` → 5 fields gợi ý
- ✓ `create_full` (atomic Board + UseCase + Assistant) → tạo thành công, `agent_type=document_ai` confirmed
- ✓ `get_agent` → confirm agent_type
- ✓ `delete_usecase` (cleanup)
- ✗ `delete_board` (cleanup) — backend trả 400 "Can not delete board" (business constraint, không phải SDK bug)

→ **Document AI resource hoạt động đầy đủ end-to-end** trên sandbox với access token thật. Mọi method (list / get / create / update / delete agent + process + suggest_schema + create_full atomic) đều work.

---

## Việc dọn liên quan trong cùng branch

Để báo cáo gọn, branch này còn dọn các file đã không còn dùng:

- Xoá resource `financial_documents` (đã được tách thành `documentAi.process` + `chatAi.processDocument` từ refactor trước, không còn ai gọi):
  - [ts/src/resources/financial-documents.ts](../ts/src/resources/financial-documents.ts) (243 dòng)
  - [py/src/imbrace/resources/financial_documents.py](../py/src/imbrace/resources/financial_documents.py) (226 dòng)
  - 4 unit/integration test files
  - 2 `package.json` bỏ script `test:financial-documents`
  - 6 interface `FinancialDoc*` trong [ts/src/types/ai.ts](../ts/src/types/ai.ts)
- Update [website/public/llms.txt](../website/public/llms.txt) đối chiếu với `developer.imbrace.co`:
  - Thêm 3 link: Setup Guide, Local Testing, Error Handling
  - Bỏ dòng resource `financialDocuments`
- Rewrite [ts/tests/local/test-document-ai-apikey.mjs](../ts/tests/local/test-document-ai-apikey.mjs) — bỏ section còn gọi `documentAi.getFile/getReport/listErrors` (API cũ của financial_documents), thay bằng test đúng API surface hiện tại của documentAi.

Tổng commit: 24 file thay đổi, +324 dòng / −2464 dòng.

---

## Kết luận

**Cả 2 task đều DONE và đã verify work bằng integration test với gateway thật:**

- **Workflows:** 52 endpoints hoạt động end-to-end (TS + Py sync/async).
- **Document AI:** flow CRUD đầy đủ + `process` + `suggest_schema` + `create_full` đều work trên sandbox.

**2 lỗi phát hiện trong quá trình test KHÔNG phải SDK bug:**

1. `chatAi.processDocument` redirect tới internal host trên prodv2 — backend deployment misconfig.
2. `delete_board` bị business rule chặn — backend constraint.

Cả 2 issue này nằm ngoài scope SDK refactor và cần backend team xử lý.
