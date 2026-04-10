[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Journey API](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference)

# Data Board API

APIs for managing Data Boards.

## [1. Data Boards](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#1-data-boards)

This section describes the APIs related to managing Data Boards, including creating, updating, deleting, and retrieving board information as well as their fields.

### [1.1. Create Board](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#11-create-board)

Create a new board with properties such as name, description, workflow, and associated teams.

* **Endpoint:** `POST https://app-gateway.dev.imbrace.co/journeys/v1/board`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "name": "board name",  "description": "board description",  "workflow_id": "real workflow id",  "team_ids": [    "t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333",    "t_912c8e28-93ac-42f1-81d3-daea01795d03"  ]}
  ```
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v1/board' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{  "name": "board name",  "description": "board description",  "workflow_id": "real workflow id",  "team_ids": ["t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333", "t_912c8e28-93ac-42f1-81d3-daea01795d03"]}'
  ```

### [1.2. Update Board](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#12-update-board)

Update the information of an existing board by its ID.

* **Endpoint:** `PUT https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "name": "board name 13",  "description": "board description",  "workflow_id": "real workflow id",  "hidden": false,  "team_ids": [    "t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333",    "t_912c8e28-93ac-42f1-81d3-daea01795d031"  ]}
  ```
* **Example:**
  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/journeys/v1/board/brd_d9a87a00-ad80-4faf-9714-b79d94256694' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{  "name": "board name 13",  "description": "board description",  "workflow_id": "real workflow id",  "hidden": false,  "team_ids": ["t_7e5b7bac-9e2b-4718-8ba4-f15f940f7333", "t_912c8e28-93ac-42f1-81d3-daea01795d031"]}'
  ```

### [1.3. Delete Board](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#13-delete-board)

Delete a specific board by its ID.

* **Endpoint:** `DELETE https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
* **Example:**
  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/journeys/v1/board/brd_2ac80aa2-582f-48d0-a8de-6217734147ad' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1'
  ```

### [1.4. Get Boards List](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#14-get-boards-list)

Retrieve a list of all boards. (Note: The provided example appears to be for getting a specific board, not a list. If it's a list, the URL should not include a specific ID).

* **Endpoint:** `GET https://app-gateway.dev.imbrace.co/journeys/v1/board` (Assumed for list)
* **Headers:**
  * `x-temp-token`:
    **Your token**
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v1/board' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1'
  ```

### [1.5. Get Board by ID](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#15-get-board-by-id)

Get detailed information for a specific board by its ID.

* **Endpoint:** `GET https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v1/board/brd_f603cc29-884e-4a5b-b370-446e011b89dc' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1'
  ```

### [1.6. Create Fields for Board](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#16-create-fields-for-board)

Add a new field to a specific board.

* **Endpoint:** `POST https://app-gateway.dev.imbrace.co/journeys/v1/board/:board_id/board_fields`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "name": "name",  "description": "description",  "is_identifier": false,  "type": "ShortText",  "hidden": false,  "data": [    {      "value": "string"    }  ]}
  ```
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v1/board/:board_id/board_fields' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{  "name": "name",  "description": "description",  "is_identifier": false,  "type": "ShortText",  "hidden": false,  "data": [    {      "value": "string"    }  ]}'
  ```

### [1.7. Update Board Fields](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#17-update-board-fields)

Update the information of a specific field within a board.

* **Endpoint:** `PUT https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}/board_fields/{field_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "name": "sss",  "type": "Email"}
  ```
* **Example:**
  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/journeys/v1/board/brd_a6c40ca4-b253-42a8-bc7c-fcae6c852ae3/board_fields/65d874253d024e32dd651c63' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{  "name": "sss",  "type": "Email"}'
  ```

### [1.8. Update Board Fields Order](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#18-update-board-fields-order)

Update the display order of fields within a board.

* **Endpoint:** `PUT https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}/board_fields/_order`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "fields": [    "65c3242b085dd896c86d297f",    "66cef19d78efe9e1c839885b",    "65c2efd2085dd896c86b8668",    "66399ef1677ac4c4a62e8da9",    "65c2efdc085dd896c86b8825",    "66399f1b677ac4c4a62e9279",    "66c69ccfbb95d32becb0c39a",    "66399f00677ac4c4a62e90a9",    "66cef19878efe9e1c839882e"  ]}
  ```
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v1/board/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6/board_fields/_order' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{    "fields": [        "65c3242b085dd896c86d297f",        "66cef19d78efe9e1c839885b",        "65c2efd2085dd896c86b8668",        "66399ef1677ac4c4a62e8da9",        "65c2efdc085dd896c86b8825",        "66399f1b677ac4c4a62e9279",        "66c69ccfbb95d32becb0c39a",        "66399f00677ac4c4a62e90a9",        "66cef19878efe9e1c839882e"    ]}'
  ```

---

## [2. Data Board Items](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#2-data-board-items)

This section guides on managing items within Data Boards.

### [2.1. Get Board Items List](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#21-get-board-items-list)

Retrieve a list of items within a specific board, with options for limit and skip (pagination).

* **Endpoint:** `GET https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}/board_items?limit={limit}&skip={skip}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v1/board/brd_f603cc29-884e-4a5b-b370-446e011b89dc/board_items?limit=20&skip=0' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1'
  ```

### [2.2. Get Board Item by ID](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#22-get-board-item-by-id)

Get detailed information for a specific item within a board.

* **Endpoint:** `GET https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}/board_items/{item_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v1/board/brd_f603cc29-884e-4a5b-b370-446e011b89dc/board_items/bi_b67239ef-60c8-45dd-ad04-1f05844f94a5' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1'
  ```

### [2.3. Delete Board Item by ID](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#23-delete-board-item-by-id)

Delete a specific item from a board.

* **Endpoint:** `DELETE https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}/board_items/{item_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
* **Example:**
  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/journeys/v1/board/brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c/board_items/bi_e162296d-d2d4-492f-8d80-c221c66359fd' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--data ''
  ```

### [2.4. Delete Multiple Board Items by IDs](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#24-delete-multiple-board-items-by-ids)

Delete multiple items from a board by providing a list of their IDs.

* **Endpoint:** `DELETE https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}/board_items`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "ids": ["id1", "id2"]}
  ```
* **Example:**
  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/journeys/v1/board/brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c/board_items' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{    "ids":[]}'
  ```

### [2.5. Update Multiple Board Items (Upload)](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/dataBoardItems#25-update-multiple-board-items-upload)

Update information for multiple items within a board. (Note: The provided example seems to duplicate the "Delete board item by id" request, please double-check the method and body. Assuming this is a `PUT` or `PATCH` request for bulk updates).

* **Endpoint:** `PUT https://app-gateway.dev.imbrace.co/journeys/v1/board/{board_id}/board_items/{board_item_id}` (Assumed)
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:** (Example for bulk update, data structure needs to be clearly defined)
  ```
  {  "data": [    {        "key": "66f666246647715bb8db1089",        "value": [            {                "message": "wwwqw",                "author_name": "System Automation"            }        ]    },  ]}
  ```
* **Example:**
  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/journeys//v1/board/brd_1c41d851-90f3-44b0-8b51-9628d30c29a6/board_items/bi_61705558-3c7b-419b-9125-98d3ebd7c930' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{     "data": [    {        "key": "66f666246647715bb8db1089",        "value": [            {                "message": "wwwqw",                "author_name": "System Automation"            }        ]    }]}'
  ```
