[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Journey API](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference)

# AI Assistant API

APIs related to AI Assistant management.

## [5. AI Assistant](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/aIAssistants#5-ai-assistant)

This section describes APIs related to AI Assistant management.

### [5.1. Get Assistants](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/aIAssistants#51-get-assistants)

Retrieve a list of AI assistants with optional parameters like limit and sorting.

* **Endpoint:** `GET https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistants?limit=2&sort=desc`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistants?limit=2&sort=desc' \--header 'x-temp-token: api_648b936b-cd1d-4553-bb30-7124d3910100' \--header 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0'
  ```

### [5.2. Create Assistant](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/aIAssistants#52-create-assistant)

Create a new AI assistant with specified attributes such as name, description, instructions, and metadata.

* **Endpoint:** `POST https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistants`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
  * `Authorization`: Bearer
    **Your token**
* **Body:**
  ```
  {    "name": "testing assistant 6",    "description": "description",    "instructions": "instructions",    "file_ids": [],    "metadata": {        "key_1": "value_1"    }}
  ```
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistants' \--header 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0' \--header 'x-temp-token: api_9fd1566e-c85b-4d31-90d1-e88ac5bfcfc1' \--header 'Content-Type: application/json' \--header 'Authorization: Bearer api_9fd1566e-c85b-4d31-90d1-e88ac5bfcfc1' \--data '{    "name": "testing assistant 6",    "description": "description",    "instructions": "instructions",    "file_ids": [],    "metadata": {        "key_1": "value_1"    }}'
  ```

### [5.3. Update Assistant](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/aIAssistants#53-update-assistant)

Update the details of an existing AI assistant by its ID.

* **Endpoint:** `PUT https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistants/{assistant_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
  * `Authorization`: Bearer
    **Your token**
* **Body:**
  ```
  {    "name": "testing assistant 15",    "description": "updated description",    "instructions": "updated instructions",    "file_ids": [],    "metadata": {        "key_2": "value_2"    }}
  ```
* **Example:**
  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistants/asst_1r0G0F5E92HN8Q3mw91Rrbxq' \--header 'x-temp-token: api_9fd1566e-c85b-4d31-90d1-e88ac5bfcfc1' \--header 'Content-Type: application/json' \--header 'Authorization: Bearer api_9fd1566e-c85b-4d31-90d1-e88ac5bfcfc1' \--header 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0' \--data '{    "name": "testing assistant 15",    "description": "updated description",    "instructions": "updated instructions",    "file_ids": [],    "metadata": {        "key_2": "value_2"    }}'
  ```

### [5.4. Delete Assistant](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/aIAssistants#54-delete-assistant)

Delete a specific AI assistant by its ID.

* **Endpoint:** `DELETE https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistants/{assistant_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
* **Example:**
  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistants/asst_1r0G0F5E92HN8Q3mw91Rrbxq' \--header 'x-temp-token: api_9fd1566e-c85b-4d31-90d1-e88ac5bfcfc1' \--header 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0' \--header 'Authorization: Bearer api_9fd1566e-c85b-4d31-90d1-e88ac5bfcfc1'
  ```

### [5.5. Create Assistant App](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/aIAssistants#55-create-assistant-app)

Create a new AI Assistant app with specified attributes.

* **Endpoint:** `POST https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistant_apps`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {    "name": "testing assistant 12",    "description": "description",    "instructions": "instructions",    "file_ids": [],    "metadata": {        "key_1": "value_1"    },    "workflow_name": "workflow test 12",    "credential_id": 0,    "credential_name": "placeholder",    "mode": "advanced"}
  ```
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistant_apps' \--header 'x-temp-token: api_9fd1566e-c85b-4d31-90d1-e88ac5bfcfc1' \--header 'Content-Type: application/json' \--header 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0' \--data '{    "name": "testing assistant 12",    "description": "description",    "instructions": "instructions",    "file_ids": [],    "metadata": {        "key_1": "value_1"    },    "workflow_name": "workflow test 12",    "credential_id": 0,    "credential_name": "placeholder",    "mode": "advanced"}'
  ```

### [5.6. Update Assistant App](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/aIAssistants#56-update-assistant-app)

Update the details of an existing Assistant app by its ID.

* **Endpoint:** `PUT https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistant_apps/{app_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {    "name": "testing assistant 15",    "description": "updated description",    "instructions": "updated instructions",    "file_ids": [],    "metadata": {},    "workflow_name": "workflow test 15",    "credential_id": 0,    "credential_name": "placeholder",    "mode": "advanced"}
  ```
* **Example:**
  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistant_apps/asst_X8JHZyPfapRrUEElNO6H7YD4' \--header 'x-temp-token: api_9fd1566e-c85b-4d31-90d1-e88ac5bfcfc1' \--header 'Content-Type: application/json' \--header 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0' \--data '{    "name": "testing assistant 15",    "description": "updated description",    "instructions": "updated instructions",    "file_ids": [],    "metadata": {},    "workflow_name": "workflow test 15",    "credential_id": 0,    "credential_name": "placeholder",    "mode": "advanced"}'
  ```

### [5.7. Delete Assistant App](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/aIAssistants#57-delete-assistant-app)

Delete a specific Assistant app by its ID.

* **Endpoint:** `DELETE https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistant_apps/{app_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Example:**
  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/journeys/v2/ai/assistant_apps/asst_X8JHZyPfapRrUEElNO6H7YD4' \--header 'x-temp-token: api_9fd1566e-c85b-4d31-90d1-e88ac5bfcfc1' \--header 'Content-Type: application/json' \--header 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0' \--data ''
  ```


[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Journey API](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference)

# Channels API

APIs related to Channel management.

## [4. Channel](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/channel#4-channel)

This section describes APIs related to Channel management.

### [4.1. Create Channel](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/channel#41-create-channel)

Create a new channel with properties such as name, icon, colors, and welcome message.

* **Endpoint:** `POST https://app-gateway.dev.imbrace.co/journeys/v1/channels`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "business_unit_id": "bu_imbrace_testing",  "name": "chih test",  "icon_url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/static/imbrace+icon_v1.png",  "primary_color": "#000000",  "secondary_color": "#FFFFFF",  "description": "",  "welcome_message": "insert welcome message here",  "fallback_url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/static/iMBRACE-Dev.html"}
  ```
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v1/channels' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{    "business_unit_id": "bu_imbrace_testing",    "name": "chih test",    "icon_url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/static/imbrace+icon_v1.png",    "primary_color": "#000000",    "secondary_color": "#FFFFFF",    "description": "",    "welcome_message": "insert welcome message here",    "fallback_url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/static/iMBRACE-Dev.html"}'
  ```

### [4.2. Update Channel](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/channel#42-update-channel)

Update the information of an existing channel by its ID.

* **Endpoint:** `PUT https://app-gateway.dev.imbrace.co/journeys/v1/channels/{channel_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "name": "modified_channel",  "icon_url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/user/org_imbrace/file_ebCRu9TQhfL6uc78omHOtMfqjM.png",  "primary_color": "#FFFFFF",  "secondary_color": "#000000",  "description": "modified",  "welcome_message": "insert updated message here1111",  "fallback_url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/static/iMBRACE-Dev.html"}
  ```
* **Example:**
  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/journeys/v1/channels/ch_528205a7-aa52-498c-9f8c-cfa80cfb8b10' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{    "name":"modified_channel",    "icon_url":"https://imbrace-uat.s3.ap-east-1.amazonaws.com/user/org_imbrace/file_ebCRu9TQhfL6uc78omHOtMfqjM.png",    "primary_color": "#FFFFFF",    "secondary_color": "#000000",    "description": "modified",    "welcome_message": "insert updated message here1111",    "fallback_url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/static/iMBRACE-Dev.html"}'
  ```

### [4.3. Delete Channel](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/channel#43-delete-channel)

Delete a specific channel by its ID.

* **Endpoint:** `DELETE https://app-gateway.dev.imbrace.co/journeys/v1/channels/{channel_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
* **Example:**
  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/journeys/v1/channels/ch_7666c70b-b8ca-4425-8052-adc712a8f3bd' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1'
  ```
