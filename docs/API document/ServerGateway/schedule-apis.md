[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Server Gateway](https://devportal.dev.imbrace.co/docs/api-document/server-gateways)

# Schedule APIs

Schedule APIs provide functionality to manage and retrieve scheduled tasks and automations within your organization. These APIs allow you to access scheduler configurations, recurring events, and automation workflows.

---

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/schedule#overview)

The Schedule APIs enable you to retrieve and manage scheduled tasks within your organization. Schedulers represent automated recurring events such as board automations, outbound messages, and workflow triggers with configurable frequencies and timing.

---

## [1. Get User Schedulers by Event Type](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/schedule#1-get-user-schedulers-by-event-type)

Retrieve all schedulers associated with a specific user, filtered by event type.

This API allows you to fetch all scheduled tasks for a user by providing the organization ID, user ID, and optional event type filters. It returns a paginated list of schedulers with their configurations, timing details, and job information.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers?event_type={event_type}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers?event_type={event_type}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers?event_type={event_type}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `user_id` (string, required): The unique identifier of the user
* **Query Parameters:**

  * `event_type` (string, optional): Filter by event type. Supports multiple values with operators:
    * `contains:` - Filter schedulers containing any of the specified event types (e.g., `contains:whatsapp_outbound,telegram_outbound`)
    * Single value - Filter by exact event type (e.g., `board_automation`)
  * `limit` (number, optional): Maximum number of results to return (default: 10)
  * `skip` (number, optional): Number of results to skip for pagination (default: 0)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "_id": "66e400607c85c0dc11b46f21",            "type": "recurring",            "name": "Board Automation - Jane - Facebook 16 days ",            "event_type": "board_automation",            "description": "",            "options": null,            "job": {                "type": "kafka",                "topic": "ROUTER.OUTGOING_CRM_EVENT",                "data": {                    "board_id": "brd_67c3766a-bedc-48dc-9a17-84551435cea6",                    "id": "662f175874c8ca8d00a1d30d"                },                "workflow_id": "1336"            },            "organization_id": "org_imbrace",            "internal_id": "662f175874c8ca8d00a1d30d",            "trigger_frequency_unit": "days",            "trigger_frequency_value": 1,            "trigger_time": "2024-04-29T01:00:00.000Z",            "start_date": "2024-04-29T01:30:00.000Z",            "start_time": "2024-04-29T01:30:00.000Z",            "start_datetime": "2024-04-29T01:30:00.000Z",            "is_paused": true,            "is_finished": false,            "channel_source": "",            "created_by": null,            "updated_by": null,            "created_at": "2024-09-13T09:05:36.286Z",            "updated_at": "2024-09-13T09:05:36.286Z"        }    ],    "count": 10,    "total": 23,    "has_more": true}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "organization_id is required"}
  ```

  ```
  {    "message": "user_id is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "User not found"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/organization/org_imbrace/users/u_imbrace_agent1/schedulers?event_type=contains%3Awhatsapp_outbound%2Ctelegram_outbound' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```

---

## [2. Get Scheduler File](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/schedule#2-get-scheduler-file)

Retrieve a specific file associated with a scheduler.

This API allows you to fetch a file attached to a scheduler by providing the organization ID, user ID, scheduler ID, and file ID. This is useful for retrieving attachments or documents associated with scheduled tasks.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}/files/{file_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}/files/{file_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}/files/{file_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `user_id` (string, required): The unique identifier of the user
  * `scheduler_id` (string, required): The unique identifier of the scheduler
  * `file_id` (string, required): The unique identifier of the file
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "file_url": "https://example.com/files/ab014eec-3b7f-4e67-8164-27ca344b6556",    "file_name": "document.pdf",    "file_type": "application/pdf",    "file_size": 1024000,    "created_at": "2024-10-16T08:30:00.000Z"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "scheduler_id is required"}
  ```

  ```
  {    "message": "file_id is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "Scheduler with id 670f990290e5ee13019669f4 not found in the organization org_imbrace"}
  ```

  ```
  {    "message": "File not found"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/organization/org_imbrace/users/u_imbrace_agent1/schedulers/670f990290e5ee13019669f4/files/ab014eec-3b7f-4e67-8164-27ca344b6556' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```

---

## [3. Get Scheduler by ID](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/schedule#3-get-scheduler-by-id)

Retrieve detailed information about a specific scheduler.

This API allows you to fetch complete scheduler details by providing the organization ID, user ID, and scheduler ID. It returns comprehensive information about the scheduler including its configuration, timing, job details, and status.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
  * `x-organization-id`: The unique identifier of the organization
  * `x-user-id`: The unique identifier of the user
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `user_id` (string, required): The unique identifier of the user
  * `scheduler_id` (string, required): The unique identifier of the scheduler
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "_id": "66e17484412c29cf84c39898",    "type": "recurring",    "name": "testing schedule",    "event_type": "whatsapp",    "description": "",    "options": null,    "job": {        "type": "kafka",        "topic": "ROUTER.OUTGOING_MESSAGE",        "workflow_id": "123"    },    "organization_id": "org_imbrace",    "trigger_frequency_unit": "minutes",    "trigger_frequency_value": 1,    "start_date": "2024-09-11T17:50:00.000Z",    "start_time": "2024-09-11T17:50:00.000Z",    "is_paused": false,    "is_finished": false,    "channel_source": "",    "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",    "updated_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",    "created_at": "2024-09-11T10:44:20.637Z",    "updated_at": "2024-09-11T10:44:20.637Z"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "scheduler_id is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "Scheduler not found"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/organization/org_imbrace/users/u_imbrace_agent1/schedulers/671603c03297cd8cf64f7ebb' \--header 'x-organization-id: org_imbrace' \--header 'x-user-id: u_imbrace_agent1' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```

---

## [4. Create Scheduler](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/schedule#4-create-scheduler)

Create a new scheduler for automated recurring tasks.

This API allows you to create a new scheduler by providing the scheduler configuration including timing, job details, and trigger settings. The scheduler will be created for the specified user within the organization.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
  * `x-organization-id`: The unique identifier of the organization
  * `x-user-id`: The unique identifier of the user
  * `Content-Type`: `application/json`
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `user_id` (string, required): The unique identifier of the user
* **Body:**

  ```
  {    "type": "recurring",    "name": "testing schedule",    "event_type": "whatsapp",    "channel_source": "",    "description": "",    "job": {        "type": "kafka",        "topic": "ROUTER.OUTGOING_MESSAGE",        "data": {},        "workflow_id": "123"    },    "trigger_frequency_unit": "years",    "trigger_frequency_value": 1,    "triger_month_and_day": "1969-12-31T16:32:00.000Z",    "trigger_time": "1969-12-31T16:00:00.000Z",    "start_datetime": "2024-09-11T14:35:00.000Z"}
  ```
* **Result:**

  * **Status code: 201 Created**

  ```
  {    "type": "recurring",    "name": "testing schedule",    "event_type": "whatsapp",    "description": "",    "options": null,    "job": {        "type": "kafka",        "topic": "ROUTER.OUTGOING_MESSAGE",        "workflow_id": "123"    },    "organization_id": "org_imbrace",    "trigger_frequency_unit": "years",    "trigger_frequency_value": 1,    "trigger_time": "1969-12-31T16:00:00.000Z",    "triger_month_and_day": "1969-12-31T16:32:00.000Z",    "start_date": "2024-09-11T14:35:00.000Z",    "start_time": "2024-09-11T14:35:00.000Z",    "is_paused": false,    "is_finished": false,    "channel_source": "",    "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",    "updated_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",    "_id": "66e1481283adbddb9ad6b8ff",    "created_at": "2024-09-11T07:34:42.158Z",    "updated_at": "2024-09-11T07:34:42.158Z"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "name is required"}
  ```

  ```
  {    "message": "event_type is required"}
  ```

  ```
  {    "message": "job is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "User not found"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/organization/org_imbrace/users/u_imbrace_agent1/schedulers' \--header 'x-organization-id: org_imbrace' \--header 'x-user-id: u_imbrace_agent1' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1' \--header 'Content-Type: application/json' \--data '{    "type": "recurring",    "name": "testing schedule",    "event_type": "whatsapp",    "channel_source": "",    "description": "",    "job": {        "type": "kafka",        "topic": "ROUTER.OUTGOING_MESSAGE",        "data": {},        "workflow_id": "123"    },    "trigger_frequency_unit": "years",    "trigger_frequency_value": 1,    "triger_month_and_day": "1969-12-31T16:32:00.000Z",    "trigger_time": "1969-12-31T16:00:00.000Z",    "start_datetime": "2024-09-11T14:35:00.000Z"}'
  ```

---

## [5. Create Scheduler with Files](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/schedule#5-create-scheduler-with-files)

Create a new scheduler with file attachments for automated recurring tasks.

This API allows you to create a new scheduler with file uploads by providing the scheduler configuration and files as multipart form data. This is useful for schedulers that need to send messages with attachments or documents.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/files`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/files`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/files`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `user_id` (string, required): The unique identifier of the user
* **Form Data:**

  * `payload` (string, required): JSON string containing scheduler configuration
  * `files` (file, optional): One or more files to upload
* **Payload Structure:**

  ```
  {    "type": "recurring",    "name": "testing schedule",    "event_type": "whatsapp",    "channel_source": "",    "description": "",    "trigger_frequency_unit": "minutes",    "trigger_frequency_value": 30,    "start_datetime": "2024-10-16T17:30:15.463Z",    "job": {        "type": "webhook",        "data": {            "topicToSend": "",            "segmentationGroup": "",            "groupToSend": "",            "outboundTags": "Marketing",            "outboundType": "sendToAllGroups",            "message": "sdsdsds",            "files": [                {                    "id": "imbrace-upload1 - 0",                    "file": {},                    "name": "20200526110944-Bank-Statement_1.jpg",                    "isValid": true,                    "status": "ok"                }            ],            "topic": "",            "sender": {                "name": "Austina Engelhardt",                "id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",                "email": "agent01@imbrace.co"            },            "appId": "app_a730320f-bc56-4857-b488-300f15bcdf8f"        },        "method": "POST",        "url": "https://org-imbrace.dev.imbrace.co/webhook/webhook_79893fd6-aa7c-483b-8ecb-7d0a20451c90"    }}
  ```
* **Result:**

  * **Status code: 201 Created**

  ```
  {    "type": "recurring",    "name": "testing schedule",    "event_type": "whatsapp",    "description": "",    "options": null,    "job": {        "type": "webhook",        "data": {            "topicToSend": "",            "segmentationGroup": "",            "groupToSend": "",            "outboundTags": "Marketing",            "outboundType": "sendToAllGroups",            "message": "sdsdsds",            "files": [                {                    "id": "imbrace-upload1 - 0",                    "name": "20200526110944-Bank-Statement_1.jpg",                    "isValid": true,                    "status": "ok"                }            ],            "topic": "",            "sender": {                "name": "Austina Engelhardt",                "id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",                "email": "agent01@imbrace.co"            },            "appId": "app_a730320f-bc56-4857-b488-300f15bcdf8f"        },        "method": "POST",        "url": "https://org-imbrace.dev.imbrace.co/webhook/webhook_79893fd6-aa7c-483b-8ecb-7d0a20451c90",        "files": [            {                "organization_id": "org_imbrace",                "name": "iphone13.jpg",                "file_path": "org_imbrace/1729074985051/iphone13.jpg",                "file_id": "514506ab-c018-4361-8f85-011b55c7cfbb",                "size": 15030,                "file_type": "image/jpeg",                "file_extension": "jpeg",                "file_url": "https://imbrace-marketplace-dev.s3.ap-east-1.amazonaws.com/org_imbrace/1729074985051/iphone13.jpg",                "is_public": true,                "short_path": "c8ddc9"            },            {                "organization_id": "org_imbrace",                "name": "logitech_mouse.jpg",                "file_path": "org_imbrace/1729074985052/logitech_mouse.jpg",                "file_id": "4194040e-0631-4327-81d3-1c6166492291",                "size": 61165,                "file_type": "image/jpeg",                "file_extension": "jpeg",                "file_url": "https://imbrace-marketplace-dev.s3.ap-east-1.amazonaws.com/org_imbrace/1729074985052/logitech_mouse.jpg",                "is_public": true,                "short_path": "d546cc"            }        ],        "scheduler_id": "670f972990e5ee13019669cc"    },    "organization_id": "org_imbrace",    "trigger_frequency_unit": "minutes",    "trigger_frequency_value": 30,    "start_date": "2024-10-16T17:30:15.463Z",    "start_time": "2024-10-16T17:30:15.463Z",    "start_datetime": "2024-10-16T17:30:15.463Z",    "is_paused": false,    "is_finished": false,    "channel_source": "",    "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",    "updated_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",    "_id": "670f972990e5ee13019669cc",    "created_at": "2024-10-16T10:36:25.116Z",    "updated_at": "2024-10-16T10:36:25.116Z"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "payload is required"}
  ```

  ```
  {    "message": "Invalid JSON in payload"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "User not found"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/organization/org_imbrace/users/u_imbrace_agent1/schedulers/files' \--form 'payload="{    \"type\": \"recurring\",    \"name\": \"testing schedule\",    \"event_type\": \"whatsapp\",    \"channel_source\": \"\",    \"description\": \"\",    \"trigger_frequency_unit\": \"minutes\",    \"trigger_frequency_value\": 30,    \"start_datetime\": \"2024-10-16T17:30:15.463Z\",    \"job\": {        \"type\": \"webhook\",        \"data\": {            \"topicToSend\": \"\",            \"segmentationGroup\": \"\",            \"groupToSend\": \"\",            \"outboundTags\": \"Marketing\",            \"outboundType\": \"sendToAllGroups\",            \"message\": \"sdsdsds\",            \"files\": [                {                    \"id\": \"imbrace-upload1 - 0\",                    \"file\": {},                    \"name\": \"20200526110944-Bank-Statement_1.jpg\",                    \"isValid\": true,                    \"status\": \"ok\"                }            ],            \"topic\": \"\",            \"sender\": {                \"name\": \"Austina Engelhardt\",                \"id\": \"u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a\",                \"email\": \"agent01@imbrace.co\"            },            \"appId\": \"app_a730320f-bc56-4857-b488-300f15bcdf8f\"        },        \"method\": \"POST\",        \"url\": \"https://org-imbrace.dev.imbrace.co/webhook/webhook_79893fd6-aa7c-483b-8ecb-7d0a20451c90\"    }}"' \--form 'files=@"/C:/Users/DEEL/OneDrive/Documents/Online Shop/logitech_mouse.jpg"'
  ```

---

## [6. Update Scheduler](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/schedule#6-update-scheduler)

Update an existing scheduler's configuration and settings.

This API allows you to update a scheduler by providing the scheduler ID and the fields you want to modify. You can update the scheduler name, timing, job configuration, and status.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
  * `x-organization-id`: The unique identifier of the organization
  * `x-user-id`: The unique identifier of the user
  * `Content-Type`: `application/json`
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `user_id` (string, required): The unique identifier of the user
  * `scheduler_id` (string, required): The unique identifier of the scheduler
* **Body:**

  ```
  {    "type": "recurring",    "name": "testing schedule updated",    "event_type": "facebook",    "channel_source": "",    "description": "",    "trigger_frequency_unit": "minutes",    "trigger_frequency_value": 1,    "start_datetime": "2024-09-19T15:36:00.000Z",    "job": {        "type": "kafka",        "topic": "ROUTER.OUTGOING_MESSAGE",        "data": {},        "workflow_id": "456"    },    "is_paused": false}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "schedule_id": "schedule_1",    "type": "recurring",    "callback_url": "https://google.com",    "organization_id": "org_imbrace",    "trigger_frequency_unit": "years",    "trigger_frequency_value": 1,    "trigger_time": "1969-12-31T16:00:00.000Z",    "triger_month_and_day": "1969-12-31T16:32:00.000Z",    "start_date": "2024-05-15T16:00:00.000Z",    "start_time": "1969-12-31T16:32:00.000Z",    "is_paused": false,    "_id": "664488701353f458e21ac2cd",    "createdAt": "2024-05-15T10:03:28.755Z",    "updatedAt": "2024-05-15T10:03:28.755Z"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "scheduler_id is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "Scheduler not found"}
  ```
* **Example:**

  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/3rd/organization/org_imbrace/users/u_imbrace_agent1/schedulers/66e6b637252463b567b080a2' \--header 'x-organization-id: org_imbrace' \--header 'x-user-id: u_imbrace_agent1' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1' \--header 'Content-Type: application/json' \--data '{    "type": "recurring",    "name": "testing schedule updated",    "event_type": "facebook",    "channel_source": "",    "description": "",    "trigger_frequency_unit": "minutes",    "trigger_frequency_value": 1,    "start_datetime": "2024-09-19T15:36:00.000Z",    "job": {        "type": "kafka",        "topic": "ROUTER.OUTGOING_MESSAGE",        "data": {},        "workflow_id": "456"    },    "is_paused": false}'
  ```

---

## [7. Update Scheduler with Files](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/schedule#7-update-scheduler-with-files)

Update an existing scheduler with file attachments using multipart form data.

This API allows you to update a scheduler and its associated files by providing the scheduler ID, updated configuration, and new files as multipart form data. This is useful for schedulers that need to send messages with updated attachments or documents.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/files/{scheduler_id}`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/files/{scheduler_id}`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/files/{scheduler_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
  * `x-organization-id`: The unique identifier of the organization
  * `x-user-id`: The unique identifier of the user
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `user_id` (string, required): The unique identifier of the user
  * `scheduler_id` (string, required): The unique identifier of the scheduler
* **Form Data:**

  * `payload` (string, required): JSON string containing updated scheduler configuration
  * `files` (file, optional): One or more files to upload/replace
* **Payload Structure:**

  ```
  {    "type": "non_recurring",    "name": "testing schedule",    "event_type": "whatsapp",    "channel_source": "",    "description": "",    "one_time_schedule_type": "exact",    "start_datetime": "2024-10-16T14:45:15.463Z",    "job": {        "type": "webhook",        "data": {            "topicToSend": "",            "segmentationGroup": "",            "groupToSend": "",            "outboundTags": "Marketing",            "outboundType": "sendToAllGroups",            "message": "sdsdsds",            "files": [                {                    "id": "imbrace-upload1 - 0",                    "file": {},                    "name": "20200526110944-Bank-Statement_1.jpg",                    "isValid": true,                    "status": "ok"                }            ],            "topic": "",            "sender": {                "name": "Austina Engelhardt",                "id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",                "email": "agent01@imbrace.co"            },            "appId": "app_a730320f-bc56-4857-b488-300f15bcdf8f"        },        "method": "POST",        "url": "https://org-imbrace.dev.imbrace.co/webhook/webhook_79893fd6-aa7c-483b-8ecb-7d0a20451c90"    }}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "_id": "670f981690e5ee13019669e1",    "type": "non_recurring",    "name": "testing schedule",    "event_type": "whatsapp",    "description": "",    "options": null,    "job": {        "type": "webhook",        "data": {            "topicToSend": "",            "segmentationGroup": "",            "groupToSend": "",            "outboundTags": "Marketing",            "outboundType": "sendToAllGroups",            "message": "sdsdsds",            "files": [                {                    "id": "imbrace-upload1 - 0",                    "name": "20200526110944-Bank-Statement_1.jpg",                    "isValid": true,                    "status": "ok"                }            ],            "topic": "",            "sender": {                "name": "Austina Engelhardt",                "id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",                "email": "agent01@imbrace.co"            },            "appId": "app_a730320f-bc56-4857-b488-300f15bcdf8f"        },        "method": "POST",        "url": "https://org-imbrace.dev.imbrace.co/webhook/webhook_79893fd6-aa7c-483b-8ecb-7d0a20451c90",        "files": [            {                "organization_id": "org_imbrace",                "name": "iphone13.jpg",                "file_id": "1d1e5bf5-9c70-4138-854b-bbcc15b9cb09",                "file_path": "org_imbrace/1729075265762/iphone13.jpg",                "size": 15030,                "file_type": "image/jpeg",                "file_extension": "jpeg",                "file_url": "https://imbrace-marketplace-dev.s3.ap-east-1.amazonaws.com/org_imbrace/1729075265762/iphone13.jpg",                "is_public": true,                "short_path": "3c13c6"            }        ]    },    "organization_id": "org_imbrace",    "trigger_frequency_unit": "minutes",    "trigger_frequency_value": 30,    "start_date": "2024-10-16T14:45:15.463Z",    "start_time": "2024-10-16T14:45:15.463Z",    "start_datetime": "2024-10-16T14:45:15.463Z",    "is_paused": false,    "is_finished": false,    "channel_source": "",    "created_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",    "updated_by": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",    "created_at": "2024-10-16T10:40:22.424Z",    "updated_at": "2024-10-16T10:41:05.822Z",    "one_time_schedule_type": "exact"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "scheduler_id is required"}
  ```

  ```
  {    "message": "payload is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "Scheduler not found"}
  ```
* **Example:**

  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/3rd/organization/org_imbrace/users/u_imbrace_agent1/schedulers/files/670f981690e5ee13019669e1' \--header 'x-organization-id: org_imbrace' \--header 'x-user-id: u_imbrace_agent1' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1' \--form 'payload="{    \"type\": \"non_recurring\",    \"name\": \"testing schedule\",    \"event_type\": \"whatsapp\",    \"channel_source\": \"\",    \"description\": \"\",    \"one_time_schedule_type\": \"exact\",    \"start_datetime\": \"2024-10-16T14:45:15.463Z\",    \"job\": {        \"type\": \"webhook\",        \"data\": {            \"topicToSend\": \"\",            \"segmentationGroup\": \"\",            \"groupToSend\": \"\",            \"outboundTags\": \"Marketing\",            \"outboundType\": \"sendToAllGroups\",            \"message\": \"sdsdsds\",            \"files\": [                {                    \"id\": \"imbrace-upload1 - 0\",                    \"file\": {},                    \"name\": \"20200526110944-Bank-Statement_1.jpg\",                    \"isValid\": true,                    \"status\": \"ok\"                }            ],            \"topic\": \"\",            \"sender\": {                \"name\": \"Austina Engelhardt\",                \"id\": \"u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a\",                \"email\": \"agent01@imbrace.co\"            },            \"appId\": \"app_a730320f-bc56-4857-b488-300f15bcdf8f\"        },        \"method\": \"POST\",        \"url\": \"https://org-imbrace.dev.imbrace.co/webhook/webhook_79893fd6-aa7c-483b-8ecb-7d0a20451c90\"    }}"' \--form 'files=@"/C:/Users/DEEL/OneDrive/Documents/Online Shop/tommy_perfume.jpg"'
  ```

---

## [8. Delete Scheduler](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/schedule#8-delete-scheduler)

Delete a specific scheduler by its ID.

This API allows you to delete a scheduler by providing the scheduler ID and optional scheduler details in the request body. Once deleted, the scheduler will be permanently removed from the system.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/users/{user_id}/schedulers/{scheduler_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
  * `x-organization-id`: The unique identifier of the organization
  * `Content-Type`: `application/json`
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `user_id` (string, required): The unique identifier of the user
  * `scheduler_id` (string, required): The unique identifier of the scheduler
* **Body:**

  ```
  {    "type": "non_recurring",    "schedule_id": "schedule_1",    "callback_url": "https://google.com",    "start_date": "2024-04-29T16:00:00.000Z",    "start_time": "1969-12-31T19:05:00.000Z"}
  ```
* **Body Parameters:**

  * `type` (string, optional): Scheduler type (e.g., "recurring", "non_recurring")
  * `schedule_id` (string, optional): Schedule identifier for confirmation
  * `callback_url` (string, optional): Callback URL associated with the scheduler
  * `start_date` (string, optional): Start date of the scheduler
  * `start_time` (string, optional): Start time of the scheduler
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "message": "schedule schedule_1 is deleted successfully"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "scheduler_id is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "Scheduler not found"}
  ```
* **Example:**

  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/3rd/organization/org_imbrace/users/u_imbrace_agent1/schedulers/schedule_1' \--header 'x-organization-id: org_imbrace' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1' \--header 'Content-Type: application/json' \--data '{    "type": "non_recurring",    "schedule_id": "schedule_1",    "callback_url": "https://google.com",    "start_date": "2024-04-29T16:00:00.000Z",    "start_time": "1969-12-31T19:05:00.000Z"}'
  ```
