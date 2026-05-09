# Imbrace SDK

## Why Imbrace SDK?

    Full TypeScript definitions and Python type hints across all 27+ resource
    namespaces. Catch errors at compile time, not runtime.
    Built-in exponential backoff for 429 and 5xx responses. Zero configuration
    needed â€” your app stays alive under load.
    API Key, JWT Bearer, and legacy access token â€” all handled transparently.
    Switch auth strategy without changing business logic.
    Parallel `AsyncImbraceClient` alongside the sync client. Drop into FastAPI,
    asyncio, or Django with one import.

## Quick Install

TypeScript

    ```bash
    npm install @imbrace/sdk
    ```

    ```ts
    import { ImbraceClient } from "@imbrace/sdk";
    const client = new ImbraceClient();
    const me = await client.platform.getMe();
    ```

Python

    ```bash
    pip install imbrace
    ```

    ```python
    from imbrace import ImbraceClient
    client = ImbraceClient()
    me = client.platform.get_me()
    ```

## Explore the Docs

  - [SDK Overview](sdk/overview/)
  - [Quick Start](sdk/quick-start/)
  - [Authentication](sdk/authentication/)
  - [Full Flow Guide](sdk/full-flow-guide/)
  - [Testing Guide](guides/testing/)
  - [Troubleshooting](guides/troubleshooting/)