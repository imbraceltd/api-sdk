"""Shared local-SDK test bootstrap.

Mirrors test-local-pkg/ts/utils/utils.ts: installs the SDK from ../../py
(editable, so source edits are picked up immediately) and exposes a single
`client` that auto-picks API Key vs Access Token from .env.
"""
from __future__ import annotations
import os
import sys

from dotenv import load_dotenv

load_dotenv()

from imbrace import ImbraceClient  # editable install of ../../py

API_KEY      = os.environ.get("IMBRACE_API_KEY")
ACCESS_TOKEN = os.environ.get("IMBRACE_ACCESS_TOKEN")
ORG_ID       = os.environ.get("IMBRACE_ORGANIZATION_ID")
GATEWAY      = os.environ.get("IMBRACE_GATEWAY_URL", "https://app-gatewayv2.imbrace.co")
TIMEOUT      = int(os.environ.get("IMBRACE_TIMEOUT", "60"))

if (not API_KEY and not ACCESS_TOKEN) or not ORG_ID:
    print("ERROR: Missing configuration in .env!")
    print("Required: (IMBRACE_API_KEY OR IMBRACE_ACCESS_TOKEN) AND IMBRACE_ORGANIZATION_ID")
    sys.exit(1)

USE_ACCESS_TOKEN = bool(ACCESS_TOKEN)
AUTH_MODE = "ACCESS TOKEN" if USE_ACCESS_TOKEN else "API KEY"

client = ImbraceClient(
    api_key=API_KEY if not USE_ACCESS_TOKEN else None,
    access_token=ACCESS_TOKEN if USE_ACCESS_TOKEN else None,
    organization_id=ORG_ID,
    gateway=GATEWAY,
    timeout=TIMEOUT,
)
