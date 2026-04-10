[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Server Gateway](https://devportal.dev.imbrace.co/docs/api-document/server-gateways)

# Data Board API

APIs for managing Data Boards.

## [1. Search Board](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#1-search-board)

Search for board using filters and pagination.

This API allows you to query a specific board and retrieve results based on matching strategies or limits.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/board_search/{board_id}/search`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/board_search/{board_id}/search`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/board_search/{board_id}/search`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`: *`Contact to iMBRACE`*
* **Query Params**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {"success": true,"message": {    "hits": [    {        "_id": "bi_e41fe9ef-fd2a-4e9b-b51e-f0a125965bb9",        "doc_name": "board_items",        "business_unit_id": "bu_efe00d4d-13d4-4673-a733-8a4fcf7ae144",        "organization_id": "org_05994568-2a16-4550-ae73-0401a7f5bde0",        "board_id": "brd_d156df21-dd75-4f2a-9c9f-8250f726bfb2",        "created_type": "manual",        "fields": {        "6700b04e89647d90e67227f1": "Dennis Tedja",        "6700b05989647d90e6722977": "Ajax X iMBrace",        "6700b05889647d90e6722961": null,        "6700b05789647d90e672294d": "1970-01-01T07:48:00.000Z",        "6700b05689647d90e672293a": "2024-10-06T07:48:00.000Z",        "6700b05689647d90e672292a": {            "country_code": "HK",            "country_calling_code": "852",            "phone": "69709328",            "calling_code_with_number": "+85269709328",            "national_number": "69709328"        }        },        "conversation_ids": [],        "public_id": "bi_e41fe9ef-fd2a-4e9b-b51e-f0a125965bb9",        "created_at": "2024-10-06T07:48:31.095Z",        "fields_timestamp": {        "6700b05789647d90e672294d": 28080,        "6700b05689647d90e672293a": 1728200880        }    },    {        "_id": "bi_d572a8b5-6bd6-42b1-9858-9871b6bf92f8",        "doc_name": "board_items",        "business_unit_id": "bu_efe00d4d-13d4-4673-a733-8a4fcf7ae144",        "organization_id": "org_05994568-2a16-4550-ae73-0401a7f5bde0",        "board_id": "brd_d156df21-dd75-4f2a-9c9f-8250f726bfb2",        "created_type": "manual",        "fields": {        "6700b04e89647d90e67227f1": "Sam",        "6700b05989647d90e6722977": "Sam",        "6700b05889647d90e6722961": "Hello, iMBrace!",        "6700b05789647d90e672294d": "1970-01-01T03:38:00.000Z",        "6700b05689647d90e672293a": "2024-10-05T03:38:00.000Z",        "6700b05689647d90e672292a": {            "country_code": "HK",            "country_calling_code": "852",            "phone": "94412310",            "calling_code_with_number": "+85294412310",            "national_number": "94412310"        }        },        "conversation_ids": [],        "public_id": "bi_d572a8b5-6bd6-42b1-9858-9871b6bf92f8",        "created_at": "2024-10-05T03:38:39.046Z",        "fields_timestamp": {        "6700b05789647d90e672294d": 13080,        "6700b05689647d90e672293a": 1728099480        },        "updated_at": "2024-10-05T03:38:44.649Z"    },    {        "_id": "bi_3aa08178-8038-4481-bd2b-f012b7d3deca",        "doc_name": "board_items",        "business_unit_id": "bu_efe00d4d-13d4-4673-a733-8a4fcf7ae144",        "organization_id": "org_05994568-2a16-4550-ae73-0401a7f5bde0",        "board_id": "brd_d156df21-dd75-4f2a-9c9f-8250f726bfb2",        "created_type": "manual",        "fields": {        "6700b04e89647d90e67227f1": "Dennis Tedja",        "6700b05989647d90e6722977": "Ajax X iMBrace",        "6700b05889647d90e6722961": "News on OpenAi API and Llama new features",        "6700b05789647d90e672294d": "1970-01-01T07:49:00.000Z",        "6700b05689647d90e672293a": "2024-10-06T07:49:00.000Z",        "6700b05689647d90e672292a": {            "country_code": "HK",            "country_calling_code": "852",            "phone": "69709328",            "calling_code_with_number": "+85269709328",            "national_number": "69709328"        }        },        "conversation_ids": [],        "public_id": "bi_3aa08178-8038-4481-bd2b-f012b7d3deca",        "created_at": "2024-10-06T07:49:24.570Z",        "fields_timestamp": {        "6700b05789647d90e672294d": 28140,        "6700b05689647d90e672293a": 1728200940        }    },    {        "_id": "bi_989eb95e-aa19-4b0d-b9b6-c1d8c6a590a6",        "doc_name": "board_items",        "business_unit_id": "bu_efe00d4d-13d4-4673-a733-8a4fcf7ae144",        "organization_id": "org_05994568-2a16-4550-ae73-0401a7f5bde0",        "board_id": "brd_d156df21-dd75-4f2a-9c9f-8250f726bfb2",        "created_type": "manual",        "fields": {        "6700b04e89647d90e67227f1": "Dennis Tedja",        "6700b05989647d90e6722977": "Ajax X iMBrace",        "6700b05889647d90e6722961": "let me know what you thikn",        "6700b05789647d90e672294d": "1970-01-01T07:49:00.000Z",        "6700b05689647d90e672293a": "2024-10-06T07:49:00.000Z",        "6700b05689647d90e672292a": {            "country_code": "HK",            "country_calling_code": "852",            "phone": "69709328",            "calling_code_with_number": "+85269709328",            "national_number": "69709328"        }        },        "conversation_ids": [],        "public_id": "bi_989eb95e-aa19-4b0d-b9b6-c1d8c6a590a6",        "created_at": "2024-10-06T07:49:30.805Z",        "fields_timestamp": {        "6700b05789647d90e672294d": 28140,        "6700b05689647d90e672293a": 1728200940        }    }    ],    "query": "",    "processingTimeMs": 4,    "limit": 20,    "offset": 0,    "estimatedTotalHits": 455}}
  ```
* **Example:**

  ```
  curl --request POST \--url https://app-gateway.dev.imbrace.co/3rd/board_search/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6/search \--header 'Authorization: Basic Og==' \--header 'content-type: application/json' \--header 'x-access-token: api_df0d164e-5cfe-4471-8063-f155aedb8af8' \--data '{"limit": 20,"matchingStrategy": "all","offset": 0}'
  ```

## [2. Create Multiple Board Items](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#2-create-multiple-board-items)

Create multiple board items for a specific board.

This API lets you create one or many items in a board by passing field values per item.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/boards/create/{board_id}/board_items`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/boards/create/{board_id}/board_items`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/boards/create/{board_id}/board_items`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`: *`Contact to iMBRACE`*
* **Query Params**

  * *(none)*
* **Body:**

  ```
  {  "items": [    {      "fields": [        { "board_field_id": "65c3242b085dd896c86d297f", "value": "117" },        { "board_field_id": "67cd8eaa6846465b7772536d", "value": null },        { "board_field_id": "67e3802cf15a6fb22ddedb7f", "value": null },        { "board_field_id": "67a21c1cae791f83be46cb08", "value": null },        { "board_field_id": "67cd92a56846465b77729eb5", "value": null },        { "board_field_id": "676cf93272d5962f16da17c5", "value": [] },        { "board_field_id": "67771b0f0e351e5e3822211c", "value": "Maintenance Service" },        { "board_field_id": "66399ef1677ac4c4a62e8da9", "value": null },        { "board_field_id": "66399f1b677ac4c4a62e9279", "value": "1970-01-01T00:00:00.000Z" },        { "board_field_id": "65c2efd2085dd896c86b8668", "value": "117" },        { "board_field_id": "66c69ccfbb95d32becb0c39a", "value": null },        { "board_field_id": "65c2efdc085dd896c86b8825", "value": null },        { "board_field_id": "66399f00677ac4c4a62e90a9", "value": null }      ]    },    {      "fields": [        { "board_field_id": "65c3242b085dd896c86d297f", "value": "118" },        { "board_field_id": "67cd8eaa6846465b7772536d", "value": null },        { "board_field_id": "67e3802cf15a6fb22ddedb7f", "value": null },        { "board_field_id": "67a21c1cae791f83be46cb08", "value": null },        { "board_field_id": "67cd92a56846465b77729eb5", "value": null },        { "board_field_id": "676cf93272d5962f16da17c5", "value": [] },        { "board_field_id": "67771b0f0e351e5e3822211c", "value": "Maintenance Service" },        { "board_field_id": "66399ef1677ac4c4a62e8da9", "value": null },        { "board_field_id": "66399f1b677ac4c4a62e9279", "value": "1970-01-01T00:00:00.000Z" },        { "board_field_id": "65c2efd2085dd896c86b8668", "value": "118" },        { "board_field_id": "66c69ccfbb95d32becb0c39a", "value": null },        { "board_field_id": "65c2efdc085dd896c86b8825", "value": null },        { "board_field_id": "66399f00677ac4c4a62e90a9", "value": null }      ]    }  ]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "success": [        {            "index": 0,            "board_item": {                "doc_name": "board_items",                "updated_at": "2025-10-17T02:29:04.748Z",                "created_at": "2025-10-17T02:29:04.748Z",                "business_unit_id": "bu_imbrace_testing",                "organization_id": "org_imbrace",                "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",                "related_board_item_list": [],                "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",                "created_type": "manual",                "fields": {                    "65c3242b085dd896c86d297f": "117",                    "68edc5b76da47b93262ee516": null,                    "67cd8eaa6846465b7772536d": null,                    "67e3802cf15a6fb22ddedb7f": {                        "country_code": null                    },                    "67a21c1cae791f83be46cb08": null,                    "67cd92a56846465b77729eb5": null,                    "676cf93272d5962f16da17c5": null,                    "67771b0f0e351e5e3822211c": "Maintenance Service",                    "66399ef1677ac4c4a62e8da9": null,                    "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",                    "65c2efd2085dd896c86b8668": "117",                    "66c69ccfbb95d32becb0c39a": null,                    "65c2efdc085dd896c86b8825": null,                    "66399f00677ac4c4a62e90a9": null                },                "conversation_ids": [],                "_id": "bi_f27b5bfe-3d39-44a1-b863-7fb3f5d67c36",                "id": "bi_f27b5bfe-3d39-44a1-b863-7fb3f5d67c36"            }        },        {            "index": 1,            "board_item": {                "doc_name": "board_items",                "updated_at": "2025-10-17T02:29:04.748Z",                "created_at": "2025-10-17T02:29:04.748Z",                "business_unit_id": "bu_imbrace_testing",                "organization_id": "org_imbrace",                "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",                "related_board_item_list": [],                "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",                "created_type": "manual",                "fields": {                    "65c3242b085dd896c86d297f": "118",                    "68edc5b76da47b93262ee516": null,                    "67cd8eaa6846465b7772536d": null,                    "67e3802cf15a6fb22ddedb7f": {                        "country_code": null                    },                    "67a21c1cae791f83be46cb08": null,                    "67cd92a56846465b77729eb5": null,                    "676cf93272d5962f16da17c5": null,                    "67771b0f0e351e5e3822211c": "Maintenance Service",                    "66399ef1677ac4c4a62e8da9": null,                    "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",                    "65c2efd2085dd896c86b8668": "118",                    "66c69ccfbb95d32becb0c39a": null,                    "65c2efdc085dd896c86b8825": null,                    "66399f00677ac4c4a62e90a9": null                },                "conversation_ids": [],                "_id": "bi_0d98b758-82da-4b0c-9e31-709e288e0269",                "id": "bi_0d98b758-82da-4b0c-9e31-709e288e0269"            }        }    ],    "errors": [],    "success_count": 2,    "error_count": 0}
  ```
* **Example:**

  ```
  curl --request POST \--url https://app-gateway.dev.imbrace.co/3rd/boards/create/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6/board_items \--header 'x-access-token: api_df0d164e-5cfe-4471-8063-f155aedb8af8' \--header 'Content-Type: application/json' \--data '{    "items": [    {        "fields": [        { "board_field_id": "65c3242b085dd896c86d297f", "value": "117" },        { "board_field_id": "67cd8eaa6846465b7772536d", "value": null },        { "board_field_id": "67e3802cf15a6fb22ddedb7f", "value": null },        { "board_field_id": "67a21c1cae791f83be46cb08", "value": null },        { "board_field_id": "67cd92a56846465b77729eb5", "value": null },        { "board_field_id": "676cf93272d5962f16da17c5", "value": [] },        { "board_field_id": "67771b0f0e351e5e3822211c", "value": "Maintenance Service" },        { "board_field_id": "66399ef1677ac4c4a62e8da9", "value": null },        { "board_field_id": "66399f1b677ac4c4a62e9279", "value": "1970-01-01T00:00:00.000Z" },        { "board_field_id": "65c2efd2085dd896c86b8668", "value": "117" },        { "board_field_id": "66c69ccfbb95d32becb0c39a", "value": null },        { "board_field_id": "65c2efdc085dd896c86b8825", "value": null },        { "board_field_id": "66399f00677ac4c4a62e90a9", "value": null }        ]    },    {        "fields": [        { "board_field_id": "65c3242b085dd896c86d297f", "value": "118" },        { "board_field_id": "67cd8eaa6846465b7772536d", "value": null },        { "board_field_id": "67e3802cf15a6fb22ddedb7f", "value": null },        { "board_field_id": "67a21c1cae791f83be46cb08", "value": null },        { "board_field_id": "67cd92a56846465b77729eb5", "value": null },        { "board_field_id": "676cf93272d5962f16da17c5", "value": [] },        { "board_field_id": "67771b0f0e351e5e3822211c", "value": "Maintenance Service" },        { "board_field_id": "66399ef1677ac4c4a62e8da9", "value": null },        { "board_field_id": "66399f1b677ac4c4a62e9279", "value": "1970-01-01T00:00:00.000Z" },        { "board_field_id": "65c2efd2085dd896c86b8668", "value": "118" },        { "board_field_id": "66c69ccfbb95d32becb0c39a", "value": null },        { "board_field_id": "65c2efdc085dd896c86b8825", "value": null },        { "board_field_id": "66399f00677ac4c4a62e90a9", "value": null }        ]    }    ]}'
  ```

## [3. Delete Board Items](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#3-delete-board-items)

Delete one or more board items from a specific board.

This API allows you to remove multiple board items at once by passing their unique IDs.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/boards/delete/{board_id}/board_items`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/boards/delete/{board_id}/board_items`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/boards/delete/{board_id}/board_items`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`: *`Contact to iMBRACE`*
* **Query Params**

  * *(none)*
* **Body:**

  ```
  {  "ids": [    "bi_07c474eb-697b-4152-8d0c-93f2940d4a6a",    "bi_71b0e99c-c170-442f-b153-26482484b2fd"  ]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "success_ids": [],  "failed": [    {      "id": "bi_49ca9158-a80c-4084-9b2b-b8d3a23ec674",      "reason": "not_found"    },    {      "id": "bi_71b0e99c-c170-442f-b153-26482484b2fd",      "reason": "not_found"    },    {      "id": "bi_49ca9158-a80c-4084-9b2b-b8d3a23ec674",      "reason": "not_found"    },    {      "id": "bi_71b0e99c-c170-442f-b153-26482484b2fd",      "reason": "not_found"    }  ],  "success_count": 0,  "failed_count": 4}
  ```
* **Example:**

  ```
  curl --request POST \--url https://app-gateway.dev.imbrace.co/3rd/delete_board_items/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6/board_items \--header 'Content-Type: application/json' \--header 'x-access-token: api_df0d164e-5cfe-4471-8063-f155aedb8af8' \--data '{    "ids": [    "bi_07c474eb-697b-4152-8d0c-93f2940d4a6a",    "bi_71b0e99c-c170-442f-b153-26482484b2fd"    ]}'
  ```

## [4. Upload File](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#4-upload-file)

Upload a file to the board system.

This API allows you to upload files using multipart/form-data format.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/boards/upload`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/boards/upload`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/boards/upload`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
* **Query Params**

  * *(none)*
* **Body:**

  * Form-data with file attachment
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "user_id": "u_1f8e2d55-d47a-4fd3-8f78-7af8a08ad069",        "uploader": "Resolve owner",        "name": "kit1",        "extension": "jpeg",        "sizeInBytes": 14879,        "uploadDate": "2025-10-16T10:56:37.416Z",        "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_48bcf0fa-9506-457c-8eb2-1448ee2f54cc/file_yJqlWJvptBfDP6ZG1jNfxWoA8z.jpeg",        "key": "board/org_48bcf0fa-9506-457c-8eb2-1448ee2f54cc/file_yJqlWJvptBfDP6ZG1jNfxWoA8z.jpeg",        "error": null    }]
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.demo.imbrace.co/3rd/boards/upload' \--header 'x-access-token: api_497c5175-560d-4cf1-b628-ba9c6a82fd6a' \--form '=@"/path/to/file"'
  ```

## [5. Update Multiple Board Items](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#5-update-multiple-board-items)

Update multiple board items for a specific board.

This API allows you to update existing board items by specifying their IDs and the field values to modify.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/3rd/boards/update/{board_id}/board_items`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/3rd/boards/update/{board_id}/board_items`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/3rd/boards/update/{board_id}/board_items`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`: *`Contact to iMBRACE`*
* **Query Params**

  * *(none)*
* **Body:**

  ```
  {  "items": [    {      "id": "bi_01727039-8ed3-4b82-a257-e377c8b9b996",      "fields": [        { "board_field_id": "68dc8544cd51ecdd3cce6e39", "value": "1" },        { "board_field_id": "68dc8545cd51ecdd3cce6e4a", "value": "1" },        { "board_field_id": "68dc8544cd51ecdd3cce6e43", "value": 111 }      ]    },    {      "id": "bi_49ca9158-a80c-4084-9b2b-b8d3a23ec674",      "fields": [        { "board_field_id": "68dc8544cd51ecdd3cce6e39", "value": "3" },        { "board_field_id": "68dc8545cd51ecdd3cce6e4a", "value": "33" },        { "board_field_id": "68dc8544cd51ecdd3cce6e43", "value": 333 }      ]    }  ]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "success_ids": [    "bi_01727039-8ed3-4b82-a257-e377c8b9b996",    "bi_49ca9158-a80c-4084-9b2b-b8d3a23ec674"  ],  "failed": [],  "success_count": 2,  "failed_count": 0}
  ```
* **Example:**

  ```
  curl --request PUT \  --url https://app-gateway.dev.imbrace.co/3rd/boards/update/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6/board_items \  --header 'Cookie: user_role=owner; pscd=join.activepieces.com; user_name=Austina; org_id=org_imbrace; user_id=u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a; org_name=iMBRACE%20Corporation; _clck=v2aiso%5E2%5Efz7%5E0%5E2073%7C2%7Cfzt%7C0%7C0; n8n-auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjhkZjE2MjBjLTUyNzUtNGM0NC1hNzY3LTI0ZjJjMTJlNGY4ZSIsImVtYWlsIjoiamFuZS5saW5AaW1icmFjZS5jbyIsInBhc3N3b3JkIjoiYWNiNzAxMjVhNTEzY2IxM2I3MjgxNWU3NjZkNmM4NDExMjJhZTliZDM3YWUzMDEzNmEwNzlkNzdhNjYzMTg5YSIsImlhdCI6MTc1OTM3Nzc4NiwiZXhwIjoxNzU5OTgyNTg2fQ.y0L7egKPEextONRa5F_BcX4gD9LI8ireIlaOX_3cWww' \  --header 'accept: application/json, text/plain, */*' \  --header 'accept-language: en-US,en;q=0.9,vi;q=0.8' \  --header 'baggage: sentry-environment=develop,sentry-release=4.4.5,sentry-public_key=c7acbd82c4e745b7975a8332a40e1df8,sentry-trace_id=ade80822657d422887904afc61699799,sentry-sample_rate=0,sentry-sampled=false' \  --header 'content-type: application/json' \  --header 'origin: https://webapp.dev.imbrace.co' \  --header 'priority: u=1, i' \  --header 'referer: https://webapp.dev.imbrace.co/databoards/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6' \  --header 'sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"' \  --header 'sec-ch-ua-mobile: ?0' \  --header 'sec-ch-ua-platform: "macOS"' \  --header 'sec-fetch-dest: empty' \  --header 'sec-fetch-mode: cors' \  --header 'sec-fetch-site: same-origin' \  --header 'sentry-trace: ade80822657d422887904afc61699799-b92991be43808508-0' \  --header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36' \  --header 'x-access-token: api_df0d164e-5cfe-4471-8063-f155aedb8af8' \  --data '{  "items": [    {      "id": "bi_01727039-8ed3-4b82-a257-e377c8b9b996",      "fields": [        { "board_field_id": "68dc8544cd51ecdd3cce6e39", "value": "1" },        { "board_field_id": "68dc8545cd51ecdd3cce6e4a", "value": "1" },        { "board_field_id": "68dc8544cd51ecdd3cce6e43", "value": 111 }      ]    },    {      "id": "bi_49ca9158-a80c-4084-9b2b-b8d3a23ec674",      "fields": [        { "board_field_id": "68dc8544cd51ecdd3cce6e39", "value": "3" },        { "board_field_id": "68dc8545cd51ecdd3cce6e4a", "value": "33" },        { "board_field_id": "68dc8544cd51ecdd3cce6e43", "value": 333 }      ]    }  ]}'
  ```

## [6. List All Boards](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#6-list-all-boards)

Retrieve a list of all available boards.

This API allows you to fetch all boards that the authenticated user has access to.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/boards`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/boards`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/boards`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`: *`Contact to iMBRACE`*
  * `accept`: `application/json, text/plain, */*`
  * `accept-language`: `en-US,en;q=0.9,vi;q=0.8`
* **Query Params**

  * *(none)*
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",  "doc_name": "boards",  "business_unit_id": "bu_imbrace_testing",  "order": 2,  "organization_id": "org_imbrace",  "name": "TestAssign",  "hidden": false,  "type": "General",  "fields": [    {      "name": "Email",      "description": "dasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhja",      "type": "Email",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": true,      "data": [],      "_id": "65c3242b085dd896c86d297f"    },    {      "name": "Nokia Report Testing",      "type": "Country",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "68edc5b76da47b93262ee516"    },    {      "settings": {        "default_currency_code": "THB"      },      "name": "Currency",      "type": "Currency",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "67cd8eaa6846465b7772536d"    },    {      "name": "Country",      "description": "dasdasdansjdnasjdnasjdnjasndjasndjasndjkasndasjkndjakndjkasndjkasndjkasndjkasndkjanskdadjaskndajksndjasndkjasndjksandkjasndkjasnjkdnasjkdnasjkdnaskjdnaskdasdasdansjdnasjdnasjdnjasndjasndjasndjkasndasjkndjakndjkasndjkasndjkasndjkasndkjanskdadjaskndajksndjasndkjasndjksandkjasndkjasnjkdnasjkdnasjkdnaskjandkjasndkjasnjkdnasjkdnasjkdnaskjdnaskdasdasdansjdnasjdnasjdnjasndjasndjasndjds",      "type": "Country",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "67e3802cf15a6fb22ddedb7f"    },    {      "name": "number",      "type": "Number",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "67a21c1cae791f83be46cb08"    },    {      "name": "Origin",      "type": "Origin",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [        {          "value": "123",          "_id": "123"        },        {          "value": "234",          "_id": "234"        }      ],      "_id": "67cd92a56846465b77729eb5"    },    {      "name": "attachment",      "type": "Attachment",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "676cf93272d5962f16da17c5"    },    {      "name": "TESTING",      "type": "SingleSelection",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [        {          "value": "Maintenance Service",          "_id": "Maintenance Service"        }      ],      "_id": "67771b0f0e351e5e3822211c"    },    {      "settings": {        "default_country_code": "MY"      },      "name": "Phone",      "description": "",      "type": "Phone",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66399ef1677ac4c4a62e8da9"    },    {      "name": "Booking Time",      "type": "Time",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66399f1b677ac4c4a62e9279"    },    {      "name": "Name",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "65c2efd2085dd896c86b8668"    },    {      "name": "Datetime",      "type": "Datetime",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66c69ccfbb95d32becb0c39a"    },    {      "name": "assign to",      "type": "Assignee",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "65c2efdc085dd896c86b8825"    },    {      "name": "Booking Date",      "type": "Date",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66399f00677ac4c4a62e90a9"    }  ],  "public_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",  "created_at": "2024-02-07T02:49:54.081Z",  "updated_at": "2025-10-14T03:38:31.564Z",  "managers": [    {      "team_id": "t_162c7a64-c13e-4055-b221-da568f0ee7c9",      "team_user_ids": [],      "_id": "68edc5b76da47b93262ee4e1"    },    {      "team_id": "t_14d7e3c3-de90-49a5-89fb-d71e02a49537",      "team_user_ids": [],      "_id": "68edc5b76da47b93262ee4e2"    }  ],  "description": "7512944342\n4959436923\n0953253947\n4903338191\n4733271239\n7538059428\n0104474899\n4280682655\n5569381874\n7629568080\n7512944342\n4959436923\n0953253947\n4903338191\n4733271239\n7538059428\n0104474899\n4280682655\n5569381874\n7629568080\n7512944342\n4959436923\n0953253947\n4903338191\n4733271239\n7538059428\n0104474899\n4280682655\n5569381874\n7629568080\n7512944342\n4959436923\n0953253947\n4903338191\n4733271239\n7538059428\n0104474899\n4280682655\n5569381874\n76295680807512944342\n4959436923\n0953253947\n4903338191\n4733271239\n753807",  "team_ids": [    "t_162c7a64-c13e-4055-b221-da568f0ee7c9",    "t_14d7e3c3-de90-49a5-89fb-d71e02a49537"  ],  "id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6"}
  ```
* **Example:**

  ```
  curl --request GET 'https://app-gateway.dev.imbrace.co/3rd/boards' \--header 'Content-Type: application/json' \--header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928' \--header 'accept: application/json, text/plain, */*' \--header 'accept-language: en-US,en;q=0.9,vi;q=0.8'
  ```

## [7. Get Board Items](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#7-get-board-items)

Retrieve a list of all items for a specific board.

This API allows you to fetch all the items associated with a particular board by its ID.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/boards/{board_id}/board_items`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}/board_items`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}/board_items`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`: *`Contact to iMBRACE`*
* **Path Parameters**

  * `board_id`: The unique identifier of the board (e.g., `brd_1c41d851-90f3-44b0-8b51-9628d30c29a6`)
* **Query Params**

  * *(none)*
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "data": [    {      "_id": "bi_7c9b0077-011f-4949-a901-ee0436533d04",      "doc_name": "board_items",      "updated_at": "2025-10-17T03:24:58.296Z",      "created_at": "2025-10-17T03:24:58.296Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "118",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null,          "country_name": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": null,        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "118",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "contacts": null,      "id": "bi_7c9b0077-011f-4949-a901-ee0436533d04",      "65c3242b085dd896c86d297f": "118",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null,        "country_name": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": null,      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "118",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_7c9b0077-011f-4949-a901-ee0436533d04"    },    {      "_id": "bi_2b5687c5-92c9-468b-9461-4d3e05617f10",      "doc_name": "board_items",      "updated_at": "2025-10-17T03:24:58.295Z",      "created_at": "2025-10-17T03:24:58.295Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "117",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null,          "country_name": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": null,        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "117",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "contacts": null,      "id": "bi_2b5687c5-92c9-468b-9461-4d3e05617f10",      "65c3242b085dd896c86d297f": "117",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null,        "country_name": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": null,      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "117",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_2b5687c5-92c9-468b-9461-4d3e05617f10"    },    {      "_id": "bi_56b30198-1381-4057-9bb4-47b38f606f92",      "doc_name": "board_items",      "updated_at": "2025-10-17T03:14:27.056Z",      "created_at": "2025-10-17T03:14:27.056Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "118",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null,          "country_name": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": null,        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "118",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "contacts": null,      "id": "bi_56b30198-1381-4057-9bb4-47b38f606f92",      "65c3242b085dd896c86d297f": "118",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null,        "country_name": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": null,      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "118",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_56b30198-1381-4057-9bb4-47b38f606f92"    },    {      "_id": "bi_712ebf93-3aa2-4300-8aad-7a4649396985",      "doc_name": "board_items",      "updated_at": "2025-10-17T03:14:27.055Z",      "created_at": "2025-10-17T03:14:27.055Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "117",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null,          "country_name": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": null,        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "117",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "contacts": null,      "id": "bi_712ebf93-3aa2-4300-8aad-7a4649396985",      "65c3242b085dd896c86d297f": "117",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null,        "country_name": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": null,      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "117",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_712ebf93-3aa2-4300-8aad-7a4649396985"    },    {      "_id": "bi_2a4623e6-9d03-457f-b9dc-7d7426cd80c5",      "doc_name": "board_items",      "updated_at": "2025-10-17T03:13:44.977Z",      "created_at": "2025-10-17T03:13:44.977Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "118",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null,          "country_name": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": null,        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "118",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "contacts": null,      "id": "bi_2a4623e6-9d03-457f-b9dc-7d7426cd80c5",      "65c3242b085dd896c86d297f": "118",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null,        "country_name": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": null,      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "118",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_2a4623e6-9d03-457f-b9dc-7d7426cd80c5"    },    {      "_id": "bi_e2513c1e-62d7-4cb0-a0d2-3b10c3dd3423",      "doc_name": "board_items",      "updated_at": "2025-10-17T03:13:44.976Z",      "created_at": "2025-10-17T03:13:44.976Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "117",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null,          "country_name": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": null,        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "117",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "contacts": null,      "id": "bi_e2513c1e-62d7-4cb0-a0d2-3b10c3dd3423",      "65c3242b085dd896c86d297f": "117",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null,        "country_name": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": null,      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "117",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_e2513c1e-62d7-4cb0-a0d2-3b10c3dd3423"    },    {      "_id": "bi_f27b5bfe-3d39-44a1-b863-7fb3f5d67c36",      "doc_name": "board_items",      "updated_at": "2025-10-17T02:29:04.748Z",      "created_at": "2025-10-17T02:29:04.748Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "117",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null,          "country_name": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": null,        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "117",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "contacts": null,      "id": "bi_f27b5bfe-3d39-44a1-b863-7fb3f5d67c36",      "65c3242b085dd896c86d297f": "117",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null,        "country_name": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": null,      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "117",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_f27b5bfe-3d39-44a1-b863-7fb3f5d67c36"    },    {      "_id": "bi_0d98b758-82da-4b0c-9e31-709e288e0269",      "doc_name": "board_items",      "updated_at": "2025-10-17T02:29:04.748Z",      "created_at": "2025-10-17T02:29:04.748Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "118",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null,          "country_name": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": null,        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "118",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "contacts": null,      "id": "bi_0d98b758-82da-4b0c-9e31-709e288e0269",      "65c3242b085dd896c86d297f": "118",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null,        "country_name": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": null,      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "118",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_0d98b758-82da-4b0c-9e31-709e288e0269"    },    {      "_id": "bi_f7fab122-c2a3-471d-88b3-179979e3c9d4",      "doc_name": "board_items",      "updated_at": "2025-10-17T03:26:48.131Z",      "created_at": "2025-10-16T04:45:30.577Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "000",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": [],        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "0001",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "public_id": "bi_f7fab122-c2a3-471d-88b3-179979e3c9d4",      "contacts": null,      "id": "bi_f7fab122-c2a3-471d-88b3-179979e3c9d4",      "65c3242b085dd896c86d297f": "000",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": [],      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "0001",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_f7fab122-c2a3-471d-88b3-179979e3c9d4"    },    {      "_id": "bi_949cf85a-574f-472b-892b-bf78aececd0b",      "doc_name": "board_items",      "updated_at": "2025-10-17T03:26:48.131Z",      "created_at": "2025-10-16T04:45:30.577Z",      "business_unit_id": "bu_imbrace_testing",      "organization_id": "org_imbrace",      "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",      "related_board_item_list": [],      "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",      "created_type": "manual",      "fields": {        "65c3242b085dd896c86d297f": "111",        "68edc5b76da47b93262ee516": null,        "67cd8eaa6846465b7772536d": null,        "67e3802cf15a6fb22ddedb7f": {          "country_code": null        },        "67a21c1cae791f83be46cb08": null,        "67cd92a56846465b77729eb5": null,        "676cf93272d5962f16da17c5": [],        "67771b0f0e351e5e3822211c": "Maintenance Service",        "66399ef1677ac4c4a62e8da9": null,        "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",        "65c2efd2085dd896c86b8668": "0002",        "66c69ccfbb95d32becb0c39a": null,        "65c2efdc085dd896c86b8825": null,        "66399f00677ac4c4a62e90a9": null      },      "conversation_ids": [],      "public_id": "bi_949cf85a-574f-472b-892b-bf78aececd0b",      "contacts": null,      "id": "bi_949cf85a-574f-472b-892b-bf78aececd0b",      "65c3242b085dd896c86d297f": "111",      "68edc5b76da47b93262ee516": null,      "67cd8eaa6846465b7772536d": null,      "67e3802cf15a6fb22ddedb7f": {        "country_code": null      },      "67a21c1cae791f83be46cb08": null,      "67cd92a56846465b77729eb5": null,      "676cf93272d5962f16da17c5": [],      "67771b0f0e351e5e3822211c": "Maintenance Service",      "66399ef1677ac4c4a62e8da9": null,      "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",      "65c2efd2085dd896c86b8668": "0002",      "66c69ccfbb95d32becb0c39a": null,      "65c2efdc085dd896c86b8825": null,      "66399f00677ac4c4a62e90a9": null,      "board_item_id": "bi_949cf85a-574f-472b-892b-bf78aececd0b"    }  ],  "count": 1129,  "total": 10,  "has_more": true}
  ```
* **Example:**

  ```
  curl --request GET \--url https://app-gateway.dev.imbrace.co/3rd/boards/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6/board_items \--header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928'
  ```

## [8. Get Board Item Detail](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#8-get-board-item-detail)

Retrieve detailed information about a specific board item.

This API allows you to fetch the complete details of a specific item within a board using its unique identifier.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/boards/{board_id}/board_items/{item_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}/board_items/{item_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}/board_items/{item_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`: *`Contact to iMBRACE`*
* **Path Parameters**

  * `board_id`: The unique identifier of the board (e.g., `brd_1c41d851-90f3-44b0-8b51-9628d30c29a6`)
  * `item_id`: The unique identifier of the board item (e.g., `bi_e2513c1e-62d7-4cb0-a0d2-3b10c3dd3423`)
* **Query Params**

  * *(none)*
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "_id": "bi_e2513c1e-62d7-4cb0-a0d2-3b10c3dd3423",  "doc_name": "board_items",  "updated_at": "2025-10-17T03:13:44.976Z",  "created_at": "2025-10-17T03:13:44.976Z",  "business_unit_id": "bu_imbrace_testing",  "organization_id": "org_imbrace",  "board_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",  "related_board_item_list": [],  "created_by": "",  "created_type": "manual",  "fields": {    "65c3242b085dd896c86d297f": "117",    "68edc5b76da47b93262ee516": null,    "67cd8eaa6846465b7772536d": null,    "67e3802cf15a6fb22ddedb7f": {      "country_code": null,      "country_name": null    },    "67a21c1cae791f83be46cb08": null,    "67cd92a56846465b77729eb5": null,    "676cf93272d5962f16da17c5": null,    "67771b0f0e351e5e3822211c": "Maintenance Service",    "66399ef1677ac4c4a62e8da9": null,    "66399f1b677ac4c4a62e9279": "1970-01-01T00:00:00.000Z",    "65c2efd2085dd896c86b8668": "117",    "66c69ccfbb95d32becb0c39a": null,    "65c2efdc085dd896c86b8825": null,    "66399f00677ac4c4a62e90a9": null  },  "conversation_ids": [],  "contacts": null,  "id": "bi_e2513c1e-62d7-4cb0-a0d2-3b10c3dd3423",  "board_item_id": "bi_e2513c1e-62d7-4cb0-a0d2-3b10c3dd3423",  "board": {    "_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",    "doc_name": "boards",    "business_unit_id": "bu_imbrace_testing",    "order": 2,    "organization_id": "org_imbrace",    "name": "TestAssign",    "hidden": false,    "type": "General",    "fields": [      {        "name": "Email",        "description": "dasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhja",        "type": "Email",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "is_identifier": true,        "data": [],        "_id": "65c3242b085dd896c86d297f"      },      {        "name": "Nokia Report Testing",        "type": "Country",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "data": [],        "_id": "68edc5b76da47b93262ee516"      },      {        "settings": {          "default_currency_code": "THB"        },        "name": "Currency",        "type": "Currency",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "data": [],        "_id": "67cd8eaa6846465b7772536d"      },      {        "name": "Country",        "description": "dasdasdansjdnasjdnasjdnjasndjasndjasndjkasndasjkndjakndjkasndjkasndjkasndjkasndkjanskdadjaskndajksndjasndkjasndjksandkjasndkjasnjkdnasjkdnasjkdnaskjdnaskdasdasdansjdnasjdnasjdnjasndjasndjasndjkasndasjkndjakndjkasndjkasndjkasndjkasndkjanskdadjaskndajksndjasndkjasndjksandkjasndkjasnjkdnasjkdnasjkdnaskjandkjasndkjasnjkdnasjkdnasjkdnaskjdnaskdasdasdansjdnasjdnasjdnjasndjasndjasndjds",        "type": "Country",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "data": [],        "_id": "67e3802cf15a6fb22ddedb7f"      },      {        "name": "number",        "type": "Number",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "data": [],        "_id": "67a21c1cae791f83be46cb08"      },      {        "name": "Origin",        "type": "Origin",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "data": [          {            "value": "123",            "_id": "123"          },          {            "value": "234",            "_id": "234"          }        ],        "_id": "67cd92a56846465b77729eb5"      },      {        "name": "attachment",        "type": "Attachment",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "data": [],        "_id": "676cf93272d5962f16da17c5"      },      {        "name": "TESTING",        "type": "SingleSelection",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "data": [          {            "value": "Maintenance Service",            "_id": "Maintenance Service"          }        ],        "_id": "67771b0f0e351e5e3822211c"      },      {        "settings": {          "default_country_code": "MY"        },        "name": "Phone",        "description": "",        "type": "Phone",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "is_identifier": false,        "data": [],        "_id": "66399ef1677ac4c4a62e8da9"      },      {        "name": "Booking Time",        "type": "Time",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "is_identifier": false,        "data": [],        "_id": "66399f1b677ac4c4a62e9279"      },      {        "name": "Name",        "type": "ShortText",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "is_identifier": false,        "data": [],        "_id": "65c2efd2085dd896c86b8668"      },      {        "name": "Datetime",        "type": "Datetime",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "is_identifier": false,        "data": [],        "_id": "66c69ccfbb95d32becb0c39a"      },      {        "name": "assign to",        "type": "Assignee",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "is_identifier": false,        "data": [],        "_id": "65c2efdc085dd896c86b8825"      },      {        "name": "Booking Date",        "type": "Date",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "is_identifier": false,        "data": [],        "_id": "66399f00677ac4c4a62e90a9"      }    ],    "public_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",    "created_at": "2024-02-07T02:49:54.081Z",    "updated_at": "2025-10-14T03:38:31.564Z",    "managers": [      {        "team_id": "t_162c7a64-c13e-4055-b221-da568f0ee7c9",        "team_user_ids": [],        "_id": "68edc5b76da47b93262ee4e1"      },      {        "team_id": "t_14d7e3c3-de90-49a5-89fb-d71e02a49537",        "team_user_ids": [],        "_id": "68edc5b76da47b93262ee4e2"      }    ],    "description": "7512944342\n4959436923\n0953253947\n4903338191\n4733271239\n7538059428\n0104474899\n4280682655\n5569381874\n7629568080\n7512944342\n4959436923\n0953253947\n4903338191\n4733271239\n7538059428\n0104474899\n4280682655\n5569381874\n7629568080\n7512944342\n4959436923\n0953253947\n4903338191\n4733271239\n7538059428\n0104474899\n4280682655\n5569381874\n7629568080\n7512944342\n4959436923\n0953253947\n4903338191\n4733271239\n7538059428\n0104474899\n4280682655\n5569381874\n76295680807512944342\n4959436923\n0953253947\n4903338191\n4733271239\n753807",    "team_ids": [      "t_162c7a64-c13e-4055-b221-da568f0ee7c9",      "t_14d7e3c3-de90-49a5-89fb-d71e02a49537"    ],    "id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6"  }} 
  ```
* **Example:**

  ```
  curl --request GET \  --url https://app-gateway.dev.imbrace.co/3rd/boards/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6/board_items/bi_e2513c1e-62d7-4cb0-a0d2-3b10c3dd3423 \  --header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928'
  ```

## [9. Export Board as CSV](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#9-export-board-as-csv)

Retrieve and export board data as a downloadable CSV file.

This API allows you to export all board items and their associated field data from a specific board into a CSV format. It can be used for reporting, data analysis, or backup purposes.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/boards/{board_id}/export_csv`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}/export_csv`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}/export_csv`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
  * `Content-Type`: `application/json`
* **Path Parameters**

  * `board_id`: The unique identifier of the board (e.g., `brd_1c41d851-90f3-44b0-8b51-9628d30c29a6`)
  * `item_id`: The unique identifier of the board item (e.g., `bi_e2513c1e-62d7-4cb0-a0d2-3b10c3dd3423`)
* **Query Params**

  * *(none)*
* **Result:**

  * **Status code: 200 OK**
  * **Content-Type:** `text/csv`
  * **Body Example (truncated):**

  ```
  Name,Age,Record Created On,Lasted Updated On"N","1",10/18/2025 02:55,10/18/2025 02:55
  ```
* **Example:**

  ```
  curl --request GET \--url https://app-gateway.dev.imbrace.co/3rd/boards/brd_5316485d-a155-4e4e-bc6b-958af5cfa47b/export_csv \--header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928'
  ```

## [10. Export Board Items](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#10-export-board-items)

Retrieve and export board items.

This API allows you to export all board items from a specific board.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/boards/{board_id}/export_board_items`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}/export_board_items`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}/export_board_items`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
  * `Content-Type`: `multipart/form-data`
* **Path Parameters**

  * `board_id`: The unique identifier of the board (e.g., `brd_1c41d851-90f3-44b0-8b51-9628d30c29a6`)
* **Query Params**

  * *(none)*
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "message": "Export successful",  "file_name": "file_3957488a-a2b3-436b-9a57-d4276eb5df32.csv",  "download_url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/board_items/file_3957488a-a2b3-436b-9a57-d4276eb5df32.csv",  "record_count": 100}
  ```
* **Example:**

  ```
  curl --request GET \--url https://app-gateway.dev.imbrace.co/3rd/boards/brd_5316485d-a155-4e4e-bc6b-958af5cfa47b/export_board_items \--header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928'
  ```

## [11. Update Board](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#11-update-board)

Update an existing board's information.

This API allows you to update the name, description, and team associations of a specific board.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/3rd/boards/{board_id}`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
  * `Content-Type`: `application/json`
* **Path Parameters**

  * `board_id`: The unique identifier of the board (e.g., `brd_1c41d851-90f3-44b0-8b51-9628d30c29a6`)
* **Request Body (JSON)**

  ```
  {  "name": "TestAssign 2",  "description": "My description 2",  "team_ids": [    "t_162c7a64-c13e-4055-b221-da568f0ee7c9",    "t_14d7e3c3-de90-49a5-89fb-d71e02a49537"  ]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",  "doc_name": "boards",  "business_unit_id": "bu_imbrace_testing",  "order": 2,  "organization_id": "org_imbrace",  "name": "TestAssign 2",  "hidden": false,  "type": "General",  "fields": [    {      "name": "Email",      "description": "dasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhja",      "type": "Email",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": true,      "data": [],      "_id": "65c3242b085dd896c86d297f"    },    {      "name": "Nokia Report Testing",      "type": "Country",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "68edc5b76da47b93262ee516"    },    {      "settings": {        "default_currency_code": "THB"      },      "name": "Currency",      "type": "Currency",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "67cd8eaa6846465b7772536d"    },    {      "name": "Country",      "description": "dasdasdansjdnasjdnasjdnjasndjasndjasndjkasndasjkndjakndjkasndjkasndjkasndjkasndkjanskdadjaskndajksndjasndkjasndjksandkjasndkjasnjkdnasjkdnasjkdnaskjdnaskdasdasdansjdnasjdnasjdnjasndjasndjasndjkasndasjkndjakndjkasndjkasndjkasndjkasndkjanskdadjaskndajksndjasndkjasndjksandkjasndkjasnjkdnasjkdnasjkdnaskjandkjasndkjasnjkdnasjkdnasjkdnaskjdnaskdasdasdansjdnasjdnasjdnjasndjasndjasndjds",      "type": "Country",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "67e3802cf15a6fb22ddedb7f"    },    {      "name": "number",      "type": "Number",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "67a21c1cae791f83be46cb08"    },    {      "name": "Origin",      "type": "Origin",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [        {          "value": "123",          "_id": "123"        },        {          "value": "234",          "_id": "234"        }      ],      "_id": "67cd92a56846465b77729eb5"    },    {      "name": "attachment",      "type": "Attachment",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "676cf93272d5962f16da17c5"    },    {      "name": "TESTING",      "type": "SingleSelection",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [        {          "value": "Maintenance Service",          "_id": "Maintenance Service"        }      ],      "_id": "67771b0f0e351e5e3822211c"    },    {      "settings": {        "default_country_code": "MY"      },      "name": "Phone",      "description": "",      "type": "Phone",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66399ef1677ac4c4a62e8da9"    },    {      "name": "Booking Time",      "type": "Time",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66399f1b677ac4c4a62e9279"    },    {      "name": "Name",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "65c2efd2085dd896c86b8668"    },    {      "name": "Datetime",      "type": "Datetime",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66c69ccfbb95d32becb0c39a"    },    {      "name": "assign to",      "type": "Assignee",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "65c2efdc085dd896c86b8825"    },    {      "name": "Booking Date",      "type": "Date",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66399f00677ac4c4a62e90a9"    }  ],  "public_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",  "created_at": "2024-02-07T02:49:54.081Z",  "updated_at": "2025-10-17T08:46:13.648Z",  "managers": [    {      "team_id": "t_162c7a64-c13e-4055-b221-da568f0ee7c9",      "team_user_ids": [],      "_id": "68f20f09b8347476fe48f3bc"    },    {      "team_id": "t_14d7e3c3-de90-49a5-89fb-d71e02a49537",      "team_user_ids": [],      "_id": "68f20f09b8347476fe48f3bd"    }  ],  "description": "My description 2",  "team_ids": [    "t_162c7a64-c13e-4055-b221-da568f0ee7c9",    "t_14d7e3c3-de90-49a5-89fb-d71e02a49537"  ],  "id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6"}
  ```
* **Example:**

  ```
  curl --request PUT \  --url https://app-gateway.dev.imbrace.co/3rd/boards/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6 \  --header 'content-type: application/json' \  --header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928' \  --data '{  "name": "TestAssign 2",  "description": "My description 2",  "team_ids": [    "t_162c7a64-c13e-4055-b221-da568f0ee7c9",    "t_14d7e3c3-de90-49a5-89fb-d71e02a49537"  ]}'
  ```

## [12. Add Multiple Board Fields](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#12-add-multiple-board-fields)

Add multiple custom fields to an existing board in a single operation.

This API allows you to add multiple custom fields to a specific board at once, supporting various field types like ShortText, Number, and other data types.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/3rd/boards/{board_id}/multiple_board_fields`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}/multiple_board_fields`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}/multiple_board_fields`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
  * `Content-Type`: `application/json`
* **Path Parameters**

  * `board_id`: The unique identifier of the board (e.g., `brd_5316485d-a155-4e4e-bc6b-958af5cfa47b`)
* **Request Body (JSON)**

  ```
  {  "fields": [    {      "name": "Name_10",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "field_id": ""    },    {      "name": "Age_10",      "type": "Number",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "field_id": ""    },    {      "name": "New field 10",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "field_id": ""    }  ]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",  "doc_name": "boards",  "business_unit_id": "bu_imbrace_testing",  "order": 2,  "organization_id": "org_imbrace",  "name": "TestAssign 2",  "hidden": false,  "type": "General",  "fields": [    {      "name": "Name_1",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": true,      "data": [],      "_id": "68f35cbe4cbf5ef0357a0250"    },    {      "name": "New field 10",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "68f3b4b2ccb39ca733ea50f5"    },    {      "name": "Age_10",      "type": "Number",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "68f3b4b2ccb39ca733ea50c5"    },    {      "name": "Name_10",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "68f3b4b1ccb39ca733ea5097"    },    {      "name": "Email",      "description": "dasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhjasbdjasbxdjhasbdhjsabdjhasxbxdhjaxsbdxhjadasbdhjasbdhjsabdjhasbdhjasbdhjasbdhjasbdjhasbdhja",      "type": "Email",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "65c3242b085dd896c86d297f"    },    {      "name": "New field 0",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "68f3509977cc5e2f05945290"    },    {      "name": "Age_0",      "type": "Number",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "68f3509977cc5e2f05945268"    },    {      "name": "Name_0",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "68f3509877cc5e2f05945242"    },    {      "settings": {        "default_currency_code": "THB"      },      "name": "Currency",      "type": "Currency",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "67cd8eaa6846465b7772536d"    },    {      "name": "Country",      "description": "dasdasdansjdnasjdnasjdnjasndjasndjasndjkasndasjkndjakndjkasndjkasndjkasndjkasndkjanskdadjaskndajksndjasndkjasndjksandkjasndkjasnjkdnasjkdnasjkdnaskjdnaskdasdasdansjdnasjdnasjdnjasndjasndjasndjkasndasjkndjakndjkasndjkasndjkasndjkasndkjanskdadjaskndajksndjasndkjasndjksandkjasndkjasnjkdnasjkdnasjkdnaskjandkjasndkjasnjkdnasjkdnasjkdnaskjdnaskdasdasdansjdnasjdnasjdnjasndjasndjasndjds",      "type": "Country",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "67e3802cf15a6fb22ddedb7f"    },    {      "name": "number",      "type": "Number",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "67a21c1cae791f83be46cb08"    },    {      "name": "Origin",      "type": "Origin",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [        {          "value": "123",          "_id": "123"        },        {          "value": "234",          "_id": "234"        }      ],      "_id": "67cd92a56846465b77729eb5"    },    {      "name": "attachment",      "type": "Attachment",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [],      "_id": "676cf93272d5962f16da17c5"    },    {      "name": "TESTING",      "type": "SingleSelection",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "data": [        {          "value": "Maintenance Service",          "_id": "Maintenance Service"        }      ],      "_id": "67771b0f0e351e5e3822211c"    },    {      "settings": {        "default_country_code": "MY"      },      "name": "Phone",      "description": "",      "type": "Phone",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66399ef1677ac4c4a62e8da9"    },    {      "name": "Booking Time",      "type": "Time",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66399f1b677ac4c4a62e9279"    },    {      "name": "Name",      "type": "ShortText",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "65c2efd2085dd896c86b8668"    },    {      "name": "Datetime",      "type": "Datetime",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66c69ccfbb95d32becb0c39a"    },    {      "name": "assign to",      "type": "Assignee",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "65c2efdc085dd896c86b8825"    },    {      "name": "Booking Date",      "type": "Date",      "is_unique_identifier": false,      "is_default": false,      "hidden": false,      "hidden_on_record": false,      "is_identifier": false,      "data": [],      "_id": "66399f00677ac4c4a62e90a9"    }  ],  "public_id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6",  "created_at": "2024-02-07T02:49:54.081Z",  "updated_at": "2025-10-18T15:39:30.988Z",  "managers": [    {      "team_id": "t_162c7a64-c13e-4055-b221-da568f0ee7c9",      "team_user_ids": [],      "_id": "68f203b9dc658fcd6a0f6863"    },    {      "team_id": "t_14d7e3c3-de90-49a5-89fb-d71e02a49537",      "team_user_ids": [],      "_id": "68f203b9dc658fcd6a0f6864"    }  ],  "description": "My description 2",  "team_ids": [    "t_162c7a64-c13e-4055-b221-da568f0ee7c9",    "t_14d7e3c3-de90-49a5-89fb-d71e02a49537"  ],  "id": "brd_1c41d851-90f3-44b0-8b51-9628d30c29a6"}
  ```
* **Example:**

  ```
  curl --request PUT \  --url https://app-gateway.dev.imbrace.co/3rd/boards/brd_5316485d-a155-4e4e-bc6b-958af5cfa47b/multiple_board_fields \  --header 'content-type: application/json' \  --header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928' \  --data '{    "fields": [      {        "name": "Name_10",        "type": "ShortText",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "data": [],        "field_id": ""      },      {        "name": "Age_10",        "type": "Number",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "data": [],        "field_id": ""      },      {        "name": "New field 10",        "type": "ShortText",        "is_unique_identifier": false,        "is_default": false,        "hidden": false,        "hidden_on_record": false,        "field_id": ""      }    ]  }'
  ```

## [13. Delete Board](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#13-delete-board)

Permanently delete a board and all its associated data.

This API allows you to delete a specific board by its ID. This action cannot be undone.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/3rd/boards/{board_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
  * `Content-Type`: `application/json`
* **Path Parameters**

  * `board_id`: The unique identifier of the board to delete (e.g., `brd_f82a6316-a854-4e2b-9394-b12ff50022a0`)
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "message": "is deleted"}
  ```
* **Example:**

  ```
  curl --request DELETE \--url https://app-gateway.dev.imbrace.co/3rd/boards/brd_f82a6316-a854-4e2b-9394-b12ff50022a0 \--header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928'
  ```

## [14. Delete Board Item](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#14-delete-board-item)

Permanently delete a specific board item from a board.

This API allows you to delete a specific board item by its ID from a specific board. This action cannot be undone.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/3rd/boards/{board_id}/board_items/{item_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}/board_items/{item_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}/board_items/{item_id}`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
  * `Content-Type`: `application/json`
* **Path Parameters**

  * `board_id`: The unique identifier of the board containing the item (e.g., `brd_5316485d-a155-4e4e-bc6b-958af5cfa47b`)
  * `item_id`: The unique identifier of the board item to delete (e.g., `bi_88620293-9920-42cd-ac44-58f682b7919c`)
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "message": "board item bi_88620293-9920-42cd-ac44-58f682b7919c is deleted"}
  ```
* **Example:**

  ```
  curl --request DELETE \  --url https://app-gateway.dev.imbrace.co/3rd/boards/brd_5316485d-a155-4e4e-bc6b-958af5cfa47b/board_items/bi_88620293-9920-42cd-ac44-58f682b7919c \  --header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928'
  ```

## [15. Import CSV](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#15-import-csv)

Import data from a CSV file into a specific board.

This API allows you to import data from a CSV file by providing the file URL and field mappings to create board items automatically.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/boards/{board_id}/import_csv`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}/import_csv`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}/import_csv`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
  * `Content-Type`: `application/json`
* **Path Parameters**

  * `board_id`: The unique identifier of the board (e.g., `brd_5316485d-a155-4e4e-bc6b-958af5cfa47b`)
* **Request Body (JSON)**

  ```
  {  "fileUrl": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_KgpLuQJpmZJVr9i0LvTNYxZSg4.csv",  "mappings": [    {      "csvHeader": "Age",      "boardFieldId": "68f301635412834c555237f1",      "boardFieldName": "Age"    },    {      "csvHeader": "Name",      "boardFieldId": "68f301635412834c555237e6",      "boardFieldName": "Name"    }  ]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "status": "success",  "message": "CSV import completed",  "results": {    "total": 1,    "successful": 1,    "failed": 0,    "skipped": 0,    "details": {      "success": [        {          "row": 1,          "mappedFields": [            {              "boardFieldName": "Name",              "value": "A"            },            {              "boardFieldName": "Age",              "value": "2"            }          ]        }      ],      "errors": [],      "skipped": 0,      "total": 1    }  }}
  ```
* **Example:**

  ```
  curl --request POST \  --url https://app-gateway.dev.imbrace.co/3rd/boards/brd_5316485d-a155-4e4e-bc6b-958af5cfa47b/import_csv \  --header 'content-type: application/json' \  --header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928' \  --data '{    "fileUrl": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_KgpLuQJpmZJVr9i0LvTNYxZSg4.csv",    "mappings": [      {        "csvHeader": "Age",        "boardFieldId": "68f301635412834c555237f1",        "boardFieldName": "Age"      },      {        "csvHeader": "Name",        "boardFieldId": "68f301635412834c555237e6",        "boardFieldName": "Name"      }    ]  }'
  ```

## [16. Import Exported Board Items](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#16-import-exported-board-items)

Import data from an exported CSV file into a specific board.

This API allows you to import data from a previously exported CSV file by providing the file URL and field mappings to create board items automatically.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/boards/{board_id}/import_exported_board_items`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/boards/{board_id}/import_exported_board_items`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/boards/{board_id}/import_exported_board_items`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
  * `Content-Type`: `application/json`
* **Path Parameters**

  * `board_id`: The unique identifier of the board (e.g., `brd_5316485d-a155-4e4e-bc6b-958af5cfa47b`)
* **Request Body (JSON)**

  ```
  {  "fileUrl": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_KgpLuQJpmZJVr9i0LvTNYxZSg4.csv",  "mappings": [    {      "csvHeader": "Age",      "boardFieldId": "68f301635412834c555237f1",      "boardFieldName": "Age"    },    {      "csvHeader": "Name",      "boardFieldId": "68f301635412834c555237e6",      "boardFieldName": "Name"    }  ]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "status": "success",  "message": "Import completed",  "results": {    "total": 1,    "success": 1,    "errors": 0,    "error_details": []  }}
  ```
* **Example:**

  ```
  curl --request POST \  --url https://app-gateway.dev.imbrace.co/3rd/boards/brd_5316485d-a155-4e4e-bc6b-958af5cfa47b/import_exported_board_items \  --header 'content-type: application/json' \  --header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928' \  --data '{    "fileUrl": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_KgpLuQJpmZJVr9i0LvTNYxZSg4.csv",    "mappings": [      {        "csvHeader": "Age",        "boardFieldId": "68f301635412834c555237f1",        "boardFieldName": "Age"      },      {        "csvHeader": "Name",        "boardFieldId": "68f301635412834c555237e6",        "boardFieldName": "Name"      }    ]  }'
  ```

## [17. Upload File (Alternative)](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#17-upload-file-alternative)

Upload a file to the board system using form-data format.

This API allows you to upload files using multipart/form-data format with a different endpoint structure.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/boards/upload`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/boards/upload`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/boards/upload`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
* **Query Params**

  * *(none)*
* **Body:**

  * Form-data with file attachment
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/undefined/file_qmGJccAZUdraW5YWulX2QNKXw3.txt"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/boards/upload' \--header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928' \--form 'file=@"og3Z9SYm2/Receipt-2573-6097.pdf"'
  ```
* Note: Please use postman to test this API.

## [18. File Upload (Alternative Endpoint)](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/dataBoard#18-file-upload-alternative-endpoint)

Upload a file to the board system and get a public URL using an alternative endpoint.

This API allows you to upload files using multipart/form-data format and returns a public URL that can be used to access the uploaded file.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/boards/_fileupload`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/boards/_fileupload`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/boards/_fileupload`
* **Headers:**

  * `x-access-token`: *`Contact to iMBRACE`*
* **Request Body (Form Data)**

  * `file`: The file to upload (binary data)
* **Result:**

  * **Status code: 200 OK**

  ```
  {  "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/undefined/file_HXdtIsQZTsiehG3N9kftxmXl5g.pdf"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/boards/_fileupload' \  --header 'x-access-token: api_72bbc6ba-0f52-489a-917e-c7200932c928' \  --form 'file=@"n8YvdroJZ/Receipt-2573-6097.pdf"'
  ```
* Note: Please use postman to test this API.
