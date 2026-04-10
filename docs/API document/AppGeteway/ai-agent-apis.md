# AI Agent APIs

AI Agent APIs enhance user interaction by providing intelligent automation and decision-making support. These APIs allow you to integrate AI-driven features into workflows such as automated approval, task assignments, and user interactions through chat-based interfaces.

---

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#overview)

Below are APIs for retrieving, creating, updating, deleting, and managing AI Agents, as well as handling workflows associated with them.

---

### [1. Get AI Agent](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#1-get-ai-agent)

Retrieve a list of all AI Agents in the system.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/templates`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/templates`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/templates`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
      {
      "data": {
          "_id": "uc_71cfa689-ea47-46ce-9845-f6e1488a5a15",
          "doc_name": "UseCase",
          "title": "test1",
          "organization_id": "org_imbrace",
          "short_description": "",
          "type": "custom",
          "channel_id": "ch_6f4df538-ce1b-455f-b563-819880e17b9b",
          "features": [],
          "tags": [],
          "demo_url": "https://chat-widget.imbrace.co?channel_id=ch_6f4df538-ce1b-455f-b563-819880e17b9b",
          "suggestion_prompts": [],
          "supported_channels": [
              {
                  "title": "channel_",
                  "icon": "",
                  "_id": "68aed93be67d29aeadb2a87b"
              }
          ],
          "assistant_id": "853d4df5-f6aa-4367-9c4e-5bc366e9e566",
          "user_id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",
          "is_deleted": false,
          "updated_at": "2025-08-27T10:08:59.288Z",
          "how_it_works": [],
          "integrations": [],
          "createdAt": "2025-08-27T09:00:16.243Z",
          "updatedAt": "2025-08-27T10:08:59.289Z",
          "public_id": "f089b14c-ddf5-4e25-b79c-58e2b446d324",
          "created_at": "2025-08-27T09:00:16.243Z"
          }
      }
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.imbrace.co/v2/backend/templates' \--header 'x-access-token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df'
  ```

### [2. Get AI Agent by ID](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#2-get-ai-agent-by-id)

Retrieve details of a specific AI Agent by its ID.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/templates/{template_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/templates/{template_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/templates/{template_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Result:**

  * **Status code: 200 OK**

  ```
          {
              "data": {
                  "_id": "uc_71cfa689-ea47-46ce-9845-f6e1488a5a15",
                  "doc_name": "UseCase",
                  "title": "test1",
                  "organization_id": "org_imbrace",
                  "short_description": "",
                  "type": "custom",
                  "channel_id": "ch_6f4df538-ce1b-455f-b563-819880e17b9b",
                  "features": [],
                  "tags": [],
                  "demo_url": "https://chat-widget.imbrace.co?channel_id=ch_6f4df538-ce1b-455f-b563-819880e17b9b",
                  "suggestion_prompts": [],
                  "supported_channels": [
                      {
                          "title": "channel_",
                          "icon": "",
                          "_id": "68aed93be67d29aeadb2a87b"
                      }
                  ],
                  "assistant_id": "853d4df5-f6aa-4367-9c4e-5bc366e9e566",
                  "user_id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",
                  "is_deleted": false,
                  "updated_at": "2025-08-27T10:08:59.288Z",
                  "how_it_works": [],
                  "integrations": [],
                  "createdAt": "2025-08-27T09:00:16.243Z",
                  "updatedAt": "2025-08-27T10:08:59.289Z",
                  "public_id": "f089b14c-ddf5-4e25-b79c-58e2b446d324",
                  "created_at": "2025-08-27T09:00:16.243Z"
              }
          }  
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.imbrace.co/v2/backend/templates/uc_71cfa689-ea47-46ce-9845-f6e1488a5a15' \--header 'x-access-token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df'
  ```

### [3. Create AI Agent](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#3-create-ai-agent)

Create a new AI Agent with configuration details.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v2/backend/templates/custom`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v2/backend/templates/custom`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v2/backend/templates/custom`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
      {
          "assistant": {
              "agent_type": "agent",
              "banned_words": "",
              "category": [],
              "channel": "",
              "core_task": "",
              "credential_name": "Standard AI Assistant | Test Agent",
              "description": "This name is for internal management only. It won't be shown in the conversation as the agent's name.",
              "file_ids": [],
              "instructions": "",
              "knowledge_hubs": [],
              "metadata": {
                  "channel_id": "",
                  "other_requirements": [],
                  "team_ids": []
              },
              "mode": "standard",
              "model_id": "Default",
              "name": "Test Agent",
              "personality_role": "",
              "response_length": "",
              "show_thinking_process": false,
              "streaming": false,
              "sub_agents": [],
              "team_leads": [],
              "temperature": 0.1,
              "tone_and_style": "",
              "use_memory": true,
              "workflow_function_call": [],
              "workflow_name": "Standard AI Assistant  | Test Agent"
          },
          "usecase": {
              "demo_url": "https://chat-widget.imbrace.co",
              "short_description": "This demo",
              "supported_channels": [
                  {
                      "icon": "",
                      "title": "channel_"
                  }
              ],
              "title": "Test Agent"
          }
      }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {
      "data": {
          "doc_name": "UseCase",
          "title": "Test Agent",
          "organization_id": "org_imbrace",
          "short_description": "This demo",
          "type": "custom",
          "channel_id": "ch_22723388-b75b-43c6-b21c-8cfef9becd01",
          "features": [],
          "tags": [],
          "demo_url": "https://chat-widget.imbrace.co?channel_id=ch_22723388-b75b-43c6-b21c-8cfef9becd01",
          "suggestion_prompts": [],
          "supported_channels": [
              {
                  "title": "channel_",
                  "icon": "",
                  "_id": "68ba559ae67d29aeadb329f5"
              }
          ],
          "assistant_id": "d2d01130-4681-4852-b8d4-3bd2366cfb70",
          "user_id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",
          "is_deleted": false,
          "_id": "uc_ea70a427-3999-48a3-a212-db9e5041d85d",
          "updated_at": "2025-09-05T03:14:34.612Z",
          "how_it_works": [],
          "integrations": [],
          "createdAt": "2025-09-05T03:14:34.612Z",
          "updatedAt": "2025-09-05T03:14:34.612Z",
          "public_id": "623291f2-deaa-4283-a381-0dfffaf4fcde",
          "created_at": "2025-09-05T03:14:34.612Z"
      }
  }
  ```

  * **Status code: 400 Bad Request**

  ```
  {    "message": "UseCase with title Test Agent already exists in organization name "}
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.imbrace.co/v2/backend/templates/custom' \
      --header 'x-access-token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \
      --header 'Content-Type: application/json' \
      --data '{
          "assistant": {
              "agent_type": "agent",
              "banned_words": "",
              "category": [],
              "channel": "",
              "core_task": "",
              "credential_name": "Standard AI Assistant | Test Agent",
              "description": "This name is for internal management only. It won'\''t be shown in the conversation as the agent'\''s name.",
              "file_ids": [],
              "instructions": "",
              "knowledge_hubs": [],
              "metadata": {
                  "channel_id": "",
                  "other_requirements": [],
                  "team_ids": []
              },
              "mode": "standard",
              "model_id": "Default",
              "name": "Test Agent",
              "personality_role": "",
              "response_length": "",
              "show_thinking_process": false,
              "streaming": false,
              "sub_agents": [],
              "team_leads": [],
              "temperature": 0.1,
              "tone_and_style": "",
              "use_memory": true,
              "workflow_function_call": [],
              "workflow_name": "Standard AI Assistant  | Test Agent"
          },
          "usecase": {
              "demo_url": "https://chat-widget.imbrace.co",
              "short_description": "This demo",
              "supported_channels": [
                  {
                      "icon": "",
                      "title": "channel_"
                  }
              ],
              "title": "Test Agent"
          }
      }'
  ```

### [4. Update AI Agent](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#4-update-ai-agent)

Update an existing AI Agent’s details.

* **Endpoint for Product:** `PATCH https://app-gateway.imbrace.co/v2/backend/templates/{template_id}/custom`
* **Endpoint for Demo:** `PATCH https://app-gateway.demo.imbrace.co/v2/backend/templates/{template_id}/custom`
* **Endpoint for Dev:** `PATCH https://app-gateway.dev.imbrace.co/v2/backend/templates/{template_id}/custom`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
      {
      "usecase": {
          "title": "Agent updated",
          "short_description": "Testing updated"
      },
      "assistant": {
          "name": "Agent updated",
          "description": "Testing updated",
          "channel": "whatsapp",
          "category": [
          "Category 1"
          ],
          "personality_role": "You are a friendly and professional assistant who acts as a Customer Support Representative for an e-commerce platform.",
          "core_task": "Your tasks include answering customer inquiries and providing order status updates.",
          "tone_and_style": "Always maintain a professional tone, ensure clarity in your explanations.",
          "response_length": "within 150 words",
          "banned_words": "bullshit, dammit",
          "file_ids": [],
          "workflow_name": "worflow test 12",
          "credential_id": 0,
          "credential_name": "placeholder",
          "mode": "standard"
      }
      }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "data": {
              "_id": "uc_510cf446-d520-4257-9753-1b15ea246b95",
              "doc_name": "UseCase",
              "title": "Agent updated",
              "organization_id": "org_imbrace",
              "short_description": "Testing updated",
              "type": "custom",
              "channel_id": "ch_552f3ef4-0c45-4e3a-b3c6-588946862da1",
              "features": [],
              "tags": [],
              "demo_url": "https://chat-widget.imbrace.co?channel_id=ch_552f3ef4-0c45-4e3a-b3c6-588946862da1",
              "suggestion_prompts": [],
              "supported_channels": [
                  {
                      "title": "channel_",
                      "icon": "",
                      "_id": "68ba5718e67d29aeadb32ed0"
                  }
              ],
              "assistant_id": "3d855968-4830-4104-aca6-9a86bfdd10a9",
              "user_id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",
              "is_deleted": false,
              "updated_at": "2025-09-05T03:21:43.262Z",
              "how_it_works": [],
              "integrations": [],
              "createdAt": "2025-09-05T03:20:56.940Z",
              "updatedAt": "2025-09-05T03:21:43.262Z",
              "public_id": "38e17846-3445-48f8-9231-a9733191a999",
              "created_at": "2025-09-05T03:20:56.941Z"
          }
      }
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "UseCase with id undefined doesn't exist"}
  ```
* **Example:**

  ```
      curl --location --request PATCH 'https://app-gateway.imbrace.co/v2/backend/templates/uc_510cf446-d520-4257-9753-1b157a246b95/custom' \
      --header 'x-access-token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \
      --header 'Content-Type: application/json' \
      --data '{
      "usecase": {
          "title": "Agent updated",
          "short_description": "Testing updated"
      },
      "assistant": {
          "name": "Agent updated",
          "description": "Testing updated",
          "channel": "whatsapp",
          "category": [
          "Category 1"
          ],
          "personality_role": "You are a friendly and professional assistant who acts as a Customer Support Representative for an e-commerce platform.",
          "core_task": "Your tasks include answering customer inquiries and providing order status updates.",
          "tone_and_style": "Always maintain a professional tone, ensure clarity in your explanations.",
          "response_length": "within 150 words",
          "banned_words": "bullshit, dammit",
          "file_ids": [],
          "workflow_name": "worflow test 12",
          "credential_id": 0,
          "credential_name": "placeholder",
          "mode": "standard"
      }
      }'
  ```

### [5. Delete AI Agent](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#5-delete-ai-agent)

Delete an AI Agent from the system.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/v2/backend/templates/{template_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/v2/backend/templates/{template_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/v2/backend/templates/{template_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
      {     "message": "UseCase deleted successfully"    }
  ```
* **Example:**

  ```
      curl --location --request DELETE 'https://app-gateway.imbrace.co/v2/backend/templates/uc_510cf446-d520-4257-9753-1b15ea246b95' \    --header 'x-access-token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \    --data ''
  ```

### [6. Answer Question](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#6-answer-question)

Ask a question to an AI Agent and get an intelligent response using RAG (Retrieval-Augmented Generation).

* **Endpoint for Demo:** `POST https://aiv2.demo.imbrace.lan/api/v1/rag/answer_question`
* **Endpoint for Dev:** `POST https://aiv2.dev.imbrace.lan/api/v1/rag/answer_question`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Api-Key`: Bearer
    **Your Access Token****Your Access Token**
  * `x-organization-id`: `Your organization ID`
* **Body:**

  ```
      {
          "text": "are there any spa services in the hotel?",
          "instructions": "",
          "thread_id": "testin-4243437433gg454bbbdfm",
          "role": "user",
          "assistant_id": "83be0c01-8242-4339-b280-2606260842ae",
          "streaming": true
      }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {
          "thread_id": "testin-4243437433gg454bbbdfm",
          "message": "Your name is Michael.",
          "is_partial": true,
          "message_id": "f7e39bb6-66d9-4c51-bc3d-1c3b94843482",
          "sources": [],
          "echart": null,
          "echart_id": ""
      }
  ```
* **Example:**

  ```
      curl --request POST \
      --url https://aiv2.dev.imbrace.lan/api/v1/rag/answer_question \
      --header 'X-Api-Key: your-api-key' \
      --header 'content-type: application/json' \
      --header 'x-organization-id: org_imbrace' \
      --data '{
          "text": "are there any spa services in the hotel?",
          "instructions": "",
          "thread_id": "testin-4243437433gg454bbbdfm",
          "role": "user",
          "assistant_id": "83be0c01-8242-4339-b280-2606260842ae",
          "streaming": true
      }'
  ```

### [7. Get File by ID](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#7-get-file-by-id)

Retrieve detailed information about a specific file by its ID.

* **Endpoint for Demo:** `GET https://aiv2.demo.imbrace.lan/api/v1/rag/files/{file_id}`
* **Endpoint for Dev:** `GET https://aiv2.dev.imbrace.lan/api/v1/rag/files/{file_id}`
* **Headers:**

  * `Content-Type`: `multipart/form-data`
  * `X-Api-Key`: Bearer
    **Your Access Token****Your Access Token**
  * `x-organization-id`: `Your organization ID`
* **Path Parameters:**

  * `file_id`: The ID of the file to retrieve
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "_id": "685b7b5f3aeda6244194c660",
          "id": "69c56098-1fc9-4937-b870-dfad8fd23144",
          "organization_id": "org_imbrace",
          "assistant_id": "dsdsds",
          "file_name": "FSHongKong-Overview-eBrochure-EN-2017.pdf",
          "file_size": 6301378,
          "file_type": "application/pdf",
          "board_id": "",
          "boarditem_id": "",
          "url": "s3://imbrace-uat/ai-chat/org_imbrace_69c56098-1fc9-4937-b870-dfad8fd23144_FSHongKong-Overview-eBrochure-EN-2017.pdf",
          "file_id": "69c56098-1fc9-4937-b870-dfad8fd23144",
          "updated_at": "2025-06-25T04:30:23",
          "created_at": "2025-06-25T04:30:23",
          "deleted_at": null
      }
  ```
* **Example:**

  ```
      curl --request GET \
      --url https://aiv2.dev.imbrace.lan/api/v1/rag/files/69c56098-1fc9-4937-b870-dfad8fd23144 \
      --header 'X-Api-Key: your-api-key' \
      --header 'content-type: multipart/form-data' \
      --header 'x-organization-id: org_imbrace'
  ```

### [8. Upload File](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#8-upload-file)

Upload a file to an AI Agent's knowledge base for RAG (Retrieval-Augmented Generation).

* **Endpoint for Demo:** `POST https://aiv2.demo.imbrace.lan/api/v1/rag/files`
* **Endpoint for Dev:** `POST https://aiv2.dev.imbrace.lan/api/v1/rag/files`
* **Headers:**

  * `Content-Type`: `multipart/form-data`
  * `x-organization-id`: `Your organization ID`
* **Body (Form Data):**

  * `file`: The file to upload
  * `text_input`: Optional text input for additional context
* **Result:**

  * **Status code: 200 OK**

  ```
  {
      "id": "4facd6e7-5cad-4808-ad58-01c36da70ab0",
      "bytes": 309438,
      "filename": "Receipt-2573-6097.pdf",
      "assistant_id": "",
      "created_at": "2025-10-21T09:17:19.780597",
      "board_id": "",
      "boarditem_id": "",
      "extraction_method": "enhanced_pdf_extractor_with_ocr",
      "tables_extracted": 0,
      "text_chunks_extracted": 1,
      "url": "s3://imbrace-uat/ai-chat/org_05994568-2a16-4550-ae73-0401a7f5bde0_4facd6e7-5cad-4808-ad58-01c36da70ab0_Receipt-2573-6097.pdf"
  }
  ```
* **Example:**

  ```
      curl --request POST \
      --url https://aiv2.dev.imbrace.lan/api/v1/rag/files \
      --header 'content-type: multipart/form-data' \
      --header 'x-organization-id: org_imbrace' \
      --form file=@/path/to/your/file.pdf \
      --form 'text_input=my name is michael'
  ```

### [9. Delete File](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#9-delete-file)

Delete a file from an AI Agent's knowledge base.

* **Endpoint for Demo:** `DELETE https://aiv2.demo.imbrace.lan/api/v1/rag/files/{file_id}`
* **Endpoint for Dev:** `DELETE https://aiv2.dev.imbrace.lan/api/v1/rag/files/{file_id}`
* **Headers:**

  * `Content-Type`: `multipart/form-data`
  * `x-organization-id`: `Your organization ID`
* **Path Parameters:**

  * `file_id`: The ID of the file to delete
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "deleted_count": 1,
          "regular_rag_deleted": 1,
          "new_rag_deleted": 0,
          "file_id": "8b2fc933-a376-4f51-a2fe-727324fa4c9d",
          "organization_id": "org_imbrace"
      }
  ```
* **Example:**

  ```
      curl --request DELETE \
      --url https://aiv2.dev.imbrace.lan/api/v1/rag/files/a8b0b955-df70-4150-9a7f-80c392032962 \
      --header 'X-Api-Key: your-api-key' \
      --header 'content-type: multipart/form-data' \
      --header 'x-organization-id: org_imbrace'
  ```

### [10. Create Embedding](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#10-create-embedding)

Create embeddings for board items data to enable AI-powered search and retrieval.

* **Endpoint for Demo:** `POST https://aiv2.demo.imbrace.lan/api/v1/embedding`
* **Endpoint for Dev:** `POST https://aiv2.dev.imbrace.lan/api/v1/embedding`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Api-Key`: Bearer
    **Your Access Token****Your Access Token**
  * `x-organization-id`: `Your organization ID`
* **Body:**

  ```
      [
          {
              "_id": "boarditem_123",
              "board_id": "board_456",
              "organization_id": "org_789",
              "fields_data": [
                  {
                      "_id": "field_001",
                      "name": "title"
                  },
                  {
                      "_id": "field_002",
                      "name": "description"
                  },
                  {
                      "_id": "field_003",
                      "name": "category"
                  },
                  {
                      "_id": "field_004",
                      "name": "attachments"
                  }
              ],
              "fields": {
                  "field_001": "Sample Project Title",
                  "field_002": "This is a detailed description of the project with important information.",
                  "field_003": "Technology",
                  "field_004": [
                      {
                          "data": {
                              "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_7Z8iiQLsI0Ubh4UJ6JMq1xhpk8.pdf",
                              "filename": "sample_document.pdf",
                              "mimetype": "application/pdf"
                          }
                      }
                  ]
              }
          },
          {
              "_id": "boarditem_124",
              "board_id": "board_456",
              "organization_id": "org_789",
              "fields_data": [
                  {
                      "_id": "field_001",
                      "name": "title"
                  },
                  {
                      "_id": "field_002",
                      "name": "description"
                  },
                  {
                      "_id": "field_003",
                      "name": "priority"
                  }
              ],
              "fields": {
                  "field_001": "Another Project",
                  "field_002": "Second project with different metadata for testing purposes.",
                  "field_003": "High"
              }
          }
      ]
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "success": true,
          "message": "Data stored",
          "data": [
              {
                  "title": "Sample Project Title",
                  "description": "This is a detailed description of the project with important information.",
                  "category": "Technology",
                  "attachments": [
                      {
                          "data": {
                              "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_7Z8iiQLsI0Ubh4UJ6JMq1xhpk8.pdf",
                              "filename": "sample_document.pdf",
                              "mimetype": "application/pdf"
                          }
                      }
                  ],
                  "boarditem_id": "boarditem_123",
                  "board_id": "board_456",
                  "organization_id": "org_789"
              },
              {
                  "title": "Another Project",
                  "description": "Second project with different metadata for testing purposes.",
                  "priority": "High",
                  "boarditem_id": "boarditem_124",
                  "board_id": "board_456",
                  "organization_id": "org_789"
              }
          ]
      }
  ```
* **Example:**

  ```
      curl --request POST \
      --url https://aiv2.dev.imbrace.lan/api/v1/embedding \
      --header 'X-Api-Key: your-api-key' \
      --header 'content-type: application/json' \
      --header 'x-organization-id: org_imbrace' \
      --data '[
          {
              "_id": "boarditem_123",
              "board_id": "board_456",
              "organization_id": "org_789",
              "fields_data": [
                  {
                      "_id": "field_001",
                      "name": "title"
                  },
                  {
                      "_id": "field_002",
                      "name": "description"
                  }
              ],
              "fields": {
                  "field_001": "Sample Project Title",
                  "field_002": "This is a detailed description of the project with important information."
              }
          }
      ]'
  ```

### [11. Delete Embedding by Board ID](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#11-delete-embedding-by-board-id)

Delete embeddings associated with a specific board ID.

* **Endpoint for Demo:** `DELETE https://aiv2.demo.imbrace.lan/api/v1/embedding/board/{board_id}`
* **Endpoint for Dev:** `DELETE https://aiv2.dev.imbrace.lan/api/v1/embedding/board/{board_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Api-Key`: Bearer
    **Your Access Token****Your Access Token**
  * `x-organization-id`: `Your organization ID`
* **Path Parameters:**

  * `board_id`: The ID of the board to delete embeddings for
* **Body:**

  ```
      {
          "text": "What is my name",
          "instructions": "",
          "thread_id": "test-tool-1",
          "role": "user",
          "secret": "擁抱科技",
          "file_ids": ["db83acff-1edb-4317-9f4e-1d4fffc30240"],
          "assistant_id": "",
          "streaming": false
      }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "success": true,
          "message": "Deleted 0 records with board_id = 123",
          "deletedCount": 0
      }
  ```
* **Example:**

  ```
      curl --request DELETE \
      --url https://aiv2.dev.imbrace.lan/api/v1/embedding/board/123 \
      --header 'X-Api-Key: your-api-key' \
      --header 'content-type: application/json' \
      --header 'x-organization-id: org_imbrace' \
      --data '{
          "text": "What is my name",
          "instructions": "",
          "thread_id": "test-tool-1",
          "role": "user",
          "secret": "擁抱科技",
          "file_ids": ["db83acff-1edb-4317-9f4e-1d4fffc30240"],
          "assistant_id": "",
          "streaming": false
      }'
  ```

### [12. Delete Embedding by Board Item ID](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#12-delete-embedding-by-board-item-id)

Delete embeddings associated with a specific board item ID.

* **Endpoint for Demo:** `DELETE https://aiv2.demo.imbrace.lan/api/v1/embedding/{boarditem_id}`
* **Endpoint for Dev:** `DELETE https://aiv2.dev.imbrace.lan/api/v1/embedding/{boarditem_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Api-Key`: Bearer
    **Your Access Token****Your Access Token**
  * `x-organization-id`: `Your organization ID`
* **Path Parameters:**

  * `boarditem_id`: The ID of the board item to delete embeddings for
* **Body:**

  ```
      {
          "text": "What is my name",
          "instructions": "",
          "thread_id": "test-tool-1",
          "role": "user",
          "secret": "擁抱科技",
          "file_ids": ["db83acff-1edb-4317-9f4e-1d4fffc30240"],
          "assistant_id": "",
          "streaming": false
      }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "success": true,
          "message": "Deleted 0 records with boarditem_id = 123",
          "deletedCount": 0
      }
  ```
* **Example:**

  ```
      curl --request DELETE \
      --url https://aiv2.dev.imbrace.lan/api/v1/embedding/123 \
      --header 'X-Api-Key: your-api-key' \
      --header 'content-type: application/json' \
      --header 'x-organization-id: org_imbrace' \
      --data '{
          "text": "What is my name",
          "instructions": "",
          "thread_id": "test-tool-1",
          "role": "user",
          "secret": "擁抱科技",
          "file_ids": ["db83acff-1edb-4317-9f4e-1d4fffc30240"],
          "assistant_id": "",
          "streaming": false
      }'
  ```

### [13. Get ECharts by Thread ID](https://devportal.dev.imbrace.co/docs/api-document/app-apis/aIAgentApis#13-get-echarts-by-thread-id)

Delete embeddings associated with a specific board item ID.

* **Endpoint for Demo:** `GET http://aiv2.demo.imbrace.lan/api/v1/rag/echarts/{thread_id}`
* **Endpoint for Dev:** `GET https://aiv2.dev.imbrace.lan/api/v1/embedding/{thread_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Api-Key`: Bearer
    **Your Access Token****Your Access Token**
  * `x-organization-id`: `Your organization ID`
* **Path Parameters:**

  * `thread_id`: The ID of the thread_id
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {
      "echarts": [
          {
              "_id": "afd439e5-2655-489b-bbf1-0c113190ccfb",
              "thread_id": "66f2ff9c-7341-4ca4-81c7-e9d5469d3364",
              "echart_data": {
                  "title": {
                      "text": "Student Total Scores and Rankings"
                  },
                  "tooltip": {},
                  "legend": {
                      "data": [
                          "Total Score"
                      ]
                  },
                  "xAxis": {
                      "type": "category",
                      "data": [
                          "Ella Vu",
                          "Alice Nguyen",
                          "Brian Tran",
                          "David Pham",
                          "Cindy Le"
                      ]
                  },
                  "yAxis": {
                      "type": "value"
                  },
                  "series": [
                      {
                          "name": "Total Score",
                          "type": "bar",
                          "data": [
                              279,
                              273,
                              265,
                              259,
                              235
                          ]
                      }
                  ]
              },
              "organization_id": "org_639ac074-5fd4-4a16-95b7-69644b849697",
              "created_at": "2025-10-20T05:18:56.007000",
              "updated_at": "2025-10-20T05:18:56.007000"
          },
          {
              "_id": "4b9a4d27-36e4-4ab8-ab15-3334066f7c0f",
              "thread_id": "66f2ff9c-7341-4ca4-81c7-e9d5469d3364",
              "echart_data": {
                  "title": {
                      "text": "Student Ranking Based on Math Score"
                  },
                  "tooltip": {},
                  "legend": {
                      "data": [
                          "Math Score"
                      ]
                  },
                  "xAxis": {
                      "type": "category",
                      "data": [
                          "Alice Nguyen",
                          "Brian Tran",
                          "Cindy Le",
                          "David Pham",
                          "Ella Vu"
                      ]
                  },
                  "yAxis": {
                      "type": "value"
                  },
                  "series": [
                      {
                          "name": "Math Score",
                          "type": "bar",
                          "data": [
                              95,
                              89,
                              76,
                              88,
                              92
                          ]
                      }
                  ]
              },
              "organization_id": "org_639ac074-5fd4-4a16-95b7-69644b849697",
              "created_at": "2025-10-20T05:22:22.726000",
              "updated_at": "2025-10-20T05:22:22.726000"
          }
      ]
  }
  ```
* **Example:**

  ```
  curl --location 'https://aiv2.demo.imbrace.lan/api/v1/rag/echarts/66f2ff9c-7341-4ca4-81c7-e9d5469d3364' \--header 'x-access-token: api_957c33c5-2342-4354-9e2e-8c1d50593bb0'
  ```
