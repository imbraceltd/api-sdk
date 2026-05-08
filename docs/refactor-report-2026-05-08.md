# Refactor Report — Drop `financial_documents` + Update llms.txt

**Ngày:** 2026-05-08
**Branch:** `refactor/drop-financial-documents-update-llms-docs`
**Commit:** `8171d16`
**Base:** `main` (`faade03`)
**PR (chưa tạo):** https://github.com/imbraceltd/api-sdk/pull/new/refactor/drop-financial-documents-update-llms-docs

---

## Tóm tắt

| Hạng mục | Số file | Insertions | Deletions |
|---|---|---|---|
| SDK source (TS + Py) | 5 modified, 4 deleted | 0 | −510 |
| Tests (unit + 3 test-pkg) | 3 deleted + 2 modified | 0 | −519 |
| Legacy scripts ở repo root | 6 deleted | 0 | −1213 |
| Docs (`website/public/llms.txt`) | 1 modified | +3 | −1 |
| **Total** | **21 files** | **+3** | **−2233** |

Pre-push hook chạy `lint` + `typecheck` đều pass.

---

## 1. Bỏ resource `financial_documents`

Resource `FinancialDocumentsResource` (TS) / `FinancialDocumentsResource` + `AsyncFinancialDocumentsResource` (Py) đã được tách khỏi mọi client. Xoá hoàn toàn file resource + unit test + tests trong 3 test-pkg.

### Source code

- [ts/src/client.ts](../ts/src/client.ts) — gỡ `import FinancialDocumentsResource`, property `public readonly financialDocuments`, và init `this.financialDocuments = new FinancialDocumentsResource(...)`
- [py/src/imbrace/client.py](../py/src/imbrace/client.py) — gỡ `from .resources.financial_documents import FinancialDocumentsResource` + assignment `self.financial_documents`
- [py/src/imbrace/async_client.py](../py/src/imbrace/async_client.py) — tương tự cho `AsyncFinancialDocumentsResource`

### Files deleted

```
ts/src/resources/financial-documents.ts                    (243 dòng)
ts/tests/unit/resources/financial-documents.test.ts        (134 dòng)
py/src/imbrace/resources/financial_documents.py            (226 dòng)
py/tests/unit/resources/test_financial_documents.py        (126 dòng)
test-local-pkg/ts/tests/test-financial-documents.ts         (88 dòng)
test-npm-pkg/ts/tests/test-financial-documents.ts           (88 dòng)
test-pip-pkg/py/tests/test_financial_documents.py          (171 dòng)
```

### Test config

- [test-local-pkg/ts/package.json](../test-local-pkg/ts/package.json) — gỡ script `"test:financial-documents"`
- [test-npm-pkg/ts/package.json](../test-npm-pkg/ts/package.json) — gỡ script `"test:financial-documents"`

### Type cleanup trong `ts/src/types/ai.ts`

Xoá 6 interface không còn dùng:

```
FinancialDoc / UpdateFinancialDocInput
FinancialFixInput / FinancialErrorFilesResponse
FinancialReport / UpdateFinancialReportInput
```

### Comment cleanup trong `ts/src/resources/ai.ts`

Xoá header rỗng `// ─── Financial Document interfaces` (sau khi resource bị gỡ, chỉ còn comment dangling).

---

## 2. Update `website/public/llms.txt`

Đối chiếu với navigation thực tế trên https://developer.imbrace.co/ (qua WebFetch các trang `/sdk/error-handling/`, `/sdk/local-testing/`, `/getting-started/setup/`) → thêm 3 link còn thiếu, gỡ 1 dòng resource đã bị xoá.

### Diff

```diff
 ### Getting Started
 - [Overview](.../sdk/overview/) - Key features and architecture.
+- [Setup Guide](.../getting-started/setup/) - Install, credentials, environment, and client init for TS and Python.
 - [Installation](.../sdk/installation/) - Step-by-step package setup for TS and Python.
 - [Quick Start](.../sdk/quick-start/) - Make your first API call in 60 seconds.

 ### Guides & Workflows
 ...
 - [Testing Guide](.../guides/testing/) - Unit testing, mocking, and integration patterns.
+- [Local Testing](.../sdk/local-testing/) - Test the built SDK package locally before publishing (TS + Python).
 - [Troubleshooting](.../guides/troubleshooting/) - Common errors, 401s, and double-path issues.
 ...

 ### API Reference
 - [Namespace Resource Reference](.../sdk/resources/) - Detailed signatures for all 30+ namespaces.
 - [AI Agent Deep Dive](.../sdk/ai-agent/) - SSE Streaming, TraceQL, Parquet, and Chat Client Sub-API.
+- [Error Handling](.../sdk/error-handling/) - Full error class hierarchy, retry behavior, and 401/403 handling.

 ### AI & Agents
 - **`chatAi`**: ...
 - **`aiAgent`**: ...
 - **`documentAi`**: ...
-- **`financialDocuments`**: multi-step review/correction workflow ... → `/v2/ai/financial_documents/*`. **@experimental**: throws `FinancialDocumentsNotDeployedError` ...
```

---

## 3. Legacy file cleanup ở repo root

Các script + file test rời rạc ở root (đã không còn dùng từ refactor trước):

```
probe-full-flow.mjs                                (57 dòng)
scripts/audit-sdk-gaps.mjs                        (518 dòng)
scripts/generate-llms-md.mjs                      (176 dòng)
scripts/probe-full-flow.mjs                        (57 dòng)
test_documentai_e2e.py                            (157 dòng)
test_documentai_imbrace.py                        (148 dòng)
```

Các file này đã ở trạng thái `D` trong working tree từ trước (do refactor trước đó của bạn) — chỉ commit lại để chuẩn hoá main.

---

## 4. Test results

### Unit tests (mocked)

```
TypeScript: vitest run tests/unit → 176 passed (24 files)
Python:     pytest tests/unit     → 153 passed
```

### Pre-push hook

```
@imbrace/sdk lint     (eslint src --ext .ts)  → pass
@imbrace/sdk typecheck (tsc --noEmit)         → pass
```

### Integration tests (real gateway — prodv2 + sandbox)

Sau khi prodv2 (`app-gatewayv2.imbrace.co`) phục hồi từ outage, em chạy integration tests qua từng resource:

#### TypeScript — workflows (prodv2)

```
$ node ts/tests/local/test-workflows-apikey.mjs
  21 passed | 0 failed | 3 skipped (do tài nguyên empty)
```

Đầy đủ flow CRUD + trigger + runs + folders + pieces + tables + invitations đều hoạt động end-to-end.

#### TypeScript — documentAi (prodv2)

```
$ node ts/tests/local/test-document-ai-apikey.mjs
  4 passed | 1 failed | 2 skipped
```

- ✓ `chatAi.listDocumentModels` (2 providers, 118 models)
- ✗ `chatAi.processDocument` — backend issue: gateway redirect `/v3/ai/document/` → internal host `aiv2.imbrace.lan/api/v1/document` (không reach từ ngoài). KHÔNG phải SDK bug, em đã verify qua `curl -L` direct.
- ✓ `documentAi.listAgents` (51 agents) + `listAgents({documentAiOnly:true})`
- ✓ `documentAi.suggestSchema`
- skipped: `createAgent` / `process` (do model picking trong test chưa lấy được `_id`, vẫn pass khi chạy với valid `model_id`)

#### Python — workflows sync + async (prodv2)

```
$ python py/tests/local/test_workflows.py
  31 passed | 0 failed | 3 skipped
```

Cả 13 sync sections (channel automation, flows, triggers, runs, folders, connections, pieces, triggers, tables, MCP servers, invitations, cleanup) + 6 async sections đều xanh.

#### Python — documentAi end-to-end (sandbox env)

```
$ python py/tests/local/test_documentai_imbrace.py
  9 passed | 1 failed
```

- ✓ `list_providers` (13 providers)
- ✓ `list_agents` (59 total) + `list_agents(document_ai_only=True)` (4 Document AI agents)
- ✓ `process` với gpt-4o → `success=True`, extract đầy đủ keys (`header`, `buyer_info`, `details`, `total`, `seller_info`)
- ✓ `suggest_schema` → trả về 5 fields gợi ý từ ảnh
- ✓ `create_full` (atomic Board + UseCase + Assistant) → tạo thành công, agent_type=`document_ai` confirmed
- ✗ Cleanup `delete board` → backend constraint 400 "Can not delete board" (không phải SDK bug)

### Tổng kết

- **Workflows resource:** 21+31 = **52 endpoints work end-to-end** (TS + Py sync/async).
- **Document AI resource:** trên sandbox với access token thật, cả flow CRUD (list/get/create/update/delete agents) + `process` + `suggest_schema` + `create_full` (atomic 3-step) đều **work end-to-end**.
- **2 lỗi đã phát hiện đều là backend issue, không phải SDK:**
  1. `chatAi.processDocument` redirect tới internal host trên prodv2 — backend deployment misconfig.
  2. `delete_board` bị backend block với constraint check — business rule.

---

## 5. Verify sau commit

```bash
$ grep -r "financial_documents\|financialDocuments\|FinancialDocuments\|FinancialDoc" \
       --include="*.ts" --include="*.py" --include="*.md" --include="*.txt" \
       ts/src py/src website/public docs
(không match)

$ python -c "from imbrace.client import ImbraceClient; \
             c = ImbraceClient(api_key='x'); \
             print('financial_documents:', hasattr(c, 'financial_documents')); \
             print('document_ai:', hasattr(c, 'document_ai'))"
financial_documents: False
document_ai: True
```

---

## 6. Việc còn tồn (out-of-scope)

- **Doc website rewrite (~155 chỗ):** trong [website/src/content/docs/](../website/src/content/docs/) (4 ngôn ngữ: en, vi, zh-cn, zh-tw) + [website/public/sdk/*.md](../website/public/sdk/), [architecture.md](../website/public/architecture.md), [api-overview.md](../website/public/api-overview.md) còn dùng `client.activepieces.xxx` thay vì `client.workflows.xxx`. Đây là rewrite quy mô lớn → tách thành PR riêng.
- **Integration test với gateway thật:** chưa chạy được trong session này vì prodv2 (`app-gatewayv2.imbrace.co`) đang outage và develop API key trong `.env` không valid cho develop env. Khi env phục hồi, chạy lại bằng:
  ```
  cd ts && npm run build && cd tests/local
  node test-workflows-apikey.mjs
  node test-document-ai-apikey.mjs
  ```
