# test-local-pkg/py — Local SDK integration tests (Python)

Mirror of `test-local-pkg/ts/` for the Python SDK. Installs `imbrace` as an
editable install of `../../py`, so edits to SDK source are picked up
immediately — no rebuild step.

## Setup

```bash
# 1. Create + activate a venv (recommended)
python3 -m venv .venv && source .venv/bin/activate

# 2. Install local SDK + deps
pip install -r requirements.txt
#   OR with uv:
#   uv pip install -e ../../py python-dotenv

# 3. Configure auth
cp .env.example .env
# edit .env — provide EITHER IMBRACE_API_KEY OR IMBRACE_ACCESS_TOKEN.
# IMBRACE_ORGANIZATION_ID is always required.
```

## Run

```bash
# v1.0.5 regression suite (9 fixes from commit ffb3708)
python test_regression_v1_0_5.py
```

Auth is auto-picked from `.env`:
- `IMBRACE_ACCESS_TOKEN` set → Access Token auth
- else `IMBRACE_API_KEY` → API Key auth

Run it twice (once with each .env var set) to cover both combos.
