[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Server Gateway](https://devportal.dev.imbrace.co/docs/api-document/server-gateways)

# AI Agent

AI Agent APIs enhance user interaction by providing intelligent automation and decision-making support. These APIs allow you to integrate AI-driven features into workflows such as automated approval, task assignments, and user interactions through chat-based interfaces.

# [AI Agent Server Gateway APIs](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis#ai-agent-server-gateway-apis)

### [1. Answer Question](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis#1-answer-question)

Ask a question to an AI Agent and get an intelligent response using RAG (Retrieval-Augmented Generation).

* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/ai-service/rag/answer_question`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/ai-service/rag/answer_question`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`: `Contact to iMBRACE`
* **Body:**

  ```
      {        "text": "are there any spa services in the hotel?",        "instructions": "",        "thread_id": "testin-4243437433gg454bbbdfm",        "role": "user",        "assistant_id": "83be0c01-8242-4339-b280-2606260842ae",        "streaming": true    }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "thread_id": "testin-4243437433gg454bbbdfm",    "message": "Your name is Michael.",    "is_partial": true,    "message_id": "f7e39bb6-66d9-4c51-bc3d-1c3b94843482",    "sources": [],    "echart": null,    "echart_id": ""}
  ```
* **Example:**

  ```
      curl --request POST \    --url https://app-gateway.demo.imbrace.co/3rd/ai-service/rag/answer_question \    --header 'X-Api-Key: your-api-key' \    --header 'content-type: application/json' \    --data '{        "text": "are there any spa services in the hotel?",        "instructions": "",        "thread_id": "testin-4243437433gg454bbbdfm",        "role": "user",        "assistant_id": "83be0c01-8242-4339-b280-2606260842ae",        "streaming": true    }'
  ```

### [2. Get File by ID](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis#2-get-file-by-id)

Retrieve detailed information about a specific file by its ID.

* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/ai-service/files/{file_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/ai-service/files/{file_id}`
* **Headers:**

  * `Content-Type`: `multipart/form-data`
  * `X-Access-Token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `file_id`: The ID of the file to retrieve
* **Result:**

  * **Status code: 200 OK**

  ```
      {        "_id": "685b7b5f3aeda6244194c660",        "id": "69c56098-1fc9-4937-b870-dfad8fd23144",        "organization_id": "org_imbrace",        "assistant_id": "dsdsds",        "file_name": "FSHongKong-Overview-eBrochure-EN-2017.pdf",        "file_size": 6301378,        "file_type": "application/pdf",        "board_id": "",        "boarditem_id": "",        "url": "s3://imbrace-uat/ai-chat/org_imbrace_69c56098-1fc9-4937-b870-dfad8fd23144_FSHongKong-Overview-eBrochure-EN-2017.pdf",        "file_id": "69c56098-1fc9-4937-b870-dfad8fd23144",        "updated_at": "2025-06-25T04:30:23",        "created_at": "2025-06-25T04:30:23",        "deleted_at": null    }
  ```
* **Example:**

  ```
      curl --request GET \    --url https://app-gateway.demo.imbrace.co/3rd/ai-service/rag/files/69c56098-1fc9-4937-b870-dfad8fd23144 \    --header 'X-Api-Key: your-api-key' \    --header 'content-type: multipart/form-data' \    --header 'x-organization-id: org_imbrace'
  ```

### [3. Upload File](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis#3-upload-file)

Upload a file to an AI Agent's knowledge base for RAG (Retrieval-Augmented Generation).

* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/ai-service/rag/files`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/ai-service/rag/files`
* **Headers:**

  * `Content-Type`: `multipart/form-data`
* **Body (Form Data):**

  * `file`: The file to upload
  * `text_input`: Optional text input for additional context
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "id": "4facd6e7-5cad-4808-ad58-01c36da70ab0",    "bytes": 309438,    "filename": "Receipt-2573-6097.pdf",    "assistant_id": "",    "created_at": "2025-10-21T09:17:19.780597",    "board_id": "",    "boarditem_id": "",    "extraction_method": "enhanced_pdf_extractor_with_ocr",    "tables_extracted": 0,    "text_chunks_extracted": 1,    "url": "s3://imbrace-uat/ai-chat/org_05994568-2a16-4550-ae73-0401a7f5bde0_4facd6e7-5cad-4808-ad58-01c36da70ab0_Receipt-2573-6097.pdf"}
  ```
* **Example:**

  ```
      curl --request POST \    --url https://app-gateway.demo.imbrace.co/3rd/ai-service/rag/files \    --header 'content-type: multipart/form-data' \    --form file=@/path/to/your/file.pdf \    --form 'text_input=my name is michael'
  ```

### [4. Delete File](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis#4-delete-file)

Delete a file from an AI Agent's knowledge base.

* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/3rd/ai-service/rag/files/{file_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/3rd/ai-service/rag/files/{file_id}`
* **Headers:**

  * `Content-Type`: `multipart/form-data`
  * `X-Access-Token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `file_id`: The ID of the file to delete
* **Result:**

  * **Status code: 200 OK**

  ```
      {        "deleted_count": 1,        "regular_rag_deleted": 1,        "new_rag_deleted": 0,        "file_id": "8b2fc933-a376-4f51-a2fe-727324fa4c9d",        "organization_id": "org_imbrace"    }
  ```
* **Example:**

  ```
      curl --request DELETE \    --url https://app-gateway.demo.imbrace.co/3rd/ai-service/rag/files/a8b0b955-df70-4150-9a7f-80c392032962 \    --header 'X-Api-Key: your-api-key' \    --header 'content-type: multipart/form-data' \    --header 'x-organization-id: org_imbrace'
  ```

### [5. Create Embedding](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis#5-create-embedding)

Create embeddings for board items data to enable AI-powered search and retrieval.

* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/ai-service/embedding`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/ai-service/embedding`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`: `Contact to iMBRACE`
* **Body:**

  ```
      [        {            "_id": "boarditem_123",            "board_id": "board_456",            "organization_id": "org_789",            "fields_data": [                {                    "_id": "field_001",                    "name": "title"                },                {                    "_id": "field_002",                    "name": "description"                },                {                    "_id": "field_003",                    "name": "category"                },                {                    "_id": "field_004",                    "name": "attachments"                }            ],            "fields": {                "field_001": "Sample Project Title",                "field_002": "This is a detailed description of the project with important information.",                "field_003": "Technology",                "field_004": [                    {                        "data": {                            "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_7Z8iiQLsI0Ubh4UJ6JMq1xhpk8.pdf",                            "filename": "sample_document.pdf",                            "mimetype": "application/pdf"                        }                    }                ]            }        },        {            "_id": "boarditem_124",            "board_id": "board_456",            "organization_id": "org_789",            "fields_data": [                {                    "_id": "field_001",                    "name": "title"                },                {                    "_id": "field_002",                    "name": "description"                },                {                    "_id": "field_003",                    "name": "priority"                }            ],            "fields": {                "field_001": "Another Project",                "field_002": "Second project with different metadata for testing purposes.",                "field_003": "High"            }        }    ]
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {        "success": true,        "message": "Data stored",        "data": [            {                "title": "Sample Project Title",                "description": "This is a detailed description of the project with important information.",                "category": "Technology",                "attachments": [                    {                        "data": {                            "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_7Z8iiQLsI0Ubh4UJ6JMq1xhpk8.pdf",                            "filename": "sample_document.pdf",                            "mimetype": "application/pdf"                        }                    }                ],                "boarditem_id": "boarditem_123",                "board_id": "board_456",                "organization_id": "org_789"            },            {                "title": "Another Project",                "description": "Second project with different metadata for testing purposes.",                "priority": "High",                "boarditem_id": "boarditem_124",                "board_id": "board_456",                "organization_id": "org_789"            }        ]    }
  ```
* **Example:**

  ```
      curl --request POST \    --url https://app-gateway.demo.imbrace.co/3rd/ai-service/embedding \    --header 'X-Api-Key: your-api-key' \    --header 'content-type: application/json' \    --data '[        {            "_id": "boarditem_123",            "board_id": "board_456",            "organization_id": "org_789",            "fields_data": [                {                    "_id": "field_001",                    "name": "title"                },                {                    "_id": "field_002",                    "name": "description"                }            ],            "fields": {                "field_001": "Sample Project Title",                "field_002": "This is a detailed description of the project with important information."            }        }    ]'
  ```

### [6. Delete Embedding by Board ID](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis#6-delete-embedding-by-board-id)

Delete embeddings associated with a specific board ID.

* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/3rd/ai-service/embedding/board/{board_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/3rd/ai-service/embedding/board/{board_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `board_id`: The ID of the board to delete embeddings for
* **Body:**

  ```
      {        "text": "What is my name",        "instructions": "",        "thread_id": "test-tool-1",        "role": "user",        "secret": "擁抱科技",        "file_ids": ["db83acff-1edb-4317-9f4e-1d4fffc30240"],        "assistant_id": "",        "streaming": false    }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {        "success": true,        "message": "Deleted 0 records with board_id = 123",        "deletedCount": 0    }
  ```
* **Example:**

  ```
      curl --request DELETE \    --url https://app-gateway.demo.imbrace.co/3rd/ai-service/embedding/board/123 \    --header 'X-Api-Key: your-api-key' \    --header 'content-type: application/json' \    --data '{        "text": "What is my name",        "instructions": "",        "thread_id": "test-tool-1",        "role": "user",        "secret": "擁抱科技",        "file_ids": ["db83acff-1edb-4317-9f4e-1d4fffc30240"],        "assistant_id": "",        "streaming": false    }'
  ```

### [7. Delete Embedding by Board Item ID](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis#7-delete-embedding-by-board-item-id)

Delete embeddings associated with a specific board item ID.

* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/3rd/ai-service/embedding/{boarditem_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/3rd/ai-service/embedding/{boarditem_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `boarditem_id`: The ID of the board item to delete embeddings for
* **Body:**

  ```
      {        "text": "What is my name",        "instructions": "",        "thread_id": "test-tool-1",        "role": "user",        "secret": "擁抱科技",        "file_ids": ["db83acff-1edb-4317-9f4e-1d4fffc30240"],        "assistant_id": "",        "streaming": false    }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {        "success": true,        "message": "Deleted 0 records with boarditem_id = 123",        "deletedCount": 0    }
  ```
* **Example:**

  ```
      curl --request DELETE \    --url https://app-gateway.demo.imbrace.co/3rd/ai-service/embedding/123 \    --header 'X-Api-Key: your-api-key' \    --header 'content-type: application/json' \    --data '{        "text": "What is my name",        "instructions": "",        "thread_id": "test-tool-1",        "role": "user",        "secret": "擁抱科技",        "file_ids": ["db83acff-1edb-4317-9f4e-1d4fffc30240"],        "assistant_id": "",        "streaming": false    }'
  ```

### [8. Get ECharts by Thread ID](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/aIAgentApis#8-get-echarts-by-thread-id)

Delete embeddings associated with a specific board item ID.

* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/ai-service/rag/echarts/{thread_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/ai-service/embedding/{thread_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `thread_id`: The ID of the thread_id
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "echarts": [        {            "_id": "afd439e5-2655-489b-bbf1-0c113190ccfb",            "thread_id": "66f2ff9c-7341-4ca4-81c7-e9d5469d3364",            "echart_data": {                "title": {                    "text": "Student Total Scores and Rankings"                },                "tooltip": {},                "legend": {                    "data": [                        "Total Score"                    ]                },                "xAxis": {                    "type": "category",                    "data": [                        "Ella Vu",                        "Alice Nguyen",                        "Brian Tran",                        "David Pham",                        "Cindy Le"                    ]                },                "yAxis": {                    "type": "value"                },                "series": [                    {                        "name": "Total Score",                        "type": "bar",                        "data": [                            279,                            273,                            265,                            259,                            235                        ]                    }                ]            },            "organization_id": "org_639ac074-5fd4-4a16-95b7-69644b849697",            "created_at": "2025-10-20T05:18:56.007000",            "updated_at": "2025-10-20T05:18:56.007000"        },        {            "_id": "4b9a4d27-36e4-4ab8-ab15-3334066f7c0f",            "thread_id": "66f2ff9c-7341-4ca4-81c7-e9d5469d3364",            "echart_data": {                "title": {                    "text": "Student Ranking Based on Math Score"                },                "tooltip": {},                "legend": {                    "data": [                        "Math Score"                    ]                },                "xAxis": {                    "type": "category",                    "data": [                        "Alice Nguyen",                        "Brian Tran",                        "Cindy Le",                        "David Pham",                        "Ella Vu"                    ]                },                "yAxis": {                    "type": "value"                },                "series": [                    {                        "name": "Math Score",                        "type": "bar",                        "data": [                            95,                            89,                            76,                            88,                            92                        ]                    }                ]            },            "organization_id": "org_639ac074-5fd4-4a16-95b7-69644b849697",            "created_at": "2025-10-20T05:22:22.726000",            "updated_at": "2025-10-20T05:22:22.726000"        }    ]}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.demo.imbrace.co/3rd/ai-service/rag/echarts/66f2ff9c-7341-4ca4-81c7-e9d5469d3364' \--header 'x-access-token: api_957c33c5-2342-4354-9e2e-8c1d50593bb0'
  ```
