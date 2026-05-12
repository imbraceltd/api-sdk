# ✨ Imbrace SDK Monorepo

Official TypeScript and Python SDKs for the [Imbrace](https://imbrace.co) platform.

[![TypeScript](https://img.shields.io/npm/v/@imbrace/sdk?label=%40imbrace%2Fsdk&color=blue)](https://www.npmjs.com/package/@imbrace/sdk)
[![Python](https://img.shields.io/pypi/v/imbrace?label=imbrace&color=blue)](https://pypi.org/project/imbrace/)
[![Docs](https://img.shields.io/badge/docs-imbraceltd.github.io%2Fapi--sdk-blue)](https://imbraceltd.github.io/api-sdk/)

---

## Packages

| Directory | Package | Version | Runtime |
| --------- | ------- | ------- | ------- |
| [`ts/`](./ts) | [`@imbrace/sdk`](https://www.npmjs.com/package/@imbrace/sdk) | 1.0.4 | Node.js 18+, browser |
| [`py/`](./py) | [`imbrace`](https://pypi.org/project/imbrace/) | 1.0.4 | Python 3.9+ |

---

## Installation

**TypeScript / JavaScript**
```bash
npm install @imbrace/sdk
```

**Python**
```bash
pip install imbrace
```

---

## Quick Start

**TypeScript**
```typescript
import { ImbraceClient } from "@imbrace/sdk"

const client = new ImbraceClient({
  apiKey: process.env.IMBRACE_API_KEY,
})

const contacts = await client.contacts.list({ limit: 20 })
console.log(contacts.data)
```

**Python**
```python
from imbrace import ImbraceClient

with ImbraceClient() as client:
    contacts = client.contacts.list(limit=20)
    print(contacts["data"])
```

Set `IMBRACE_API_KEY` in your environment or `.env` file. Both SDKs read it automatically.

---

## Documentation

Full reference, authentication guides, and examples:

**[developer.imbrace.co](https://developer.imbrace.co/)**

Available in: English · Tiếng Việt · 简体中文 · 繁體中文

---

## Development Setup

### TypeScript SDK

```bash
cd ts
npm install
npm run build       # compile to dist/
npm run dev         # watch mode
npm run typecheck   # type check
npm run lint        # lint
npm test            # unit tests (no API key needed)
```

### Python SDK

```bash
cd py
pip install -e ".[dev]"   # install with dev tools
pytest tests/unit -v      # unit tests (no API key needed)
ruff check src/ tests/    # lint
mypy src/imbrace          # type check
```

### Docs Site

```bash
cd website
npm install
npm run dev     # dev server at localhost:4321
npm run build   # production build
```

---

## Integration Tests

Integration tests make real API calls and require credentials.

**TypeScript**
```bash
cd ts
IMBRACE_API_KEY=api_xxx npm run test:integration
```

**Python**

Create `py/.env`:
```env
IMBRACE_API_KEY=api_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
IMBRACE_ORG_ID=org_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Then:
```bash
cd py
pytest tests/integration -v -m integration
```

---

## Repository Structure

```
api-sdk/
├── ts/                  # TypeScript SDK (@imbrace/sdk)
│   ├── src/             # Source — client, resources, types
│   ├── tests/
│   │   ├── unit/        # Vitest unit tests
│   │   ├── integration/ # Live API tests
│   │   └── local/       # Local package link tests
│   └── dist/            # Compiled output (gitignored)
├── py/                  # Python SDK (imbrace)
│   ├── src/imbrace/     # Source — client, resources, types
│   └── tests/
│       ├── unit/        # pytest unit tests
│       └── integration/ # Live API tests
└── website/             # Docs site (Astro Starlight)
    └── src/content/docs/
        ├── (en root)
        ├── vi/
        ├── zh-cn/
        └── zh-tw/
```

---

## License

MIT — see [LICENSE](./LICENSE).
