
# Conversation APIs

Conversation APIs provide functionality to manage and retrieve conversation messages within your organization. These APIs allow you to access message history, conversation details, and message interactions.

---

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/conversations#overview)

The Conversation APIs enable you to retrieve and manage conversation messages within your organization. Conversations represent communication threads between users and contacts, containing various message types including text, quick replies, responses, and other interactive content.

---

## [1. Get Conversation Messages](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/conversations#1-get-conversation-messages)

Retrieve all messages from a specific conversation with pagination support.

This API allows you to fetch all messages from a conversation by providing the conversation ID. It returns a paginated list of messages with their content, timestamps, and metadata. Messages are returned in reverse chronological order (newest first).

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/conversations/{conversation_id}/messages?limit={limit}&skip={skip}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/conversations/{conversation_id}/messages?limit={limit}&skip={skip}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/conversations/{conversation_id}/messages?limit={limit}&skip={skip}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `conversation_id` (string, required): The unique identifier of the conversation (format: `conv_*`)
* **Query Parameters:**

  * `limit` (number, optional): Maximum number of messages to return (default: 10)
  * `skip` (number, optional): Number of messages to skip for pagination (default: 0)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "items": [        {            "_id": "msg_c41ae57d-a851-4556-b79b-e9b3cce8e2d9",            "doc_name": "message",            "public_id": "msg_c41ae57d-a851-4556-b79b-e9b3cce8e2d9",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "conversation_id": "conv_f262dad4-dcb1-44b9-8d7e-407b022dc4b7",            "from": "con_1b1a92ca-af43-48c2-80bf-663a5458263f",            "type": "quick_reply",            "content": {                "title": "Red",                "payload": "0_iMBrace x DEV - Imbrace TW",                "description": ""            },            "created_at": "2024-12-10T09:53:17.127Z",            "updated_at": "2024-12-10T09:53:17.127Z"        },        {            "_id": "msg_86889109-cecf-4fa0-b237-2fe2dc92cde4",            "doc_name": "message",            "public_id": "msg_86889109-cecf-4fa0-b237-2fe2dc92cde4",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "conversation_id": "conv_f262dad4-dcb1-44b9-8d7e-407b022dc4b7",            "from": "u_71585462-0af0-4581-a72b-e82141dcb1c2",            "type": "response",            "content": {                "title": "",                "text": "Jane test MC from Postman",                "quick_replies": [                    {                        "id": 0,                        "content_type": "text",                        "title": "Red",                        "payload": "0_iMBrace x DEV - Imbrace TW"                    },                    {                        "id": 1,                        "content_type": "text",                        "title": "Blue",                        "payload": "1_iMBrace x DEV - Imbrace TW"                    },                    {                        "id": 2,                        "content_type": "text",                        "title": "White",                        "payload": "2_iMBrace x DEV - Imbrace TW"                    }                ]            },            "created_at": "2024-12-10T09:53:09.246Z",            "updated_at": "2024-12-10T09:53:09.246Z"        },        {            "_id": "msg_18c859c2-88c3-4ff5-a2c6-7c638e7a6bee",            "doc_name": "message",            "public_id": "msg_18c859c2-88c3-4ff5-a2c6-7c638e7a6bee",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "conversation_id": "conv_f262dad4-dcb1-44b9-8d7e-407b022dc4b7",            "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",            "type": "text",            "content": {                "text": "okokokokokok",                "is_mail": false            },            "created_at": "2024-12-10T09:51:51.910Z",            "updated_at": "2024-12-10T09:51:51.910Z"        }    ],    "count": 304,    "total": 10,    "has_more": true}
  ```
* **Response Fields:**

  * `items` (array): Array of message objects
    * `_id` (string): Internal message identifier
    * `doc_name` (string): Document type name ("message")
    * `public_id` (string): Public message identifier (format: `msg_*`)
    * `organization_id` (string): Organization the message belongs to
    * `business_unit_id` (string): Business unit identifier
    * `conversation_id` (string): Conversation this message belongs to
    * `from` (string): Sender identifier (user ID or contact ID)
    * `type` (string): Message type (e.g., "text", "quick_reply", "response")
    * `content` (object): Message content structure (varies by message type)
      * For `text` messages:
        * `text` (string): Message text content
        * `is_mail` (boolean): Whether message is marked as mail
      * For `quick_reply` messages:
        * `title` (string): Quick reply button title
        * `payload` (string): Quick reply payload data
        * `description` (string): Quick reply description
      * For `response` messages:
        * `title` (string): Response title
        * `text` (string): Response text content
        * `quick_replies` (array): Array of quick reply options
          * `id` (number): Quick reply option ID
          * `content_type` (string): Content type ("text")
          * `title` (string): Option title
          * `payload` (string): Option payload
    * `created_at` (string): Message creation timestamp
    * `updated_at` (string): Last update timestamp
  * `count` (number): Total number of messages in the conversation
  * `total` (number): Number of messages returned in this response
  * `has_more` (boolean): Whether there are more messages available
* **Message Types:**

  * `text`: Simple text messages
  * `quick_reply`: Quick reply button selections
  * `response`: Messages with quick reply options
  * `image`: Image messages
  * `file`: File attachments
  * `location`: Location sharing
  * `contact`: Contact sharing
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "conversation_id is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "Conversation not found"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/conversations/conv_f262dad4-dcb1-44b9-8d7e-407b022dc4b7/messages?limit=10&skip=0' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```

---

## [2. Get Conversation Links by Phone Numbers](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/conversations#2-get-conversation-links-by-phone-numbers)

Retrieve conversation links associated with specific phone numbers within an organization.

This API allows you to fetch conversation links by providing one or more phone numbers and the organization ID. It returns the conversation links that are associated with the specified phone numbers, enabling you to find existing conversations for contacts.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/conversations/links?phone_numbers={phone_number}&organization_id={organization_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/conversations/links?phone_numbers={phone_number}&organization_id={organization_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/conversations/links?phone_numbers={phone_number}&organization_id={organization_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Query Parameters:**

  * `phone_numbers` (string, required): One or more phone numbers to search for. Multiple phone numbers can be provided by repeating the parameter (e.g., `phone_numbers=886911425977&phone_numbers=12345678`)
  * `organization_id` (string, required): The unique identifier of the organization
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "phone_number": "886911425977",        "conversation_links": [            {                "link": "https://webapp.dev.imbrace.co/chatroom-routing?conv_id=conv_85130be2-db16-435e-910e-8c21b5cb2044",                "created_at": "2024-08-16T09:53:34.868Z"            },            {                "link": "https://webapp.dev.imbrace.co/chatroom-routing?conv_id=conv_e2db3e49-a82a-43ef-912c-345e123d2b19",                "created_at": "2024-08-16T07:25:50.293Z"            },            {                "link": "https://webapp.dev.imbrace.co/chatroom-routing?conv_id=conv_205e3bc5-774a-45fc-b604-2a762a86262f",                "created_at": "2024-01-25T09:30:20.414Z"            }        ]    },    {        "phone_number": "12345678",        "conversation_links": []    }]
  ```
* **Response Fields:**

  * `data` (array): Array of conversation link objects
    * `phone_number` (string): The phone number associated with the conversation
    * `conversation_id` (string): The unique identifier of the conversation (format: `conv_*`)
    * `contact_id` (string): The unique identifier of the contact (format: `con_*`)
    * `organization_id` (string): The organization the conversation belongs to
    * `created_at` (string): Conversation link creation timestamp
    * `updated_at` (string): Last update timestamp
  * `count` (number): Total number of conversation links found
  * `found` (number): Number of phone numbers that had associated conversations
  * `not_found` (array): Array of phone numbers that did not have associated conversations
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "phone_numbers is required"}
  ```

  ```
  {    "message": "organization_id is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "No conversations found for the provided phone numbers"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/conversations/links?phone_numbers=886911425977&phone_numbers=12345678&organization_id=org_imbrace' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```
