[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[App Gateway](https://devportal.dev.imbrace.co/docs/api-document/app-apis)

# Setting APIs

Setting APIs provide comprehensive message template management capabilities including creating, updating, and managing message templates within your organization. These APIs enable you to organize message templates, manage categories, and control template access across your iMBRACE workspace.

# [Setting APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#setting-apis)

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#overview)

Setting APIs allow you to manage message templates, categories, and template configurations within your iMBRACE workspace. These APIs provide the foundation for organizing message templates, managing template categories, and controlling template access across different features and communication channels.

---

## [1. Get Message Templates with Filtering and Pagination](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#1-get-message-templates-with-filtering-and-pagination)

Retrieve message templates with advanced filtering, pagination, and sorting options.

This API allows you to fetch message templates with specific filters, pagination controls, and sorting. It's useful for building message template management interfaces with search, filtering, and pagination capabilities.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/message_templates?business_unit_id=bu_imbrace_testing&limit=20&skip=0&sort=-updated_at&fields=title`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/message_templates?business_unit_id=bu_imbrace_testing&limit=20&skip=0&sort=-updated_at&fields=title`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/message_templates?business_unit_id=bu_imbrace_testing&limit=20&skip=0&sort=-updated_at&fields=title`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * `business_unit_id` (string, required): The unique identifier of the business unit
  * `limit` (number, optional): Number of results per page (default: 20)
  * `skip` (number, optional): Number of results to skip for pagination (default: 0)
  * `sort` (string, optional): Sort field and direction (e.g., "-updated_at" for descending)
  * `fields` (string, optional): Comma-separated list of fields to include in response
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "_id": "mtemp_b34b8597-064c-4f4f-b920-8e55011baced",            "doc_name": "message_template",            "public_id": "mtemp_b34b8597-064c-4f4f-b920-8e55011baced",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "title": "hi",            "text": "hi {{1}}{{2}}",            "categories": [],            "created_at": "2024-12-19T04:32:08.249Z",            "updated_at": "2024-12-19T04:32:08.249Z",            "template_language": "en",            "category": null,            "lang": {                "_id": "67b5506c547dae5afbef7bda",                "code": "en",                "doc_name": "languages",                "name": {                    "en": "English",                    "cn": "English",                    "zh": "English"                },                "__v": 0            }        }    ],    "has_more": true,    "count": 66,    "total": 20,    "skip": 0}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/message_templates?business_unit_id=bu_imbrace_testing&limit=20&skip=0&sort=-updated_at&fields=title' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [2. Search Email Templates](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#2-search-email-templates)

Search and retrieve email templates with pagination and filtering options.

This API allows you to search for email templates with pagination controls and filtering. It's useful for building email template management interfaces with search, filtering, and pagination capabilities.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/marketplaces/email-templates/search?limit=20&skip=0`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/marketplaces/email-templates/search?limit=20&skip=0`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/marketplaces/email-templates/search?limit=20&skip=0`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * `limit` (number, optional): Number of results per page (default: 20)
  * `skip` (number, optional): Number of results to skip for pagination (default: 0)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "_id": "ema_43687b9b-6d2b-4c46-9a06-2e4a7e77f7e7",            "doc_name": "EmailTemplate",            "name": "Chien test Template",            "subject": "d",            "body": "<p>Test 16 normak</p><p><span class=\"ql-size-large\" style=\"color: rgb(202, 65, 65);\">test 24 normal</span></p><p><span class=\"ql-size-small\">test 12 normal</span></p><p><span class=\"ql-size-huge\">test 42 normal</span></p><p><br></p><p><strong><em>test B U I 16</em></strong></p><p><strong class=\"ql-size-large\"><u>test BU 24</u></strong></p><p><em class=\"ql-size-small\"><u>test UI 12</u></em></p><p><strong class=\"ql-size-huge\" style=\"background-color: rgb(174, 35, 35);\"><em>test BI 42</em></strong></p><p><br></p><ol><li>test ul li 16</li><li><span class=\"ql-size-small\">test ul li 42</span></li></ol><ul><li>test ol li 16</li><li><span class=\"ql-size-huge\">test ol li 42</span></li></ul><p><br></p><p><a href=\"https://qrcode-page.imbrace.co?id=tp_0cc97469-88dd-4f14-a99f-a0396fec5731&env=demo\" rel=\"noopener noreferrer\" target=\"_blank\">test href 16</a></p><p><a href=\"https://qrcode-page.imbrace.co/?id=tp_0cc97469-88dd-4f14-a99f-a0396fec5731&env=demo\" rel=\"noopener noreferrer\" target=\"_blank\" class=\"ql-size-large\">test href 42</a></p>",            "status": "draft",            "category": {                "id": "cat_f8568268-2475-4311-ac21-de21b304dfec",                "name": "Chien test Catagory"            },            "organization_id": "org_imbrace",            "attachments": [],            "updated_at": "2025-01-14T07:13:42.934Z",            "links": [],            "public_id": "897841f7-745a-4aa2-ac13-ab4e62936776",            "created_at": "2024-10-03T07:59:16.007Z"        }    ],    "meta": {        "count": 95,        "skip": 0,        "limit": 20,        "total": 5,        "has_more": true    }}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/marketplaces/email-templates/search?limit=20&skip=0' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [3. Update Email Template](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#3-update-email-template)

Update an existing email template's information including name, subject, body, and category.

This API allows you to modify email template properties such as name, subject, HTML body content, category, and attachments. It's useful for email template management interfaces where users need to update template content and settings.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/v2/backend/marketplaces/email-templates/{template_id}`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/v2/backend/marketplaces/email-templates/{template_id}`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/v2/backend/marketplaces/email-templates/{template_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `template_id` (string, required): The unique identifier of the email template to update
* **Request Body (JSON)**

  ```
  {    "name": "Chien test Template",    "category": "cat_f8568268-2475-4311-ac21-de21b304dfec",    "subject": "Test",    "body": "<p>Test 16 normak</p><p><span style=\"color: rgb(202, 65, 65);\" class=\"ql-size-large\">test 24 normal</span></p><p><span class=\"ql-size-small\">test 12 normal</span></p><p><span class=\"ql-size-huge\">test 42 normal</span></p><p><br></p><p><strong><em>test B U I 16</em></strong></p><p><strong class=\"ql-size-large\"><u>test BU 24</u></strong></p><p><em class=\"ql-size-small\"><u>test UI 12</u></em></p><p><strong style=\"background-color: rgb(174, 35, 35);\" class=\"ql-size-huge\"><em>test BI 42</em></strong></p><p><br></p><ol><li>test ul li 16</li><li><span class=\"ql-size-small\">test ul li 42</span></li></ol><ul><li>test ol li 16</li><li><span class=\"ql-size-huge\">test ol li 42</span></li></ul><p><br></p><p><a href=\"https://qrcode-page.imbrace.co?id=tp_0cc97469-88dd-4f14-a99f-a0396fec5731&env=demo\" rel=\"noopener noreferrer\" target=\"_blank\">test href 16</a></p><p><a href=\"https://qrcode-page.imbrace.co/?id=tp_0cc97469-88dd-4f14-a99f-a0396fec5731&env=demo\" rel=\"noopener noreferrer\" target=\"_blank\" class=\"ql-size-large\">test href 42</a></p>",    "attachments": []}
  ```
* **Request Parameters:**

  * `name` (string, required): The name of the email template
  * `category` (string, required): The category ID for the template
  * `subject` (string, required): The email subject line
  * `body` (string, required): The HTML email body content
  * `attachments` (array, optional): Array of attachment objects
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": {        "_id": "ema_43687b9b-6d2b-4c46-9a06-2e4a7e77f7e7",        "doc_name": "EmailTemplate",        "name": "Chien test Template",        "subject": "Test",        "body": "<p>Test 16 normak</p><p><span style=\"color: rgb(202, 65, 65);\" class=\"ql-size-large\">test 24 normal</span></p><p><span class=\"ql-size-small\">test 12 normal</span></p><p><span class=\"ql-size-huge\">test 42 normal</span></p><p><br></p><p><strong><em>test B U I 16</em></strong></p><p><strong class=\"ql-size-large\"><u>test BU 24</u></strong></p><p><em class=\"ql-size-small\"><u>test UI 12</u></em></p><p><strong style=\"background-color: rgb(174, 35, 35);\" class=\"ql-size-huge\"><em>test BI 42</em></strong></p><p><br></p><ol><li>test ul li 16</li><li><span class=\"ql-size-small\">test ul li 42</span></li></ol><ul><li>test ol li 16</li><li><span class=\"ql-size-huge\">test ol li 42</span></li></ul><p><br></p><p><a href=\"https://qrcode-page.imbrace.co?id=tp_0cc97469-88dd-4f14-a99f-a0396fec5731&env=demo\" rel=\"noopener noreferrer\" target=\"_blank\">test href 16</a></p><p><a href=\"https://qrcode-page.imbrace.co/?id=tp_0cc97469-88dd-4f14-a99f-a0396fec5731&env=demo\" rel=\"noopener noreferrer\" target=\"_blank\" class=\"ql-size-large\">test href 42</a></p>",        "status": "draft",        "category": "cat_f8568268-2475-4311-ac21-de21b304dfec",        "organization_id": "org_imbrace",        "attachments": [],        "updated_at": "2025-10-20T08:19:27.618Z",        "links": [],        "public_id": "897841f7-745a-4aa2-ac13-ab4e62936776",        "created_at": "2024-10-03T07:59:16.007Z"    }}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Template not found"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```

  * **Status code: 403 Forbidden**

  ```
  {    "code": 40003,    "message": "Forbidden, insufficient permission"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "code": 40004,    "message": "Email template not found"}
  ```
* **Example:**

  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/v2/backend/marketplaces/email-templates/ema_43687b9b-6d2b-4c46-9a06-2e4a7e77f7e7' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "name": "Chien test Template",    "category": "cat_f8568268-2475-4311-ac21-de21b304dfec",    "subject": "Test",    "body": "<p>Test 16 normak</p><p><span style=\"color: rgb(202, 65, 65);\" class=\"ql-size-large\">test 24 normal</span></p><p><span class=\"ql-size-small\">test 12 normal</span></p><p><span class=\"ql-size-huge\">test 42 normal</span></p><p><br></p><p><strong><em>test B U I 16</em></strong></p><p><strong class=\"ql-size-large\"><u>test BU 24</u></strong></p><p><em class=\"ql-size-small\"><u>test UI 12</u></em></p><p><strong style=\"background-color: rgb(174, 35, 35);\" class=\"ql-size-huge\"><em>test BI 42</em></strong></p><p><br></p><ol><li>test ul li 16</li><li><span class=\"ql-size-small\">test ul li 42</span></li></ol><ul><li>test ol li 16</li><li><span class=\"ql-size-huge\">test ol li 42</span></li></ul><p><br></p><p><a href=\"https://qrcode-page.imbrace.co?id=tp_0cc97469-88dd-4f14-a99f-a0396fec5731&env=demo\" rel=\"noopener noreferrer\" target=\"_blank\">test href 16</a></p><p><a href=\"https://qrcode-page.imbrace.co/?id=tp_0cc97469-88dd-4f14-a99f-a0396fec5731&env=demo\" rel=\"noopener noreferrer\" target=\"_blank\" class=\"ql-size-large\">test href 42</a></p>",    "attachments": []}'
  ```

## [4. Get Categories](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#4-get-categories)

Retrieve all available categories for organizing templates and content.

This API allows you to fetch all categories available in the system. It's useful for template management interfaces where you need to display available categories for organizing templates and other content.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/categories`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/categories`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/categories`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * None
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "_id": "cat_imbrace_operation",            "doc_name": "category",            "apply_to": [],            "is_default": true,            "is_deleted": false,            "organization_id": "default",            "name": "Operation",            "description": "Operation",            "public_id": "cat_imbrace_operation",            "created_at": "2024-07-17T06:29:11.226Z",            "id": "cat_imbrace_operation"        },        {            "_id": "cat_imbrace_marketing",            "doc_name": "category",            "apply_to": [],            "is_default": true,            "is_deleted": false,            "organization_id": "default",            "name": "Marketing",            "description": "Marketing",            "public_id": "cat_imbrace_marketing",            "created_at": "2024-07-17T06:29:11.184Z",            "id": "cat_imbrace_marketing"        },        {            "_id": "cat_f8568268-2475-4311-ac21-de21b304dfec",            "doc_name": "category",            "name": "Chien test Catagory",            "description": "Chien test Catagory",            "apply_to": [],            "is_default": false,            "organization_id": "org_imbrace",            "is_deleted": false,            "public_id": "cat_f8568268-2475-4311-ac21-de21b304dfec",            "created_at": "2024-09-27T05:26:42.660Z",            "id": "cat_f8568268-2475-4311-ac21-de21b304dfec"        }    ]}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/categories' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [5. Create Category](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#5-create-category)

Create a new category for organizing templates and content.

This API allows you to create a new category for organizing templates and other content within your organization. Categories help structure and organize content for better management and user experience.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/api/v1/backend/categories`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/api/v1/backend/categories`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/api/v1/backend/categories`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "name": "Test",    "description": "test api"}
  ```
* **Request Parameters:**

  * `name` (string, required): The name of the category
  * `description` (string, required): Description of the category
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "doc_name": "category",    "name": "Test",    "description": "test api",    "apply_to": [],    "is_default": false,    "organization_id": "org_imbrace",    "is_deleted": false,    "_id": "cat_60a90614-bd7c-4ef4-935c-58aabded19f9",    "public_id": "cat_60a90614-bd7c-4ef4-935c-58aabded19f9",    "created_at": "2025-10-20T08:26:03.536Z",    "id": "cat_60a90614-bd7c-4ef4-935c-58aabded19f9"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Category name already exists"}
  ```

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
  curl --location 'https://app-gateway.dev.imbrace.co/api/v1/backend/categories' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "name": "Test",    "description": "test api"}'
  ```

## [6. Create Email Template](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#6-create-email-template)

Create a new email template with rich HTML content and category assignment.

This API allows you to create a new email template with HTML body content, subject line, and category assignment. Email templates support rich text formatting and can be used for automated email communications.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v2/backend/marketplaces/email-templates`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v2/backend/marketplaces/email-templates`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v2/backend/marketplaces/email-templates`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "name": "Vani Test",    "category": "cat_60a90614-bd7c-4ef4-935c-58aabded19f9",    "subject": "Vani Test",    "body": "<p>Test</p><p><strong>Test</strong></p><p><span class=\"ql-font-monospace\">Test</span></p>",    "attachments": []}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": {        "doc_name": "EmailTemplate",        "name": "Vani Test",        "subject": "Vani Test",        "body": "<p>Test</p><p><strong>Test</strong></p><p><span class=\"ql-font-monospace\">Test</span></p>",        "status": "draft",        "category": "cat_60a90614-bd7c-4ef4-935c-58aabded19f9",        "organization_id": "org_imbrace",        "attachments": [],        "_id": "ema_c4b95444-8fe9-45f5-9009-671cfadaf110",        "updated_at": "2025-10-20T08:29:03.334Z",        "links": [],        "public_id": "72361b02-3233-488a-968c-83d0c639de08",        "created_at": "2025-10-20T08:29:03.334Z"    }}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/marketplaces/email-templates' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "name": "Vani Test",    "category": "cat_60a90614-bd7c-4ef4-935c-58aabded19f9",    "subject": "Vani Test",    "body": "<p>Test</p><p><strong>Test</strong></p><p><span class=\"ql-font-monospace\">Test</span></p>",    "attachments": []}'
  ```

## [7. Create Message Template](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#7-create-message-template)

Create a new message template with text content and category assignment.

This API allows you to create a new message template with text content, language specification, and category assignment. Message templates support variable placeholders and can be used for automated messaging across different channels.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/message_templates`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/message_templates`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/message_templates`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "title": "Vani test",    "category": "cat_60a90614-bd7c-4ef4-935c-58aabded19f9",    "template_language": "en",    "text": "Hello {name}",    "business_unit_id": "bu_imbrace_testing"}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "message_template",    "id": "mtemp_50044713-c63e-474f-8b12-083d74f74668",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "title": "Vani test",    "text": "Hello {name}",    "categories": [],    "created_at": "2025-10-20T08:35:49.084Z",    "updated_at": "2025-10-20T08:35:49.084Z",    "template_language": "en"}
  ```
* **Response Fields:**

  * `object_name` (string): Object type identifier ("message_template")
  * `id` (string): Message template identifier
  * `organization_id` (string): Organization the template belongs to
  * `business_unit_id` (string): Business unit the template belongs to
  * `title` (string): Message template title
  * `text` (string): Message text content with variable placeholders
  * `categories` (array): Array of category IDs (empty by default)
  * `created_at` (string): Template creation timestamp
  * `updated_at` (string): Last update timestamp
  * `template_language` (string): Language code for the template
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid category ID or business unit ID"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/message_templates' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "title": "Vani test",    "category": "cat_60a90614-bd7c-4ef4-935c-58aabded19f9",    "template_language": "en",    "text": "Hello {name}",    "business_unit_id": "bu_imbrace_testing"}'
  ```

## [8. Delete Message Template](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#8-delete-message-template)

Delete an existing message template by its ID.

This API allows you to delete a specific message template from your organization. Once deleted, the template cannot be recovered and will no longer be available for use in messaging operations.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/v1/backend/message_templates/{template_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/v1/backend/message_templates/{template_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/v1/backend/message_templates/{template_id}`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `template_id` (string, required): The unique identifier of the message template to delete
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "message": "Message template deleted successfully"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid template ID"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "code": 40004,    "message": "Message template not found"}
  ```
* **Example:**

  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/v1/backend/message_templates/mtemp_b34b8597-064c-4f4f-b920-8e55011baced' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [9. Delete Email Template](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#9-delete-email-template)

Delete an existing email template by its ID.

This API allows you to delete a specific email template from your organization. Once deleted, the template cannot be recovered and will no longer be available for use in email operations.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/v2/backend/marketplaces/email-templates/{template_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/v2/backend/marketplaces/email-templates/{template_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/v2/backend/marketplaces/email-templates/{template_id}`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `template_id` (string, required): The unique identifier of the email template to delete
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": {        "_id": "ema_c4b95444-8fe9-45f5-9009-671cfadaf110",        "doc_name": "EmailTemplate",        "name": "Vani Test",        "subject": "Vani Test",        "body": "<p>Test</p><p><strong>Test</strong></p><p><span class=\"ql-font-monospace\">Test</span></p>",        "status": "draft",        "category": "cat_60a90614-bd7c-4ef4-935c-58aabded19f9",        "organization_id": "org_imbrace",        "attachments": [],        "updated_at": "2025-10-20T08:29:03.334Z",        "links": [],        "public_id": "72361b02-3233-488a-968c-83d0c639de08",        "created_at": "2025-10-20T08:29:03.334Z"    }}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid template ID"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "code": 40004,    "message": "Email template not found"}
  ```
* **Example:**

  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/v2/backend/marketplaces/email-templates/ema_c4b95444-8fe9-45f5-9009-671cfadaf110' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [10. Get User Roles Count](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#10-get-user-roles-count)

Retrieve the count of users for each role within the organization.

This API allows you to fetch statistics about user distribution across different roles in your organization. It's useful for administrative dashboards, user management interfaces, and organizational analytics.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/users/_roles_count`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/users/_roles_count`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/users/_roles_count`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * None
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "admin": 20,    "owner": 10,    "technician": 2,    "user": 29}
  ```
* **Response Fields:**

  * `admin` (number): Count of users with admin role
  * `owner` (number): Count of users with owner role
  * `technician` (number): Count of users with technician role
  * `user` (number): Count of users with user role
* **Error Responses:**

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/users/_roles_count' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [11. Get Users with Filtering and Pagination](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#11-get-users-with-filtering-and-pagination)

Retrieve users with advanced filtering, pagination, and sorting options.

This API allows you to fetch users with specific filters, pagination controls, and sorting. It's useful for building user management interfaces with search, filtering, and pagination capabilities.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/users?skip=0&limit=10&search=&roles=owner&sort=-created_at&status=`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/users?skip=0&limit=10&search=&roles=owner&sort=-created_at&status=`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/users?skip=0&limit=10&search=&roles=owner&sort=-created_at&status=`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * `skip` (number, optional): Number of results to skip for pagination (default: 0)
  * `limit` (number, optional): Number of results per page (default: 10)
  * `search` (string, optional): Search term for filtering users by name or email
  * `roles` (string, optional): Filter by specific role (e.g., "owner", "admin", "user", "technician")
  * `sort` (string, optional): Sort field and direction (e.g., "-created_at" for descending)
  * `status` (string, optional): Filter by user status (e.g., "active", "inactive")
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "list",    "data": [        {            "object_name": "user",            "id": "u_44f5af79-97aa-4b74-bc5b-0a11ce317c7e",            "display_name": "chien.nguyen@imbrace.com",            "avatar_url": "",            "first_name": "chien.nguyen@imbrace.com",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "status": "active",            "email": "chien.nguyen@imbrace.com",            "is_bot": false,            "is_active": true,            "is_archived": false,            "is_deleted": false,            "created_at": "2024-09-26T02:29:26.485Z",            "updated_at": "2024-12-15T10:26:55.895Z",            "organization_id": "org_imbrace",            "role": "owner",            "team_ids": ["t_90c54b8a-c06e-439a-8844-d5798d5acf8c", "t_50fd5451-0342-48c2-bed8-888abf752181", "t_14d7e3c3-de90-49a5-89fb-d71e02a49537"]        }    ],    "nested": {        "teams": {            "t_90c54b8a-c06e-439a-8844-d5798d5acf8c": {                "object_name": "team",                "id": "t_90c54b8a-c06e-439a-8844-d5798d5acf8c",                "organization_id": "org_imbrace",                "business_unit_id": "bu_imbrace_testing",                "name": "Chien test 1",                "mode": "grab",                "icon_url": "",                "description": "",                "is_default": false,                "user_state": "",                "created_at": "2024-09-26T02:34:56.970Z",                "updated_at": "2024-09-26T02:34:56.970Z",                "is_disabled": false,                "is_delete": false            }        }    },    "has_more": true,    "count": 10,    "total": 10}
  ```
* **Error Responses:**

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/users?skip=0&limit=10&search=&roles=owner&sort=-created_at&status=' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [12. Bulk Invite Users](https://devportal.dev.imbrace.co/docs/api-document/app-apis/setting#12-bulk-invite-users)

Invite multiple users to the organization with specified roles.

This API allows you to invite multiple users to your organization in a single request. Each user can be assigned a specific role during the invitation process. This is useful for onboarding multiple users at once.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/users/_bulk_invite`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/users/_bulk_invite`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/users/_bulk_invite`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "invitations": [        {            "email": "vani.hoang@imbrace.co",            "role": "user"        }    ]}
  ```
* **Request Parameters:**

  * `invitations` (array, required): Array of invitation objects
    * `email` (string, required): Email address of the user to invite
    * `role` (string, required): Role to assign to the user (owner, admin, user, technician)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "list",    "data": [        {            "object_name": "user",            "id": "u_8ce50faf-a858-4c25-aeac-4b5c78577be3",            "display_name": "vani.hoang@imbrace.co",            "avatar_url": "",            "first_name": "vani.hoang@imbrace.co",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "status": "active",            "email": "vani.hoang@imbrace.co",            "is_bot": false,            "is_active": true,            "is_archived": false,            "is_deleted": false,            "created_at": "2025-10-20T08:46:23.042Z",            "updated_at": "2025-10-20T08:46:23.042Z",            "organization_id": "org_imbrace",            "role": "user"        }    ],    "nested": {},    "has_more": false,    "total": 1}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid email address or role"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "code": 40001,    "message": "Unauthorized"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/users/_bulk_invite' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "invitations": [        {            "email": "vani.hoang@imbrace.co",            "role": "user"        }    ]}'
  ```
