[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Journey API](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference)

# Workflow API

APIs related to Workflow management.

## [3. Workflow](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/workflow#3-workflow)

This section describes APIs related to Workflow management.

### [3.1. Get Workflow by ID](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/workflow#31-get-workflow-by-id)

Get detailed information for a specific workflow by its ID.

* **Endpoint:** `GET https://app-gateway.dev.imbrace.co/journeys/api/v1/workflows/{workflow_id}`
* **Headers:**
  * `X-Organization-Id`: `org_test`
  * `x-temp-token`:
    **Your token**
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/api/v1/workflows/5653' \--header 'x-organization-id: org_test' \--header 'x-temp-token: api_yourtemptoken' \
  ```

### [3.2. Verify Workflow List](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/workflow#32-verify-workflow-list)

Verify the status of a list of workflows by their IDs.

* **Endpoint:** `GET https://app-gateway.dev.imbrace.co/journeys/api/v1/workflows/verify`
* **Headers:**
  * `X-Organization-Id`: `org_test`
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "workflow_ids": [1, 4204, 12486]}
  ```
* **Example:**
  ```
  curl --location --request GET 'https://app-gateway.dev.imbrace.co/journeys/api/v1/workflows/verify' \--header 'x-organization-id: org_test' \--header 'x-temp-token: api_yourtemptoken' \--header 'Content-Type: application/json' \--data '{  "workflow_ids": [    1,    4204,    12486  ]}'
  ```

### [3.3. Update Workflow](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/workflow#33-update-workflow)

Update the configuration of a workflow, including its name, active status, and nodes.

* **Endpoint:** `PATCH https://app-gateway.dev.imbrace.co/journeys/v1/workflow/{workflow_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "id": "47",  "name": "My workflow",  "active": false,  "nodes": [    {      "parameters": {        "icsTitle": "Start"      },      "name": "Start",      "type": "n8n-nodes-base.start",      "typeVersion": 1,      "position": [320, 300]    }  ],  "connections": {},  "createdAt": "2022-07-22T10:57:40.815Z",  "updatedAt": "2022-07-22T10:57:50.939Z",  "settings": {},  "staticData": null,  "tags": []}
  ```
* **Example:**
  ```
  curl --location --request PATCH 'https://app-gateway.dev.imbrace.co/journeys/v1/workflow/12481' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{    "id": "47",    "name": "My workflow",    "active": false,    "nodes": [        {            "parameters": {                "icsTitle": "Start"            },            "name": "Start",            "type": "n8n-nodes-base.start",            "typeVersion": 1,            "position": [                320,                300            ]        }    ],    "connections": {},    "createdAt": "2022-07-22T10:57:40.815Z",    "updatedAt": "2022-07-22T10:57:50.939Z",    "settings": {},    "staticData": null,    "tags": []}'
  ```

### [3.4. Update Workflow Status](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/workflow#34-update-workflow-status)

Update the active/inactive status of a workflow. (Note: The provided example uses `GET` method but includes a request body, which typically suggests a `PATCH` or `PUT` request. Assuming `PATCH` method).

* **Endpoint:** `PATCH https://app-gateway.dev.imbrace.co/journeys/v1/workflows/{workflow_id}/status`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "active": false}
  ```
* **Example:**
  ```
  curl --location --request PATCH 'https://app-gateway.dev.imbrace.co/journeys/v1/workflows/12486/status' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{"active": false}'
  ```
