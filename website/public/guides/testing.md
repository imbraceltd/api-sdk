## Testing Guide

Unit tests run offline (no server needed). Integration tests call the real API and require a valid API key.

### TypeScript — Unit Tests

```bash
npm test
# or
npx vitest run tests/unit/http.test.ts
```

### TypeScript — Integration Tests

```bash
IMBRACE_API_KEY=api_xxx npm run test:integration
```

### Python — Unit Tests

```bash
cd py
pytest tests/unit -v
# Run a specific test
pytest tests/unit/test_http.py::test_401_raises_auth_error -v
```

### Python — Integration Tests

```bash
cd py
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration
```

### Coverage Report (Python)

```bash
pytest tests/unit --cov=src/imbrace --cov-report=term-missing
```

### Lint & Type Check

**TypeScript:**
```bash
npm run typecheck
npm run lint
```

**Python:**
```bash
cd py
ruff check src/ tests/
mypy src/imbrace
```
