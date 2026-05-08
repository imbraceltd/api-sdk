# Overview

Imbrace is a customer engagement platform â€” it handles chat channels, CRM pipelines, AI assistants, automated workflows, and document processing in one place. The SDK lets you embed those features directly into your own applications without building the infrastructure yourself.

### What You Can Build

- **AI chat assistants** â€” stream live responses from an AI assistant trained on your knowledge base
- **Automated workflows** â€” trigger and manage multi-step automations via Activepieces
- **CRM pipelines** â€” create boards, manage leads, search and export deal data
- **Document processing** â€” extract structured data from PDFs and invoices, generate embeddings

### Available SDKs

| SDK | Package | Runtime |
|---|---|---|
| TypeScript / JavaScript | `@imbrace/sdk` | Node.js 18+, browser |
| Python | `imbrace` | Python 3.9+ |

### Authentication

There are two ways to authenticate:

- **Access token** â€” for user-facing apps. Obtained after a user logs in via OTP or OAuth. Pass it as `accessToken` when initializing the client.
- **API key** â€” for server-to-server integrations. Generate one from the Imbrace admin dashboard. Pass it as `apiKey`.

### Gateway

All SDK requests route through:

```
https://app-gatewayv2.imbrace.co
```

The gateway is set by default â€” you do not need to configure it unless you are targeting a different environment.

### Quick Example

```typescript
import { ImbraceClient } from "@imbrace/sdk"

const client = new ImbraceClient({
  accessToken: "your-access-token",
  baseUrl: "https://app-gatewayv2.imbrace.co",
})

const stream = await client.aiAgent.streamChat({
  assistant_id: "asst_xxx",
  messages: [{ role: "user", content: "What deals closed this quarter?" }],
})
```

---