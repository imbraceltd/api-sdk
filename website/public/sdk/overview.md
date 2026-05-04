# Overview

> What the Imbrace SDK is, how it works, and when to use it.

The Imbrace SDK is the official client for the Imbrace Gateway, available in **TypeScript** and **Python**. Both SDKs wrap the same Gateway API with the same resource namespaces, the same auth model, and the same retry/error semantics — pick whichever language fits your stack.

> Toggle the language tabs anywhere on this site once and the rest of the docs remember your choice.

### Key Features

| Feature | Detail |
|---|---|
| **Type safety** | TypeScript types and Python type hints across every resource |
| **Two credential types** | `apiKey` or `accessToken` — see [Authentication](/sdk/authentication/) |
| **Auto retry** | 429 and 5xx retry with exponential backoff, no config needed |
| **Streaming AI** | SSE / async iterator for `streamChat` and AI completions |
| **Async & sync (Py)** | `ImbraceClient` (sync) and `AsyncImbraceClient` (async) |
| **Cancellation (TS)** | `AbortSignal` propagation for in-flight cancellation |

### Install

  
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
  

### Available resources

Every namespace is on both SDKs. Methods follow the language conventions — `client.aiAgent.streamChat()` in TS, `client.ai_agent.stream_chat()` in Python.

| Namespace | Purpose |
|---|---|
| `client.aiAgent` / `client.ai_agent` | Streaming AI chat, embeddings, parquet, chat-client sub-API |
| `client.chatAi` / `client.chat_ai` | Assistant CRUD (create/update/delete/list assistants) |
| `client.activepieces` | Workflow automation — flows, triggers, runs |
| `client.boards` | CRM boards — CRUD, items, fields, search, segments, CSV; KH folders & files |
| `client.platform` | Users, organizations, permissions |
| `client.contacts`, `client.conversations`, `client.messages`, `client.channel` | Contact / channel layer |
| `client.ai` | OpenAI-compatible completions and embeddings |

For the complete list and method reference, see [Resources](/sdk/resources/).

### When to pick which credential

| | API Key | Access Token |
|---|---|---|
| **Whose backend is Imbrace?** | A feature inside *your* backend | *Imbrace IS* your backend |
| **Whose users?** | Yours | Imbrace's |
| **Best for** | Server-to-server, internal scripts, CRM integrations | User-facing apps where each end-user logs in |

Full decision tree: [Authentication →](/sdk/authentication/).

### Next steps

- [Installation →](/sdk/installation/) — set up the package and credentials
- [Quick Start →](/sdk/quick-start/) — make your first call in 60 seconds
- [Full Flow Guide →](/sdk/full-flow-guide/) — end-to-end walkthrough of the four major workflows (assistants, workflows, knowledge hub, boards)
