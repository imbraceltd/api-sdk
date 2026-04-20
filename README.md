# 🌌 Imbrace SDK Monorepo

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](./ts)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](./py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

Welcome to the **Imbrace SDK Monorepo**. This unified repository houses the professional-grade SDKs used to interface with the Imbrace Gateway, providing seamless integration for both frontend and backend ecosystems.

---

## 🏗️ Architecture at a Glance

Our SDKs are built with a focus on **type safety**, **predictability**, and **performance**. Both languages share a unified resource-based domain model covering:

*   **Core Services**: Marketplace, Platform, Channel, IPS, Agent, AI
*   **Transport Layer**: Robust HTTP handling with automatic retries and error mapping
*   **Authentication**: Support for both Client-side Access Tokens and Server-side API Keys

---

## 📂 Repository Structure

| Directory | Language | Description |
| :--- | :--- | :--- |
| [**`ts/`**](./ts) | **TypeScript** | The `@imbrace/sdk` package for Node.js and Browser environments. |
| [**`py/`**](./py) | **Python** | The `imbrace` Python package for backend integrations. |
| [**`docs/`**](./docs) | **Guides** | Comprehensive documentation, architecture diagrams, and test guides. |

---

## 📚 Essential Documentation

Dive deep into the implementation and usage details:

*   📖 **[Core Guide](./docs/document_en.md)** — Comprehensive guide on SDK logic and testing.
*   📘 **[TypeScript SDK Guide](./ts/README.md)** — Installation and usage for JS/TS developers.
*   🐍 **[Python SDK Guide](./py/README.md)** — Integration details for Python/FastAPI/Django.

---

## 🛠️ Developer Setup

### 📦 TypeScript / JavaScript
```bash
cd ts
npm install
npm run build
```

### 🐍 Python
```bash
cd py
pip install -e ".[dev]"
```

---

## 🧪 Quality Assurance

We maintain a high standard of code quality through rigorous testing. See the [**Testing Documentation**](./docs/document_en.md) for:
- ✅ **Unit Tests**: Mocked HTTP layers for lightning-fast local validation.
- 🌐 **Integration Tests**: End-to-end verification against `app-gatewayv2.imbrace.co`.
- 🛠️ **Linting**: Consistent code style enforced by ESLint, Ruff, and MyPy.

---

<div align="center">
  <sub>Built with ❤️ by the Imbrace Team</sub>
</div>
