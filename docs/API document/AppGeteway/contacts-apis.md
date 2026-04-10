# Contacts apis

The Contacts APIs provide a centralized way to manage users, their contact information, and communication history across multiple channels. These APIs are essential for building a unified customer or user communication system. They allow you to

---

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#overview)

The following APIs help you manage contact data and active conversations for your teams and channels.

---

### [1. Get Contact](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#1-get-contact)

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/contacts?limit=10&skip=0&sort=-created_at`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/contacts?limit=10&skip=0&sort=-created_at`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/contacts?limit=10&skip=0&sort=-created_at`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "list",    "data": [        {            "object_name": "contact",            "id": "con_66d67483-8982-43d6-acbe-139568688add",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_2592e13f-c43f-48a2-a416-a7bb12a5caec",            "channel_type": "web",            "display_name": "UNK#DO1695",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Saigon",            "last_seen": "2025-10-15T10:07:59.066Z",            "created_at": "2025-10-15T10:06:26.630Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        },        {            "object_name": "contact",            "id": "con_56e4e804-30f7-497a-905d-dade09b561cc",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_2592e13f-c43f-48a2-a416-a7bb12a5caec",            "channel_type": "web",            "display_name": "UNK#DX2694",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Saigon",            "last_seen": "2025-10-15T05:09:29.391Z",            "created_at": "2025-10-15T03:35:27.277Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        },        {            "object_name": "contact",            "id": "con_1ae4ac42-173c-4549-b2ab-dff386bbe886",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_2592e13f-c43f-48a2-a416-a7bb12a5caec",            "channel_type": "web",            "display_name": "UNK#LO8002",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Saigon",            "last_seen": "2025-10-14T12:09:45.151Z",            "created_at": "2025-10-14T08:38:49.111Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        },        {            "object_name": "contact",            "id": "con_be4c69d0-bf0b-44e0-95e4-c0e5f66e446a",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_2592e13f-c43f-48a2-a416-a7bb12a5caec",            "channel_type": "web",            "display_name": "UNK#GV7261",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Saigon",            "last_seen": "2025-10-14T05:27:38.324Z",            "created_at": "2025-10-14T04:01:52.524Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        },        {            "object_name": "contact",            "id": "con_21f02e1d-ddcb-4e52-b95b-db94ef9a5e62",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_2592e13f-c43f-48a2-a416-a7bb12a5caec",            "channel_type": "web",            "display_name": "UNK#UC5549",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Saigon",            "last_seen": "2025-10-14T03:30:29.594Z",            "created_at": "2025-10-14T03:27:35.939Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        },        {            "object_name": "contact",            "id": "con_d33dfa92-2979-4621-9fd7-eb6731169abf",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_7eddc925-f8c0-409f-96b7-b88c0c013f6a",            "channel_type": "web",            "display_name": "VNM#HJ9208",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Bangkok",            "last_seen": "2025-10-14T11:13:22.833Z",            "created_at": "2025-10-13T23:11:50.187Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        },        {            "object_name": "contact",            "id": "con_bb32705f-b799-4989-b64a-a30131c9d835",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_3c172ef8-d417-4467-8c2c-4d98aeff9eed",            "channel_type": "web",            "display_name": "UNK#OZ2092",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Saigon",            "last_seen": "2025-10-13T00:53:16.542Z",            "created_at": "2025-10-13T00:50:08.140Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        },        {            "object_name": "contact",            "id": "con_a119565f-6c84-49ba-8c64-6da7772175e8",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_06d9eb49-acde-4d3e-b457-d7cb73b277b4",            "channel_type": "web",            "display_name": "UNK#EU0957",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Saigon",            "last_seen": "2025-10-13T08:48:08.659Z",            "created_at": "2025-10-11T00:19:38.698Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        },        {            "object_name": "contact",            "id": "con_3a99e79d-4d5d-44cf-b44f-50848e19a4ed",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_06d9eb49-acde-4d3e-b457-d7cb73b277b4",            "channel_type": "web",            "display_name": "UNK#WB7192",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Saigon",            "last_seen": "2025-10-10T08:05:17.772Z",            "created_at": "2025-10-10T08:01:18.366Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        },        {            "object_name": "contact",            "id": "con_a0c05c8e-d75e-4347-8bb0-bd9cd6ef26ba",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "channel_id": "ch_06d9eb49-acde-4d3e-b457-d7cb73b277b4",            "channel_type": "web",            "display_name": "UNK#TL3680",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "email": "",            "remark": "",            "time_zone": "Asia/Saigon",            "last_seen": "2025-10-10T11:43:30.834Z",            "created_at": "2025-10-10T07:47:44.199Z",            "updated_at": null,            "odooContactID": "",            "title": "",            "birthday": "",            "location": "",            "company_name": "",            "position": "",            "whatsapp_id": "",            "facebook_id": "",            "messenger_id": "",            "wechat_id": "",            "line_id": "",            "instagram_id": "",            "additional_params": {}        }    ],    "nested": {},    "has_more": true,    "count": 65681,    "total": 10}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/contacts?limit=10&skip=0&sort=-created_at' \--header 'X-Access-Token: acc_f7124766-e633-429c-b24a-ab0421a202e3' \--data ''
  ```

### [2. Get Contact by contact_id](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#2-get-contact-by-contact_id)

Retrieve detailed contact information, including conversation history, associated teams, and the latest messages.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/contacts/:contact_id/conversations?channel_types=web&channel_types=whatsapp&channel_types=facebook&channel_types=email&channel_types=wechat&channel_types=instagram&channel_types=line`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/contacts/:contact_id/conversations?channel_types=web&channel_types=whatsapp&channel_types=facebook&channel_types=email&channel_types=wechat&channel_types=instagram&channel_types=line`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/contacts/:contact_id/conversations?channel_types=web&channel_types=whatsapp&channel_types=facebook&channel_types=email&channel_types=wechat&channel_types=instagram&channel_types=line`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Params** **Path Variables**

  * `contact_id`: `con_32a507dd-dc57-49a9-8456-7fb9c48d2a41`
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "_id": "conv_31b75006-beac-49af-b3b3-b8591d3438e6",            "doc_name": "team_conversation_user",            "public_id": "tcu_f0a533ff-4813-4b74-bc70-8c68725e83db",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "assign_from": "",            "created_at": "2024-11-14T14:12:16.056Z",            "updated_at": "2024-11-14T14:12:16.056Z",            "conversation": {                "_id": "conv_31b75006-beac-49af-b3b3-b8591d3438e6",                "doc_name": "conversation",                "public_id": "conv_31b75006-beac-49af-b3b3-b8591d3438e6",                "organization_id": "org_imbrace",                "business_unit_id": "bu_imbrace_testing",                "channel_id": "ch_ed6e2673-fd52-459f-b3a1-d392addcd771",                "channel_type": "web",                "contact_id": "con_32a507dd-dc57-49a9-8456-7fb9c48d2a41",                "status": "pending",                "name": "TWN#NJ9585@14 Nov 2024",                "timestamp": "2024-12-07T07:54:40.910Z",                "is_ready": true,                "is_agent_joined": true,                "created_at": "2024-11-14T14:12:16.016Z",                "updated_at": "2025-09-05T09:40:47.437Z",                "_language": "en",                "mode": "hybrid"            },            "contact": {                "_id": "con_32a507dd-dc57-49a9-8456-7fb9c48d2a41",                "doc_name": "contact",                "public_id": "con_32a507dd-dc57-49a9-8456-7fb9c48d2a41",                "updated_at": null,                "created_at": "2024-11-14T14:12:15.771Z",                "business_unit_id": "bu_imbrace_testing",                "organization_id": "org_imbrace",                "channel_id": "ch_ed6e2673-fd52-459f-b3a1-d392addcd771",                "channel_type": "web",                "display_name": "TWN#NJ9585",                "provider_user_id": "4a73b612-809b-4406-b358-e0b5ac8db42b",                "avatar_url": "",                "first_name": "",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "email": "",                "remark": "",                "time_zone": "Asia/Taipei",                "last_seen": "2024-12-08T11:03:21.114Z",                "title": "",                "birthday": "",                "location": "",                "position": "",                "company_name": "",                "whatsapp_id": "",                "facebook_id": "",                "messenger_id": "",                "wechat_id": "",                "line_id": "",                "instagram_id": "",                "_language": "en",                "board_id": "brd_eebbc2af-14b3-4c3a-99fb-8e6f9ccbc15c",                "board_item_id": "bi_311f5661-4aa3-4bbc-bb0c-fe18883e444e"            },            "latest_message": {                "_id": "msg_46272ba0-b9b3-40b6-a5d0-25fa5628620e",                "type": "text",                "content": {                    "text": "as",                    "is_mail": false,                    "parent_url": "https://dev-chat-widget.imbrace.co/test.html"                },                "created_at": "2024-12-07T07:54:40.910Z"            },            "contacts_latest_message": {                "_id": "msg_46272ba0-b9b3-40b6-a5d0-25fa5628620e",                "type": "text",                "content": {                    "text": "as",                    "is_mail": false,                    "parent_url": "https://dev-chat-widget.imbrace.co/test.html"                },                "created_at": "2024-12-07T07:54:40.910Z"            },            "available_team_conversations": [                {                    "_id": "tcu_3d2368a9-550e-4fc1-8af9-dbcaba7acae4",                    "user_id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a"                },                {                    "_id": "tcu_fcd0ce0c-e5a7-449f-9a78-9b5962055a95",                    "user_id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a"                }            ],            "teams": [                {                    "_id": "t_4ffefd06-ab08-4035-9c21-6ab5e97271cf",                    "doc_name": "team",                    "public_id": "t_4ffefd06-ab08-4035-9c21-6ab5e97271cf",                    "organization_id": "org_imbrace",                    "business_unit_id": "bu_imbrace_testing",                    "icon_url": "",                    "name": "Harris Grab mode long long long long",                    "mode": "grab",                    "description": "",                    "is_default": false,                    "created_at": "2023-02-09T09:49:43.037Z",                    "updated_at": "2023-07-20T03:28:09.029Z"                },                {                    "_id": "t_imbrace_default_team",                    "doc_name": "team",                    "public_id": "t_imbrace_default_team",                    "organization_id": "org_imbrace",                    "business_unit_id": "bu_imbrace_testing",                    "icon_url": "",                    "name": "General",                    "mode": "public",                    "description": "Default iMBRACE team, auto create by system for testing purpose",                    "is_default": true,                    "created_at": "2022-06-22T09:19:58.929Z",                    "updated_at": "2023-09-22T05:59:18.581Z",                    "is_disabled": false                }            ]        }    ]}
  ```

  * **Status code: 400 Not Found**

  ```
       {         "message": "Not Found"     }
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/contacts/con_32a507dd-dc57-49a9-8456-7fb9c48d2a41/conversations?channel_types=web&channel_types=whatsapp&channel_types=facebook&channel_types=email&channel_types=wechat&channel_types=instagram&channel_types=line' \--header 'X-Access-Token: acc_3064efc7-4ccc-4b48-8ffa-50313e5b19df'
  ```

### [3. Search Contact](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#3-search-contact)

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/contacts/_search?limit=10&skip=0&q=&type=text`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/contacts/_search?limit=10&skip=0&q=&type=text`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/contacts/_search?limit=10&skip=0&q=&type=text`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Params** **Path Variables**

  * `contact_id`: `con_32a507dd-dc57-49a9-8456-7fb9c48d2a41`
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "list",    "data": [],    "nested": {},    "has_more": false,    "count": 0,    "total": 0}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/contacts/_search?limit=10&skip=0&q=a&type=text' \--header 'X-Access-Token: acc_f7124766-e633-429c-b24a-ab0421a202e3' \--data ''
  ```

### [4. Update Contact](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#4-update-contact)

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/v1/backend/contacts/:contact_id`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/v1/backend/contacts/:contact_id`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/v1/backend/contacts/:contact_id`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Params** **Path Variables**

  * `contact_id`: `con_32a507dd-dc57-49a9-8456-7fb9c48d2a41`
* **Body:**

  ```
  {    "email": "abc@imbrace.co",    "avatar_url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/contact/org_imbrace/file_wYDqtXuHdyuhwDVTPRi9LKTMQB.png",    "gender": "m",    "first_name": "Hi",    "last_name": "Bye Bye",    "language": "en",    "area_code": "852",    "phone_number": "88888888",    "remark": ""}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "contact",    "id": "con_32a507dd-dc57-49a9-8456-7fb9c48d2a41",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "channel_id": "ch_web_fake_channel",    "channel_type": "web",    "display_name": "Hi Bye Bye",    "avatar_url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/contact/org_imbrace/file_wYDqtXuHdyuhwDVTPRi9LKTMQB.png",    "first_name": "Hi",    "last_name": "Bye Bye",    "gender": "Male",    "area_code": "852",    "phone_number": "88888888",    "language": "en",    "email": "abc@imbrace.co",    "remark": "",    "time_zone": "Asia/Hong_Kong",    "last_seen": "",    "created_at": "2023-11-20T04:33:55.703Z",    "updated_at": "2025-10-16T03:31:43.379Z",    "odooContactID": "",    "title": "",    "birthday": "",    "location": "",    "company_name": "",    "position": "",    "whatsapp_id": "",    "facebook_id": "",    "messenger_id": "",    "wechat_id": "",    "line_id": "",    "instagram_id": "",    "additional_params": {},    "action": "bu.contact_updated"}
  ```
* **Example:**

  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/v1/backend/contacts/con_test_contact' \--header 'X-Access-Token: acc_f7124766-e633-429c-b24a-ab0421a202e3' \--header 'Content-Type: application/json' \--data-raw '{    "email": "abc@imbrace.co",    "avatar_url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/contact/org_imbrace/file_wYDqtXuHdyuhwDVTPRi9LKTMQB.png",    "gender": "m",    "first_name": "Hi",    "last_name": "Bye Bye",    "language": "en",    "area_code": "852",    "phone_number": "88888888",    "remark": ""}'
  ```

### [5. Get notification](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#5-get-notification)

Fetches a paginated list of notifications for the authenticated user, including unread/read state and a summary count. Use to render the notification center/badge, infinite-scroll lists, or to check how many items are unread.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/notifications?limit=10&skip=0`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/notifications?limit=10&skip=0`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/notifications?limit=10&skip=0`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
* **Result:**

  * **Status code: 200 OK**

  ```
    {    "data": [        {            "object_name": "notifications",            "id": "not_0b5ea835-177d-456c-b2b3-e7e9a838efe6",            "title": "UNK#FR3184@16 Sep 2025",            "content": "",            "from": "General",            "type": 201,            "action_to": {                "team_conversation_user_id": "tcu_96e47d5a-913e-4cd0-b3ae-4eadfb7d8f9b"            },            "recipient": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",            "is_read": false,            "created_at": "2025-09-16T04:03:01.293Z",            "action_disable": false,            "channel_type": "web"        },        {            "object_name": "notifications",            "id": "not_a811cf18-42aa-4226-8fb0-6a20fdf1b94e",            "title": "UNK#UY4364@12 Sep 2025",            "content": "",            "from": "General",            "type": 201,            "action_to": {                "team_conversation_user_id": "tcu_812ca05d-6a38-46bb-b08e-973417228338"            },            "recipient": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",            "is_read": false,            "created_at": "2025-09-12T04:18:30.645Z",            "action_disable": false,            "channel_type": "web"        }    ],    "count": 618,    "total": 2,    "unread_count": 595,    "has_more": true}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/notifications?limit=10&skip=0' \
  ```

--header 'X-Access-Token: acc_87681c72-6dd9-4057-adce-f01c3bc6cfd8'

```
### 4. Put notification readMarks one or more notifications as read for the authenticated user. Call after a user opens or views specific items so the unread badge/count updates.* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/v1/backend/notifications/read`* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/v1/backend/notifications/read`* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/v1/backend/notifications/read`* **Headers:*** `Content-Type`: `application/json`* `x-access-token`: <AccessTokenLoader/>* **Body:**```json["not_a3bd1037-d190-4195-8071-0673b1ed3f97", "not_d1cd4ab6-1bba-4096-acdc-6d2b9dd46b2b"]
```

* **Result:**
  * **Status code: 200 OK**
* **Example:**
  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/v1/notifications/read' \--header 'X-Access-Token: acc_87681c72-6dd9-4057-adce-f01c3bc6cfd8' \--data '["not_a3bd1037-d190-4195-8071-0673b1ed3f97", "not_d1cd4ab6-1bba-4096-acdc-6d2b9dd46b2b"]'
  ```

### [5. Deleted notification dismiss](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#5-deleted-notification-dismiss)

Dismisses (removes) specific notifications from the user’s list. This is typically a soft delete from the client’s perspective. Use when the user explicitly dismisses one or multiple notifications (e.g., “Clear” button on an item).

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/v1/backend/notifications/dismiss`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/v1/backend/notifications/dismiss`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/v1/backend/notifications/dismiss`
* **Headers:**
  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body:**
  ```
  ["not_a3bd1037-d190-4195-8071-0673b1ed3f97", "not_d1cd4ab6-1bba-4096-acdc-6d2b9dd46b2b"]
  ```
* **Result:**
  * **Status code: 200 OK**
* **Example:**
  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/v1/notifications/dismiss' \--header 'X-Access-Token: acc_87681c72-6dd9-4057-adce-f01c3bc6cfd8' \--data '["not_9fdb4db1-0920-486d-b42d-e99a6ba75960", "not_c5e3c17b-bc82-47b4-b146-c3fb5a802363"]'
  ```

### [6. Deleted notification all dismiss](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#6-deleted-notification-all-dismiss)

Bulk-dismisses all notifications for a given category/type (or all, depending on server rules). Useful for “Clear all” actions. Use for one-click “Clear all notifications” in a specific section (e.g., conversations) or globally if supported.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/v1/backend/notifications/dismiss/all`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/v1/backend/notifications/dismiss/all`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/v1/backend/notifications/dismiss/all`
* **Headers:**
  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Query Params**
  * `type`:`conversations`
* **Body:**
* **Result:**
  * **Status code: 200 OK**
* **Example:**
  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/v1/notifications/dismiss/all?type=conversations' \--header 'X-Access-Token: acc_87681c72-6dd9-4057-adce-f01c3bc6cfd8'
  ```

### [7. Get Contact Conversations by Channel Type](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#7-get-contact-conversations-by-channel-type)

Retrieve contact conversations filtered by specific channel types.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/contacts/{contact_id}/conversations?channel_types=web`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/contacts/{contact_id}/conversations?channel_types=web`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/contacts/{contact_id}/conversations?channel_types=web`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `contact_id` (string, required): The unique identifier of the contact
* **Query Parameters:**

  * `channel_types` (string, required): The type of channel to filter conversations (e.g., "web", "whatsapp", "facebook", etc.)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": [        {            "_id": "conv_31b75006-beac-49af-b3b3-b8591d3438e6",            "doc_name": "team_conversation_user",            "public_id": "tcu_f0a533ff-4813-4b74-bc70-8c68725e83db",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "assign_from": "",            "created_at": "2024-11-14T14:12:16.056Z",            "updated_at": "2024-11-14T14:12:16.056Z",            "conversation": {                "_id": "conv_31b75006-beac-49af-b3b3-b8591d3438e6",                "doc_name": "conversation",                "public_id": "conv_31b75006-beac-49af-b3b3-b8591d3438e6",                "organization_id": "org_imbrace",                "business_unit_id": "bu_imbrace_testing",                "channel_id": "ch_ed6e2673-fd52-459f-b3a1-d392addcd771",                "channel_type": "web",                "contact_id": "con_32a507dd-dc57-49a9-8456-7fb9c48d2a41",                "status": "pending",                "name": "TWN#NJ9585@14 Nov 2024",                "timestamp": "2024-12-07T07:54:40.910Z",                "is_ready": true,                "is_agent_joined": true,                "created_at": "2024-11-14T14:12:16.016Z",                "updated_at": "2025-09-05T09:40:47.437Z",                "_language": "en",                "mode": "hybrid"            }        }    ]}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/contacts/con_66d67483-8982-43d6-acbe-139568688add/conversations?channel_types=web' \--header 'X-Access-Token: con_66d67483-8982-43d6-acbe-139568688add'
  ```

### [8. Get Contact Comments](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#8-get-contact-comments)

Retrieve comments associated with a specific contact and comment ID.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/contacts/{contact_id}/comment/{comment_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/contacts/{contact_id}/comment/{comment_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/contacts/{contact_id}/comment/{comment_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `contact_id` (string, required): The unique identifier of the contact
  * `comment_id` (string, required): The unique identifier of the comment
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": []}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/contacts/con_32a507dd-dc57-49a9-8456-7fb9c48d2a41/comment/cmc_a430220f-c132-4ea6-bf69-6a13b91d327b' \--header 'X-Access-Token: acc_6f1f1e25-627e-464d-a5dc-19a1c8350b73'
  ```

### [9. Upload Contact File](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#9-upload-contact-file)

Upload a file associated with contacts. This API supports file uploads and returns a URL to the uploaded file.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/contacts/_fileupload`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/contacts/_fileupload`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/contacts/_fileupload`
* **Headers:**

  * `Content-Type`: `multipart/form-data`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Body Parameters:**

  * `file` (file, required): The file to upload
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "url": "https://imbrace-uat.s3.ap-east-1.amazonaws.com/contact/org_imbrace/file_5W9XPQ96XguTW4jhh5dca15rQU.png"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/contacts/_fileupload' \--header 'X-Access-Token: acc_6f1f1e25-627e-464d-a5dc-19a1c8350b73' \--form 'file=@"/C:/Users/Koson/Downloads/loginDevPortal.png"'
  ```

### [10. Get Contact Files](https://devportal.dev.imbrace.co/docs/api-document/app-apis/contactsApis#10-get-contact-files)

Retrieve all files associated with a specific contact.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/contact/{contact_id}/files`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/contact/{contact_id}/files`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/contact/{contact_id}/files`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `contact_id` (string, required): The unique identifier of the contact
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "_id": "msg_ba947f15-3396-4530-9138-477af72804ec",        "content": {            "caption": "test aiaiai",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_SQOSHxwqOxofYxBkhS9aZZAtRN.mpeg",            "extension": "mpeg"        },        "created_at": "2022-09-23T09:47:08.714Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T09:47:08.714Z"    },    {        "_id": "msg_e798b20b-5d7a-424e-b2ee-14e5f5e3e146",        "content": {            "caption": "file01",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_rlp61qhHs5s1rvsKAWSVgTW8Zf.plain",            "extension": "plain"        },        "created_at": "2022-09-23T09:45:17.654Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T09:45:17.654Z"    },    {        "_id": "msg_e20e2be4-382f-4f89-ad2b-2351d27e9436",        "content": {            "caption": "file02",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_PxuIKaptfC9XBWWpPOSzqduW41.mpeg",            "extension": "mpeg"        },        "created_at": "2022-09-23T09:26:48.488Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T09:26:48.488Z"    },    {        "_id": "msg_031f5f2b-c40f-48e4-9fa6-9de41786c9bb",        "content": {            "caption": "file03",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_8nue2v8SIfQNzDtbcHd9YF7y4a.mpeg",            "extension": "mpeg"        },        "created_at": "2022-09-23T09:26:14.393Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T09:26:14.393Z"    },    {        "_id": "msg_efe28919-6bc9-41cd-b64f-f244fc75aba1",        "content": {            "caption": "file04",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_7vw2T7AQ9j6blnoX5wwMhsOjBG.plain",            "extension": "plain"        },        "created_at": "2022-09-23T09:20:53.522Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T09:20:53.522Z"    },    {        "_id": "msg_861c85d7-9517-495b-84e2-a2c34f723d5b",        "content": {            "caption": "file05",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_6epctcMWC4QkCrsvSTo4qTrKWv.bmp",            "extension": "bmp"        },        "created_at": "2022-09-23T09:18:20.425Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T09:18:20.425Z"    },    {        "_id": "msg_9e661135-0aee-4c8a-88f9-77e9ffe01070",        "content": {            "caption": "file06",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_yKK0YqdEJAFB1pvbIBgzgiCfzE.mp4",            "extension": "mp4"        },        "created_at": "2022-09-23T08:53:53.774Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:53:53.774Z"    },    {        "_id": "msg_009a0bcb-6f80-4f31-833b-f64b83059f50",        "content": {            "caption": "file07",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_8VjUrAXtYgE3W9FSt3fP2Ue1XQ.mp4",            "extension": "mp4"        },        "created_at": "2022-09-23T08:53:46.552Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:53:46.552Z"    },    {        "_id": "msg_3639c357-b47f-4466-98c4-d13dfe85ec76",        "content": {            "caption": "file08",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_jx1Cvne0RasUfPlyryhZQeOBum.png",            "extension": "png"        },        "created_at": "2022-09-23T08:53:33.066Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:53:33.066Z"    },    {        "_id": "msg_066a42ac-68a6-44d2-a31a-d6a1e9b4f6eb",        "content": {            "caption": "file09",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_Mbl2B1T4QiOhCw6xQgKHnGpPAM.png",            "extension": "png"        },        "created_at": "2022-09-23T08:53:25.943Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:53:25.943Z"    },    {        "_id": "msg_7ef149ab-7f11-4389-a941-ad1d9411ba78",        "content": {            "caption": "file10",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_aol2J2m82WWK1nL8CtlXF5HQEi.plain",            "extension": "plain"        },        "created_at": "2022-09-23T08:53:18.975Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:53:18.975Z"    },    {        "_id": "msg_f3c18989-9588-42c3-b57b-6ad30275322f",        "content": {            "caption": "file11",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_axE38ekiqgCeOTbukI0TVM9Dif.mp4",            "extension": "mp4"        },        "created_at": "2022-09-23T08:53:12.196Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:53:12.196Z"    },    {        "_id": "msg_48b478a4-a113-4e37-85dc-b76367cf57b1",        "content": {            "caption": "file12",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_AVHAKbQAsOHfI819xqyhTXvEe7.pdf",            "extension": "pdf"        },        "created_at": "2022-09-23T08:53:05.236Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:53:05.236Z"    },    {        "_id": "msg_79479a48-d146-47eb-9dac-c911e984e228",        "content": {            "caption": "file13",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_ap15IpVtQnRnFxbRzwjn9rdezm.gif",            "extension": "gif"        },        "created_at": "2022-09-23T08:52:58.392Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:52:58.392Z"    },    {        "_id": "msg_d86da14f-5c78-450f-b651-62a51cc1dce5",        "content": {            "caption": "file14",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_IMwoEXSBOHW93RT4qKincnMZUD.webp",            "extension": "webp"        },        "created_at": "2022-09-23T08:52:51.509Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:52:51.509Z"    },    {        "_id": "msg_8c7bdb63-b8eb-4f62-8863-e3d8fa38ea43",        "content": {            "caption": "file15",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_Xe51gPJj7KLvTnZEbpOgXmJxud.tiff",            "extension": "tiff"        },        "created_at": "2022-09-23T08:52:44.726Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:52:44.726Z"    },    {        "_id": "msg_da29283a-dd1f-4216-b3fa-d22e621d99de",        "content": {            "caption": "file16",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_IIdNouW9VjyQUC6mGoQnIxsT29.png",            "extension": "png"        },        "created_at": "2022-09-23T08:52:37.856Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:52:37.856Z"    },    {        "_id": "msg_ab875998-5825-4922-a392-b65764e3a4a9",        "content": {            "caption": "file17",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_ImMm1tXT2v9kjtLQxHrMwh3Ht9.octet-stream",            "extension": "octet-stream"        },        "created_at": "2022-09-23T08:52:30.901Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:52:30.901Z"    },    {        "_id": "msg_c57e671c-d0cf-4d25-a28d-e38e811ecbdb",        "content": {            "caption": "file18",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_jYyRTtLzhHyAV1LOw3uSrRTXqd.jpeg",            "extension": "jpeg"        },        "created_at": "2022-09-23T08:52:23.993Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:52:23.993Z"    },    {        "_id": "msg_1adfc003-0093-4452-b391-2f355f68f2d5",        "content": {            "caption": "file19",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_JP0Sug1ju4t1Eii1YGXbVaAAMJ.octet-stream",            "extension": "octet-stream"        },        "created_at": "2022-09-23T08:46:10.428Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:46:10.428Z"    },    {        "_id": "msg_cacb7f13-2f99-4805-ba9b-ff4fa08187f2",        "content": {            "caption": "file20",            "url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/chat/org_imbrace/file_faUsgQKpXzNDGkYKIwn9fcpnxn.jpeg",            "extension": "jpeg"        },        "created_at": "2022-09-23T08:46:03.652Z",        "from": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",        "type": "image",        "updated_at": "2022-09-23T08:46:03.652Z"    }]
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/contact/con_32a507dd-dc57-49a9-8456-7fb9c48d2a41/files' \--header 'X-Access-Token: acc_6f1f1e25-627e-464d-a5dc-19a1c8350b73' \--data ''
  ```
