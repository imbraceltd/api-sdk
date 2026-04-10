# Board Apis

Board APIs focus on managing the data within the Data Board, including Create, Update, Delete operations for requests, orders, and other data records. These APIs also support exporting data in formats such as CSV for easier sharing and analysis.

---

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#overview)

## [Use these APIs to build and maintain data structures (Boards, Fields, Items) and to automate imports/exports.All responses are JSON unless otherwise stated.](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#use-these-apis-to-build-and-maintain-data-structures-boards-fields-items-and-to-automate-importsexportsall-responses-are-json-unless-otherwise-stated)

### [1. Get Boards](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#1-get-boards)

Retrieve a paginated list of boards with basic metadata.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/board?limit=0&skip=0&sort=-created_at`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/board?limit=0&skip=0&sort=-created_at`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/board?limit=0&skip=0&sort=-created_at`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 201 Created** - Indicates that the OTP has been successfully sent to the provided email.

  ```
      {
          "data": [
              {
                  "_id": "brd_9c6f7a5f-82c4-4e48-b164-dd8378a618b6",
                  "doc_name": "boards",
                  "business_unit_id": "bu_imbrace_testing",
                  "order": 82,
                  "organization_id": "org_imbrace",
                  "name": "Test Form",
                  "hidden": true,
                  "type": "General",
                  "journey": {
                      "id": "app_eabec669-4b35-49f5-8982-7db13dc0dde6",
                      "name": "Form Management - iMBRACE Corporation",
                      "type": "form_management",
                      "extra": {
                          "form_id": "6694aaa95ba1031a1250b8c2",
                          "form_name": "Test Form"
                      }
                  },
                  "fields": [
                      {
                          "name": "Name",
                          "type": "ShortText",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "is_identifier": true,
                          "_id": "6694aaa932801761f155b140",
                          "data": []
                      },
                      {
                          "name": "Submission Source",
                          "description": "The source of the form submission",
                          "type": "SingleSelection",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "is_identifier": false,
                          "data": [],
                          "_id": "6694aaa932801761f155b141"
                      },
                      {
                          "name": "Submission Time",
                          "description": "The time of the form submission",
                          "type": "Time",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "is_identifier": false,
                          "data": [],
                          "_id": "6694aaa932801761f155b142"
                      },
                      {
                          "name": "Title",
                          "type": "ShortText",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "is_identifier": false,
                          "_id": "6694aaa932801761f155b143",
                          "data": []
                      },
                      {
                          "name": "Company",
                          "type": "ShortText",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "_id": "6694aaa932801761f155b144",
                          "data": []
                      },
                      {
                          "name": "Phone",
                          "type": "Phone",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "_id": "6694aaa932801761f155b145",
                          "data": []
                      },
                      {
                          "name": "Email",
                          "type": "Email",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "_id": "6694aaa932801761f155b146",
                          "data": []
                      },
                      {
                          "name": "Location",
                          "type": "Country",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "_id": "6694aaa932801761f155b147",
                          "data": []
                      },
                      {
                          "name": "Address",
                          "type": "LongText",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "_id": "6694aaa932801761f155b148",
                          "data": []
                      },
                      {
                          "name": "Interested Product",
                          "type": "MultipleSelection",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "is_identifier": false,
                          "data": [
                              {
                                  "value": "Product A",
                                  "_id": "Product A"
                              },
                              {
                                  "value": "Product B",
                                  "_id": "Product B"
                              }
                          ],
                          "_id": "6694aaa932801761f155b149"
                      },
                      {
                          "name": "Categories",
                          "description": "",
                          "type": "MultipleSelection",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "is_identifier": false,
                          "data": [
                              {
                                  "value": "Brand Owners",
                                  "_id": "Brand Owners"
                              },
                              {
                                  "value": "Traders",
                                  "_id": "Traders"
                              },
                              {
                                  "value": "Partners",
                                  "_id": "Partners"
                              },
                              {
                                  "value": "Others",
                                  "_id": "Others"
                              }
                          ],
                          "_id": "6694aaa932801761f155b14a"
                      },
                      {
                          "name": "Remarks",
                          "type": "LongText",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "_id": "6694aaa932801761f155b14b",
                          "data": []
                      },
                      {
                          "name": "Owner",
                          "description": "The owner of the form",
                          "type": "Assignee",
                          "is_unique_identifier": false,
                          "is_default": false,
                          "hidden": false,
                          "is_identifier": false,
                          "data": [],
                          "_id": "6694aaa932801761f155b14c"
                      }
                  ],
                  "public_id": "brd_9c6f7a5f-82c4-4e48-b164-dd8378a618b6",
                  "created_at": "2024-07-15T04:50:49.485Z",
                  "managers": [],
                  "team_ids": [],
                  "id": "brd_9c6f7a5f-82c4-4e48-b164-dd8378a618b6"
              }
          ],
          "count": 1
      }
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/board?limit=0&skip=0&sort=-created_at' \
  --header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df'
  ```

### [2. Get Boards by ID](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#2-get-boards-by-id)

Fetch details of a single board.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/board/{boad_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/board/{boad_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/board/{boad_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "doc_name": "boards",
          "business_unit_id": "bu_imbrace_testing",
          "order": 101,
          "organization_id": "org_imbrace",
          "name": "board name 13",
          "hidden": false,
          "description": "board description",
          "type": "General",
          "managers": [
              {
                  "team_id": "t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333",
                  "team_user_ids": [],
                  "_id": "66cda0cf42253eb6c5e967f4"
              },
              {
                  "team_id": "t_912c8e28-93ac-42f1-81d3-daea01795d03",
                  "team_user_ids": [],
                  "_id": "66cda0cf42253eb6c5e967f5"
              }
          ],
          "_id": "brd_d9a87a00-ad80-4faf-9714-b79d94256694",
          "fields": [
              {
                  "is_unique_identifier": false,
                  "is_default": false,
                  "hidden": false,
                  "_id": "66cda0cf42253eb6c5e967f6",
                  "data": [],
                  "name": "Name",
                  "type": "ShortText",
                  "is_identifier": true
              }
          ],
          "public_id": "brd_d9a87a00-ad80-4faf-9714-b79d94256694",
          "created_at": "2024-08-27T09:47:59.736Z",
          "team_ids": [
              "t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333",
              "t_912c8e28-93ac-42f1-81d3-daea01795d03"
          ],
          "id": "brd_d9a87a00-ad80-4faf-9714-b79d94256694"
      }
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "Not found"}
  ```

  * **Status code: 403 Forbidden**

  ```
  {    "message": "Forbidden, insufficient permission"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/board/brd_9c6f7a5f-82c4-4e48-b164-dd8378a618b6' \--header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df'
  ```

### [3. Create board](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#3-create-board)

Create a new board with optional description and initial settings.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/board`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/board`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/board`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-tokem`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {
  "name": "board name 13",
  "description": "board description",
  "workflow_id": "real workflow id",
  "hidden": false,
  "team_ids": ["t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333", "t_912c8e28-93ac-42f1-81d3-daea01795d031"]
  }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "doc_name": "boards",
          "business_unit_id": "bu_imbrace_testing",
          "order": 101,
          "organization_id": "org_imbrace",
          "name": "board name 13",
          "hidden": false,
          "description": "board description",
          "type": "General",
          "managers": [
              {
                  "team_id": "t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333",
                  "team_user_ids": [],
                  "_id": "66cda0cf42253eb6c5e967f4"
              },
              {
                  "team_id": "t_912c8e28-93ac-42f1-81d3-daea01795d03",
                  "team_user_ids": [],
                  "_id": "66cda0cf42253eb6c5e967f5"
              }
          ],
          "_id": "brd_d9a87a00-ad80-4faf-9714-b79d94256694",
          "fields": [
              {
                  "is_unique_identifier": false,
                  "is_default": false,
                  "hidden": false,
                  "_id": "66cda0cf42253eb6c5e967f6",
                  "data": [],
                  "name": "Name",
                  "type": "ShortText",
                  "is_identifier": true
              }
          ],
          "public_id": "brd_d9a87a00-ad80-4faf-9714-b79d94256694",
          "created_at": "2024-08-27T09:47:59.736Z",
          "team_ids": [
              "t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333",
              "t_912c8e28-93ac-42f1-81d3-daea01795d03"
          ],
          "id": "brd_d9a87a00-ad80-4faf-9714-b79d94256694"
      }
  ```

  * **Status code: 400 Bad Request**

  ```
  {"code": ,"message": "duplicate name"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/board' \--header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \--header 'Content-Type: application/json' \--data '{"name": "board name","description": "board description"}'
  ```

### [4. Update Boards](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#4-update-boards)

Update Boards for databoard

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/v1/backend/:board_id`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/v1/backend/:board_id`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/v1/backend/:board_id`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-tokem`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {
  "name": "board name 13",
  "description": "board description",
  "workflow_id": "real workflow id",
  "hidden": false,
  "team_ids": ["t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333", "t_912c8e28-93ac-42f1-81d3-daea01795d031"]
  }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "doc_name": "boards",
          "business_unit_id": "bu_imbrace_testing",
          "order": 101,
          "organization_id": "org_imbrace",
          "name": "board name 13",
          "hidden": false,
          "description": "board description",
          "type": "General",
          "managers": [
              {
                  "team_id": "t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333",
                  "team_user_ids": [],
                  "_id": "66cda0cf42253eb6c5e967f4"
              },
              {
                  "team_id": "t_912c8e28-93ac-42f1-81d3-daea01795d03",
                  "team_user_ids": [],
                  "_id": "66cda0cf42253eb6c5e967f5"
              }
          ],
          "_id": "brd_d9a87a00-ad80-4faf-9714-b79d94256694",
          "fields": [
              {
                  "is_unique_identifier": false,
                  "is_default": false,
                  "hidden": false,
                  "_id": "66cda0cf42253eb6c5e967f6",
                  "data": [],
                  "name": "Name",
                  "type": "ShortText",
                  "is_identifier": true
              }
          ],
          "public_id": "brd_d9a87a00-ad80-4faf-9714-b79d94256694",
          "created_at": "2024-08-27T09:47:59.736Z",
          "team_ids": [
              "t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333",
              "t_912c8e28-93ac-42f1-81d3-daea01795d03"
          ],
          "id": "brd_d9a87a00-ad80-4faf-9714-b79d94256694"
      }
  ```

  * **Status code: 403 Forbidden**

  ```
  {"code": ,"message": "Forbidden, insufficient permission"}
  ```

  * **Status code: 404 Not Found**

  ```
  {"code": ,"message": "Not Found"}
  ```
* **Example:**

  ```
  curl --location --request PUT 'https://app-gateway.imbrace.co/v1/backend/board/brd_2ac80aa2-582f-48d0-a8de-6217734147ad' \
  --header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \
  --data '{
  "name": "board name123123",
  "description": "board description",
  "workflow_id": "real workflow id",
  "hidden": false,
  "team_ids": ["t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333", "t_912c8e28-93ac-42f1-81d3-daea01795d03", "t_32c57386-a5fe-40e2-b9c5-b236adbfe1eb"]
  }'
  ```

### [5. Delete board](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#5-delete-board)

Permanently delete a board and optionally its items.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/v1/backend/board/{board_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
      {     "message": "is deleted"    }
  ```

  * **Status code: 403 Forbidden**

  ```
      {     "message": "Forbidden"    }
  ```

  * **Status code: 404 Not Found**

  ```
      {     "message": "Not Found"    }
  ```
* **Example:**

  ```
      curl --location --request DELETE 'https://app-gateway.imbrace.co/v1/backend/board/brd_2ac80aa2-582f-48d0-a8de-6217734147ad1' \
      --header 'x-access-token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \
      --data ''
  ```

### [6. Create Fields](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#6-create-fields)

Add fields (columns) to a board.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_fields`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_fields`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_fields`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {
  "name": "name",
  "description": "description",
  "is_identifier": false,
  "type": "ShortText",
  "hidden": false,
  "data": [
      {
      "value": "string"
      }
  ]
  }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          {
          "_id": "brd_9b27fc5b-266a-4ea1-838a-a1de4219a014",
          "doc_name": "boards",
          "business_unit_id": "bu_imbrace_testing",
          "order": 282,
          "organization_id": "org_imbrace",
          "name": "testboard_001",
          "hidden": false,
          "description": "test",
          "type": "General",
          "managers": [],
          "fields": [
              {
                  "is_unique_identifier": false,
                  "is_default": false,
                  "hidden": false,
                  "hidden_on_record": false,
                  "_id": "68a3ea33aa94c2a210236f29",
                  "data": [],
                  "name": "Name",
                  "type": "ShortText",
                  "is_identifier": true
              },
              {
                  "name": "name",
                  "description": "description",
                  "type": "ShortText",
                  "is_unique_identifier": false,
                  "is_default": false,
                  "hidden": false,
                  "hidden_on_record": false,
                  "is_identifier": false,
                  "data": [
                      {
                          "value": "string",
                          "_id": "string"
                      }
                  ],
                  "_id": "68ba8a626e4158be4360fa8f"
              }
          ],
          "public_id": "brd_9b27fc5b-266a-4ea1-838a-a1de4219a014",
          "created_at": "2025-08-19T03:06:27.369Z",
          "updated_at": "2025-09-05T06:59:46.637Z",
          "team_ids": [],
          "id": "brd_9b27fc5b-266a-4ea1-838a-a1de4219a014"
      }
      }
  ```

  * **Status code: 403 Forbidden**

  ```
      {     "message": "Forbidden"    }
  ```

  * **Status code: 404 Not Found**

  ```
      {     "message": "Not Found"    }
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.imbrace.co/v1/backend/board/brd_72c61774-32ab-4d6f-b831-a9862978f051/board_fields' \
      --header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \
      --data '{
      "name": "Name",
      "description": "Name",
      "is_identifier": true,
      "type": "ShortText",
      "hidden": false
      }'
  ```

### [7. Update Fields](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#7-update-fields)

Update field properties

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_fields/{filed_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_fields/{filed_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_fields/{filed_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {    "name": "Name",    "type": "ShortText",}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "_id": "brd_72c61774-32ab-4d6f-b831-a9862978f051",
          "doc_name": "boards",
          "business_unit_id": "bu_imbrace_testing",
          "organization_id": "org_imbrace",
          "name": "dynamic",
          "description": "dynamic",
          "type": "General",
          "fields": [
              {
                  "name": "Name",
                  "description": "Name",
                  "type": "ShortText",
                  "is_unique_identifier": false,
                  "is_default": false,
                  "hidden": false,
                  "is_identifier": true,
                  "data": [
                      {
                          "value": "string",
                          "_id": "string"
                      }
                  ],
                  "_id": "64cb2b0ebdaa6acd179ed716"
              }
          ],
          "public_id": "brd_72c61774-32ab-4d6f-b831-a9862978f051",
          "created_at": "2023-08-03T04:16:58.625Z",
          "updated_at": "2023-08-03T04:20:30.530Z",
          "id": "brd_72c61774-32ab-4d6f-b831-a9862978f051"
      }
  ```

  * **Status code: 403 Forbidden**

  ```
      {     "message": "Forbidden"    }
  ```

  * **Status code: 404 Not Found**

  ```
      {     "message": "Not Found"    }
  ```
* **Example:**

  ```
      curl --location --request PUT 'https://app-gateway.imbrace.co/v1/backend/board/brd_a6c40ca4-b253-42a8-bc7c-fcae6c852ae3/board_fields/65d874253d024e32dd651c63' \
      --header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \
      --header 'Content-Type: application/json' \
      --data '{
      "name": "sss",
      "type": "Email"
      }'
  ```

### [8. Get Board Items](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#8-get-board-items)

List items (rows) in a board with filters and pagination.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_items?limit=20&skip=0`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_items?limit=20&skip=0`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_items?limit=20&skip=0`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "data": [
              {
                  "_id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6",
                  "doc_name": "board_items",
                  "business_unit_id": "bu_imbrace_testing",
                  "organization_id": "org_imbrace",
                  "board_id": "brd_9b27fc5b-266a-4ea1-838a-a1de4219a014",
                  "related_board_item_list": [],
                  "created_by": "Austina",
                  "created_type": "manual",
                  "fields": {
                      "68a3ea33aa94c2a210236f29": "test1",
                      "68ba8a626e4158be4360fa8f": null
                  },
                  "conversation_ids": [],
                  "public_id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6",
                  "created_at": "2025-08-19T03:11:06.227Z",
                  "contacts": null,
                  "id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6",
                  "68a3ea33aa94c2a210236f29": "test1",
                  "68ba8a626e4158be4360fa8f": null,
                  "board_item_id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6"
              }
          ],
          "count": 1,
          "total": 1,
          "has_more": false
      }
  ```

  * **Status code: 403 Forbidden**

  ```
      {     "message": "Forbidden"    }
  ```

  * **Status code: 404 Not Found**

  ```
      {     "message": "Not Found"    }
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.imbrace.co/v1/backend/board/brd_9b27fc5b-266a-4ea1-838a-a1de4219a014/board_items?limit=20&skip=0' \    --header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df'
  ```

### [9. Get Board Items By BoardItemId](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#9-get-board-items-by-boarditemid)

Fetch a single item with all its field values.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
      {
          "_id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6",
          "doc_name": "board_items",
          "business_unit_id": "bu_imbrace_testing",
          "organization_id": "org_imbrace",
          "board_id": "brd_9b27fc5b-266a-4ea1-838a-a1de4219a014",
          "related_board_item_list": [],
          "created_by": "Austina",
          "created_type": "manual",
          "fields": {
              "68a3ea33aa94c2a210236f29": "test1",
              "68ba8a626e4158be4360fa8f": null
          },
          "conversation_ids": [],
          "public_id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6",
          "created_at": "2025-08-19T03:11:06.227Z",
          "contacts": null,
          "id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6",
          "board_item_id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6",
          "board": {
              "_id": "brd_9b27fc5b-266a-4ea1-838a-a1de4219a014",
              "doc_name": "boards",
              "business_unit_id": "bu_imbrace_testing",
              "order": 282,
              "organization_id": "org_imbrace",
              "name": "testboard_001",
              "hidden": false,
              "description": "test",
              "type": "General",
              "managers": [],
              "fields": [
                  {
                      "is_unique_identifier": false,
                      "is_default": false,
                      "hidden": false,
                      "hidden_on_record": false,
                      "_id": "68a3ea33aa94c2a210236f29",
                      "data": [],
                      "name": "Name",
                      "type": "ShortText",
                      "is_identifier": true
                  },
                  {
                      "name": "name",
                      "description": "description",
                      "type": "ShortText",
                      "is_unique_identifier": false,
                      "is_default": false,
                      "hidden": false,
                      "hidden_on_record": false,
                      "is_identifier": false,
                      "data": [
                          {
                              "value": "string",
                              "_id": "string"
                          }
                      ],
                      "_id": "68ba8a626e4158be4360fa8f"
                  }
              ],
              "public_id": "brd_9b27fc5b-266a-4ea1-838a-a1de4219a014",
              "created_at": "2025-08-19T03:06:27.369Z",
              "updated_at": "2025-09-05T06:59:46.637Z",
              "team_ids": [],
              "id": "brd_9b27fc5b-266a-4ea1-838a-a1de4219a014"
          }
      }
  ```

  * **Status code: 403 Forbidden**

  ```
      {     "message": "Forbidden"    }
  ```

  * **Status code: 404 Not Found**

  ```
      {     "message": "Not Found"    }
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/board/brd_9b27fc5b-266a-4ea1-838a-a1de4219a014/board_items/bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6' \
      --header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df'
  ```

### [10. Create Board Items](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#10-create-board-items)

Insert one or many items in bulk.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_items`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_items`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_items`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {
      "fields":[
          {
              "board_field_id": "64ba48e42261fdc660addf19",
              "value": "chih test"
          }
      ],
      "related_board_item_id": "bi_4f21a762-2f63-4fb9-ac98-332a45185900"
  }
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {
      "doc_name": "board_items",
      "business_unit_id": "bu_imbrace_testing",
      "organization_id": "org_imbrace",
      "board_id": "brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c",
      "related_board_item_list": [
          "bi_4f21a762-2f63-4fb9-ac98-332a45185900"
      ],
      "created_type": "manual",
      "fields": {
          "64ba48e32261fdc660addefb": "chih test",
          "64ba48e32261fdc660addf0c": null,
          "66b5bc497816021da57a7aed": null,
          "66ac5a2a2aa00cbc6cccb4b6": null,
          "64ba48e32261fdc660addf0a": "Unidentified Lead",
          "659e013776ea7aae7e4162f4": null,
          "667a2d7a0c39f3d2f5e632aa": null,
          "65815aef9f33bffa5811c6fa": null,
          "6583b06c0d3c02654cb0072e": null,
          "65606b383ceb702260c4b579": null,
          "64c76de21b78fefe7185f55e": null,
          "657c23d6a48890dc05a9826e": null,
          "64ba48e32261fdc660addefd": null,
          "64ba48e32261fdc660addf02": null,
          "64ba48e32261fdc660addefc": null,
          "64c76d471b78fefe71856597": null,
          "64c76a8e1b78fefe7184224f": null,
          "64c9d980bdaa6acd17982f35": null,
          "64c76cd81b78fefe7184d983": null,
          "64ba48e32261fdc660addf01": null,
          "64ba48e32261fdc660addf0b": null,
          "64ba48e32261fdc660addf04": null,
          "64ba48e32261fdc660addeff": null,
          "64ba48e32261fdc660addefe": null,
          "64ba48e32261fdc660addf00": null,
          "64ba48e32261fdc660addf03": null,
          "64ba48e32261fdc660addf05": null,
          "64ba48e32261fdc660addf06": null,
          "64ba48e32261fdc660addf07": null,
          "64ba48e32261fdc660addf08": "2024-09-18T07:02:04.962Z",
          "64ba48e32261fdc660addf09": null,
          "6674073f0000000000ac757b": null,
          "64e32f695fe5acacec5f9586": null,
          "66d92ac5ef8cbe8a5fc20831": null
      },
      "conversation_ids": [],
      "_id": "bi_1c7eba48-2d40-4845-af9f-7d1492fcb87e",
      "public_id": "bi_1c7eba48-2d40-4845-af9f-7d1492fcb87e",
      "created_at": "2024-09-18T07:02:04.963Z",
      "id": "bi_1c7eba48-2d40-4845-af9f-7d1492fcb87e",
      "contact_id": "con_d890776f-49d0-44ab-ace2-8e66d2ba16ef"
  }
  ```

  * **Status code: 403 Forbidden**

  ```
      {     "message": "Forbidden"    }
  ```

  * **Status code: 404 Not Found**

  ```
      {     "message": "Not Found"    }
  ```

  * **Status code: 400 Bad Request**

  ```
      {     "message": "type required"    }
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/board/brd_c3a66c61-cbe7-40fb-bbc2-17622b30329c/board_items' \
  --header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \
  --header 'Content-Type: application/json' \
  --data '{
      "fields":[
          {
              "board_field_id": "64ba48e42261fdc660addf19",
              "value": "chih test"
          }
      ],
      "related_board_item_id": "bi_4f21a762-2f63-4fb9-ac98-332a45185900"
  }'
  ```

### [11. Update Board Item](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#11-update-board-item)

Update field values of a specific item.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {    "data": [        {            "key": "68a3ea33aa94c2a210236f29",            "value": "test1"        },        {            "key": "68ba8a626e4158be4360fa8f",            "value": "B"        }    ]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "_id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6",    "doc_name": "board_items",    "business_unit_id": "bu_imbrace_testing",    "organization_id": "org_imbrace",    "board_id": "brd_9b27fc5b-266a-4ea1-838a-a1de4219a014",    "related_board_item_list": [],    "created_by": "Austina",    "created_type": "manual",    "fields": {        "68a3ea33aa94c2a210236f29": "test1",        "68ba8a626e4158be4360fa8f": "B"    },    "conversation_ids": [],    "public_id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6",    "created_at": "2025-08-19T03:11:06.227Z",    "updated_at": "2025-09-05T08:19:10.748Z",    "contacts": null,    "id": "bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6"}
  ```

  * **Status code: 403 Forbidden**

  ```
      {     "message": "Forbidden"    }
  ```

  * **Status code: 404 Not Found**

  ```
      {     "message": "Not Found"    }
  ```

  * **Status code: 400 Bad Request**

  ```
      {     "message": "Invalid field"    }
  ```
* **Example:**

  ```
  curl --location --request PUT 'https://app-gateway.imbrace.co/v1/backend/board/brd_9b27fc5b-266a-4ea1-838a-a1de4219a014/board_items/bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6' \--header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \--header 'Content-Type: application/json' \--data '{    "data": [        {            "key": "68a3ea33aa94c2a210236fd29",            "value": "test1"        },        {            "key": "68ba8a626e4158be4360fa8f",            "value": "B"        }    ]}'
  ```

### [12. Delete Board Item](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#12-delete-board-item)

Remove an item from a board.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
      {        "message": "board item bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6 is deleted"    }
  ```

  * **Status code: 404 Not Found**

  ```
      {     "message": "Not Found"    }
  ```
* **Example:**

  ```
  curl --location --request DELETE 'https://app-gateway.imbrace.co/v1/backend/board/brd_9b27fc5b-266a-4ea1-838a-a1de4219a014/board_items/bi_3d8ef240-79ad-4b21-9806-0a76d44d50e6' \--header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \--data ''
  ```

### [13. Multiple upload file](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#13-multiple-upload-file)

Attach one or many files to an item (or board).

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/board/upload`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/board/upload`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/board/upload`
* **Headers:**

  * `Content-Type`: `multipart/form-data; boundary=<calculated when request is sent>`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  form-date

```
  upload file
```

* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "name": "5.0mb",        "extension": "jpeg",        "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_doXyPY8bE9HO4sp3UhegFL04OW.jpeg",        "key": "board/org_imbrace/file_doXyPY8bE9HO4sp3UhegFL04OW.jpeg",        "error": null    },    {        "name": "5.3mb",        "extension": "jpeg",        "url": null,        "key": null,        "error": "reached file size limit 5 MB"    },    {        "name": "17.9mb",        "extension": "jpeg",        "url": null,        "key": null,        "error": "reached file size limit 5 MB"    },    {        "name": "17.9mb",        "extension": "pdf",        "url": null,        "key": null,        "error": "reached file size limit 5 MB"    },    {        "name": "48.9mb",        "extension": "jpeg",        "url": null,        "key": null,        "error": "reached file size limit 5 MB"    },    {        "name": "48.9mb",        "extension": "pdf",        "url": null,        "key": null,        "error": "reached file size limit 5 MB"    },    {        "name": "文件",        "extension": "docx",        "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_ocwouHSTzFwhHiY1Uqcz5BTseG.docx",        "key": "board/org_imbrace/file_ocwouHSTzFwhHiY1Uqcz5BTseG.docx",        "error": null    },    {        "name": "未命名文件",        "extension": "odt",        "url": null,        "key": null,        "error": "unsupported file type odt"    },    {        "name": "cat_test",        "extension": "jpeg",        "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_fEnM1YfrPT8oKOtfE45ni7Mu4d.jpeg",        "key": "board/org_imbrace/file_fEnM1YfrPT8oKOtfE45ni7Mu4d.jpeg",        "error": null    },    {        "name": "5.0mb",        "extension": "jpeg",        "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/board/org_imbrace/file_6w2G3RB1abLD4lXapozDqCZ5hN.jpeg",        "key": "board/org_imbrace/file_6w2G3RB1abLD4lXapozDqCZ5hN.jpeg",        "error": null    }]
  ```

  * **Status code: 400 Bad Request**

  ```
  {    "code": 1,    "message": "maximum 10 files are allowed"}
  ```
* **Example:**

```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/board/upload' \--header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df' \--form '=@"WPXycIboz/5.0mb.jpeg"' \--form '=@"WPXycIboz/5.3mb.jpeg"' \--form '=@"WPXycIboz/17.9mb.jpeg"' \--form '=@"WPXycIboz/17.9mb.pdf"' \--form '=@"WPXycIboz/48.9mb.jpeg"' \--form '=@"WPXycIboz/48.9mb.pdf"' \--form '=@"WPXycIboz/文件.docx"' \--form '=@"WPXycIboz/未命名文件.odt"' \--form '=@"WPXycIboz/cat_test.jpg"' \--form '=@"BwOsIlhwP/5.0mb.jpeg"'
```

### [14. Export Csv](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#14-export-csv)

Export board as a CSV file.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/board/{board_id}/export_csv?tz=Asia/Taipei&sort=-updated_at`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/export_csv?tz=Asia/Taipei&sort=-updated_at`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/export_csv?tz=Asia/Taipei&sort=-updated_at`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**
* **Status code: 200 OK**

  csv

  ```
      Name,name,Record Created On,Lasted Updated On    "B","B",09/05/2025 16:30,09/05/2025 16:30    "A","A",09/05/2025 16:30,09/05/2025 16:30    "Test","Test",09/05/2025 16:30,09/05/2025 16:30
  ```
* **Status code: 404 Not Found**

  ```
      {        "message": "Not Found"    }
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.imbrace.co/v1/backend/board/brd_9b27fc5b-266a-4ea1-838a-a1de4219a014/export_csv?tz=Asia%2FTaipei&sort=-updated_at' \    --header 'X-access-token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df'
  ```

### [15. Get Related Boards](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#15-get-related-boards)

Get all boards related to a specific board item.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "show_id": false,        "_id": "brd_40942243-dff6-4900-89ba-85c322e6bdd7",        "doc_name": "boards",        "business_unit_id": "bu_imbrace_testing",        "organization_id": "org_imbrace",        "name": "Tasks",        "description": "Dedicated to internal collaboration and task management",        "type": "Tasks",        "fields": [            {                "name": "Name",                "description": "Title of the tasks",                "type": "ShortText",                "is_unique_identifier": false,                "is_default": true,                "default_field_name": "name",                "hidden": false,                "hidden_on_record": false,                "is_identifier": true,                "data": [],                "_id": "64ba48e42261fdc660addf21"            }        ],        "public_id": "brd_40942243-dff6-4900-89ba-85c322e6bdd7",        "created_at": "2023-07-21T08:59:16.019Z",        "updated_at": "2025-01-15T07:42:01.313Z",        "order": 3,        "hidden": false,        "managers": [],        "team_ids": [],        "id": "brd_40942243-dff6-4900-89ba-85c322e6bdd7"    }]
  ```

  * **Status code: 404 Not Found**

  ```
      {        "message": "Not Found"    }
  ```

  * **Status code: 403 Forbidden**

  ```
      {        "message": "Forbidden"    }
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/board/brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c/board_items/bi_4f21a762-2f63-4fb9-ac98-332a45185900/related_boards' \    --header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

### [16. Get Related Board Items](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#16-get-related-board-items)

Get items from a specific related board for a board item.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards/{related_board_id}/board_items?limit=10&skip=0`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards/{related_board_id}/board_items?limit=10&skip=0`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards/{related_board_id}/board_items?limit=10&skip=0`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * `limit`: Number of items to return (default: 10)
  * `skip`: Number of items to skip for pagination (default: 0)
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "_id": "bi_c8b19633-dc2f-4282-9b96-8653757f3f1d",            "doc_name": "board_items",            "business_unit_id": "bu_imbrace_testing",            "organization_id": "org_imbrace",            "board_id": "brd_c3a66c61-cbe7-40fb-bbc2-17622b30329c",            "related_board_item_id": "bi_9c440e9f-37e8-430d-821e-865248e3a96d",            "created_type": "manual",            "fields": {                "64ba48e42261fdc660addf19": "Link OP",                "652e7275a35aa2aacdd5e9cd": "https://webapp.dev.imbrace.co/crm/brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c/bi_9c440e9f-37e8-430d-821e-865248e3a96d"            },            "conversation_ids": [],            "public_id": "bi_c8b19633-dc2f-4282-9b96-8653757f3f1d",            "created_at": "2024-08-07T03:36:37.086Z",            "related_board_item_list": [                "bi_9c440e9f-37e8-430d-821e-865248e3a96d",                "bi_e9e9301e-cf33-46a5-9db7-c656469d4724",                "bi_8be17453-9766-40c4-bf6d-e71ff196cd53",                "bi_4f21a762-2f63-4fb9-ac98-332a45185900"            ],            "updated_at": "2025-02-07T04:33:45.588Z",            "created_by": "",            "id": "bi_c8b19633-dc2f-4282-9b96-8653757f3f1d"        }    ],    "count": 4,    "total": 4,    "has_more": false}
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/board/brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c/board_items/bi_4f21a762-2f63-4fb9-ac98-332a45185900/related_boards/brd_c3a66c61-cbe7-40fb-bbc2-17622b30329c/board_items?limit=10&skip=0' \    --header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

### [17. Link Board Items](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#17-link-board-items)

Link multiple board items to a specific board item.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards/{related_board_id}/link`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards/{related_board_id}/link`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards/{related_board_id}/link`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {    "ids": ["bi_c8b19633-dc2f-4282-9b96-8653757f3f1d", "bi_33925b72-9a06-4f60-98dc-9cb6a0a19994"]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "_id": "bi_9ef0035f-8dae-4f04-a58d-0ad278faaab0",            "doc_name": "board_items",            "business_unit_id": "bu_imbrace_testing",            "organization_id": "org_imbrace",            "board_id": "brd_c3a66c61-cbe7-40fb-bbc2-17622b30329c",            "related_board_item_list": [                "bi_4f21a762-2f63-4fb9-ac98-332a45185900"            ],            "created_type": "manual",            "fields": {                "64ba48e42261fdc660addf19": "chih test"            },            "conversation_ids": [],            "public_id": "bi_9ef0035f-8dae-4f04-a58d-0ad278faaab0",            "created_at": "2024-09-18T07:36:17.287Z",            "id": "bi_9ef0035f-8dae-4f04-a58d-0ad278faaab0"        }    ],    "count": 1,    "total": 1,    "has_more": false}
  ```

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "must have required property 'ids'"}
  ```

  ```
  {    "code": 40000,    "message": "must NOT have fewer than 1 items"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "invalid board item id"}
  ```

  * **Status code: 403 Forbidden**

  ```
  {    "message": "related board forbidden, insufficient permission"}
  ```
* **Example:**

  ```
      curl --location --request PUT 'https://app-gateway.dev.imbrace.co/v1/backend/board/brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c/board_items/bi_4f21a762-2f63-4fb9-ac98-332a45185900/related_boards/brd_c3a66c61-cbe7-40fb-bbc2-17622b30329c/link' \    --header 'X-Access-Token: acc_test_admin_token' \    --header 'Content-Type: application/json' \    --data '{        "ids": ["bi_c8b19633-dc2f-4282-9b96-8653757f3f1d", "bi_33925b72-9a06-4f60-98dc-9cb6a0a19994"]    }'
  ```

### [18. Unlink Board Items](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#18-unlink-board-items)

Unlink multiple board items from a specific board item.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards/{related_board_id}/unlink`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards/{related_board_id}/unlink`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/v1/backend/board/{board_id}/board_items/{board_item_id}/related_boards/{related_board_id}/unlink`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {    "ids": ["bi_c8b19633-dc2f-4282-9b96-8653757f3f1d", "bi_33925b72-9a06-4f60-98dc-9cb6a0a19994"]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "_id": "bi_ba0b9229-18c1-4679-b1c9-76085b99c7b6",            "doc_name": "board_items",            "business_unit_id": "bu_imbrace_testing",            "organization_id": "org_imbrace",            "board_id": "brd_c3a66c61-cbe7-40fb-bbc2-17622b30329c",            "created_type": "manual",            "fields": {                "64ba48e42261fdc660addf19": "Opportunities 50"            },            "related_board_item_list": [],            "conversation_ids": [],            "public_id": "bi_ba0b9229-18c1-4679-b1c9-76085b99c7b6",            "created_at": "2024-08-15T09:46:27.702Z",            "id": "bi_ba0b9229-18c1-4679-b1c9-76085b99c7b6"        }    ],    "count": 50,    "total": 10,    "has_more": true}
  ```

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "must have required property 'ids'"}
  ```

  ```
  {    "code": 40000,    "message": "must NOT have fewer than 1 items"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "invalid board item id"}
  ```

  * **Status code: 403 Forbidden**

  ```
  {    "message": "related board forbidden, insufficient permission"}
  ```
* **Example:**

  ```
      curl --location --request PUT 'https://app-gateway.dev.imbrace.co/v1/backend/board/brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c/board_items/bi_4f21a762-2f63-4fb9-ac98-332a45185900/related_boards/brd_c3a66c61-cbe7-40fb-bbc2-17622b30329c/unlink' \    --header 'X-Access-Token: acc_test_admin_token' \    --header 'Content-Type: application/json' \    --data '{        "ids": ["bi_c8b19633-dc2f-4282-9b96-8653757f3f1d", "bi_33925b72-9a06-4f60-98dc-9cb6a0a19994"]    }'
  ```

### [19. Search Board Items](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#19-search-board-items)

Search for board items using Meilisearch.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/meilisearch/{board_id}/search`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/meilisearch/{board_id}/search`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/meilisearch/{board_id}/search`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {    "limit": 20,    "q": "No Name",    "matchingStrategy": "all",    "offset": 0}
  ```
* **Parameters:**

  * `limit`: Maximum number of results to return (default: 20)
  * `q`: Search query string
  * `matchingStrategy`: Search matching strategy (e.g., "all")
  * `offset`: Number of results to skip for pagination (default: 0)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "success": true,    "message": {        "hits": [            {                "_id": "bi_f86e1a34-65d7-4154-a9b6-14154c1c3e9f",                "doc_name": "board_items",                "business_unit_id": "bu_be188361-fbec-4505-9a05-d9d34a5d5961",                "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",                "board_id": "brd_35e929a0-ec7d-44df-acd7-1a5c2d5784b7",                "related_board_item_list": [],                "created_by": "",                "created_type": "manual",                "fields": {                    "68536a602119123ca3ee6786": "No Name",                    "68536a602119123ca3ee6787": "sample1@gmail.com"                },                "conversation_ids": [],                "fields_timestamp": {}            }        ],        "query": "No Name",        "processingTimeMs": 9,        "limit": 20,        "offset": 0,        "estimatedTotalHits": 3    }}
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/meilisearch/brd_35e929a0-ec7d-44df-acd7-1a5c2d5784b7/search' \    --header 'X-Access-Token: acc_20bea5ac-9e26-4864-b60f-ae7834c2c63e' \    --header 'Content-Type: application/json' \    --data '{        "limit": 20,        "q": "No Name",        "matchingStrategy": "all",        "offset": 0    }'
  ```

### [20. Fetch Filtered Board Items](https://devportal.dev.imbrace.co/docs/api-document/app-apis/boardApis#20-fetch-filtered-board-items)

Fetch board items with specific field filters using Meilisearch.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/meilisearch/{board_id}/fetch`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/meilisearch/{board_id}/fetch`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/meilisearch/{board_id}/fetch`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**

  ```
  {    "limit": 1000,    "filter": "fields.64ba48e32261fdc660addf0a = 'Unidentified Lead' AND fields.64ba48e32261fdc660addf02 = Male"}
  ```
* **Parameters:**

  * `limit`: Maximum number of results to return
  * `filter`: Filter expression for field values. Format: `fields.{field_id} = '{value}'`
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "success": true,    "message": {        "results": [],        "offset": 0,        "limit": 1000,        "total": 0    }}
  ```
* **Example:**

  ```
      curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/meilisearch/brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c/fetch' \    --header 'Content-Type: application/json' \    --header 'X-Access-Token: acc_20bea5ac-9e26-4864-b60f-ae7834c2c63e' \    --data '{        "limit": 1000,        "filter": "fields.64ba48e32261fdc660addf0a = '\''Unidentified Lead'\'' AND fields.64ba48e32261fdc660addf02 = Male"    }'
  ```
