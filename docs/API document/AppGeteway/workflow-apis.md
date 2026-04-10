[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[App Gateway](https://devportal.dev.imbrace.co/docs/api-document/app-apis)

# Workflow APIs

Workflow APIs provide comprehensive workflow management capabilities including creating, updating, and managing automated workflows within your organization. These APIs enable you to build, deploy, and manage complex business processes and automation workflows.

# [Workflow APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#workflow-apis)

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#overview)

Workflow APIs allow you to manage automated workflows, business processes, and workflow templates within your iMBRACE workspace. These APIs provide the foundation for building sophisticated automation systems, managing workflow execution, and controlling business process flows.

---

## [1. Get workflow](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#1-get-workflow)

Retrieve all workflows available in the system.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/n8n/workflows`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/n8n/workflows`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/n8n/workflows`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
      {        "data": [            {                "id": "12845",                "name": "kong1",                "active": false,                "nodes": [                    {                        "parameters": {                            "icsTitle": "Start"                        },                        "name": "Start",                        "type": "n8n-nodes-base.start",                        "typeVersion": 1,                        "position": [                            62,                            334.5                        ],                        "nodeStyleVersion": 2                    },                    {                        "parameters": {                            "path": "05e73bb7-3c95-46fc-aa5a-94b2f34a1beb",                            "options": {},                            "icsTitle": "Webhook",                            "displayWebhookUrls": true,                            "retrigger": false,                            "authentication": "none",                            "httpMethod": "POST",                            "responseMode": "onReceived",                            "responseCode": 200                        },                        "name": "Webhook",                        "type": "n8n-nodes-base.webhook",                        "typeVersion": 1,                        "position": [                            140,                            400                        ],                        "webhookId": "05e73bb7-3c95-46fc-aa5a-94b2f34a1beb",                        "nodeStyleVersion": 2                    }                ],                "connections": {},                "createdAt": "2025-09-03T02:12:28.912Z",                "updatedAt": "2025-09-03T02:12:28.912Z",                "settings": {},                "staticData": null,                "description": null,                "tags": [                    {                        "id": "61",                        "name": "automation",                        "createdAt": "2022-12-09T09:46:44.442Z",                        "updatedAt": "2022-12-09T09:46:44.442Z"                    },                    {                        "id": "62",                        "name": "web",                        "createdAt": "2022-12-09T09:52:36.513Z",                        "updatedAt": "2022-12-09T09:52:36.513Z"                    }                ]            }        ]    }
  ```
* **Status code: 404 Not Found**

  ```
      {        "message": "Not Found"    }
  ```
* **Example:**

```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/n8n/workflows' \--header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \--data ''
```

## [2. Get workflow by Id](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#2-get-workflow-by-id)

Retrieve details of a workflow by its ID.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/n8n/workflows/{id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/n8n/workflows/{id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/n8n/workflows/{id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
      {        "data": {            "id": "12845",            "name": "kong1",            "active": false,            "nodes": [                {                    "parameters": {                        "icsTitle": "Start"                    },                    "name": "Start",                    "type": "n8n-nodes-base.start",                    "typeVersion": 1,                    "position": [                        62,                        334.5                    ],                    "nodeStyleVersion": 2                },                {                    "parameters": {                        "path": "05e73bb7-3c95-46fc-aa5a-94b2f34a1beb",                        "options": {},                        "icsTitle": "Webhook",                        "displayWebhookUrls": true,                        "retrigger": false,                        "authentication": "none",                        "httpMethod": "POST",                        "responseMode": "onReceived",                        "responseCode": 200                    },                    "name": "Webhook",                    "type": "n8n-nodes-base.webhook",                    "typeVersion": 1,                    "position": [                        140,                        400                    ],                    "webhookId": "05e73bb7-3c95-46fc-aa5a-94b2f34a1beb",                    "nodeStyleVersion": 2                }            ],            "connections": {},            "createdAt": "2025-09-03T02:12:28.912Z",            "updatedAt": "2025-09-03T02:12:28.912Z",            "settings": {},            "staticData": null,            "description": null,            "tags": [                {                    "id": "61",                    "name": "automation",                    "createdAt": "2022-12-09T09:46:44.442Z",                    "updatedAt": "2022-12-09T09:46:44.442Z"                },                {                    "id": "62",                    "name": "web",                    "createdAt": "2022-12-09T09:52:36.513Z",                    "updatedAt": "2022-12-09T09:52:36.513Z"                }            ]        }    }
  ```
* **Status code: 404 Not Found**

  ```
      {        "message": "Not Found"    }
  ```
* **Example:**

```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/n8n/workflows/12845' \--header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \--data ''
```

## [3. Get Workflows by Tag](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#3-get-workflows-by-tag)

Retrieve workflows filtered by specific tags.

This API allows you to fetch workflows that are associated with specific tags. It's useful for organizing and filtering workflows by categories, channels, or other classification systems.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/workflows?tag=automation`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/workflows?tag=automation`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/workflows?tag=automation`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
  * `Cookie`: `n8n-auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (optional, for n8n authentication)
* **Query Parameters:**

  * `tag` (string, required): Tag name to filter workflows by
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "id": "135",            "name": "Main workflow 1019",            "active": false,            "createdAt": "2022-10-19T07:20:09.299Z",            "updatedAt": "2022-10-19T07:20:09.299Z",            "tags": []        },        {            "id": "288",            "name": "Email Automation",            "active": false,            "createdAt": "2022-12-22T08:42:57.221Z",            "updatedAt": "2023-01-31T01:57:35.861Z",            "tags": [                {                    "id": "61",                    "name": "automation",                    "createdAt": "2022-12-09T09:46:44.442Z",                    "updatedAt": "2022-12-09T09:46:44.442Z"                }            ]        },        {            "id": "334",            "name": "My Automation",            "active": false,            "createdAt": "2023-01-13T04:31:36.050Z",            "updatedAt": "2023-01-13T04:31:36.050Z",            "tags": [                {                    "id": "61",                    "name": "automation",                    "createdAt": "2022-12-09T09:46:44.442Z",                    "updatedAt": "2022-12-09T09:46:44.442Z"                }            ]        }    ]}
  ```
* **Response Fields:**

  * `data` (array): Array of workflow objects matching the tag filter
* **Workflow Object Fields:**

  * `id` (string): Workflow identifier
  * `name` (string): Workflow name
  * `active` (boolean): Whether the workflow is currently active
  * `createdAt` (string): Workflow creation timestamp
  * `updatedAt` (string): Last update timestamp
  * `tags` (array): Array of tag objects associated with the workflow
  * `channel` (object, optional): Channel information if workflow is associated with a channel
    * `id` (string): Channel identifier
    * `is_init` (boolean): Whether this is an initialization channel
    * `type` (string): Channel type (web, whatsapp, facebook, etc.)
    * `name` (string): Channel name
* **Tag Object Fields:**

  * `id` (string): Tag identifier
  * `name` (string): Tag name
  * `createdAt` (string): Tag creation timestamp
  * `updatedAt` (string): Last update timestamp
* **Common Tag Types:**

  * `automation` - Automated workflows
  * `web` - Web widget workflows
  * `whatsapp` - WhatsApp channel workflows
  * `facebook` - Facebook channel workflows
  * `wechat` - WeChat channel workflows
  * `line` - LINE channel workflows
  * `email` - Email channel workflows
  * `preset` - Preset workflow templates
* **Error Responses:**

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```

  * **Status code: 403 Forbidden**

  ```
  {    "code": 40003,    "message": "Forbidden, insufficient permission"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/workflows?tag=automation' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Cookie: n8n-auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjhkZjE2MjBjLTUyNzUtNGM0NC1hNzY3LTI0ZjJjMTJlNGY4ZSIsImVtYWlsIjoiamFuZS5saW5AaW1icmFjZS5jbyIsInBhc3N3b3JkIjoiYWNiNzAxMjVhNTEzY2IxM2I3MjgxNWU3NjZkNmM4NDExMjJhZTliZDM3YWUzMDEzNmEwNzlkNzdhNjYzMTg5YSIsImlhdCI6MTY4NjA0NjkzMSwiZXhwIjoxNjg2NjUxNzMxfQ.vY4fWR0laOEVfy_5jeYZropI1tl8ro2FLIaPRMzKj-c'
  ```

## [4. Get workflow by Channel Type](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#4-get-workflow-by-channel-type)

Retrieve details of a workflow by its ID.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/workflows/channel_automation?channelType=web`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/workflows/channel_automation?channelType=web`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/workflows/channel_automation?channelType=web`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "id": "564",            "name": "test web widget automation",            "active": false,            "createdAt": "2023-03-06T03:55:26.627Z",            "updatedAt": "2023-03-06T03:55:33.918Z",            "tags": [                {                    "id": "61",                    "name": "automation",                    "createdAt": "2022-12-09T09:46:44.442Z",                    "updatedAt": "2022-12-09T09:46:44.442Z"                },                {                    "id": "62",                    "name": "web",                    "createdAt": "2022-12-09T09:52:36.513Z",                    "updatedAt": "2022-12-09T09:52:36.513Z"                }            ]        },        {            "id": "466",            "name": "Test widget channel automation",            "active": false,            "createdAt": "2023-02-15T07:25:45.228Z",            "updatedAt": "2023-02-15T07:26:03.300Z",            "tags": [                {                    "id": "61",                    "name": "automation",                    "createdAt": "2022-12-09T09:46:44.442Z",                    "updatedAt": "2022-12-09T09:46:44.442Z"                },                {                    "id": "62",                    "name": "web",                    "createdAt": "2022-12-09T09:52:36.513Z",                    "updatedAt": "2022-12-09T09:52:36.513Z"                }            ]        },        {            "id": "618",            "name": "testsetst",            "active": false,            "createdAt": "2023-03-13T07:05:15.771Z",            "updatedAt": "2023-03-13T07:05:18.726Z",            "tags": [                {                    "id": "61",                    "name": "automation",                    "createdAt": "2022-12-09T09:46:44.442Z",                    "updatedAt": "2022-12-09T09:46:44.442Z"                },                {                    "id": "62",                    "name": "web",                    "createdAt": "2022-12-09T09:52:36.513Z",                    "updatedAt": "2022-12-09T09:52:36.513Z"                }            ]        },        {            "id": "669",            "name": "New WF",            "active": true,            "createdAt": "2023-03-20T03:45:10.440Z",            "updatedAt": "2023-03-23T06:45:17.937Z",            "tags": [                {                    "id": "61",                    "name": "automation",                    "createdAt": "2022-12-09T09:46:44.442Z",                    "updatedAt": "2022-12-09T09:46:44.442Z"                },                {                    "id": "62",                    "name": "web",                    "createdAt": "2022-12-09T09:52:36.513Z",                    "updatedAt": "2022-12-09T09:52:36.513Z"                }            ]        }    ]}
  ```
* **Status code: 404 Not Found**

  ```
      {        "message": "Not Found"    }
  ```
* **Example:**

```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/workflows/channel_automation?channelType=web' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
```

## [5. Get Credentials](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#5-get-credentials)

Retrieve all credentials available in the system.

This API allows you to fetch all credentials that are stored in the system. Credentials are used for authentication with external services and APIs within workflows.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/n8n/credentials`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/n8n/credentials`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/n8n/credentials`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  * No request body required
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "id": "1",            "name": "My Credential",            "type": "httpBasicAuth",            "data": "encrypted_credential_data",            "createdAt": "2022-10-19T07:20:09.299Z",            "updatedAt": "2022-10-19T07:20:09.299Z"        },        {            "id": "2",            "name": "API Key Credential",            "type": "httpHeaderAuth",            "data": "encrypted_credential_data",            "createdAt": "2022-12-22T08:42:57.221Z",            "updatedAt": "2023-01-31T01:57:35.861Z"        }    ]}
  ```
* **Error Responses:**

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```

  * **Status code: 403 Forbidden**

  ```
  {    "code": 40003,    "message": "Forbidden, insufficient permission"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/n8n/credentials' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--data ''
  ```

## [6. Get workflow by Channel Type](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#6-get-workflow-by-channel-type)

Retrieve details of a workflow by its ID.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/users/:user_id/workflows`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/users/:user_id/workflows`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/users/:user_id/workflows`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "id": "755",            "name": "My workflow 45",            "active": false        },        {            "id": "1086",            "name": "My workflow 46",            "active": false        }    ]}
  ```
* **Status code: 404 Not Found**

  ```
      {        "message": "Not Found"    }
  ```
* **Example:**

```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/users/u_5e336d97-e26d-4c6b-9452-36c90bd0769f/workflows' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
```

## [7. Get workflow by Credential id](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#7-get-workflow-by-credential-id)

Retrieve details of a workflow by its ID.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/workflow/credentials/:credential_id`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/workflow/credentials/:credential_id`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/workflow/credentials/:credential_id`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  // {{host}}/v1/workflow/credentials/{{credential_id}}{    "data": {        "id": "11",        "name": "Web Widget account ",        "type": "WebWidget",        "nodesAccess": [            {                "nodeType": "n8n-nodes-base.WebWidgetTrigger",                "date": "2022-05-19T09:49:39.853Z"            }        ],        "createdAt": "2022-05-19T09:49:39.858Z",        "updatedAt": "2022-09-04T15:24:16.223Z"    }}
  ```
* **Status code: 404 Not Found**

  ```
      {        "message": "Not Found"    }
  ```
* **Example:**

```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/workflow/credentials/11' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
```

## [8. Update Workflow](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#8-update-workflow)

Update an existing workflow with new configuration and settings.

This API allows you to modify an existing workflow by updating its name, active status, nodes, connections, and other properties. This is useful for making changes to workflow logic, adding new nodes, or updating workflow settings.

* **Endpoint for Product:** `PATCH https://app-gateway.imbrace.co/v1/backend/workflow/{workflow_id}`
* **Endpoint for Demo:** `PATCH https://app-gateway.demo.imbrace.co/v1/backend/workflow/{workflow_id}`
* **Endpoint for Dev:** `PATCH https://app-gateway.dev.imbrace.co/v1/backend/workflow/{workflow_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `workflow_id` (string, required): The unique identifier of the workflow to update
* **Request Body (JSON):**

  ```
  {    "id": "47",    "name": "My workflow",    "active": false,    "nodes": [        {            "parameters": {                "icsTitle": "Start"            },            "name": "Start",            "type": "n8n-nodes-base.start",            "typeVersion": 1,            "position": [320, 300]        }    ],    "connections": {},    "createdAt": "2022-07-22T10:57:40.815Z",    "updatedAt": "2022-07-22T10:57:50.939Z",    "settings": {},    "staticData": null,    "tags": []}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "id": "47",    "name": "My workflow",    "active": false,    "nodes": [        {            "parameters": {                "icsTitle": "Start"            },            "name": "Start",            "type": "n8n-nodes-base.start",            "typeVersion": 1,            "position": [320, 300]        }    ],    "connections": {},    "createdAt": "2022-07-22T10:57:40.815Z",    "updatedAt": "2022-07-22T10:57:50.939Z",    "settings": {},    "staticData": null,    "tags": []}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid workflow data"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "code": 40004,    "message": "Workflow not found"}
  ```
* **Example:**

  ```
  curl --location --request PATCH 'https://app-gateway.dev.imbrace.co/v1/backend/workflow/11' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "id":"47",    "name":"My workflow",    "active":false,    "nodes":[        {            "parameters":            {"icsTitle":"Start"},            "name":"Start",            "type":"n8n-nodes-base.start",            "typeVersion":1,            "position":[320,300]        }    ],    "connections":{},    "createdAt":"2022-07-22T10:57:40.815Z",    "updatedAt":"2022-07-22T10:57:50.939Z",    "settings":{},    "staticData":null,    "tags":[]}'
  ```

## [9. Update Credential](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#9-update-credential)

Update an existing credential with new configuration and data.

This API allows you to modify an existing credential by updating its name, type, data, and node access permissions. This is useful for updating authentication details, changing credential names, or modifying access permissions for external service integrations.

* **Endpoint for Product:** `PATCH https://app-gateway.imbrace.co/v1/backend/workflow/credentials/{credential_id}`
* **Endpoint for Demo:** `PATCH https://app-gateway.demo.imbrace.co/v1/backend/workflow/credentials/{credential_id}`
* **Endpoint for Dev:** `PATCH https://app-gateway.dev.imbrace.co/v1/backend/workflow/credentials/{credential_id}`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `credential_id` (string, required): The unique identifier of the credential to update
* **Request Body (JSON):**

  ```
  {    "id": "45",    "name": "Odoo account 2",    "type": "odooApi",    "data": {        "url": "http://imbrace.odoo.com/",        "username": "michael.wong@imbrace.co",        "password": "NotASecret",        "db": "imbraceDB"    },    "nodesAccess": []}
  ```
* **Request Parameters:**

  * `id` (string, required): Credential identifier
  * `name` (string, required): Updated credential name
  * `type` (string, required): Credential type (e.g., odooApi, httpBasicAuth, etc.)
  * `data` (object, required): Credential-specific data containing authentication details
    * `url` (string): Service URL
    * `username` (string): Username for authentication
    * `password` (string): Password for authentication
    * `db` (string): Database name (for Odoo API)
  * `nodesAccess` (array, required): Array of nodes that can access this credential
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": {        "id": "45",        "name": "Odoo account 2",        "type": "odooApi",        "nodesAccess": [],        "createdAt": "2022-09-08T08:10:33.562Z",        "updatedAt": "2022-09-08T08:33:48.484Z"    }}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid credential data"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "code": 40004,    "message": "Credential not found"}
  ```
* **Example:**

  ```
  curl --location --request PATCH 'https://app-gateway.dev.imbrace.co/v1/backend/workflow/credentials/45' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--data-raw '{    "id": "45",    "name": "Odoo account 2",    "type": "odooApi",    "data": {        "url": "http://imbrace.odoo.com/",        "username": "michael.wong@imbrace.co",        "password": "NotASecret",        "db": "imbraceDB"    },    "nodesAccess": []}'
  ```

## [10. Create Workflow](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#10-create-workflow)

Create a new workflow with specified nodes, connections, and settings.

This API allows you to create a new workflow by defining its name, nodes, connections between nodes, and other configuration settings. This is useful for building new automation workflows from scratch or creating workflow templates.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/workflow`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/workflow`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/workflow`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON):**

  ```
  {    "name": "My workflow 3",    "nodes": [        {            "parameters": {                "icsTitle": "Start"            },            "name": "Start",            "type": "n8n-nodes-base.start",            "typeVersion": 1,            "position": [240, 300]        },        {            "parameters": {                "icsTitle": "Reddit",                "resource": "post",                "operation": "create",                "subreddit": "",                "kind": "self",                "title": "",                "text": ""            },            "name": "Reddit",            "type": "n8n-nodes-base.reddit",            "typeVersion": 1,            "position": [400, 300]        }    ],    "connections": {        "Start": {            "main": [                [                    {                        "node": "Reddit",                        "type": "main",                        "index": 0                    }                ]            ]        }    },    "active": false,    "settings": {},    "tags": []}
  ```
* **Result:**

  * **Status code: 201 Created**

  ```
  {    "id": "12345",    "name": "My workflow 3",    "active": false,    "nodes": [        {            "parameters": {                "icsTitle": "Start"            },            "name": "Start",            "type": "n8n-nodes-base.start",            "typeVersion": 1,            "position": [240, 300]        },        {            "parameters": {                "icsTitle": "Reddit",                "resource": "post",                "operation": "create",                "subreddit": "",                "kind": "self",                "title": "",                "text": ""            },            "name": "Reddit",            "type": "n8n-nodes-base.reddit",            "typeVersion": 1,            "position": [400, 300]        }    ],    "connections": {        "Start": {            "main": [                [                    {                        "node": "Reddit",                        "type": "main",                        "index": 0                    }                ]            ]        }    },    "createdAt": "2025-01-27T10:30:00.000Z",    "updatedAt": "2025-01-27T10:30:00.000Z",    "settings": {},    "staticData": null,    "tags": []}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid workflow configuration"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```

  * **Status code: 409 Conflict**

  ```
  {    "code": 40009,    "message": "Workflow with this name already exists"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/workflow' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "name": "My workflow 3",    "nodes": [        {            "parameters": {                "icsTitle": "Start"            },            "name": "Start",            "type": "n8n-nodes-base.start",            "typeVersion": 1,            "position": [240, 300]        },        {            "parameters": {                "icsTitle": "Reddit",                "resource": "post",                "operation": "create",                "subreddit": "",                "kind": "self",                "title": "",                "text": ""            },            "name": "Reddit",            "type": "n8n-nodes-base.reddit",            "typeVersion": 1,            "position": [400, 300]        }    ],    "connections": {        "Start": {            "main": [                [                    {                        "node": "Reddit",                        "type": "main",                        "index": 0                    }                ]            ]        }    },    "active": false,    "settings": {},    "tags": []}'
  ```

## [11. Save Workflow](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#11-save-workflow)

Save a new workflow with specified nodes, connections, and credentials.

This API allows you to save a new workflow by defining its name, nodes, connections, credentials, and other configuration settings. This is useful for creating workflows with specific credentials and trigger configurations.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/n8n/workflows`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/n8n/workflows`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/n8n/workflows`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON):**

  ```
  {    "name": "Save new workflow 測試 - web widget",    "nodes": [        {            "parameters": {                "icsTitle": "Start"            },            "name": "Start",            "type": "n8n-nodes-base.start",            "typeVersion": 1,            "position": [240, 300]        },        {            "parameters": {                "options": {},                "icsTitle": "Web Widget Trigger",                "retrigger": false            },            "name": "Web Widget Trigger",            "type": "n8n-nodes-base.WebWidgetTrigger",            "typeVersion": 1,            "position": [540, 300],            "credentials": {                "WebWidget": {                    "id": "30",                    "name": "Demo-test (Web widget)"                }            }        }    ],    "connections": {},    "active": false,    "settings": {},    "tags": [],    "id": "78"}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": {        "id": "79",        "name": "Save new workflow 測試 - web widget",        "nodes": [            {                "parameters": {                    "icsTitle": "Start"                },                "name": "Start",                "type": "n8n-nodes-base.start",                "typeVersion": 1,                "position": [240, 300]            },            {                "parameters": {                    "options": {},                    "icsTitle": "Web Widget Trigger",                    "retrigger": false                },                "name": "Web Widget Trigger",                "type": "n8n-nodes-base.WebWidgetTrigger",                "typeVersion": 1,                "position": [540, 300],                "credentials": {                    "WebWidget": {                        "id": "30",                        "name": "Demo-test (Web widget)"                    }                }            }        ],        "connections": {},        "active": false,        "settings": {},        "tags": [],        "staticData": null,        "createdAt": "2022-09-21T06:20:50.139Z",        "updatedAt": "2022-09-21T06:20:50.139Z"    }}
  ```
* **Response Fields:**

  * `data` (object): Saved workflow object
    * `id` (string): Generated workflow identifier
    * `name` (string): Workflow name
    * `nodes` (array): Array of workflow nodes with credentials
    * `connections` (object): Workflow node connections
    * `active` (boolean): Workflow active status
    * `settings` (object): Workflow settings
    * `tags` (array): Array of workflow tags
    * `staticData` (object|null): Static data for the workflow
    * `createdAt` (string): Workflow creation timestamp
    * `updatedAt` (string): Last update timestamp
* **Common Trigger Node Types:**

  * `n8n-nodes-base.WebWidgetTrigger` - Web widget trigger
  * `n8n-nodes-base.webhook` - Webhook trigger
  * `n8n-nodes-base.scheduleTrigger` - Schedule trigger
  * `n8n-nodes-base.emailTrigger` - Email trigger
  * `n8n-nodes-base.manualTrigger` - Manual trigger
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid workflow configuration"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "code": 40004,    "message": "Credential not found"}
  ```
* **Example:**

  ```
  Getting Started
  A quick introduction to the Developer Portal and how to begin building your first app.

  1. What You Can Do Here
  The iMBRACE Developer Portal lets you:

  Create and manage app integrations (a.k.a. Journeys)
  Link your hosted UI and embed it via iframe
  Test the app using Dev Test URL
  Publish your app to the public Marketplace
  2. Sign In
  👉 Visit: https://app.imbrace.co

  🔑 Select Developer Portal Mode
  Make sure to select “Developer Portal” to access the developer environment.

  You will then see the login screen with multiple options:

  Login via email and password
  Continue with Google or Microsoft
  Sign in with OTP (One-Time Password)
  If you don’t have an account, click "Sign Up For An Account".

  Select Developer Mode
  3. Developer Workspace Overview
  Once logged in, you'll enter the Developer Workspace, which includes:

  My Apps: All your apps in one place
  Data Boards, Workflows, AI Agent, and Settings
  Status filters:
  ✅ Published
  🕒 In Review
  📝 Draft
  Click Create New App to begin your first integration.

  4. Create an App
  Learn how to build and publish a new app using the Dev Portal's guided wizard.

  Creating an app is a 4-step process:

  Step 1: App Details
  Fill in:

  App Name
  Description
  App Icon (120×120 px)
  Cover Picture (664×385 px)
  Categories (optional)
  ✅ Click NEXT.

  Step 2: Link Your App UI
  Paste your hosted App UI URL.

  The platform embeds this via iframe
  A Dev Test URL is generated
  Preview appears live in the dashboard
  ✅ Click NEXT.

  Step 3: Test the App
  Use the Dev Test URL to simulate actual user behavior.

  Checklist:

  ✅ UI URL is reachable
  ✅ Workflow is connected
  ✅ Test preview renders correctly
  Click Test Now. Once validated, move to the final step.

  Step 4: Submit for Review
  If all tests pass:

  You’ll see a confirmation message
  The app status becomes In Review
  It now appears in the Marketplace review queue
  🔒 Need to Publish?
  To publish your app to the live Marketplace, please contact the system administrator.

  📧 Email: superadmin@imbrace.co

  The admin team will verify and approve the app for public listing.

  You're done! 🎉
  You’ve now completed the creation and submission process for your application.

  5. Manage Apps
  Learn how to edit, test, update, or delete your apps in the Developer Workspace.

  5.1. Edit App Details
  From the My Apps section, click EDIT.

  You can update:

  App name, description
  Icon or cover image
  UI URL
  Linked workflow
  Categories
  Click UPDATE to apply changes.

  5.2. Preview and Test
  Use the Preview and Test tab to:

  View the Dev Test URL
  See a live iframe preview
  Click Expand Preview for full size
  This helps you validate UI behavior without leaving the portal.

  5.3. App Status and Actions
  In the Status tab, you can:

  View:

  ✅ Current Status: Draft / In Review / Published
  📌 App Version
  📈 Total installs
  Take action:

  Deactivate: Temporarily unpublish the app
  Delete App: Permanently remove it
  ⚠️ Deleting an app is irreversible and will remove it from both workspace and marketplace.curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/n8n/workflows' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--data '{    "name": "Save new workflow 測試 - web widget",    "nodes": [        {            "parameters": {                "icsTitle": "Start"            },            "name": "Start",            "type": "n8n-nodes-base.start",            "typeVersion": 1,            "position": [240, 300]        },        {            "parameters": {                "options": {},                "icsTitle": "Web Widget Trigger",                "retrigger": false            },            "name": "Web Widget Trigger",            "type": "n8n-nodes-base.WebWidgetTrigger",            "typeVersion": 1,            "position": [540, 300],            "credentials": {                "WebWidget": {                    "id": "30",                    "name": "Demo-test (Web widget)"                }            }        }    ],    "connections": {},    "active": false,    "settings": {},    "tags": [],    "id": "78"}'
  ```

## [12. Create Credential](https://devportal.dev.imbrace.co/docs/api-document/app-apis/workflow#12-create-credential)

Create a new credential with specified configuration and data.

This API allows you to create a new credential by defining its name, type, data, and node access permissions. This is useful for setting up authentication details for external service integrations within workflows.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/workflow/credentials`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/workflow/credentials`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/workflow/credentials`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON):**

  ```
  {    "id": "",    "name": "Odoo account 2",    "type": "odooApi",    "data": {        "url": "http://imbrace.odoo.com/",        "username": "michael.wong@imbrace.co",        "password": "secrethehe",        "db": "imbraceDB"    },    "nodesAccess": []}
  ```
* **Request Parameters:**

  * `id` (string, optional): Credential identifier (empty string for new credentials)
  * `name` (string, required): Name of the credential
  * `type` (string, required): Credential type (e.g., odooApi, httpBasicAuth, etc.)
  * `data` (object, required): Credential-specific data containing authentication details
    * `url` (string): Service URL
    * `username` (string): Username for authentication
    * `password` (string): Password for authentication
    * `db` (string): Database name (for Odoo API)
  * `nodesAccess` (array, required): Array of nodes that can access this credential
* **Result:**

  * **Status code: 201 Created**

  ```
  {    "data": {        "id": "46",        "name": "Odoo account 2",        "type": "odooApi",        "nodesAccess": [],        "createdAt": "2025-01-27T10:30:00.000Z",        "updatedAt": "2025-01-27T10:30:00.000Z"    }}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid credential data"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```

  * **Status code: 409 Conflict**

  ```
  {    "code": 40009,    "message": "Credential with this name already exists"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/workflow/credentials' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--data-raw '{    "id": "",    "name": "Odoo account 2",    "type": "odooApi",    "data": {        "url": "http://imbrace.odoo.com/",        "username": "michael.wong@imbrace.co",        "password": "secrethehe",        "db": "imbraceDB"    },    "nodesAccess": []}'
  ```
