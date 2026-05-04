# Giới Thiệu

> Imbrace SDK là gì, cách hoạt động, và khi nào nên sử dụng.

Imbrace SDK là client chính thức cho Imbrace Gateway, có sẵn cho cả **TypeScript** và **Python**. Cả hai SDK đều wrap cùng một Gateway API với cùng resource namespaces, cùng auth model, và cùng retry/error semantics — chọn ngôn ngữ phù hợp với stack của bạn.

> Chuyển đổi tab ngôn ngữ ở bất kỳ đâu trên trang web này một lần và phần còn lại sẽ ghi nhớ lựa chọn của bạn.

### Tính Năng Nổi Bật

| Tính năng | Chi tiết |
|---|---|
| **Type safety** | TypeScript types và Python type hints trên mọi resource |
| **Hai loại credential** | `apiKey` hoặc `accessToken` — xem [Xác Thực](/vi/sdk/authentication/) |
| **Auto retry** | 429 và 5xx retry với exponential backoff, không cần cấu hình |
| **Streaming AI** | SSE / async iterator cho `streamChat` và AI completions |
| **Async & sync (Py)** | `ImbraceClient` (sync) và `AsyncImbraceClient` (async) |
| **Cancellation (TS)** | `AbortSignal` propagation để hủy request đang chạy |

### Cài Đặt

  
    ```bash
    npm install @imbrace/sdk
    ```
  
  
    ```bash
    pip install imbrace
    ```
  

### Hello, world

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"

    const client = new ImbraceClient({ accessToken: "acc_your_token" })
    const me = await client.platform.getMe()
    ```
  
  
    ```python
    from imbrace import ImbraceClient

    with ImbraceClient(access_token="acc_your_token") as client:
        me = client.platform.get_me()
    ```
  

### Các Resource Có Sẵn

Mọi namespace đều có trên cả hai SDK. Các method theo quy ước ngôn ngữ — `client.aiAgent.streamChat()` trong TS, `client.ai_agent.stream_chat()` trong Python.

| Namespace | Mục đích |
|---|---|
| `client.aiAgent` / `client.ai_agent` | Streaming AI chat, embeddings, parquet, chat-client sub-API |
| `client.chatAi` / `client.chat_ai` | Assistant CRUD (create/update/delete/list assistants) |
| `client.activepieces` | Workflow automation — flows, triggers, runs |
| `client.boards` | CRM boards — CRUD, items, fields, search, segments, CSV; KH folders & files |
| `client.platform` | Users, organizations, permissions |
| `client.contacts`, `client.conversations`, `client.messages`, `client.channel` | Contact / channel layer |
| `client.ai` | OpenAI-compatible completions and embeddings |

Để xem danh sách đầy đủ và tham chiếu method, xem [Resources](/vi/sdk/resources/).

### Khi Nào Chọn Credential Nào

| | API Key | Access Token |
|---|---|---|
| **Imbrace đóng vai trò gì?** | Một tính năng trong backend *của bạn* | *Imbrace LÀ* backend của bạn |
| **User của ai?** | Của bạn | Của Imbrace |
| **Dùng tốt nhất cho** | Server-to-server, internal scripts, CRM integrations | User-facing apps nơi mỗi end-user đăng nhập |

Xem chi tiết: [Xác Thực →](/vi/sdk/authentication/).

### Bước Tiếp Theo

- [Cài Đặt →](/vi/sdk/installation/) — thiết lập package và credentials
- [Bắt Đầu Nhanh →](/vi/sdk/quick-start/) — thực hiện cuộc gọi đầu tiên trong 60 giây
- [Hướng Dẫn Luồng Đầy Đủ →](/vi/sdk/full-flow-guide/) — hướng dẫn end-to-end qua bốn luồng chính (assistants, workflows, knowledge hub, boards)
