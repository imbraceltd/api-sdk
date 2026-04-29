---
title: AI Agent
description: Reference for the aiAgent / ai_agent resource — streaming chat, embeddings, parquet, distributed tracing, and the Chat Client sub-API.
---

import { Tabs, TabItem, Aside } from "@astrojs/starlight/components";

The AI Agent resource connects to a dedicated service that runs on a separate base URL from the main API gateway. It exposes streaming chat, knowledge-base embedding management, columnar data (Parquet), distributed tracing (Tempo), and the full Chat Client sub-API used by frontend applications.

For an end-to-end example of `streamChat` against a real assistant, see [Full Flow Guide §1](/sdk/full-flow-guide/#1-create-an-ai-assistant-and-start-chatting).

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
import { ImbraceClient } from "@imbrace/sdk";
const client = new ImbraceClient();
```
</TabItem>
<TabItem label="Python">
```python
from imbrace import ImbraceClient
client = ImbraceClient()
```

Both sync (`ImbraceClient`) and async (`AsyncImbraceClient`) clients expose the same surface — async methods are awaited and the client uses `AsyncAiAgentResource` under the hood.
</TabItem>
</Tabs>

---

## Chat v2 — Streaming (SSE)

Returns a raw response. Consume the body as a Server-Sent Events stream.

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
const response = await client.aiAgent.streamChat({
  id: "chat_id",
  assistant_id: "asst_abc",
  organization_id: "org_abc",
  messages: [{ role: "user", content: "What can you do?" }],
});

const reader = response.body!.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  process.stdout.write(decoder.decode(value));
}
```
</TabItem>
<TabItem label="Python">
```python
response = client.ai_agent.stream_chat({
    "id": "chat_id",
    "assistant_id": "asst_abc",
    "organization_id": "org_abc",
    "messages": [{"role": "user", "content": "What can you do?"}],
})

for line in response.iter_lines():
    if line:
        print(line)
```

**Async:**

```python
import asyncio
from imbrace import AsyncImbraceClient

async def main():
    async with AsyncImbraceClient() as client:
        response = await client.ai_agent.stream_chat({
            "id": "chat_id",
            "assistant_id": "asst_abc",
            "organization_id": "org_abc",
            "messages": [{"role": "user", "content": "Hello"}],
        })
        async for line in response.aiter_lines():
            if line:
                print(line)

asyncio.run(main())
```
</TabItem>
</Tabs>

---

## Sub-agent Chat v2

Stream responses from a sub-agent and retrieve its conversation history.

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
const res = await client.aiAgent.streamSubAgentChat({
  assistant_id: "asst_sub",
  organization_id: "org_abc",
  session_id: "sess_xyz",
  chat_id: "chat_id",
  messages: [{ role: "user", content: "Explain the data." }],
});

const history = await client.aiAgent.getSubAgentHistory({
  session_id: "sess_xyz",
  chat_id: "chat_id",
});
```
</TabItem>
<TabItem label="Python">
```python
res = client.ai_agent.stream_sub_agent_chat({
    "assistant_id": "asst_sub",
    "organization_id": "org_abc",
    "session_id": "sess_xyz",
    "chat_id": "chat_id",
    "messages": [{"role": "user", "content": "Explain the data."}],
})

history = client.ai_agent.get_sub_agent_history(
    session_id="sess_xyz",
    chat_id="chat_id",
)
```
</TabItem>
</Tabs>

---

## Prompt Suggestions

Fetch pre-built prompt suggestions for a given assistant.

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
const suggestions = await client.aiAgent.getAgentPromptSuggestion("asst_abc");
```
</TabItem>
<TabItem label="Python">
```python
suggestions = client.ai_agent.get_agent_prompt_suggestion("asst_abc")
```
</TabItem>
</Tabs>

---

## Embeddings & Knowledge Base

Manage files used for Retrieval-Augmented Generation (RAG). Upload files first via [`client.boards.uploadFile`](/sdk/full-flow-guide/#3-manage-knowledge-hubs-and-attach-to-an-assistant) (TypeScript) / `client.boards.upload_file` (Python), then trigger embedding processing.

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
// Trigger embedding processing for an uploaded file
await client.aiAgent.processEmbedding({ fileId: "file_abc" });

// List and inspect embedding files
const files   = await client.aiAgent.listEmbeddingFiles({ page: 1, limit: 20 });
const file    = await client.aiAgent.getEmbeddingFile("file_abc");
const preview = await client.aiAgent.previewEmbeddingFile({ file_id: "file_abc" });

// Update status and delete
await client.aiAgent.updateEmbeddingFileStatus("file_abc", "active");
await client.aiAgent.deleteEmbeddingFile("file_abc");

// Classify a file for RAG categorization
const classification = await client.aiAgent.classifyFile({ file_id: "file_abc" });
```
</TabItem>
<TabItem label="Python">
```python
# Trigger embedding processing for an uploaded file
client.ai_agent.process_embedding("file_abc")

# With optional processing options
client.ai_agent.process_embedding("file_abc", options={"chunk_size": 512})

# List and inspect embedding files
files   = client.ai_agent.list_embedding_files(page=1, limit=20)
file    = client.ai_agent.get_embedding_file("file_abc")
preview = client.ai_agent.preview_embedding_file(file_id="file_abc")

# Update status and delete
client.ai_agent.update_embedding_file_status("file_abc", "active")
client.ai_agent.delete_embedding_file("file_abc")

# Classify a file for RAG categorization
classification = client.ai_agent.classify_file(file_id="file_abc")
```
</TabItem>
</Tabs>

---

## Data Board

AI-assisted field type suggestion for structured datasets.

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
const result = await client.aiAgent.suggestFieldTypes({
  fields: [
    { name: "created_at", samples: ["2024-01-01", "2024-02-15"] },
    { name: "amount",     samples: [100, 200.5, 999] },
    { name: "is_active",  samples: [true, false, true] },
  ],
});
// result.fields[i].suggestedType → "datetime" | "number" | "boolean" | ...
```
</TabItem>
<TabItem label="Python">
```python
result = client.ai_agent.suggest_field_types(fields=[
    {"name": "created_at", "samples": ["2024-01-01", "2024-02-15"]},
    {"name": "amount",     "samples": [100, 200.5, 999]},
    {"name": "is_active",  "samples": [True, False, True]},
])
# result["fields"][i]["suggestedType"] → "datetime" | "number" | "boolean" | ...
```
</TabItem>
</Tabs>

---

## Parquet

Generate and manage Parquet columnar data files for analytics pipelines.

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
// Generate a Parquet file from JSON data
const result = await client.aiAgent.generateParquet({
  data: [{ id: 1, name: "Alice" }, { id: 2, name: "Bob" }],
  fileName: "users",
  folderName: "exports",
});

const files = await client.aiAgent.listParquetFiles();
await client.aiAgent.deleteParquetFile("exports/users.parquet");
```
</TabItem>
<TabItem label="Python">
```python
result = client.ai_agent.generate_parquet(
    data=[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
    file_name="users",
    folder_name="exports",
)

files = client.ai_agent.list_parquet_files()
client.ai_agent.delete_parquet_file("exports/users.parquet")
```
</TabItem>
</Tabs>

---

## Distributed Tracing (Tempo)

Query Grafana Tempo traces emitted by the AI Agent service for observability and debugging.

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
// List recent traces
const traces = await client.aiAgent.getTraces({
  service:   "ai-agent",
  limit:     50,
  timeRange: 3600,     // seconds
  orgId:     "org_abc",
  details:   true,
});

// Inspect a single trace
const trace = await client.aiAgent.getTrace("trace_id_hex");

// Enumerate services, tags, and tag values
const services = await client.aiAgent.getTraceServices();
const tags     = await client.aiAgent.getTraceTags();
const values   = await client.aiAgent.getTraceTagValues("http.status_code");

// TraceQL search
const results = await client.aiAgent.searchTraceQL(
  `{ .service.name = "ai-agent" && .http.status = 500 }`
);
```
</TabItem>
<TabItem label="Python">
```python
# List recent traces
traces = client.ai_agent.get_traces(
    service="ai-agent",
    limit=50,
    time_range=3600,     # seconds
    org_id="org_abc",
    details=True,
)

# Inspect a single trace
trace = client.ai_agent.get_trace("trace_id_hex")

# Enumerate services, tags, and tag values
services = client.ai_agent.get_trace_services()
tags     = client.ai_agent.get_trace_tags()
values   = client.ai_agent.get_trace_tag_values("http.status_code")

# TraceQL search
results = client.ai_agent.search_traceql(
    '{ .service.name = "ai-agent" && .http.status = 500 }'
)
```
</TabItem>
</Tabs>

---

## Chat Client

The Chat Client sub-API powers frontend applications (e.g. the embedded chat widget). For framework-level wiring (React singleton, Express auth proxy, etc.), see [Integrations](/sdk/integrations/).

### Auth

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
await client.aiAgent.verifyChatClientCredentials({ token: "tok_xxx" });
await client.aiAgent.registerChatClient({ name: "web-app", secret: "s3cr3t" });
const user = await client.aiAgent.getChatClientUser({ token: "tok_xxx" });
```
</TabItem>
<TabItem label="Python">
```python
client.ai_agent.verify_chat_client_credentials({"token": "tok_xxx"})
client.ai_agent.register_chat_client({"name": "web-app", "secret": "s3cr3t"})
user = client.ai_agent.get_chat_client_user({"token": "tok_xxx"})
```
</TabItem>
</Tabs>

### Chats

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
// Create a new chat session
await client.aiAgent.createClientChat({
  id: "chat_uuid",
  message: {
    id: "msg_uuid",
    role: "user",
    parts: [{ type: "text", text: "Hello!" }],
  },
  assistantId:    "asst_abc",
  organizationId: "org_abc",
});

// List, read, update, delete chats
const chats = await client.aiAgent.listClientChats({
  organization_id: "org_abc",
  limit: 20,
});
const chat = await client.aiAgent.getClientChat("chat_id");
await client.aiAgent.updateClientChat("chat_id", { visibility: "private" });
await client.aiAgent.deleteClientChat("chat_id");
await client.aiAgent.deleteAllClientChats({ organization_id: "org_abc" });

// Auto-generate a title for the chat
await client.aiAgent.generateClientChatTitle("chat_id");

// Stream real-time chat status as SSE — returns raw Response
const statusStream = await client.aiAgent.streamClientChatStatus("chat_id");
```
</TabItem>
<TabItem label="Python">
```python
# Create a new chat session
client.ai_agent.create_client_chat({
    "id": "chat_uuid",
    "message": {
        "id": "msg_uuid",
        "role": "user",
        "parts": [{"type": "text", "text": "Hello!"}],
    },
    "assistantId":    "asst_abc",
    "organizationId": "org_abc",
})

# List, read, update, delete
chats = client.ai_agent.list_client_chats(organization_id="org_abc", limit=20)
chat  = client.ai_agent.get_client_chat("chat_id")
client.ai_agent.update_client_chat("chat_id", {"visibility": "private"})
client.ai_agent.delete_client_chat("chat_id")
client.ai_agent.delete_all_client_chats("org_abc")

# Auto-generate a title for the chat
client.ai_agent.generate_client_chat_title("chat_id")

# Stream real-time chat status as SSE — returns raw httpx.Response
status_stream = client.ai_agent.stream_client_chat_status("chat_id")
```
</TabItem>
</Tabs>

### Messages

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
await client.aiAgent.persistClientMessage({ chatId: "chat_id", content: "Hello" });
const messages = await client.aiAgent.listClientMessages("chat_id");
await client.aiAgent.deleteTrailingMessages("message_id");
```
</TabItem>
<TabItem label="Python">
```python
client.ai_agent.persist_client_message({"chatId": "chat_id", "content": "Hello"})
messages = client.ai_agent.list_client_messages("chat_id")
client.ai_agent.delete_trailing_messages("message_id")
```
</TabItem>
</Tabs>

### Votes

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
const votes = await client.aiAgent.getVotes("chat_id");
await client.aiAgent.updateVote({ messageId: "msg_id", vote: "up" });
```
</TabItem>
<TabItem label="Python">
```python
votes = client.ai_agent.get_votes("chat_id")
client.ai_agent.update_vote({"messageId": "msg_id", "vote": "up"})
```
</TabItem>
</Tabs>

### Documents (AI-generated artifacts)

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
await client.aiAgent.createDocument({ kind: "text", content: "Draft..." });

const doc        = await client.aiAgent.getDocument("doc_id");
const latest     = await client.aiAgent.getDocumentLatest("doc_id");
const pub        = await client.aiAgent.getDocumentPublic("doc_id");
const byKind     = await client.aiAgent.getDocumentLatestByKind({ kind: "text" });
const suggestion = await client.aiAgent.getDocumentSuggestions("doc_id");

await client.aiAgent.deleteDocument("doc_id");
```
</TabItem>
<TabItem label="Python">
```python
client.ai_agent.create_document({"kind": "text", "content": "Draft..."})

doc        = client.ai_agent.get_document("doc_id")
latest     = client.ai_agent.get_document_latest("doc_id")
pub        = client.ai_agent.get_document_public("doc_id")
by_kind    = client.ai_agent.get_document_latest_by_kind(kind="text")
suggestion = client.ai_agent.get_document_suggestions("doc_id")

client.ai_agent.delete_document("doc_id")
```
</TabItem>
</Tabs>

---

## Admin Guides

Access admin documentation hosted by the AI Agent service. Guide files are returned as raw binary streams (typically PDF).

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
const guides = await client.aiAgent.listAdminGuides();

// Download a specific guide — returns raw Response (PDF stream)
const response = await client.aiAgent.getAdminGuide("onboarding.pdf");
const blob = await response.blob();
```
</TabItem>
<TabItem label="Python">
```python
guides = client.ai_agent.list_admin_guides()

# Download a specific guide — returns raw httpx.Response
response = client.ai_agent.get_admin_guide("onboarding.pdf")
with open("onboarding.pdf", "wb") as f:
    f.write(response.content)
```
</TabItem>
</Tabs>

---

## Legacy v1 chat

The original REST chat endpoints persist conversation history without streaming. New code should use [Chat v2 streaming](#chat-v2--streaming-sse) above; v1 stays for backwards compatibility with existing chats.

<Tabs syncKey="lang">
<TabItem label="TypeScript">
```typescript
// List chats for an organization
const chats = await client.aiAgent.listChats({
  organization_id: "org_abc",
  user_id: "user_123",
  limit: 20,
});

// Get a single chat (pass true to include messages)
const chat = await client.aiAgent.getChat("chat_id", true);

// Delete a chat
await client.aiAgent.deleteChat("chat_id", {
  organization_id: "org_abc",
  user_id: "user_123",
});
```
</TabItem>
<TabItem label="Python">
```python
chats = client.ai_agent.list_chats(
    organization_id="org_abc",
    user_id="user_123",
    limit=20,
)

chat = client.ai_agent.get_chat("chat_id", include_messages=True)

client.ai_agent.delete_chat(
    "chat_id",
    organization_id="org_abc",
    user_id="user_123",
)
```
</TabItem>
</Tabs>
