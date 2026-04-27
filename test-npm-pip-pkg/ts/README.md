# Imbrace TypeScript SDK — NPM Package Test Suite

Bộ kiểm thử tích hợp cho **@imbrace/sdk** (TypeScript), cài đặt trực tiếp từ NPM registry (`^1.0.1`). Dùng để xác nhận SDK đã publish hoạt động đúng trên môi trường thực.

---

## 1. Thiết lập

### Yêu cầu
- Node.js v18+
- npm

### Cấu hình `.env`
```env
IMBRACE_ACCESS_TOKEN=your_access_token_here
# hoặc:
# IMBRACE_API_KEY=your_api_key_here

IMBRACE_ORGANIZATION_ID=your_org_id_here
IMBRACE_GATEWAY_URL=https://app-gatewayv2.imbrace.co
```

### Cài đặt
```bash
npm install
```
> SDK được cài từ NPM: `@imbrace/sdk@^1.0.1`

---

## 2. Chạy Test

### ⭐ Full Flow Guide (Ưu tiên cao nhất)
```bash
npm run test:full-flow
```
**Phủ:** Assistant CRUD → Activepieces Flow (tạo + bind) → Knowledge Hub RAG → Board & Items → Cleanup

---

### 🚀 Chạy toàn bộ Test Suite
```bash
npm run test:all
```

---

### 🧩 Danh sách đầy đủ các module

| Lệnh | Module | Mô tả | Trạng thái |
|------|--------|-------|-----------|
| `npm run test:ai` | AI Agent | Health, Chat v1/v2 SSE, getChat/deleteChat, Embeddings, Parquet, Sub-agent, Tracing, Documents, Chat Client | ✅ |
| `npm run test:chat-ai` | Chat AI | Assistants CRUD, completions, listModels, uploadFile, extractFile, Knowledge, Folders | ✅ |
| `npm run test:boards` | Boards | CRUD bảng, fields, items, bulkDelete, search, segments, exportCsv, Folders, uploadFile, searchFiles | ✅ |
| `npm run test:activepieces` | Activepieces | Flows, Runs, Folders, Connections, Tables, listPieces, listMcpServers | ✅ |
| `npm run test:crm` | CRM | Contacts, Conversations, Messages, Channel | ✅ |
| `npm run test:crm-advanced` | CRM Advanced | Activities, Comments, Board-contact linking | ✅ |
| `npm run test:frontend` | Frontend SDK | Chat Client auth, chats CRUD, messages, votes, documents | ✅ |
| `npm run test:multi-agent` | Multi-Agent | Sub-agent streaming, history, Parquet, multi-turn | ✅ |
| `npm run test:multimedia` | Multimedia AI | OCR, STT, TTS, Document AI | ✅ |
| `npm run test:agent` | Agent | Agent templates và runs | ✅ |
| `npm run test:marketplace` | Marketplace | listProducts, listUseCaseTemplates | ✅ |
| `npm run test:platform` | Platform | getMe, listUsers, listTeams | ⚠️ 502 |
| `npm run test:settings` | Settings | Message templates, WA templates | ✅ |
| `npm run test:error-paths` | Error Paths | AuthError, ApiError, NetworkError | ✅ |
| `npm run test:full-flow` | Full Flow Guide | ⭐ E2E: Assistant → Flow → RAG → Board | ✅ |

---

## 3. Tình trạng Backend (prodv2)

| Trạng thái | Dịch vụ |
|-----------|---------|
| ✅ Hoạt động | `chatAi`, `aiAgent`, `activepieces`, `boards`, `marketplace`, `auth`, `crm`, `settings` |
| ⚠️ 502 (down) | `platform.getMe`, `channel`, `account` |
| 🔴 404 (route missing) | `sessions`, `marketplace.orders`, `aiAgent v3/` routes |

---

## 4. Cấu trúc thư mục

```
test-npm-pip-pkg/ts/
├── .env
├── .env.example
├── package.json                # npm scripts (giống local, trỏ NPM registry)
├── utils/
│   └── utils.ts
└── tests/                      # Giống hệt test-local-pkg/ts/tests
    ├── test-all.ts             # ▶ Runner tổng hợp
    ├── test-full-flow-guide.ts # ⭐ Full E2E
    └── ...                     # (15+ module files)
```

---

## 5. Quy tắc đồng bộ

> Bộ test này phải **luôn giống hệt** `test-local-pkg/ts/tests`. **Không sửa trực tiếp tại đây.**

```powershell
# Sau khi sửa local-pkg, sync sang đây:
$src = "d:\HUANGJUNFENG\IMBrace\sdk\test-local-pkg\ts\tests"
$dst = "d:\HUANGJUNFENG\IMBrace\sdk\test-npm-pip-pkg\ts\tests"
Copy-Item "$src\*" $dst -Force
Write-Host "✅ Sync done."
```

Xem README đầy đủ tại: [`test-local-pkg/ts/README.md`](../../test-local-pkg/ts/README.md)
