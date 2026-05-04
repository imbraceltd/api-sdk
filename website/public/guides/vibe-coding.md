# Vibe Coding

> Use the Imbrace SDK faster by dropping llms.txt into your AI coding assistant — Claude, Cursor, Copilot, or any LLM-powered IDE.

**Vibe Coding** means writing code by collaborating with an AI assistant — describing what you want in plain language and letting the AI generate, explain, or refactor the code for you. The Imbrace SDK ships an [`llms.txt`](https://imbraceltd.github.io/api-sdk/llms.txt) file so any AI tool can instantly understand the SDK without hallucinating method names or argument shapes.

## What is `llms.txt`?

`llms.txt` is a plain-text file (similar to `robots.txt`) that gives AI models a compact, accurate summary of a library — its clients, resources, authentication, and common patterns. When you paste it into an AI context window, the model already knows the SDK and can write correct code on the first try.

**File URL:** [`https://imbraceltd.github.io/api-sdk/llms.txt`](https://imbraceltd.github.io/api-sdk/llms.txt)

## How to use it

### Claude (claude.ai or Claude Code)

1. Open a new conversation.
2. Paste the contents of `llms.txt` at the top of your message, then describe your task:

```
<context>
[paste llms.txt here]
</context>

Write a TypeScript snippet that streams a chat response from assistant "asst_abc"
and prints each text delta to the console.
```

### Cursor / VS Code Copilot

Add the URL to your AI context via **@ docs** or the equivalent "add context" feature in your IDE. Cursor supports `@URL` directly:

```
@https://imbraceltd.github.io/api-sdk/llms.txt

How do I upload a file and trigger embedding processing?
```

### Any other LLM

Copy the raw file content and paste it at the start of your prompt before asking your question. Most LLMs with a 32k+ context window can ingest the full file without summarisation loss.

## Example prompts

Once the AI has the `llms.txt` context, try prompts like:

- *"Show me how to create an AI assistant and stream a chat response in Python."*
- *"Generate TypeScript code to list all embedding files and delete ones with status `error`."*
- *"What's the difference between `streamChat` and `streamSubAgentChat`?"*
- *"Write an Express.js auth proxy for the Chat Client, following the Integrations guide pattern."*

> For long sessions keep `llms.txt` pinned as a **system prompt** or **project instruction** so it applies to every message automatically.

## Keep it up to date

The file is regenerated on every release. Re-fetch the URL if you upgrade the SDK to pick up new methods or changed signatures.
