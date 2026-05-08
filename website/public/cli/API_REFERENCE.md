# Imbrace CLI — Local API Reference

The local API server (Hono, Bun, port `3456`) acts as a proxy to the Imbrace platform (`https://app-gatewayv2.imbrace.co`). The CLI calls this API; it never calls the platform directly.

**Base URL:** `http://localhost:3456`

---

## Authentication

All endpoints under `/data-board/*`, `/ai-agent/*`, and `/workflow/*` are **protected** by auth middleware.

**Header:** `Authorization: Bearer <credential>`

Where `credential` is either:
- An **API key** (starts with `sk-` or `api_`)
- A **JWT token** (returned from email+password login)

**Middleware behavior** (`api/src/middleware/auth.ts`):
1. Extracts `Bearer <credential>` from header
2. Creates `ImbraceClient`:
   - API key: `new ImbraceClient({ apiKey: credential, baseUrl: "https://app-gatewayv2.imbrace.co" })`
   - JWT: `new ImbraceClient({ baseUrl })` + `client.setAccessToken(credential)`
3. Verifies credential via `client.boards.list()` (lightweight call)
4. Attaches `imbraceClient` and `credential` to Hono context

**Public endpoints** (no auth): `GET /`, `POST /auth/login`

---

## Health

### `GET /`

**Auth:** None

**Response:**
```json
{
  "name": "Imbrace API",
  "version": "1.0.0",
  "status": "running",
  "docs": "imbrace --help"
}
```

---

## Auth

### `POST /auth/login`

**Auth:** None

**Request body** (choose one):
```json
// Method 1: API key
{ "apiKey": "api_xxx..." }

// Method 2: Email + password
{ "email": "user@example.com", "password": "mypass" }
```

**Success response** (200):
```json
// API key method
{
  "ok": true,
  "method": "api-key",
  "message": "Authenticated with API key",
  "credential": "api_xxx..."
}

// Email + password method
{
  "ok": true,
  "method": "password",
  "message": "Logged in as user@example.com",
  "credential": "<jwt-token>",
  "email": "user@example.com"
}
```

**Error responses:**
- `401` — `{ "ok": false, "message": "Invalid API key: ..." }` or `{ "ok": false, "message": "Login failed: ..." }`
- `400` — `{ "ok": false, "message": "Provide { email, password } or { apiKey }" }`

---

## Data Board

All endpoints require `Authorization: Bearer <credential>`.

### `GET /data-board/list`

List all boards.

**Response:**
```json
{ "ok": true, "count": 5, "data": [ { "_id": "brd_...", "name": "...", "fields": [...] }, ... ] }
```

### `GET /data-board/:id`

Get a single board by ID.

**Response:**
```json
{ "ok": true, "data": { "_id": "brd_...", "name": "...", "fields": [...] } }
```

### `POST /data-board/create`

Create a new board.

**Request body:**
```json
{ "name": "Sales Pipeline" }
```

Board body is freestyle — any additional fields are passed through.

**Response:**
```json
{ "ok": true, "message": "Board \"Sales Pipeline\" created", "data": { "_id": "brd_...", ... } }
```

### `GET /data-board/:id/fields`

List fields of a board.

**Response:**
```json
{ "ok": true, "data": [ { "_id": "...", "name": "Company", "type": "ShortText" }, ... ] }
```

### `POST /data-board/:id/fields`

Create a field on a board.

**Request body:**
```json
{ "name": "Company", "type": "ShortText" }
```

Valid types: `ShortText`, `LongText`, `Number`, `Date`, `Email`, `Phone`, `Currency`, `SingleSelection`, `MultipleSelection`, `Checkbox`, `Assignee`, `MultipleAssignee`, `Link`, `Notes`, `Origin`, `Priority`.

**Response:**
```json
{ "ok": true, "message": "Field \"Company\" created", "data": { ... } }
```

### `GET /data-board/:id/items?limit=20&skip=0&q=Acme`

List/search items in a board.

**Query params:** `limit` (default 20), `skip` (default 0), `q` (full-text search via Meilisearch).

**Response:**
```json
{ "ok": true, "count": 2, "data": [ { "_id": "...", "fields": [...] }, ... ] }
```

### `POST /data-board/:id/items`

Create an item (record) in a board.

**Request body:**
```json
{ "fields": [ { "board_field_id": "...", "value": "Acme Corp" }, { "board_field_id": "...", "value": 50000 } ] }
```

**Response:**
```json
{ "ok": true, "message": "Item created", "data": { ... } }
```

### `PUT /data-board/:id/items/:itemId`

Update an item.

**Request body:**
```json
{ "data": [ { "key": "<fieldId>", "value": "Updated value" } ] }
```

**Response:**
```json
{ "ok": true, "message": "Item updated", "data": { ... } }
```

### `DELETE /data-board/:id/items/:itemId`

Delete an item.

**Response:**
```json
{ "ok": true, "message": "Item deleted" }
```

### `GET /data-board/:id/search?q=Acme&limit=10`

Search items via Meilisearch (dedicated search endpoint).

**Response:** Same format as `list-items`.

### `GET /data-board/:id/export-csv`

Export board as CSV. Returns raw text (not JSON).

**Response:** `Content-Type: text/plain` with CSV content.

---

## AI Agent

All endpoints require `Authorization: Bearer <credential>`.

### `GET /ai-agent/list`

List all AI agents.

**Response:**
```json
{ "ok": true, "count": 3, "data": [ ... ] }
```

### `GET /ai-agent/providers`

List LLM providers (system + custom). Returns system provider with its models.

**Response:**
```json
{
  "ok": true,
  "count": 4,
  "data": [
    { "id": "system", "provider_id": "system", "name": "system", "type": "system", "is_default": true, "models": ["Default", ...] },
    { "id": "<uuid>", "provider_id": "<uuid>", "name": "openai", "type": "custom", "is_default": false, "models": ["gpt-4o", ...] }
  ]
}
```

> `provider_id` (UUID) is the canonical ID — not the MongoDB `_id`.

### `GET /ai-agent/folders?q=<search>`

List Knowledge Hub folders. Optional `q` param for name search.

**Response:**
```json
{ "ok": true, "count": 5, "data": [ ... ] }
```

### `GET /ai-agent/folders/:folderId/files`

List files in a Knowledge Hub folder.

**Response:**
```json
{ "ok": true, "count": 10, "data": [ ... ] }
```

### `GET /ai-agent/providers/:providerId/models`

List models for a specific provider. Use `system` for the system provider.

**Response:**
```json
{ "ok": true, "count": 2, "data": ["Default", ...] }
```

### `GET /ai-agent/:id`

Get agent details.

**Response:**
```json
{ "ok": true, "data": { ... } }
```

### `POST /ai-agent/create`

Create a new AI agent (atomic: assistant + channel + template).

**Request body (all fields optional except `name`):**
```json
{
  "name": "Support Bot",
  "description": "A helpful support agent",
  "instructions": "You are a support agent...",
  "model": "gpt-4o-mini",
  "provider_id": "e2629292-...",
  "mode": "standard",
  "temperature": 0.3,
  "personality_role": "Friendly and professional",
  "core_task": "Answer product inquiries",
  "tone_and_style": "Polite, professional",
  "response_length": "medium",
  "banned_words": "stupid, idiot",
  "category": ["Support"],
  "guardrail_id": "gr_...",
  "preload_information": "...",
  "show_thinking_process": false,
  "streaming": true,
  "use_memory": true,
  "knowledge_hubs": ["..."],
  "folder_ids": ["..."],
  "default_folder_id": "...",
  "board_ids": ["brd_..."],
  "file_ids": ["..."]
}
```

**Response:**
```json
{ "ok": true, "message": "AI Agent \"Support Bot\" created", "data": { "_id": "...", ... } }
```

### `PUT /ai-agent/:id`

Update an AI agent (partial update via PUT-merge). Accepts same fields as create.

**Response:**
```json
{ "ok": true, "message": "AI Agent updated", "data": { "assistant": {...}, "template": {...} } }
```

### `DELETE /ai-agent/:id`

Delete an AI agent.

**Response:**
```json
{ "ok": true, "message": "AI Agent deleted" }
```

---

## Workflow

All endpoints require `Authorization: Bearer <credential>`.

### Flow CRUD

#### `GET /workflow/list?folderId=<id|NULL>`

List workflows. Optional folderId filter.
- Omitted → all flows
- `NULL` → only unfiled flows
- `<id>` → only flows in that folder

**Response:**
```json
{ "ok": true, "count": 3, "data": [ ... ] }
```

#### `GET /workflow/:id`

Get flow details (includes version, trigger, nodes).

**Response:**
```json
{ "ok": true, "data": { "id": "...", "status": "DISABLED", "version": { "trigger": {...}, ... } } }
```

#### `POST /workflow/create`

Create a new workflow.

**Request body:**
```json
{ "name": "My Flow", "projectId": "...", "folderId": "..." }
```

`projectId` is auto-resolved from the first existing flow if not provided.

**Response:**
```json
{ "ok": true, "message": "Workflow \"My Flow\" created", "data": { ... } }
```

#### `POST /workflow/:id/move`

Move workflow to a folder.

**Request body:**
```json
{ "folderId": "<folderId>" }
```

Use `{ "folderId": null }` to unfile.

**Response:**
```json
{ "ok": true, "message": "Workflow moved to <folderId>", "data": { ... } }
```

#### `DELETE /workflow/:id`

Delete a workflow.

**Response:**
```json
{ "ok": true, "message": "Workflow deleted" }
```

### Pieces

#### `GET /workflow/piece/list?search=<query>`

List pieces (integrations). Optional search filter (matches name, displayName, description).

**Response:**
```json
{ "ok": true, "count": 126, "data": [ { "name": "@activepieces/piece-slack", "displayName": "Slack", ... }, ... ] }
```

#### `GET /workflow/piece/detail?name=<pieceName>`

Get full piece schema (actions, triggers, fields). Uses raw fetch from backend.

`name` can be short (`slack`) or full (`@activepieces/piece-slack`).

**Response:**
```json
{ "ok": true, "data": { "name": "...", "version": "0.3.9", "actions": {...}, "triggers": {...} } }
```

### Nodes

#### `GET /workflow/:flowId/nodes`

List all nodes in a workflow (flattened).

**Response:**
```json
{ "ok": true, "count": 3, "data": [ { "name": "trigger", "type": "PIECE_TRIGGER", "displayName": "...", ... }, ... ] }
```

#### `POST /workflow/:flowId/nodes`

Add a trigger or action node.

**Request body** (trigger):
```json
{ "type": "trigger", "piece": "webhook", "triggerName": "catch_webhook", "input": {}, "displayName": "Webhook" }
```

**Request body** (action):
```json
{ "type": "action", "piece": "slack", "actionName": "send_channel_message", "input": { "channel": "C1", "text": "hi" }, "after": "trigger", "name": "step_1", "displayName": "Send Slack" }
```

**Response:**
```json
{ "ok": true, "message": "Trigger set", "data": { ... } }
```

#### `PUT /workflow/:flowId/nodes/:nodeName`

Update node input/displayName.

**Request body:**
```json
{ "input": { "channel": "C2" }, "displayName": "New Name" }
```

**Response:**
```json
{ "ok": true, "message": "Node \"step_1\" updated", "data": { ... } }
```

#### `DELETE /workflow/:flowId/nodes/:nodeName`

Delete an action node. Trigger cannot be deleted.

**Response:**
```json
{ "ok": true, "message": "Node \"step_1\" deleted" }
```

#### `POST /workflow/:flowId/nodes/raw`

Raw passthrough to `applyFlowOperation()`. For advanced node types: ROUTER, LOOP_ON_ITEMS, CODE.

**Request body:**
```json
{ "type": "ADD_ACTION", "request": { ... } }
```

**Response:**
```json
{ "ok": true, "message": "Operation \"ADD_ACTION\" applied", "data": { ... } }
```

### Connections

#### `GET /workflow/conn/list`

List all connections.

**Response:**
```json
{ "ok": true, "count": 2, "data": [ { "id": "...", "pieceName": "@activepieces/piece-slack", ... }, ... ] }
```

#### `GET /workflow/conn/:connId`

Get connection details.

**Response:**
```json
{ "ok": true, "data": { "id": "...", "pieceName": "...", "type": "SECRET_TEXT", ... } }
```

#### `POST /workflow/conn/create`

Create a connection (credential for an external service).

**Request body:**
```json
{ "piece": "slack", "type": "SECRET_TEXT", "value": "xoxb-...", "displayName": "My Slack", "externalId": "cli_123456" }
```

For `BASIC_AUTH`, value is an object:
```json
{ "piece": "custom", "type": "BASIC_AUTH", "value": { "username": "admin", "password": "pass" } }
```

For `OAUTH2`/`CLOUD_OAUTH2`/`CUSTOM_AUTH`, caller supplies the full structured value with `type` field at top level.

**Response:**
```json
{ "ok": true, "message": "Connection created", "data": { "id": "...", ... } }
```

#### `DELETE /workflow/conn/:connId`

Delete a connection.

**Response:**
```json
{ "ok": true, "message": "Connection deleted" }
```

### Folders

#### `GET /workflow/folder/list`

List all folders (categories).

**Response:**
```json
{ "ok": true, "count": 4, "data": [ { "id": "...", "displayName": "Channel Workflow" }, ... ] }
```

#### `GET /workflow/folder/:folderId`

Get folder details.

**Response:**
```json
{ "ok": true, "data": { "id": "...", "displayName": "..." } }
```

#### `POST /workflow/folder/create`

Create a folder.

**Request body:**
```json
{ "name": "My Category", "projectId": "..." }
```

**Response:**
```json
{ "ok": true, "message": "Folder \"My Category\" created", "data": { ... } }
```

#### `PUT /workflow/folder/:folderId`

Rename a folder.

**Request body:**
```json
{ "name": "New Name" }
```

**Response:**
```json
{ "ok": true, "message": "Folder renamed", "data": { ... } }
```

#### `DELETE /workflow/folder/:folderId`

Delete a folder.

**Response:**
```json
{ "ok": true, "message": "Folder deleted" }
```

### MCP Servers

#### `GET /workflow/mcp/list`

List MCP servers.

**Response:**
```json
{ "ok": true, "count": 2, "data": [ { "id": "...", "name": "...", ... }, ... ] }
```

#### `GET /workflow/mcp/:mcpId`

Get MCP server details.

**Response:**
```json
{ "ok": true, "data": { "id": "...", "name": "...", "tools": [...], ... } }
```

#### `POST /workflow/mcp/create`

Create an MCP server.

**Request body:**
```json
{ "name": "My MCP", "projectId": "..." }
```

**Response:**
```json
{ "ok": true, "message": "MCP server \"My MCP\" created", "data": { ... } }
```

#### `POST /workflow/mcp/:mcpId/rotate-token`

Rotate MCP server token. Token is shown once.

**Response:**
```json
{ "ok": true, "message": "Token rotated. Save the new token now — it won't be shown again.", "data": { "token": "...", ... } }
```

#### `DELETE /workflow/mcp/:mcpId`

Delete an MCP server.

**Response:**
```json
{ "ok": true, "message": "MCP server deleted" }
```

### Lifecycle

#### `POST /workflow/:flowId/publish`

Lock and publish the current draft.

**Response:**
```json
{ "ok": true, "message": "Workflow published", "data": { ... } }
```

#### `POST /workflow/:flowId/enable`

Enable auto-trigger. Requires publish first.

**Response:**
```json
{ "ok": true, "message": "Workflow enabled", "data": { ... } }
```

#### `POST /workflow/:flowId/disable`

Disable auto-trigger.

**Response:**
```json
{ "ok": true, "message": "Workflow disabled", "data": { ... } }
```

### Runs

#### `GET /workflow/runs?limit=10`

List recent runs.

**Response:**
```json
{ "ok": true, "count": 3, "data": [ { "id": "...", "flowId": "...", "status": "...", "startTime": "...", ... }, ... ] }
```

#### `GET /workflow/runs/:runId`

Get run details.

**Response:**
```json
{ "ok": true, "data": { "id": "...", "status": "SUCCEEDED", ... } }
```

#### `POST /workflow/:flowId/run?sync=true`

Manually trigger a workflow.

**Request body:**
```json
{ "payload": { "text": "hello" } }
```

**Query:** `?sync=true` waits for completion (may time out at ~30s). Without `sync`, returns immediately (fire-and-forget).

**Response (async):**
```json
{ "ok": true, "message": "Workflow triggered (async)", "mode": "async", "data": { ... } }
```

**Response (sync):**
```json
{ "ok": true, "message": "Workflow triggered (sync)", "mode": "sync", "data": { ... } }
```

---

## Error Responses

All endpoints return errors in a consistent format:

```json
{ "ok": false, "message": "<error description>" }
```

| Status | Meaning |
|---|---|
| `400` | Bad request (missing required fields, invalid input) |
| `401` | Authentication failed (missing/invalid credential) |
| `404` | Route not found or resource not found |
| `500` | Internal server error (backend error, network issue) |

The global 404 handler returns:
```json
{ "ok": false, "message": "Route not found. Try: imbrace --help" }
```

The global error handler returns:
```json
{ "ok": false, "message": "<error.message>", "status": <httpStatus> }
```
