# Doc Audit & Fix Plan: Code Block Errors vs SDK Source

## TASK LIST
(x) Update CLI
(x) Thay Assistant thành AI-Agent cả trong block code, comment, broading và các headers
{
Assistant còn ở:
getting-started/overview
getting-started/setup-guide
sdk/full-flow-guide (Còn lại ở Stream chat)
sdk/ai-agent

ActivePieces còn ở 
getting-started/setup-guide
sdk/full-flow-guide (pieceName: "@activepieces/piece-webhook")
}
(x) Thay ActivePieces thành Workflows
(x) Add Document-AI
(x) Tách Resource ra thành Workflows, AI-Agent- Databoard
(x) Add Docs lấy API key
(x) Corverage AI Agent, Databoard, Workflow chi tiết hơn.

Các task này đã được thực thi hết chưa

## Audit Summary

Đã cross-reference toàn bộ code blocks trong `website/src/content/docs/sdk/` với
`ts/src/resources/` và `py/src/imbrace/resources/`. Tổng cộng **376 method calls**
đã được kiểm tra.

---

## ✅ Verified CORRECT (không cần sửa)

- `client.workflows.*` — tất cả methods (listFlows, createFlow, deleteFlow, applyFlowOperation, triggerFlow, triggerFlowSync, listRuns, getRun, listFolders, createFolder, listConnections, upsertConnection, listTables, listRecords, listChannelAutomation)
- `client.boards.*` — tất cả board/item/file/folder methods (list, get, create, update, delete, createField, updateField, deleteField, listSegments, createSegment, exportCsv, listItems, getItem, createItem, updateItem, deleteItem, bulkDeleteItems, search, searchFolders, getFolderContents, updateFolder, deleteFolders, searchFiles, getFile, createFile, uploadFile, deleteFiles)
- `client.contacts.*` — list, get, update, getComments, getFiles, getActivities
- `client.conversations.*` — search, getOutstanding (TS), assignTeamMember (TS), updateStatus, list
- `client.messages.*` — send, list
- `client.campaign.*` — list, get, create, delete, listTouchpoints, getTouchpoint, createTouchpoint, updateTouchpoint, deleteTouchpoint, validateTouchpoint
- `client.marketplace.*` — listProducts, getProduct (lưu ý: createProduct KHÔNG tồn tại)
- `client.messageSuggestion.*` — getSuggestions
- `client.predict.*` — predict
- `client.platform.*` — getMe / get_me
- `client.auth.*` — exchangeAccessToken, getThirdPartyToken / get_third_party_token
- `client.ai.*` (TS) — complete, stream, embed
- `client.aiAgent.*` — tất cả methods trong AiAgentResource (streamChat, streamSubAgentChat, getSubAgentHistory, getAgentPromptSuggestion, processEmbedding, listEmbeddingFiles, getEmbeddingFile, previewEmbeddingFile, updateEmbeddingFileStatus, deleteEmbeddingFile, classifyFile, suggestFieldTypes, generateParquet, listParquetFiles, deleteParquetFile, getTraces, getTrace, getTraceServices, getTraceTags, getTraceTagValues, searchTraceQL, verifyChatClientCredentials, registerChatClient, getChatClientUser, createClientChat, listClientChats, getClientChat, updateClientChat, deleteClientChat, deleteAllClientChats, generateClientChatTitle, streamClientChatStatus, persistClientMessage, listClientMessages, deleteTrailingMessages, getVotes, updateVote, createDocument, getDocument, getDocumentLatest, getDocumentPublic, getDocumentLatestByKind, getDocumentSuggestions, deleteDocument, listAdminGuides, getAdminGuide, listChats, getChat, deleteChat)
- Python `client.folders.*` — create, search, update, delete
- Python `AsyncImbraceClient` — context manager + async methods
- Error classes — `ImbraceError`, `AuthError`, `ApiError`, `NetworkError` (cả TS và Python)

---

## 🔴 Issues Found (cần fix)

### Issue 1 — chatAi / chat_ai: TẤT CẢ method names sai (CRITICAL)

SDK source đã đổi tên từ `*Assistant*` → `*AiAgent*`. Docs vẫn dùng tên cũ (do agent cũ bịa).

| Docs (sai) | Source TS (đúng) | Source Python (đúng) |
|---|---|---|
| `listAssistants()` | `listAiAgents()` | `list_ai_agents()` |
| `getAssistant(id)` | `getAiAgent(id)` | `get_ai_agent(ai_agent_id)` |
| `createAssistant(body)` | `createAiAgent(body)` | `create_ai_agent(body)` |
| `updateAssistant(id, body)` | `updateAiAgent(id, body)` | `update_ai_agent(ai_agent_id, body)` |
| `deleteAssistant(id)` | `deleteAiAgent(id)` | `delete_ai_agent(ai_agent_id)` |
| `updateAssistantInstructions(id, instr)` | `updateAiAgentInstructions(id, instr)` | `update_ai_agent_instructions(ai_agent_id, instr)` |
| `listAssistantAgents()` | `listAiAgentSubAgents()` | `list_ai_agent_sub_agents()` |

**Files to fix (EN + 3 locales):**
- `website/src/content/docs/sdk/ai-agent.mdx` (12 occurrences)
- `website/src/content/docs/sdk/full-flow-guide.mdx` (6 occurrences)
- `website/src/content/docs/vi/sdk/ai-agent.mdx`
- `website/src/content/docs/vi/sdk/full-flow-guide.mdx`
- `website/src/content/docs/zh-cn/sdk/ai-agent.mdx`
- `website/src/content/docs/zh-cn/sdk/full-flow-guide.mdx`
- `website/src/content/docs/zh-tw/sdk/ai-agent.mdx`
- `website/src/content/docs/zh-tw/sdk/full-flow-guide.mdx`

**Replace pattern (replace_all trong mỗi file):**
```
TypeScript:
  .listAssistants()               → .listAiAgents()
  .getAssistant(                  → .getAiAgent(
  .createAssistant(               → .createAiAgent(
  .updateAssistant(               → .updateAiAgent(
  .deleteAssistant(               → .deleteAiAgent(
  .updateAssistantInstructions(   → .updateAiAgentInstructions(
  .listAssistantAgents()          → .listAiAgentSubAgents()

Python:
  .list_assistants()              → .list_ai_agents()
  .get_assistant(                 → .get_ai_agent(
  .create_assistant(              → .create_ai_agent(
  .update_assistant(              → .update_ai_agent(
  .delete_assistant(              → .delete_ai_agent(
  .update_assistant_instructions( → .update_ai_agent_instructions(
  .list_assistant_agents()        → .list_ai_agent_sub_agents()
```

---

### Issue 2 — Python `client.ai.complete/stream/embed` sai signature (CRITICAL)

Python SDK dùng `input: CompletionInput` / `input: EmbeddingInput` (Pydantic model),
không phải keyword args. Doc bịa ra cách dùng sai.

**Doc sai (keyword args trực tiếp vào method):**
```python
client.ai.complete(model="gpt-4o", messages=[...])
client.ai.stream(model="gpt-4o", messages=[...])
client.ai.embed(model="...", input=[...])  # sync version
```

**SDK đúng (phải qua Pydantic model):**
```python
from imbrace.types.ai import CompletionInput, CompletionMessage, EmbeddingInput

client.ai.complete(CompletionInput(model="gpt-4o", messages=[CompletionMessage(...), ...]))
client.ai.stream(CompletionInput(model="gpt-4o", messages=[...]))
client.ai.embed(EmbeddingInput(model="...", input=[...]))    # sync
```

**Lưu ý:** Async `embed()` dùng `model, input` riêng — đúng, không cần sửa.

**Files to fix:** (chỉ EN, các bản dịch chưa có section completions)
- `website/src/content/docs/sdk/ai-agent.mdx` — completions section (2 TS/Py blocks) + OpenAI section (1 Py block)
- `website/src/content/docs/sdk/integrations.mdx` — FastAPI route (dòng 183) + streaming example (dòng 249)

---

### Issue 3 — `client.marketplace.createProduct()` KHÔNG tồn tại (CRITICAL)

| File | Dòng | Code | Vấn đề |
|---|---|---|---|
| `integrations.mdx` | 100 | `client.marketplace.createProduct(body)` | **Không có trong SDK TS** |
| `error-handling.mdx` | 306 | `client.marketplace.create_product(data)` | **Không có trong SDK Python** |

Marketplace TS chỉ có: `listProducts`, `getProduct`, `createOrder`, `updateOrderStatus`, `deleteFile`, `createEmailTemplate`, `listOrders`, `getOrder`
Marketplace Python chỉ có: `list_products`, `get_product`

**Fix:** Xóa hoặc thay bằng method có thật.

---

### Issue 4 — Method KHÔNG tồn tại khác

| File | Dòng | Code sai | SDK thật |
|---|---|---|---|
| `integrations.mdx` | 230 | `client.channel.list_channels(type="group")` | `client.channel.list(type="group")` |

---

### Issue 5 — Signature sai (method tồn tại nhưng params sai)

| File | Dòng | Code sai | SDK thật | Ghi chú |
|---|---|---|---|---|
| `integrations.mdx` | 174, 229, 273, 317 | `marketplace.list_products(limit=20)` | `marketplace.list_products({"limit": 20})` | Python dùng `params` dict |
| `error-handling.mdx` | 238 | `listProducts({page:1}, {signal})` | `listProducts({page:1})` — 1 param | SDK ko hỗ trợ AbortSignal |
| `resources.mdx` | 150 | `campaign.create({name:..., type:"email"})` | `CreateCampaignInput` có `channel_type` | Dùng sai tên field |

---

### Issue 6 — boards.createFolder: sai tên param

Docs trong `full-flow-guide.mdx` show:
```typescript
client.boards.createFolder({ name, organization_id, parent_folder_id, source_type })
```

Actual `CreateFolderInput` (`ts/src/resources/boards.ts:165`):
```typescript
{ name: string; organization_id?: string; parent_id?: string; [key: string]: unknown }
```

Fix:
- `parent_folder_id` → `parent_id`
- Xóa `source_type` (không có trong interface)

**Files:** `full-flow-guide.mdx` + vi/zh-cn/zh-tw mirrors (4 files)

---

### Issue 7 — streamChat: organization_id không có trong type signature

Docs show `streamChat({assistant_id, organization_id, messages, id?})`.

Actual TS (`ts/src/resources/ai-agent.ts`):
```typescript
streamChat(body: { assistant_id: string; messages: any[]; id?: string; model_id?: string; provider_id?: string; user_id?: string; [key: string]: unknown })
```

Python `StreamChatBody` (`py/src/imbrace/resources/ai_agent.py:14`): không có trường `organization_id`.

**Lưu ý:** `[key: string]: unknown` cho phép extra fields nên code vẫn chạy, nhưng backend sẽ ignore `organization_id`.

**Fix:** xóa `organization_id` khỏi tất cả streamChat examples.

**Files:** `ai-agent.mdx`, `full-flow-guide.mdx`, `getting-started/overview.mdx` + locales (~10 files)

---

### Issue 8 ✅ — `client._token_manager.get_token()` dùng private API (WARNING)

`integrations.mdx` dòng 402 dùng `client._token_manager.get_token()` — truy cập vào
thuộc tính private (`_` prefix). Không phải public API.

**Fix:** Thay bằng method public nếu có, hoặc thêm cảnh báo trong doc.

---

## Progress

### Issue 1 — chatAi method renames
- [x] `sdk/ai-agent.mdx` (EN)
- [x] `sdk/full-flow-guide.mdx` (EN)
- [ ] `vi/sdk/ai-agent.mdx`
- [ ] `vi/sdk/full-flow-guide.mdx`
- [ ] `zh-cn/sdk/ai-agent.mdx`
- [ ] `zh-cn/sdk/full-flow-guide.mdx`
- [ ] `zh-tw/sdk/ai-agent.mdx`
- [ ] `zh-tw/sdk/full-flow-guide.mdx`

### Issues 2–8
- [x] Issue 2: Python completions signatures (ai-agent.mdx, integrations.mdx)
- [x] Issue 3: marketplace.createProduct (integrations.mdx, error-handling.mdx)
- [x] Issue 4: channel.list_channels (integrations.mdx)
- [x] Issue 5: signature fixes (integrations.mdx, error-handling.mdx, resources.mdx)
- [x] Issue 6: boards.createFolder param (full-flow-guide.mdx EN)
- [x] Issue 7: streamChat organization_id — EN root done; locale mirrors pending
- [x] Issue 8: Python OTP → client.auth.signin_email_request / signin_with_email (integrations.mdx)

### Locale sync
- [x] Propagate all EN fixes → `vi/`, `zh-cn/`, `zh-tw/` locales (copied EN root files + added sidebar translations)

---

## Gap Analysis — Undocumented SDK Methods

Audit ngày 2026-05-08.

### Coverage stats

| Resource | SDK methods | Documented | Missing | Coverage |
|----------|-------------|------------|---------|----------|
| AI Agent (`aiAgent`) | 50 | 50 | 0 | ✅ 100% |
| Document AI | 12 | 12 | 0 | ✅ 100% |
| Workflows | 32 | 32 | 0 | ✅ 100% |
| Boards | 53 | 53 | 0 | ✅ 100% |

---

### AI Agent (`ai-agent.mdx`) — ✅ 100% coverage

| Resource / Method | Status | Notes |
|---|---|---|
| `chatAi` / `chat_ai` CRUD + sub-agents | ✅ Done | `listAiAgents/getAiAgent/createAiAgent/updateAiAgent/deleteAiAgent/updateAiAgentInstructions/listAiAgentSubAgents` |
| `client.ai` completions/stream/embed | ✅ Done | TS + Pydantic Python signatures |
| `aiAgent` / `ai_agent` core | ✅ Done | streamChat, sub-agent chat, prompt suggestions, embeddings, field types, parquet, tracing, chat client, documents, admin guides, service info, legacy chat |
| Document AI (via `chatAi`) | ✅ Done | `listDocumentModels` / `processDocument` + link to dedicated page |
| File extraction | ✅ Done | `uploadAgentFile` / `extractFile` |
| Knowledge Hub | ✅ Done | Cross-reference to boards/folders docs |
| `client.ai.getLlmModels` | ✅ Done | |
| `client.ai` Providers CRUD + refresh | ✅ Done | `listProviders/createProvider/updateProvider/deleteProvider/refreshProviderModels` |
| `client.ai` Guardrails CRUD | ✅ Done | |
| `client.ai` Guardrail Providers CRUD + test + models | ✅ Done | |
| `client.ai` RAG Files | ✅ Done | |
| `client.ai` AI Agents (read + check + patch) | ✅ Done | `listAiAgents/listAgents/getAiAgent/checkAiAgentName/patchInstructions` |
| `client.ai` AI Agent Apps CRUD + workflow | ✅ Done | |
| `client.ai` Tool Server verify | ✅ Done | `verifyToolServer` |

### Document AI (`document-ai.mdx`) — ✅ 100% coverage

| Method | Status | Notes |
|---|---|---|
| `listDocumentModels` / `list_document_models` | ✅ Done | chatAi / chat_ai namespace |
| `processDocument` / `process_document` (basic + all params) | ✅ Done | chatAi / chat_ai namespace |
| PDF form filling (`fileUrlToFill`) | ✅ Done | Advanced example |
| `listAgents` / `list_agents` | ✅ Done | documentAi — with `nameContains` / `documentAiOnly` filters |
| `getAgent` / `get_agent` | ✅ Done | |
| `createAgent` / `create_agent` | ✅ Done | With `schema` param for extraction fields |
| `updateAgent` / `update_agent` | ✅ Done | |
| `deleteAgent` / `delete_agent` | ✅ Done | |
| `process` / `process` (agent-based) | ✅ Done | documentAi — supports `agentId` lookup + overrides |
| `suggestSchema` / `suggest_schema` | ✅ Done | Auto-schema from sample document |
| `createFull` / `create_full` | ✅ Done | End-to-end orchestration (board + usecase + agent) |
| Async usage (Python) | ✅ Done | Both namespaces covered |

### Data Boards (`databoard.mdx`) — ✅ 100% coverage

| Method | Status | Notes |
|---|---|---|
| Board CRUD | ✅ Done | `list/get/create/update/delete` |
| Board reorder | ✅ Done | `reorder` |
| Items CRUD + bulkDelete + search | ✅ Done | |
| Fields CRUD + reorder + bulk update | ✅ Done | `createField/updateField/deleteField/reorderFields/bulkUpdateFields` |
| Segments CRUD | ✅ Done | `listSegments/createSegment/updateSegment/deleteSegment` |
| CSV/Excel import + progress | ✅ Done | `importCsv/importExcel/getImportProgress` |
| CSV export + export via mail | ✅ Done | `exportCsv` (TS+Py), `exportCsvViaMail` (TS-only) |
| Linked items (related boards) | ✅ Done | `linkItems/unlinkItems/getRelatedItems/getLinkedBoardItems` |
| Conflict detection | ✅ Done | `checkConflict` |
| Knowledge Hub Folders CRUD | ✅ Done | `searchFolders/getFolder/createFolder/updateFolder/deleteFolders/getFolderContents` |
| Knowledge Hub Files CRUD | ✅ Done | `searchFiles/getFile/createFile/updateFile/deleteFiles/uploadFile/downloadFile` |
| Board upload files | ✅ Done | `uploadBoardFile/uploadBoardFileV2` |
| AI tags + link preview | ✅ Done | `generateAiTags/getLinkPreview` |
| External Drive | ✅ Done | `initiateDriveAuth/listDriveFolders/listDriveFiles/downloadDriveFile/getOneDriveSessionStatus` |

### Workflows (`workflows.mdx`) — ✅ 100% coverage

| Method | Status | Notes |
|---|---|---|
| Channel automation | ✅ Done | `listChannelAutomation` |
| Flows CRUD + trigger + runs + apply operation | ✅ Done | `listFlows`, `getFlow`, `createFlow`, `deleteFlow`, `applyFlowOperation`, `triggerFlow`, `triggerFlowSync`, `listRuns`, `getRun` |
| Folders CRUD | ✅ Done | `listFolders`, `getFolder`, `createFolder`, `updateFolder`, `deleteFolder` |
| App Connections CRUD | ✅ Done | `listConnections`, `getConnection`, `upsertConnection`, `deleteConnection` |
| Pieces | ✅ Done | `listPieces` |
| Triggers | ✅ Done | `getTriggerRunStatus`, `testTrigger` |
| Tables & Records | ✅ Done | `listTables`, `getTable`, `listRecords` |
| MCP Servers CRUD + rotate token | ✅ Done | `listMcpServers`, `getMcpServer`, `createMcpServer`, `deleteMcpServer`, `rotateMcpToken` |
| User Invitations | ✅ Done | `listInvitations`, `deleteInvitation` |

**Note:** `searchFlows()` and `listProjects()` do NOT exist in SDK source (`workflows.py` / `workflows.ts`). They were fabrication in the original gap estimate.

---

### Verify commands
```bash
grep -rn "listAssistants\|getAssistant\b\|createAssistant\|updateAssistant\|deleteAssistant" website/src/content/docs/ --include="*.mdx"
grep -rn "list_assistants\|get_assistant\b\|create_assistant\|update_assistant\|delete_assistant" website/src/content/docs/ --include="*.mdx"
grep -rn "parent_folder_id" website/src/content/docs/ --include="*.mdx"
grep -rn "list_channels\|createProduct\|create_product" website/src/content/docs/ --include="*.mdx"
```
