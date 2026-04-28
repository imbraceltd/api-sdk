# Imbrace TypeScript SDK — Local Integration Test Suite

Bộ kiểm thử tích hợp cho **@imbrace/sdk** (TypeScript), cài đặt từ file đóng gói cục bộ `.tgz` trước khi publish lên NPM.

---

## 1. Thiết lập

### Yêu cầu

- Node.js v18+
- npm

### Cấu hình `.env`

Copy `.env.example` thành `.env`:

```env
IMBRACE_ACCESS_TOKEN=your_access_token_here
# hoặc dùng API Key:
# IMBRACE_API_KEY=your_api_key_here

IMBRACE_ORGANIZATION_ID=your_org_id_here
IMBRACE_GATEWAY_URL=https://app-gatewayv2.imbrace.co
```

### Cài đặt

```bash
npm install
```

> SDK được cài từ file cục bộ: `file:../../ts/imbrace-sdk-x.x.x.tgz`

**Build cho sdk/ts.**

```bash
npm run build
```

---

## 2. Chạy Test

### ⭐ Full Flow Guide (Ưu tiên cao nhất)

Kiểm tra toàn bộ 4 luồng nghiệp vụ chính end-to-end:

```bash
npm run test:full-flow
```

**Phủ:** Assistant CRUD → Activepieces Flow (tạo + bind) → Knowledge Hub RAG → Board & Items → Cleanup

---

### 🚀 Chạy toàn bộ Test Suite

```bash
npm run test:all
```

> Chạy tuần tự 15 module. Nếu một module gặp lỗi 502/404 từ backend, hệ thống ghi nhận và chạy tiếp.

---

### 🧩 Danh sách đầy đủ các module

| Lệnh                         | Module          | Mô tả                                                                                                     | Trạng thái |
| ----------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------- | ------------ |
| `npm run test:ai`           | AI Agent        | Health, Chat v1/v2 SSE, getChat/deleteChat, Embeddings, Parquet, Sub-agent, Tracing, Documents, Chat Client | ✅           |
| `npm run test:chat-ai`      | Chat AI         | Assistants CRUD, completions, listModels, uploadFile, extractFile, Knowledge, Folders                       | ✅           |
| `npm run test:boards`       | Boards          | CRUD bảng, fields, items, bulkDelete, search, segments, exportCsv, Folders, uploadFile, searchFiles        | ✅           |
| `npm run test:activepieces` | Activepieces    | Flows, Runs, Folders, Connections, Tables, listPieces, listMcpServers                                       | ✅           |
| `npm run test:crm`          | CRM             | Contacts (list/get/update/activity), Conversations (search/assign/status), Messages (send/list), Channel    | ✅           |
| `npm run test:crm-advanced` | CRM Advanced    | Activities, Comments, Board-contact linking                                                                 | ✅           |
| `npm run test:frontend`     | Frontend SDK    | Chat Client auth, chats CRUD, messages, votes, documents, streaming                                         | ✅           |
| `npm run test:multi-agent`  | Multi-Agent     | Sub-agent streaming, getSubAgentHistory, Parquet, multi-turn context                                        | ✅           |
| `npm run test:multimedia`   | Multimedia AI   | OCR (extractFile), STT (transcribe), TTS (speech), Document AI                                              | ✅           |
| `npm run test:agent`        | Agent           | Agent templates và runs                                                                                    | ✅           |
| `npm run test:marketplace`  | Marketplace     | listProducts, listUseCaseTemplates                                                                          | ✅           |
| `npm run test:platform`     | Platform        | getMe, listUsers, getOrganization, listTeams                                                                | ⚠️ 502     |
| `npm run test:settings`     | Settings        | Message templates, WA templates                                                                             | ✅           |
| `npm run test:error-paths`  | Error Paths     | Xác thực xử lý lỗi: AuthError, ApiError, NetworkError                                                  | ✅           |
| `npm run test:full-flow`    | Full Flow Guide | ⭐ E2E: Assistant → Flow → RAG → Board                                                                   | ✅           |

> **Ghi chú ⚠️ 502:** `platform.getMe` đang bị 502 từ backend prodv2. Module vẫn chạy nhưng section này sẽ bị skip tự động.

---

### 🧩 Chạy theo nhóm

```bash
# AI group
npm run test:ai && npm run test:chat-ai

# CRM + Boards group
npm run test:crm && npm run test:boards && npm run test:crm-advanced

# Workflow group
npm run test:activepieces && npm run test:multi-agent

# Frontend group
npm run test:frontend && npm run test:multimedia
```

---

## 3. Tình trạng Backend (prodv2)

| Trạng thái           | Dịch vụ                                                                                                             |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------- |
| ✅ Hoạt động        | `chatAi`, `aiAgent`, `activepieces`, `boards`, `marketplace`, `auth`, `crm`, `messages`, `settings` |
| ⚠️ 502 (down)        | `platform.getMe`, `channel`, `account` — Chờ backend team khôi phục                                         |
| 🔴 404 (route missing) | `sessions`, `marketplace.orders`, `aiAgent v3/` routes                                                          |

---

## 4. Cấu trúc thư mục

```
test-local-pkg/ts/
├── .env                        # Config cục bộ (không commit)
├── .env.example                # Template
├── package.json                # npm scripts
├── tsconfig.json
├── utils/
│   └── utils.ts                # Client init, runTestSection, logResult
└── tests/
    ├── test-all.ts             # ▶ Runner tổng hợp (15 modules)
    ├── test-full-flow-guide.ts # ⭐ Full E2E flow (PRIORITY)
    ├── test-ai-agent.ts        # AI Agent: health, chat, embed, parquet, docs
    ├── test-chat-ai.ts         # Chat AI assistants & completions
    ├── test-activepieces.ts    # Workflows, flows, triggers
    ├── test-boards.ts          # Data boards, items, folders, files
    ├── test-crm.ts             # CRM contacts & conversations
    ├── test-crm-advanced.ts    # CRM advanced
    ├── test-frontend-sdk.ts    # Chat client sub-API
    ├── test-multi-agent.ts     # Multi-agent & sub-agent
    ├── test-multimedia-ai.ts   # Vision, audio AI
    ├── test-marketplace.ts     # Marketplace products
    ├── test-platform.ts        # Platform users & teams (⚠️ 502)
    ├── test-agent.ts           # Agent templates
    ├── test-settings.ts        # Org settings
    └── test-error-paths.ts     # Error handling validation
```

---

## 5. Quy tắc đồng bộ

> **Quan trọng:** Mọi thay đổi test phải được áp dụng đồng thời cho cả hai môi trường. **Không sửa trực tiếp** trong `test-npm-pip-pkg/ts`.

```powershell
# Sau khi sửa local-pkg, sync sang npm-pip-pkg:
$src = "d:\HUANGJUNFENG\IMBrace\sdk\test-local-pkg\ts\tests"
$dst = "d:\HUANGJUNFENG\IMBrace\sdk\test-npm-pip-pkg\ts\tests"
Copy-Item "$src\*" $dst -Force
Write-Host "✅ Sync done."
```

---

## 6. Ghi chú thêm

- `test-full-flow.ts` là phiên bản cũ hơn của `test-full-flow-guide.ts`. Giữ lại để debug nhanh nhưng không đăng ký trong `test:all`.
- File `.bak` (`test-full-flow-guide.ts.bak`) chỉ tồn tại trong `test-local-pkg` — không sync sang npm-pip-pkg.
- Khi backend fix xong service 502: cập nhật bảng trạng thái từ `⚠️ 502` → `✅` và xóa các `try/catch` skip.
