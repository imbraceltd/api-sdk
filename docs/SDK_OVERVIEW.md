# @opencode-ai/sdk — Tổng quan kiến trúc

Đây là TypeScript SDK để tương tác với OpenCode server (công cụ hỗ trợ code bằng AI) qua REST API.

---

## Cấu trúc thư mục

```
src/
├── index.ts          ← Entry point chính, export các factory functions
├── client.ts         ← Wrapper tùy chỉnh cho HTTP client
├── server.ts         ← Khởi động OpenCode server như subprocess
├── process.ts        ← Tiện ích quản lý process
├── gen/              ← CODE ĐƯỢC SINH TỰ ĐỘNG từ OpenAPI spec
│   ├── sdk.gen.ts    ← Class OpencodeClient với 16+ resource classes
│   ├── types.gen.ts  ← Tất cả type definitions
│   ├── client/       ← HTTP client dùng fetch API
│   └── core/         ← Auth, serializers, SSE streaming
└── v2/               ← V2 API (hỗ trợ workspace)
```

---

## Phân biệt code tay vs code sinh tự động

|                          | Mô tả                                                                         |
| ------------------------ | ------------------------------------------------------------------------------- |
| **Hand-written**   | `client.ts`, `server.ts`, `process.ts`, `index.ts`                      |
| **Auto-generated** | Toàn bộ thư mục `gen/` (từ `openapi.json` qua `@hey-api/openapi-ts`) |

---

## 3 cách khởi tạo

```typescript
// 1. Chỉ tạo client (server đã chạy sẵn)
const client = createOpencodeClient({ baseUrl: "http://localhost:4096" })

// 2. Tạo server + client cùng lúc
const { client, server } = await createOpencode({ port: 4096 })

// 3. V2 với workspace support
import { createOpencodeClient } from "./v2"
const client = createOpencodeClient({ directory: "/path/to/project" })
```

---

## Các nhóm API chính

| Resource     | Chức năng                              |
| ------------ | ---------------------------------------- |
| `session`  | Tạo/quản lý AI session, gửi prompt   |
| `file`     | Đọc/liệt kê file trong workspace     |
| `pty`      | Quản lý terminal session               |
| `provider` | OAuth / auth provider                    |
| `mcp`      | Model Context Protocol                   |
| `event`    | Subscribe Server-Sent Events (streaming) |
| `config`   | Cấu hình ứng dụng                    |

---

## Cách authentication hoạt động (`gen/core/auth.gen.ts`)

Hỗ trợ 3 scheme:

- **Bearer**: `Authorization: Bearer {token}`
- **Basic**: Base64-encoded credentials
- **API Key**: token thô trong header/query/cookie

---

## Đặc điểm `client.ts` (code tay)

Phần quan trọng nhất so với code sinh tự động:

1. Tắt timeout: `req.timeout = false`
2. Thêm header `x-opencode-directory` nếu có `directory`
3. Rewrite header thành query param `_directory` (cho một số trường hợp đặc biệt)

---

## `server.ts` làm gì?

Dùng `cross-spawn` để chạy binary `opencode` như subprocess, đọc stdout để phát hiện URL server đã ready (`"opencode server listening on ..."`), hỗ trợ `AbortSignal` để dừng server.

---

## Luồng request

1. Gọi method trên `OpencodeClient` (vd: `client.session.create(...)`)
2. Method gọi HTTP client từ `gen/client/client.gen.ts` (dùng native `fetch`)
3. Request interceptor của `client.ts` thêm header/query param
4. Response tự động parse (JSON, text, blob, SSE stream)
5. Trả về `{ data, error }` hoặc throw nếu `throwOnError: true`



# Phân tích cấu trúc SDK của OpenCode

Dựa trên cấu trúc thư mục bạn cung cấp, đây là chức năng của từng phần:

## **1. example/example.ts**

- **Mục đích**: Demo cách sử dụng SDK
- **Chức năng**:
  - Khởi tạo OpenCode server và client
  - Quét các file TypeScript trong `packages/core/*.ts`
  - Tạo sessions để AI viết tests cho các functions
  - Xử lý song song nhiều file với `Promise.all()`

## **2. script/build.ts** (đã xem ở trên)

- **Mục đích**: Build SDK từ OpenAPI spec
- **Chức năng**: Generate TypeScript code từ OpenAPI

## **3. script/publish.ts**

- **Mục đích**: Publish package lên npm
- **Chức năng**:
  - Transform exports từ [./src/](cci:9://file:///d:/HUANGJUNFENG/opencode/packages/sdk/js/src:0:0-0:0) thành `./dist/`
  - Pack và publish với tag và access public
  - Restore original package.json sau khi publish

## **4. src/gen/client/** (v1)

- **client.gen.ts**: HTTP client implementation
- **types.gen.ts**: Type definitions cho client
- **utils.gen.ts**: Utility functions cho client
- **index.ts**: Export các client functions

## **5. src/gen/core/** (v1)

- **auth.gen.ts**: Xử lý authentication (Bearer, Basic, API key)
- **bodySerializer.gen.ts**: Serialize request body
- **params.gen.ts**: Xử lý path/query parameters
- **pathSerializer.gen.ts**: Serialize URL paths
- **queryKeySerializer.gen.ts**: Serialize query parameters
- **serverSentEvents.gen.ts**: Xử lý SSE connections
- **types.gen.ts**: Core type definitions
- **utils.gen.ts**: Core utilities

## **6. src/v2/gen/client/** (v2)

- Tương tự v1 nhưng cho phiên bản API v2
- Files lớn hơn, có thể có thêm features

## **7. src/v2/gen/core/** (v2)

- Tương tự v1 core nhưng cho v2
- Có thể có improvements và additional features

## **Tổng kết**

SDK này được chia thành **2 phiên bản**:

- **v1**: [src/gen/](cci:9://file:///d:/HUANGJUNFENG/opencode/packages/sdk/js/src/gen:0:0-0:0) - Implementation hiện tại
- **v2**: `src/v2/gen/` - Version mới hơn với improvements

Mỗi phiên bản có:

- **Client layer**: HTTP client với authentication, interceptors
- **Core layer**: Low-level serialization, SSE, auth handling
- **Generated code**: Tự động từ OpenAPI spec

SDK hỗ trợ:

- REST API calls
- Server-Sent Events (real-time)
- Multiple authentication methods
- TypeScript typesafety
- Parallel request processing
