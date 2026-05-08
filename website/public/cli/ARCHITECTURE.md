# Imbrace CLI — Architecture

## Overview

The Imbrace CLI uses a **two-layer proxy architecture**:

```
imbrace (CLI) → http://localhost:3456 (API proxy) → https://app-gatewayv2.imbrace.co (Imbrace Platform)
```

The CLI never calls the Imbrace platform directly. All commands route through a local Hono REST API server that proxies requests using the `@imbrace/sdk` npm package.

### Components

| Component | Directory | Tech | Role |
|---|---|---|---|
| **CLI** | `cli/` | oclif (TypeScript) | Terminal commands (`imbrace login`, `imbrace data-board list`, ...) |
| **API** | `api/` | Hono (TypeScript, Bun) | Local proxy server on port 3456 |

### API Server Entry Point

File: `api/src/index.ts`

- Framework: **Hono** with CORS, JSON logger, pretty JSON middleware
- Port: `3456` (configurable via `PORT` env)
- Routes mounted under 3 protected groups:
  - `/data-board/*` — auth middleware
  - `/ai-agent/*` — auth middleware
  - `/workflow/*` — auth middleware
- Public routes:
  - `GET /` — health check
  - `POST /auth/login` — authentication
- 404 handler returns `{ ok: false, message: "Route not found. Try: imbrace --help" }`

---

## Authentication Flow

### Two auth methods

**1. API Key** (credential starts with `sk-` or `api_`):
- Passed directly to SDK: `new ImbraceClient({ apiKey: credential, baseUrl })`
- Stored as-is in local config

**2. Email + Password** (returns JWT token):
- SDK: `client.login(email, password)` → internally calls `client.tokenManager.getToken()` (internal API)
- JWT token stored as credential

### Auth Middleware (API side)

File: `api/src/middleware/auth.ts`

1. Extract `Authorization: Bearer <credential>` header
2. Create `ImbraceClient` instance:
   - API key → `new ImbraceClient({ apiKey: credential, baseUrl: "https://app-gatewayv2.imbrace.co" })`
   - Token → `new ImbraceClient({ baseUrl })` + `client.setAccessToken(credential)`
3. Verify credential via lightweight call: `client.boards.list()`
4. Attach client to Hono context: `c.set("imbraceClient", client)`, `c.set("credential", credential)`

### Credential Storage (CLI side)

File: `cli/src/config.ts` — uses `conf` npm package with `projectName: "imbrace"`.

| OS | Config path |
|---|---|
| macOS | `~/Library/Preferences/imbrace-nodejs/config.json` |
| Linux | `~/.config/imbrace-nodejs/config.json` |
| Windows | `%APPDATA%\imbrace-nodejs\Config\config.json` |

Stored fields: `credential`, `method` (`"api-key"` | `"password"`), `email`, `apiUrl`.

### Auto-login

File: `cli/src/base-command.ts`

Every CLI command (except `login`) extends `BaseCommand`, which calls `ensureLoggedIn()` in `init()`. If no credential is found, it interactively prompts the user to choose login method (API Key or Email + Password) using `@inquirer/prompts`.

---

## AI Agent Create Flow

File: `api/src/routes/ai-agent.ts:130-207`

`POST /ai-agent/create` calls `client.agent.createUseCase({ usecase, assistant })` which atomically creates:

1. **AI Assistant** — model, instructions, prompt configuration
2. **Web channel** — for the chat widget (`demo_url: "https://chat-widgetv2.imbrace.co"`)
3. **Use-case template** — the card shown in the UI

The `workflow_name` is auto-generated as `<slug>_v<timestamp>` to ensure backend uniqueness (snake_case required):
```typescript
const slug = body.name.toLowerCase().replace(/[^a-z0-9]+/g, "_")
const workflowName = `${slug}_v${Date.now()}`
```

The assistant payload mirrors the frontend's `createCustomUseCase` hook from `new-frontend/src/pages/AIAssistantManagement/useAIAssistantFormHook.tsx`.

### AI Agent Update Flow

File: `api/src/routes/ai-agent.ts:215-287`

`PUT /ai-agent/:id` performs a **partial update** via PUT-merge:
1. Fetch current assistant via raw fetch to `GET /v3/ai/assistants/<id>` (SDK's `updateAssistant` uses full PUT — fields not in body get reset to null)
2. Merge requested fields into the current assistant payload
3. Update two groups:
   - **Assistant fields** (most settings): via SDK `client.chatAi.updateAssistant()`
   - **Template fields** (title + short_description): via SDK `client.agent.updateUseCase()`

---

## Workflow Node Architecture

### Node Tree Structure

Workflows use a **linked list** structure via `nextAction` pointers:

```typescript
// api/src/routes/workflow.ts — Workflow Version structure
{
  version: {
    trigger: {
      name: "trigger",
      type: "PIECE_TRIGGER" | "EMPTY" | "PIECE" | "ROUTER" | "LOOP_ON_ITEMS" | "CODE",
      displayName: string,
      settings: {
        pieceName: string,     // e.g. "@activepieces/piece-slack"
        pieceVersion: string,  // e.g. "0.3.9"
        triggerName?: string,
        actionName?: string,
        input: Record<string, any>,
        propertySettings: Record<string, any>,
        sampleData: Record<string, any>,
      },
      nextAction: { ... },     // ← linked list pointer
      children?: any[],         // ← ROUTER branches
      firstLoopAction?: any,    // ← LOOP_ON_ITEMS body
      valid: boolean,
    }
  }
}
```

### flattenNodes() Helper

File: `api/src/routes/workflow.ts:56-78`

Walks the full node tree (including `children[]` for ROUTER and `firstLoopAction` for LOOP_ON_ITEMS) to produce a flat list for display and targeting:

```typescript
function flattenNodes(trigger: any): any[] {
  const nodes: any[] = [];
  function visit(node: any) {
    if (!node) return;
    nodes.push({ name, type, displayName, pieceName, actionName, triggerName, input, valid });
    if (node.nextAction) visit(node.nextAction);
    for (const ch of (node.children || [])) if (ch) visit(ch);
    if (node.firstLoopAction) visit(node.firstLoopAction);
  }
  visit(trigger);
  return nodes;
}
```

### Operation Types (applyFlowOperation)

File: `api/src/routes/workflow.ts` — all node operations use Activepieces' `applyFlowOperation()`:

| Operation type | Used by | Code location |
|---|---|---|
| `UPDATE_TRIGGER` | `node add --type trigger`, `node update <trigger>` | Lines 311-330, 409-418 |
| `ADD_ACTION` | `node add --type action` | Lines 342-366 |
| `UPDATE_ACTION` | `node update <nodeName>` | Lines 409-418 |
| `DELETE_ACTION` | `node delete <nodeName>` | Lines 459-464 |
| `LOCK_AND_PUBLISH` | `workflow publish` | Lines 718-721 |
| `CHANGE_STATUS` | `workflow enable / disable` | Lines 733-736, 748-751 |
| `CHANGE_FOLDER` | `workflow move` | Lines 176-179 |

### Piece Schema Discovery

File: `api/src/routes/workflow.ts:237-258`

Piece details are fetched via **raw fetch** to `GET /activepieces/v1/pieces/<pieceName>` because the SDK's `listPieces()` only returns action/trigger counts, not the full field schemas needed to build node inputs.

### Connection Value Structure

File: `api/src/routes/workflow.ts:658-668`

For Activepieces connections, the API builds nested `value` objects:

- `SECRET_TEXT`: `{ type: "SECRET_TEXT", secret_text: token }`
- `BASIC_AUTH`: `{ type: "BASIC_AUTH", username, password }`
- Other types (OAUTH2, CLOUD_OAUTH2, CUSTOM_AUTH): caller supplies full structured value

---

## Project Structure

```
imbrace-cli/
├── api/                     ← Hono REST API (proxy)
│   └── src/
│       ├── index.ts              ← Entry, port 3456
│       ├── middleware/auth.ts    ← Auth via @imbrace/sdk
│       └── routes/
│           ├── auth.ts           ← POST /auth/login
│           ├── data-board.ts     ← CRUD /data-board/*
│           ├── ai-agent.ts       ← CRUD /ai-agent/*
│           └── workflow.ts       ← CRUD /workflow/*
│
└── cli/                     ← oclif CLI
    └── src/
        ├── base-command.ts       ← Auto-login
        ├── config.ts             ← Credential store (conf)
        ├── http.ts               ← HTTP client → API server
        ├── select-board.ts       ← Interactive board selector
        └── commands/
            ├── login.ts / logout.ts / whoami.ts
            ├── data-board/   (8 commands)
            ├── ai-agent/     (9 commands)
            └── workflow/     (20 commands across piece/ node/ conn/ folder/ mcp/)
```
