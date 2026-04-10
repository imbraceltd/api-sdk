# Getting Started

Welcome to the iMBRACE Server Gateway! This guide will help you get started with our server-to-server API integration.

## [What is Server Gateway?](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#what-is-server-gateway)

The **Server Gateway** provides APIs that allow your server or workflow engine to call iMBRACE services directly. This is designed for:

* **Server-to-Server Integration** - Your backend systems calling iMBRACE APIs
* **Workflow Engine Integration** - Workflow engines like n8n, Zapier, or custom systems
* **Data Synchronization** - Automated data flow between your systems and iMBRACE
* **Bulk Operations** - Processing large datasets programmatically

## [Quick Setup](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#quick-setup)

1. **Get Access Token** - Contact iMBRACE support for your organization's access token
2. **Configure Your Server** - Set up your server or workflow engine to call iMBRACE APIs
3. **Start Integrating** - Begin calling iMBRACE services from your systems

## [Authentication](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#authentication)

Server Gateway uses token-based authentication. Include your token in every request:

```
curl -H "x-access-token: your-access-token-here" \     -H "Content-Type: application/json" \     https://app-gateway.dev.imbrace.co/3rd/boards
```

## [Environments](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#environments)

| Environment           | Base URL                                     | Purpose                 |
| --------------------- | -------------------------------------------- | ----------------------- |
| **Production**  | `https://app-gateway.imbrace.co/3rd/`      | Live environment        |
| **Demo**        | `https://app-gateway.demo.imbrace.co/3rd/` | Testing environment     |
| **Development** | `https://app-gateway.dev.imbrace.co/3rd/`  | Development environment |

## [API Documentation](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#api-documentation)

### [📊 Data Board APIs](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#-data-board-apis)

* **[Data Board Management](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard)** - Complete data board operations, CRUD operations, field management, and bulk data processing

### [🤖 AI Agent Server Gateway APIs](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#-ai-agent-server-gateway-apis)

* **[AI Agent Server Gateway APIs](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis)** - Complete AI Agent operations, RAG operations, and ECharts operations

## [Common Use Cases](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#common-use-cases)

### [Workflow Engine Integration](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#workflow-engine-integration)

```
# Your workflow engine calls iMBRACE APIsPOST /3rd/boards/create/brd_123/board_itemsPUT /3rd/boards/update/brd_123/board_itemsGET /3rd/boards/brd_123/export_csv
```

### [Server Integration](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#server-integration)

```
# Your server synchronizes data with iMBRACEGET /3rd/boards/{board_id}/board_itemsPOST /3rd/board_search/{board_id}/searchPOST /3rd/boards/{board_id}/import_csv
```

### [Data Pipeline](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#data-pipeline)

```
# Automated data processing workflowsPOST /3rd/boards/_fileuploadPOST /3rd/boards/{board_id}/import_csvGET /3rd/boards/{board_id}/export_csv
```

## [Next Steps](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/_gettingStarted#next-steps)

1. **Get Your Token** - Contact iMBRACE support for access
2. **Read the Documentation** - Explore detailed API documentation
3. **Set Up Your Integration** - Configure your server or workflow engine
4. **Test Your Integration** - Start with development environment
5. **Deploy to Production** - Move to production when ready

Need help? Contact our support team for assistance with your server integration.
