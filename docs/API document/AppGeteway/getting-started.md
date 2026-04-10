# Getting Started

Welcome to the iMBRACE App APIs! This guide will help you get started with building applications using our comprehensive API suite.

## [What are App APIs?](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#what-are-app-apis)

The **iMBRACE App APIs** provide a complete set of REST APIs that enable you to build custom applications that integrate with the iMBRACE platform. Use these APIs to create web applications, mobile apps, or integrate with existing systems.

## [Quick Setup](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#quick-setup)

1. **Get API Access** - Contact our team for API credentials
2. **Authenticate** - Use OTP-based authentication to get access tokens
3. **Start Building** - Use our APIs to build your custom applications

## [API Documentation](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#api-documentation)

Explore our comprehensive API documentation:

### [🔐 Authentication &amp; User Management](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#-authentication--user-management)

* **[User Management APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_userManagement)** - OTP authentication, organization management, and account information

### [📊 Data Management](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#-data-management)

* **[Board APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis)** - Create and manage data boards with custom fields and operations

### [💬 Communication](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#-communication)

* **[Contacts APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis)** - Contact management and conversation tracking
* **[Conversations APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations)** - Advanced conversation and message management
* **[Channel APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/channel)** - Multi-channel communication (WhatsApp, Facebook, Web, Email, etc.)

### [🤖 AI &amp; Automation](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#-ai--automation)

* **[AI Agent APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis)** - AI-powered automation and intelligent workflows
* **[Workflow APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow)** - Business process automation and workflow management

### [👥 Team &amp; Organization](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#-team--organization)

* **[Team APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team)** - Team management and role-based access control
* **[Setting APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting)** - Message templates, email templates, and user management

## [Environments](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#environments)

| Environment           | Base URL | Purpose                 |
| --------------------- | -------- | ----------------------- |
| **Production**  |          | Live environment        |
| **Demo**        |          | Testing environment     |
| **Development** |          | Development environment |

## [Authentication](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#authentication)

```
# 1. Request OTP
curl -X POST https://app-gateway.imbrace.co/v1/backend/login/_signin_email_request \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@example.com"}'

# 2. Verify OTP and get access token
curl -X POST https://app-gateway.imbrace.co/v1/login/_signin_with_email \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@example.com", "otp": "123456"}'
```

## [Next Steps](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_gettingStarted#next-steps)

1. **Start with Authentication** - Set up OTP-based authentication
2. **Choose Your APIs** - Select the APIs that match your use case
3. **Read the Documentation** - Explore detailed endpoint documentation
4. **Build Your Application** - Start integrating with our APIs

Need help? Contact our support team for assistance with your integration.
