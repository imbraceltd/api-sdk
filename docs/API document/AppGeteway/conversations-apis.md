[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[App Gateway](https://devportal.dev.imbrace.co/docs/api-document/app-apis)

# Conversations apis

The Conversations APIs provide a centralized way to manage users, their contact information, and communication history across multiple channels. These APIs are essential for building a unified customer or user communication system. They allow you to

---

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations#overview)

The following APIs help you manage contact data and active conversations for your teams and channels.

---

### [1. Get Conversation View Count by Business Unit](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations#1-get-conversation-view-count-by-business-unit)

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/team_conversations/_views_count?type=business_unit_id&q=bu_imbrace_testing`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/team_conversations/_views_count?type=business_unit_id&q=bu_imbrace_testing`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/team_conversations/_views_count?type=business_unit_id&q=bu_imbrace_testing`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "all": 975,    "yours": 293,    "closed": 61,    "spam": 0,    "online": 0,    "rep_needed": 567,    "pending": 101,    "soon_to_be": 0,    "overdue": 229,    "t_imbrace_default_team": 930,    "t_44370caa-a1ba-4e88-9040-4997251061e8": 1,    "t_b680c5f1-255b-4e09-8b3d-5b6e2bbb58a0": 0,    "t_4ffefd06-ab08-4035-9c21-6ab5e97271cf": 8,    "t_7faa1c32-f4f8-42ab-86a1-257d3a1583c2": 0,    "t_840ceccf-5b62-4fed-a677-7084b8e7f9c1": 2,    "t_14d7e3c3-de90-49a5-89fb-d71e02a49537": 0,    "t_df344a60-04d7-4791-b0d7-1a0227d53079": 0,    "t_596edf28-bf97-4668-9263-bfac26d4ff8d": 2,    "t_c8d75364-17a9-4e6c-945e-d989eb5e707f": 2,    "t_ee0f3d9b-03e7-4ec4-ad96-4c565fcd02a5": 0,    "t_ab40a925-e6d5-41ad-b885-28fb740a0abc": 0,    "t_339f37b2-22f0-439d-b82c-a61956f4c2fd": 2,    "t_f989f50e-a8d7-4e22-bbb2-fbde10393fd7": 0,    "t_ec83ad2d-ef76-451e-99a1-1e695fcdebc4": 0,    "t_9e5294df-e7a4-4119-be55-a30e16d8e813": 2,    "t_32c57386-a5fe-40e2-b9c5-b236adbfe1eb": 0,    "t_7b7b858e-7ee9-4108-9896-d64d0fb6380b": 0,    "t_912c8e28-93ac-42f1-81d3-daea01795d03": 0,    "t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333": 0,    "t_50fd5451-0342-48c2-bed8-888abf752181": 10,    "t_90c54b8a-c06e-439a-8844-d5798d5acf8c": 8,    "t_7b6b71d1-8623-496b-9106-1d545f9eb5aa": 0,    "t_e9886f36-9612-4c25-9759-76049a5a63fb": 0,    "t_3a9d2635-ca64-401f-93f3-ccd7fbd9bc9e": 8,    "null": 0}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/team_conversations/_views_count' \--header 'x-access-: https://app-gateway.dev.imbrace.co'
  ```

### [2. Channel Conversation Count](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations#2-channel-conversation-count)

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/channels/_conv_count?view=all`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/channels/_conv_count?view=all`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/channels/_conv_count?view=all`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "web": 757,    "facebook": 46,    "whatsapp": 111,    "instagram": 48,    "wechat": 0,    "line": 13,    "email": 0,    "wecom": 0,    "all": 975}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/team_conversations/_views_count' \--header 'x-access-: https://app-gateway.dev.imbrace.co'
  ```

### [3. Get All Chatroom (conversation)](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations#3-get-all-chatroom-conversation)

Retrieve a count of conversations segmented by channel type (web, WhatsApp, Facebook, etc.).

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/channels/_conv_count?team_id={team_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/channels/_conv_count?team_id={team_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/channels/_conv_count?team_id={team_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
    {      "web": 7,      "facebook": 0,      "whatsapp": 1,      "instagram": 0,      "wechat": 0,      "line": 0,      "email": 0,      "wecom": 0,      "all": 8  }
  ```

  * **Status code: 400 Not Found**

  ```
       {         "message": "Not Found"     }
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/channels/_conv_count?team_id=t_4ffefd06-ab08-4035-9c21-6ab5e97271cf' \--header 'x-access-token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df'
  ```

### [4. Create Conversation](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations#4-create-conversation)

Create a new conversation for a contact across different channels.

This API allows you to create a new conversation for a contact, which can be used for tracking communication history and managing customer interactions across various channels.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/conversation`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/conversation`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/conversation`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body:**

  * Empty body (no data required)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "conversation",    "id": "conv_f8ca2a03-b7f5-4060-a988-c9c90d48c284",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "channel_id": "imbrace_channel",    "channel_type": "web",    "contact_id": "con_da38689f-ac07-476f-90d9-4a45ec327337",    "status": "active",    "name": "Guest#753342@7 Apr 2022",    "timestamp": "2022-04-07T04:11:28.148Z",    "users": [        {            "object_name": "simple_user",            "id": "u_imbrace_bot",            "display_name": "imbrace bot",            "avatar_url": ""        }    ]}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid request"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/conversation' \--header 'X-Access-Token: ch_a97ef358-3625-412a-a328-8f5661f13ef1' \--data ''
  ```

### [5. Get Conversation Messages](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations#5-get-conversation-messages)

Retrieve messages from a conversation with pagination support.

This API allows you to fetch messages from a specific conversation with pagination controls. It's useful for building chat interfaces, message history views, and conversation management systems.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/conversation_messages?limit=10&skip=0`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/conversation_messages?limit=10&skip=0`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/conversation_messages?limit=10&skip=0`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * `limit` (number, optional): Number of messages per page (default: 10)
  * `skip` (number, optional): Number of messages to skip for pagination (default: 0)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "list",    "data": [        {            "object_name": "message",            "id": "msg_efb6b7f0-5ef2-422d-ad09-4b4ce6eb8bb2",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "conversation_id": "conv_testing_conversation1",            "from": "con_test_contact",            "type": "quick_reply",            "content": {                "title": "what ever payload provided in quick_replies option",                "payload": "what ever payload provided in quick_replies option"            },            "created_at": "2022-03-31T15:12:41.496Z",            "updated_at": "2022-03-31T15:12:41.496Z"        },        {            "object_name": "message",            "id": "msg_00ebf998-0d13-4062-9f42-eff19ffbc4b5",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "conversation_id": "conv_testing_conversation1",            "from": "con_test_contact",            "type": "text",            "content": {                "text": "Hello"            },            "created_at": "2022-03-31T15:10:33.193Z",            "updated_at": "2022-03-31T15:10:33.193Z"        }    ],    "nested": {},    "has_more": true,    "count": 15,    "total": 10}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid request parameters"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/conversation_messages?limit=10&skip=0' \--header 'X-Access-Token: {{contact_id}}' \--data ''
  ```

### [6. Send Message to Conversation](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations#6-send-message-to-conversation)

Send a message to a conversation.

This API allows you to send a message to a specific conversation. It supports different message types including text, images, and interactive elements like quick replies.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/conversation_messages`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/conversation_messages`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/conversation_messages`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "type": "text",    "text": "Hello"}
  ```
* **Request Parameters:**

  * `type` (string, required): Message type (text, image, quick_reply, etc.)
  * `text` (string, required for text messages): Text content of the message
  * `url` (string, optional for image messages): URL of the image
  * `caption` (string, optional for image messages): Caption for the image
  * `title` (string, optional for quick_reply messages): Title of the quick reply button
  * `payload` (string, optional for quick_reply messages): Payload of the quick reply button
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "message",    "id": "msg_7c9ba4d9-9bd5-4149-8c4d-0a02fd2a0573",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "channel_id": "imbrace_channel",    "channel_type": "web",    "conversation_id": "conv_testing_conversation1",    "from": "con_test_contact",    "type": "text",    "content": {        "text": "Hello"    },    "created_at": "2022-03-31T15:08:11.650Z",    "updated_at": "2022-03-31T15:08:11.650Z"}
  ```
* **Message Types:**

  * **Text Messages:**

  ```
  {    "type": "text",    "text": "Hello World"}
  ```

  * **Image Messages:**

  ```
  {    "type": "image",    "url": "http://image.url",    "caption": "Image caption"}
  ```

  * **Quick Reply Messages:**

  ```
  {    "type": "quick_reply",    "title": "title from reponse options",    "payload": "what ever payload provided in quick_replies option"}
  ```

  * **File Messages:**

  ```
  {    "type": "file",    "url": "http://pdf.url",    "caption": "this url is invalid XD1"}
  ```

  * **PDF Messages:**

  ```
  {    "type": "pdf",    "url": "http://pdf.url",    "caption": "this url is invalid XD1"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid message type or content"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/conversation_messages' \--header 'X-Access-Token: {{contact_id}}' \--header 'Content-Type: application/json' \--data '{    "type": "text",    "text": "Hello"}'
  ```

### [7. Search Organization Messages](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations#7-search-organization-messages)

Search for messages within an organization using Meilisearch.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/meilisearch/{organization_id}/search`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/meilisearch/{organization_id}/search`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/meilisearch/{organization_id}/search`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {    "limit": 100,    "q": ""}
  ```
* **Parameters:**

  * `limit` (number, optional): Maximum number of results to return (default: 100)
  * `q` (string, optional): Search query string
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "success": true,    "message": {        "hits": [            {                "_id": "msg_c0dbd66d-06ed-4883-bdac-36f5d56a4d5f",                "doc_name": "message",                "public_id": "msg_c0dbd66d-06ed-4883-bdac-36f5d56a4d5f",                "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",                "business_unit_id": "bu_be188361-fbec-4505-9a05-d9d34a5d5961",                "conversation_id": "conv_bd2b66bd-9381-4a57-9f2f-6cae180dd815",                "from": "u_d61efde6-9379-49b5-a095-2dcad27fe7a5",                "type": "text",                "content": {                    "text": "Hi there^! How can I help you today?",                    "is_mail": false,                    "subtext": "",                    "message_id": "",                    "sequence_number": 0,                    "postMessage": {},                    "counter": null,                    "tool_calls": ""                },                "created_at": "2025-07-16T07:55:51.602Z",                "updated_at": "2025-07-16T07:55:51.602Z",                "fields_timestamp": {}            }        ],        "query": "",        "processingTimeMs": 0,        "limit": 100,        "offset": 0,        "estimatedTotalHits": 0    }}
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/meilisearch/org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd/search' \    --header 'Content-Type: application/json' \    --header 'X-Access-Token: acc_20bea5ac-9e26-4864-b60f-ae7834c2c63e' \    --data '{        "limit": 100,        "q": ""    }'
  ```

## [8. Fetch Organization Messages](https://devportal.dev.imbrace.co/docs/api-document/app-apis/conversations#8-fetch-organization-messages)

Fetch messages from an organization with specific filters using Meilisearch.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/meilisearch/{organization_id}/fetch`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/meilisearch/{organization_id}/fetch`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/meilisearch/{organization_id}/fetch`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {    "filter": "fields.64ba48e32261fdc660addf02 = Male",    "limit": 10000}
  ```
* **Parameters:**

  * `filter` (string, required): Filter expression for field values
  * `limit` (number, optional): Maximum number of results to return
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "success": true,    "message": {        "results": [],        "offset": 0,        "limit": 10000,        "total": 0    }}
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/meilisearch/org_imbrace/fetch' \    --header 'Content-Type: application/json' \    --header 'X-Access-Token: acc_20bea5ac-9e26-4864-b60f-ae7834c2c63e' \    --data '{        "filter": "fields.64ba48e32261fdc660addf02 = Male",        "limit": 10000    }'
  ```
