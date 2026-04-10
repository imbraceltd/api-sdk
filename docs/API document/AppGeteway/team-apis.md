[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[App Gateway](https://devportal.dev.imbrace.co/docs/api-document/app-apis)

# Team APIs

Team APIs provide comprehensive team management capabilities including creating, updating, and managing teams within your organization. These APIs enable you to organize users into teams, assign roles, and control access permissions across your iMBRACE workspace.

# [Team APIs](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#team-apis)

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#overview)

Team APIs allow you to manage organizational teams, user assignments, and role-based access control within your iMBRACE workspace. These APIs provide the foundation for organizing users into functional groups and managing their permissions across different features and data access levels.

---

## [1. Create Team](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#1-create-team)

Create a new team within your organization.

This API allows you to create a new team with specified name, description, mode, and other team properties. Teams are used to organize users and control access to various features and data within your workspace.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/teams`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/teams`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/teams`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "business_unit_id": "{{business_unit_id}}",    "name": "Sales",    "mode": "grab",    "icon_url": "",    "description": "Sales team"}
  ```
* **Request Parameters:**

  * `business_unit_id` (string, required): The unique identifier of the business unit
  * `name` (string, required): The name of the team
  * `mode` (string, required): The team mode (e.g., "grab", "assign", "round_robin")
  * `icon_url` (string, optional): URL of the team icon
  * `description` (string, optional): Description of the team
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "team",    "id": "t_35d4663e-ace7-4698-9348-dc30d5638c99",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "name": "Sales",    "icon_url": "",    "description": "Sales team",    "created_at": "2022-04-01T08:28:13.541Z",    "updated_at": "2022-04-01T08:28:13.541Z",    "team_user_ids": [        "tu_974ef6cd-863d-418c-90c3-2b8ab1c3a7a8"    ],    "team_users": [        {            "object_name": "team_user",            "id": "tu_974ef6cd-863d-418c-90c3-2b8ab1c3a7a8",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "user_id": "u_imbrace_admin",            "role": "admin",            "created_at": "2022-04-01T08:28:13.545Z",            "updated_at": "2022-04-01T08:28:13.545Z"        }    ]}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Team already exist"}
  ```

  * **Status code: 403 Forbidden**

  ```
  {    "code": 40003,    "message": "Forbidden, insufficient permission"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/teams' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "business_unit_id": "bu_imbrace_testing",    "name": "Sales",    "mode": "grab",    "icon_url": "",    "description": "Sales team"}'
  ```

## [2. Add Multiple Users to Team](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#2-add-multiple-users-to-team)

Add multiple users to an existing team in a single operation.

This API allows you to add multiple users to a team with their respective roles in one request. This is more efficient than adding users one by one and supports bulk operations.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v2/backend/teams/_add_users`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v2/backend/teams/_add_users`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v2/backend/teams/_add_users`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "team_id": "t_imbrace_default_team",    "reserve_leave": true,    "users": [        {            "user_id": "u_imbrace_agent1",            "role": "member"        },        {            "user_id": "u_imbrace_agent2",            "role": "admin"        },        {            "user_id": "u_imbrace_bot",            "role": "test"        }    ]}
  ```
* **Request Parameters:**

  * `team_id` (string, required): The unique identifier of the team
  * `reserve_leave` (boolean, required): Whether to reserve leave for existing team members
  * `users` (array, required): Array of user objects to add to the team
    * `user_id` (string, required): The unique identifier of the user
    * `role` (string, required): The role to assign to the user
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "team",    "id": "t_imbrace_default_team",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "name": "General",    "mode": "public",    "icon_url": "",    "description": "Default iMBRACE team, auto create by system for testing purpose",    "is_default": true,    "user_state": "",    "created_at": "2022-06-22T09:19:58.929Z",    "updated_at": "2023-09-22T05:59:18.581Z",    "is_disabled": false,    "team_user_ids": [        "tu_2c2f8943-01c4-41fc-90ff-5a427ae416fb",        "tu_21b9c7b0-a7c0-4e4d-8d75-899229d199b0",        "tu_fc2b83f7-c053-498e-9642-da178bda13d7",        "tu_b7719e49-6135-44ff-a0f8-1230cd7d7e36",        "tu_b6d12f57-8e49-4372-84c0-1dcb735929c9",        "tu_ad0c8cd9-c344-4c7d-941c-6c7e96248c5e",        "tu_imbrace_admin",        "tu_89003b21-c723-4a0f-96c2-83d358044f85",        "tu_e3d43e3f-852d-47f4-b810-27ca00f6ca85",        "tu_4fdc4974-01cc-4645-9d70-48036233da1b",        "tu_imbrace_agent1",        "tu_imbraec_agent2",        "tu_deaf5d87-8e49-4f8c-8193-ad6013fc7b80",        "tu_159f11b2-b117-41b1-b797-44f83a76e503",        "tu_a765a251-d3bf-4598-82b1-f2337b97a44e",        "tu_4cfee84f-8752-462f-9caf-92a658b447ff",        "tu_a267a4ea-4109-4c52-8245-0edbd6100a1b",        "tu_1b0e7d71-0b81-4dce-9f68-404ed61d6d8b",        "tu_a296029c-1096-46ff-98b4-23cebae70c14",        "tu_40864d3b-0550-4760-a27f-8d153c4f3540"    ],    "team_users": [        {            "object_name": "team_user",            "id": "tu_2c2f8943-01c4-41fc-90ff-5a427ae416fb",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_09173225-d34e-4f1b-8b80-9e97a608db07",            "role": "admin",            "state": "join"        },        {            "object_name": "team_user",            "id": "tu_21b9c7b0-a7c0-4e4d-8d75-899229d199b0",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_f7dfc4b2-96bb-4c38-a74a-608bbb22bf9c",            "role": "member",            "state": "join"        },        {            "object_name": "team_user",            "id": "tu_imbrace_agent1",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_imbrace_agent1",            "role": "member",            "state": "join"        },        {            "object_name": "team_user",            "id": "tu_imbraec_agent2",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_imbrace_agent2",            "role": "member",            "state": "join"        }    ]}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid team_id"}
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
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/teams/_add_users' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "team_id": "t_imbrace_default_team",    "reserve_leave": true,    "users": [        {            "user_id": "u_imbrace_agent1",            "role": "member"        },        {            "user_id": "u_imbrace_agent2",            "role": "admin"        },        {            "user_id": "u_imbrace_bot",            "role": "test"        }    ]}'
  ```

## [3. Join Team (for administrators)](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#3-join-team-for-administrators)

Join an existing team as the current user.

This API allows the authenticated user to join a specific team. The user will be added to the team with appropriate permissions based on the team's configuration.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v2/backend/teams/_join_team`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v2/backend/teams/_join_team`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v2/backend/teams/_join_team`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "team_id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9"}
  ```
* **Request Parameters:**

  * `team_id` (string, required): The unique identifier of the team to join
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "team",    "id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9",    "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",    "business_unit_id": "bu_be188361-fbec-4505-9a05-d9d34a5d5961",    "name": "Admin",    "mode": "public",    "icon_url": "",    "description": "",    "is_default": true,    "user_state": "",    "created_at": "2025-06-19T01:39:42.765Z",    "updated_at": "2025-06-19T01:39:42.765Z",    "is_disabled": false,    "is_delete": false,    "team_user_ids": [        "tu_c31be420-ba40-4ab0-ac1e-e1164357f2fa"    ],    "team_users": [        {            "object_name": "team_user",            "id": "tu_c31be420-ba40-4ab0-ac1e-e1164357f2fa",            "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",            "business_unit_id": "bu_be188361-fbec-4505-9a05-d9d34a5d5961",            "team_id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9",            "user_id": "u_09173225-d34e-4f1b-8b80-9e97a608db07",            "role": "admin",            "state": "join"        }    ]}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid team_id"}
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
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/teams/_join_team' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "team_id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9"}'
  ```

## [4. Request to Join Team](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#4-request-to-join-team)

Request to join a specific team (requires team approval).

This API allows users to send a join request to a team. The request will need to be approved by team administrators before the user is added to the team.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v2/backend/teams/{team_id}/join_request`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v2/backend/teams/{team_id}/join_request`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v2/backend/teams/{team_id}/join_request`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `team_id` (string, required): The unique identifier of the team to request joining
* **Request Body:**

  * No request body required
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "message": "Join request submitted successfully"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 4,    "message": "team user existed"}
  ```

  * **Status code: 403 Forbidden**

  ```
  {    "code": 40003,    "message": "super admin no need to join request"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "code": 40004,    "message": "not found team"}
  ```
* **Example:**

  ```
  curl --location --request POST 'https://app-gateway.dev.imbrace.co/v2/backend/teams/t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9/join_request' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [5. Get My Teams](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#5-get-my-teams)

Retrieve all teams that the current user is a member of.

This API allows users to fetch all teams they belong to, including their role within each team. This is useful for displaying team memberships in user interfaces and determining access permissions.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/teams/my`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/teams/my`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/teams/my`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * None
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "_id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9",        "doc_name": "team",        "public_id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9",        "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",        "business_unit_id": "bu_be188361-fbec-4505-9a05-d9d34a5d5961",        "icon_url": "",        "name": "Admin",        "mode": "public",        "description": "",        "is_default": true,        "is_disabled": false,        "created_at": "2025-06-19T01:39:42.765Z",        "updated_at": "2025-06-19T01:39:42.765Z",        "is_delete": false,        "deleted_by": "",        "deleted_at": "",        "role": "admin"    },    {        "_id": "t_imbrace_default_team",        "doc_name": "team",        "public_id": "t_imbrace_default_team",        "organization_id": "org_imbrace",        "business_unit_id": "bu_imbrace_testing",        "icon_url": "",        "name": "General",        "mode": "public",        "description": "Default iMBRACE team, auto create by system for testing purpose",        "is_default": true,        "created_at": "2022-06-22T09:19:58.929Z",        "updated_at": "2023-09-22T05:59:18.581Z",        "is_disabled": false,        "role": "admin"    }]
  ```
* **Empty Result:**

  * **Status code: 200 OK** (when user is not a member of any teams)

  ```
  []
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/teams/my' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [6. Get All Teams](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#6-get-all-teams)

Retrieve all teams within the organization that the user has access to.

This API allows users to fetch all teams in their organization, regardless of whether they are members or not. This is useful for administrative purposes, team discovery, and management interfaces.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/teams/all`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/teams/all`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/teams/all`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * None
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "_id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9",        "doc_name": "team",        "public_id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9",        "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",        "business_unit_id": "bu_be188361-fbec-4505-9a05-d9d34a5d5961",        "icon_url": "",        "name": "Admin",        "mode": "public",        "description": "",        "is_default": true,        "is_disabled": false,        "created_at": "2025-06-19T01:39:42.765Z",        "updated_at": "2025-06-19T01:39:42.765Z",        "is_delete": false,        "deleted_by": "",        "deleted_at": ""    }]
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/teams/all' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [7. Get Teams with Filtering and Pagination](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#7-get-teams-with-filtering-and-pagination)

Retrieve teams with advanced filtering, pagination, and sorting options.

This API allows you to fetch teams with specific filters, pagination controls, and sorting. It's useful for building team management interfaces with search, filtering, and pagination capabilities.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/teams?type=business_unit_id&limit=20&skip=0&sort=-created_at&q=bu_6cc91e00-d704-47e6-a21e-169bc96fe416`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/teams?type=business_unit_id&limit=20&skip=0&sort=-created_at&q=bu_6cc91e00-d704-47e6-a21e-169bc96fe416`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/teams?type=business_unit_id&limit=20&skip=0&sort=-created_at&q=bu_6cc91e00-d704-47e6-a21e-169bc96fe416`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * `type` (string, optional): Filter type (e.g., "business_unit_id")
  * `limit` (number, optional): Number of results per page (default: 20)
  * `skip` (number, optional): Number of results to skip for pagination (default: 0)
  * `sort` (string, optional): Sort field and direction (e.g., "-created_at" for descending)
  * `q` (string, optional): Filter value (e.g., business unit ID)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "list",    "data": [        {            "object_name": "team",            "id": "t_4f81b80b-2c05-4656-a789-a823c109ede2",            "organization_id": "org_ee097eef-0792-4dcc-867b-99fe653b27ec",            "business_unit_id": "bu_6cc91e00-d704-47e6-a21e-169bc96fe416",            "name": "Admin",            "mode": "public",            "icon_url": "",            "description": "",            "is_default": true,            "is_joined": false,            "user_state": "",            "created_at": "2025-02-20T09:13:26.285Z",            "updated_at": "2025-02-20T09:13:26.285Z",            "is_disabled": false,            "is_delete": false,            "members_count": 0,            "admin_count": 0        }    ],    "nested": {},    "has_more": false,    "count": 1,    "total": 1}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/teams?type=business_unit_id&limit=20&skip=0&sort=-created_at&q=bu_6cc91e00-d704-47e6-a21e-169bc96fe416' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [8. Get Team Users with Filtering and Pagination](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#8-get-team-users-with-filtering-and-pagination)

Retrieve team members with advanced filtering, pagination, and detailed user information.

This API allows you to fetch team members with specific filters, pagination controls, and complete user details. It's useful for building team member management interfaces with search, filtering, and detailed user profiles.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/team_users?type=team_id&q=t_imbrace_default_team&limit=20&skip=0`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/team_users?type=team_id&q=t_imbrace_default_team&limit=20&skip=0`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/team_users?type=team_id&q=t_imbrace_default_team&limit=20&skip=0`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * `type` (string, required): Filter type (e.g., "team_id")
  * `q` (string, required): Filter value (e.g., team ID)
  * `limit` (number, optional): Number of results per page (default: 20)
  * `skip` (number, optional): Number of results to skip for pagination (default: 0)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "list",    "data": [        {            "object_name": "team_user",            "id": "tu_2c2f8943-01c4-41fc-90ff-5a427ae416fb",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_09173225-d34e-4f1b-8b80-9e97a608db07",            "role": "admin",            "state": "join",            "user": {                "object_name": "user",                "id": "u_09173225-d34e-4f1b-8b80-9e97a608db07",                "display_name": "TUAN ORG owner",                "avatar_url": "",                "first_name": "agent01@imbrace.co",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "agent01@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2025-06-19T01:39:42.685Z",                "updated_at": "2025-06-19T02:18:44.807Z",                "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",                "role": "owner"            }        },        {            "object_name": "team_user",            "id": "tu_21b9c7b0-a7c0-4e4d-8d75-899229d199b0",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_f7dfc4b2-96bb-4c38-a74a-608bbb22bf9c",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_f7dfc4b2-96bb-4c38-a74a-608bbb22bf9c",                "display_name": "Brendan Lum",                "avatar_url": "",                "first_name": "Brendan",                "last_name": "Lum",                "gender": "",                "area_code": "",                "phone_number": "60125089136",                "language": "en",                "status": "active",                "email": "brendan.lum@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2025-03-27T03:51:26.419Z",                "updated_at": "2025-07-28T04:59:13.258Z",                "organization_id": "org_imbrace",                "role": "admin"            }        },        {            "object_name": "team_user",            "id": "tu_fc2b83f7-c053-498e-9642-da178bda13d7",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_5dee09c7-2b28-466c-a85d-e692b5d88285",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_5dee09c7-2b28-466c-a85d-e692b5d88285",                "display_name": "minh@imbrace.co",                "avatar_url": "",                "first_name": "minh@imbrace.co",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "minh@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2024-11-08T03:15:10.034Z",                "updated_at": "2024-11-08T03:16:29.499Z",                "organization_id": "org_imbrace",                "role": "user"            }        },        {            "object_name": "team_user",            "id": "tu_b7719e49-6135-44ff-a0f8-1230cd7d7e36",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_60af0ad2-e5e2-49c7-8f73-931c6f2e84a4",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_60af0ad2-e5e2-49c7-8f73-931c6f2e84a4",                "display_name": "chiennguyen040396@gmail.com",                "avatar_url": "",                "first_name": "chiennguyen040396@gmail.com",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "chiennguyen040396@gmail.com",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2024-12-15T10:20:46.301Z",                "updated_at": "2025-01-09T08:34:39.907Z",                "organization_id": "org_imbrace",                "role": "user"            }        },        {            "object_name": "team_user",            "id": "tu_b6d12f57-8e49-4372-84c0-1dcb735929c9",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_3415ef91-4b10-402f-bdcf-df2b3f69ad2d",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_3415ef91-4b10-402f-bdcf-df2b3f69ad2d",                "display_name": "cuong.nguyen@imbrace.co",                "avatar_url": "",                "first_name": "cuong.nguyen@imbrace.co",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "cuong.nguyen@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2023-07-20T02:36:19.144Z",                "updated_at": "2024-11-01T09:12:18.011Z",                "organization_id": "org_imbrace",                "role": "owner"            }        },        {            "object_name": "team_user",            "id": "tu_ad0c8cd9-c344-4c7d-941c-6c7e96248c5e",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_1443bf82-2a62-477f-acb2-0bb7ede3c028",            "role": "admin",            "state": "join",            "user": {                "object_name": "user",                "id": "u_1443bf82-2a62-477f-acb2-0bb7ede3c028",                "display_name": "07franco.solis@gmail.com",                "avatar_url": "",                "first_name": "07franco.solis@gmail.com",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "07franco.solis@gmail.com",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2024-09-02T04:05:03.308Z",                "updated_at": "2024-09-02T23:09:24.469Z",                "organization_id": "org_imbrace",                "role": "admin"            }        },        {            "object_name": "team_user",            "id": "tu_imbrace_admin",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_imbrace_admin",            "role": "admin",            "state": "join",            "user": {                "object_name": "user",                "id": "u_imbrace_admin",                "display_name": "imbrace owner",                "avatar_url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/user/org_imbrace/file_QLYwjovSEDrHqlBSRQP1R3aM96.png",                "first_name": "Super",                "last_name": "Man",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "superadmin@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2022-01-04T03:26:24.738Z",                "updated_at": "2024-07-14T08:56:20.323Z",                "organization_id": "org_imbrace",                "role": "owner"            }        },        {            "object_name": "team_user",            "id": "tu_89003b21-c723-4a0f-96c2-83d358044f85",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_7e39d84d-6c36-415d-9b67-8047503578aa",            "role": "admin",            "state": "join",            "user": {                "object_name": "user",                "id": "u_7e39d84d-6c36-415d-9b67-8047503578aa",                "display_name": "michael.wong@imbrace.co",                "avatar_url": "",                "first_name": "michael.wong@imbrace.co",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "michael.wong@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2024-07-25T08:22:30.889Z",                "updated_at": "2025-01-08T08:23:02.505Z",                "organization_id": "org_imbrace",                "role": "admin"            }        },        {            "object_name": "team_user",            "id": "tu_e3d43e3f-852d-47f4-b810-27ca00f6ca85",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_71585462-0af0-4581-a72b-e82141dcb1c2",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_71585462-0af0-4581-a72b-e82141dcb1c2",                "display_name": "khong.ng@imbrace.co",                "avatar_url": "",                "first_name": "khong.ng@imbrace.co",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "khong.ng@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2023-11-21T02:34:48.195Z",                "updated_at": "2024-03-25T09:45:34.703Z",                "organization_id": "org_imbrace",                "role": "admin"            }        },        {            "object_name": "team_user",            "id": "tu_4fdc4974-01cc-4645-9d70-48036233da1b",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_3749c4a9-e538-45f1-b457-be100d0b8637",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_3749c4a9-e538-45f1-b457-be100d0b8637",                "display_name": "sherry.gui@imbrace.co",                "avatar_url": "",                "first_name": "sherry.gui@imbrace.co",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "sherry.gui@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2023-11-01T07:01:34.654Z",                "updated_at": "2024-03-28T09:27:23.335Z",                "organization_id": "org_imbrace",                "role": "admin"            }        },        {            "object_name": "team_user",            "id": "tu_imbrace_agent1",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_imbrace_agent1",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_imbrace_agent1",                "display_name": "imbrace agent 1",                "avatar_url": "",                "first_name": "",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "agent1@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2022-01-04T03:26:24.740Z",                "updated_at": "2022-01-04T03:26:24.740Z",                "organization_id": "org_imbrace",                "role": "user"            }        },        {            "object_name": "team_user",            "id": "tu_imbraec_agent2",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_imbrace_agent2",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_imbrace_agent2",                "display_name": "imbrace agent 2",                "avatar_url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/user/org_imbrace/file_5ACJq6DJlwqYwZbDWpx4OudugQ.jpeg",                "first_name": "",                "last_name": "",                "gender": "m",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "agent2@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2022-01-04T03:26:24.741Z",                "updated_at": "2024-01-05T08:33:39.114Z",                "organization_id": "org_imbrace",                "role": "user"            }        },        {            "object_name": "team_user",            "id": "tu_deaf5d87-8e49-4f8c-8193-ad6013fc7b80",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_000ed63e-e9c1-4d38-be2e-a5b29ef3be18",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_000ed63e-e9c1-4d38-be2e-a5b29ef3be18",                "display_name": "aiman.rahman@imbrace.co",                "avatar_url": "",                "first_name": "aiman.rahman@imbrace.co",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "aiman.rahman@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2023-04-03T08:08:49.560Z",                "updated_at": "2023-04-03T08:08:49.560Z",                "organization_id": "org_imbrace",                "role": "admin"            }        },        {            "object_name": "team_user",            "id": "tu_159f11b2-b117-41b1-b797-44f83a76e503",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_a93ece5a-0515-4fd4-8592-3b92497eb538",            "role": "admin",            "state": "join",            "user": {                "object_name": "user",                "id": "u_a93ece5a-0515-4fd4-8592-3b92497eb538",                "display_name": "queenie.dinh@imbrace.co",                "avatar_url": "",                "first_name": "queenie.dinh@imbrace.co",                "last_name": "Tran",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "queenie.dinh@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2023-06-05T03:52:05.740Z",                "updated_at": "2024-05-02T07:26:30.955Z",                "organization_id": "org_imbrace",                "role": "owner"            }        },        {            "object_name": "team_user",            "id": "tu_a765a251-d3bf-4598-82b1-f2337b97a44e",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_a756160b-c83c-48d0-9da3-b09fd4897381",            "role": "admin",            "state": "join",            "user": {                "object_name": "user",                "id": "u_a756160b-c83c-48d0-9da3-b09fd4897381",                "display_name": "sam.tang@imbrace.co",                "avatar_url": "",                "first_name": "sam.tang@imbrace.co",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "sam.tang@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2023-01-05T15:48:09.504Z",                "updated_at": "2023-01-05T15:48:09.504Z",                "organization_id": "org_imbrace",                "role": "owner"            }        },        {            "object_name": "team_user",            "id": "tu_4cfee84f-8752-462f-9caf-92a658b447ff",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_8c62e71f-1b5c-49d9-9985-ab1728a461fe",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_8c62e71f-1b5c-49d9-9985-ab1728a461fe",                "display_name": "Kennedy",                "avatar_url": "",                "first_name": "Kennedy",                "last_name": "Yu",                "gender": "",                "area_code": "852",                "phone_number": "98765432",                "language": "en",                "status": "active",                "email": "kennedy.yu@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2022-06-07T03:38:06.159Z",                "updated_at": "2024-03-27T03:32:46.360Z",                "organization_id": "org_imbrace",                "role": "admin"            }        },        {            "object_name": "team_user",            "id": "tu_a267a4ea-4109-4c52-8245-0edbd6100a1b",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_5e336d97-e26d-4c6b-9452-36c90bd0769f",            "role": "member",            "state": "join",            "user": {                "object_name": "user",                "id": "u_5e336d97-e26d-4c6b-9452-36c90bd0769f",                "display_name": "Agent02",                "avatar_url": "",                "first_name": "iMBRACE",                "last_name": "Agent02",                "gender": "",                "area_code": "852",                "phone_number": "99999999",                "language": "en",                "status": "active",                "email": "agent02@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2022-06-06T05:08:31.168Z",                "updated_at": "2024-05-07T10:00:39.535Z",                "organization_id": "org_imbrace",                "role": "user"            }        },        {            "object_name": "team_user",            "id": "tu_1b0e7d71-0b81-4dce-9f68-404ed61d6d8b",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",            "role": "admin",            "state": "join",            "user": {                "object_name": "user",                "id": "u_ed1ffffc-73ca-4dc3-85fc-2c7da6c87b7a",                "display_name": "Austina",                "avatar_url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/user/org_imbrace/file_rNB7yin5UFxIUEiBb9cwJwF42S.jpeg",                "first_name": "Austina",                "last_name": "Engelhardt",                "gender": "",                "area_code": "852",                "phone_number": "31198920",                "language": "en",                "status": "active",                "email": "agent01@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2022-06-06T05:08:21.761Z",                "updated_at": "2025-01-15T02:38:26.063Z",                "organization_id": "org_imbrace",                "role": "owner"            }        },        {            "object_name": "team_user",            "id": "tu_a296029c-1096-46ff-98b4-23cebae70c14",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_2a508e6e-09d3-4d65-9825-5e71940d0bcb",            "role": "admin",            "state": "join",            "user": {                "object_name": "user",                "id": "u_2a508e6e-09d3-4d65-9825-5e71940d0bcb",                "display_name": "shin.tu@imbrace.co",                "avatar_url": "",                "first_name": "shin.tu@imbrace.co",                "last_name": "",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "shin.tu@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2022-07-20T03:24:29.396Z",                "updated_at": "2023-08-10T02:40:19.831Z",                "organization_id": "org_imbrace",                "role": "admin"            }        },        {            "object_name": "team_user",            "id": "tu_40864d3b-0550-4760-a27f-8d153c4f3540",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "team_id": "t_imbrace_default_team",            "user_id": "u_imbrace_admin",            "role": "admin",            "state": "join",            "user": {                "object_name": "user",                "id": "u_imbrace_admin",                "display_name": "imbrace owner",                "avatar_url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/user/org_imbrace/file_QLYwjovSEDrHqlBSRQP1R3aM96.png",                "first_name": "Super",                "last_name": "Man",                "gender": "",                "area_code": "",                "phone_number": "",                "language": "en",                "status": "active",                "email": "superadmin@imbrace.co",                "is_bot": false,                "is_active": true,                "is_archived": false,                "is_deleted": false,                "created_at": "2022-01-04T03:26:24.738Z",                "updated_at": "2024-07-14T08:56:20.323Z",                "organization_id": "org_imbrace",                "role": "owner"            }        }    ],    "nested": {        "team": {            "object_name": "team",            "id": "t_imbrace_default_team",            "organization_id": "org_imbrace",            "business_unit_id": "bu_imbrace_testing",            "name": "General",            "mode": "public",            "icon_url": "",            "description": "Default iMBRACE team, auto create by system for testing purpose",            "is_default": true,            "user_state": "",            "created_at": "2022-06-22T09:19:58.929Z",            "updated_at": "2023-09-22T05:59:18.581Z",            "is_disabled": false        }    },    "has_more": true,    "count": 20,    "total": 20}
  ```
* **Error Responses:**

  * **Status code: 403 Forbidden**

  ```
  {    "code": 40003,    "message": "Forbidden, insufficient permission"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/team_users?type=team_id&q=t_imbrace_default_team&limit=20&skip=0' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--data ''
  ```

## [9. Get Team Invite List](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#9-get-team-invite-list)

Retrieve users who can be invited to join a specific team.

This API allows you to fetch a list of users who are eligible to be invited to join a team. This is useful for team management interfaces where you need to show available users for team invitations.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/team_users/_invite_list?type=team_id&team_id=t_imbrace_default_team`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/team_users/_invite_list?type=team_id&team_id=t_imbrace_default_team`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/team_users/_invite_list?type=team_id&team_id=t_imbrace_default_team`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * `type` (string, required): Filter type (e.g., "team_id")
  * `team_id` (string, required): The team ID to get invite list for
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "list",    "data": [        {            "object_name": "user",            "id": "u_myau",            "display_name": "imbrace owner",            "avatar_url": "",            "first_name": "",            "last_name": "",            "gender": "",            "area_code": "",            "phone_number": "",            "language": "en",            "status": "active",            "is_bot": false,            "is_active": true,            "is_archived": false,            "created_at": "2022-05-30T06:20:18.115Z",            "updated_at": "2022-05-30T06:20:18.115Z"        }    ],    "nested": {},    "has_more": false,    "count": 1,    "total": 1}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/team_users/_invite_list?type=team_id&team_id=t_imbrace_default_team' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [10. Get Team Users by Team ID](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#10-get-team-users-by-team-id)

Retrieve all users belonging to a specific team with detailed user information.

This API allows you to fetch all team members for a specific team with complete user profiles. It's useful for displaying team member lists, user directories, and team management interfaces.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/team/{team_id}/users`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/team/{team_id}/users`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/team/{team_id}/users`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `team_id` (string, required): The unique identifier of the team
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "_id": "tu_deaf5d87-8e49-4f8c-8193-ad6013fc7b80",        "role": "member",        "user": {            "_id": "u_000ed63e-e9c1-4d38-be2e-a5b29ef3be18",            "doc_name": "user",            "public_id": "u_000ed63e-e9c1-4d38-be2e-a5b29ef3be18",            "organization_id": "org_imbrace",            "email": "aiman.rahman@imbrace.co",            "role": "admin",            "display_name": "aiman.rahman@imbrace.co",            "avatar_url": "",            "gender": "",            "first_name": "aiman.rahman@imbrace.co",            "last_name": "",            "address_line1": "",            "address_line2": "",            "area_code": "",            "phone_number": "",            "language": "en",            "status": "active",            "is_active": true,            "is_archived": false,            "is_bot": false,            "is_admin": false,            "created_at": "2023-04-03T08:08:49.560Z",            "updated_at": "2023-04-03T08:08:49.560Z",            "_language": "en",            "is_deleted": false        }    }]
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/team/t_imbrace_default_team/users' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [11. Update Team](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#11-update-team)

Update an existing team's information including name, icon, and status.

This API allows you to modify team properties such as name, icon URL, and disabled status. It's useful for team management interfaces where administrators need to update team settings and configurations.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/v2/backend/teams/{team_id}`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/v2/backend/teams/{team_id}`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/v2/backend/teams/{team_id}`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `team_id` (string, required): The unique identifier of the team to update
* **Request Body (JSON)**

  ```
  {    "name": "Grab mode team yoooo",    "icon_url": "123123",    "is_disabled": true}
  ```
* **Request Parameters:**

  * `name` (string, optional): The new name of the team
  * `icon_url` (string, optional): URL of the team icon
  * `is_disabled` (boolean, optional): Whether to disable the team
* **Result:**

  * **Status code: 200 OK** (when successful)

  ```
  {    "object_name": "team",    "id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9",    "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",    "business_unit_id": "bu_be188361-fbec-4505-9a05-d9d34a5d5961",    "name": "Grab mode team yoooo",    "mode": "public",    "icon_url": "123123",    "description": "",    "is_default": true,    "user_state": "",    "created_at": "2025-06-19T01:39:42.765Z",    "updated_at": "2025-06-19T01:39:42.765Z",    "is_disabled": true,    "is_delete": false}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 8,    "message": "is default team, refuse to disabled"}
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
  {    "code": 40004,    "message": "Team not found"}
  ```
* **Example:**

  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/v2/backend/teams/t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "name": "Grab mode team yoooo",    "icon_url": "123123",    "is_disabled": true}'
  ```

## [12. Update User Role in Team](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#12-update-user-role-in-team)

Update a specific user's role within a team.

This API allows you to change a user's role (e.g., from member to admin) within a specific team. It's useful for team management interfaces where administrators need to promote or demote team members.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/v2/backend/teams/{team_id}/user/{user_id}/role`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/v2/backend/teams/{team_id}/user/{user_id}/role`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/v2/backend/teams/{team_id}/user/{user_id}/role`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `team_id` (string, required): The unique identifier of the team
  * `user_id` (string, required): The unique identifier of the user
* **Request Body (JSON)**

  ```
  {    "role": "admin"}
  ```
* **Request Parameters:**

  * `role` (string, required): The new role for the user (e.g., "admin", "member")
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "team_user",    "id": "tu_66e112e0-9811-4896-9cd9-828aa9a8b216",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "team_id": "t_imbrace_team2",    "user_id": "u_imbrace_admin",    "role": "admin",    "state": "join",    "user": {        "object_name": "user",        "id": "u_imbrace_admin",        "display_name": "imbrace owner",        "avatar_url": "https://imbrace-data.s3.ap-east-1.amazonaws.com/user/org_imbrace/file_QLYwjovSEDrHqlBSRQP1R3aM96.png",        "first_name": "Super",        "last_name": "Man",        "gender": "",        "area_code": "",        "phone_number": "",        "language": "en",        "status": "active",        "is_bot": false,        "is_active": true,        "is_archived": false,        "created_at": "2022-01-04T03:26:24.738Z",        "updated_at": "2022-06-20T03:51:08.328Z",        "organization_id": "org_imbrace",        "email": "superadmin@imbrace.co",        "role": "owner"    },    "team": {        "object_name": "team",        "id": "t_imbrace_team2",        "organization_id": "org_imbrace",        "business_unit_id": "bu_imbrace_testing",        "name": "team2",        "mode": "public",        "icon_url": "",        "description": "iMBRACE team 2, auto create by system for testing purpose",        "is_default": false,        "is_pending": false,        "created_at": "2022-05-05T08:28:57.398Z",        "updated_at": "2022-05-05T08:28:57.398Z",        "is_disabled": false    }}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 11,    "message": "is last admin, forbidden"}
  ```

  ```
  {    "code": 3,    "field": "role",    "message": "role format error"}
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
  {    "code": 40004,    "message": "not found team user"}
  ```
* **Example:**

  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/v2/backend/teams/t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9/user/u_09173225-d34e-4f1b-8b80-9e97a608db07/role' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "role": "admin"}'
  ```

## [13. Accept Team Join Request](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#13-accept-team-join-request)

Accept a user's request to join a team.

This API allows team administrators to approve pending join requests from users who have requested to join the team. It's useful for team management workflows where join requests require approval.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v2/backend/teams/{team_id}/user/{user_id}/accept`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v2/backend/teams/{team_id}/user/{user_id}/accept`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v2/backend/teams/{team_id}/user/{user_id}/accept`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body:**

  * No request body required
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "team_user",    "id": "tu_14b0304a-b895-4702-8e61-5d49e32c3503",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "team_id": "t_imbrace_default_team",    "user_id": "u_5e336d97-e26d-4c6b-9452-36c90bd0769f",    "role": "member",    "state": "join",    "user": {        "object_name": "user",        "id": "u_5e336d97-e26d-4c6b-9452-36c90bd0769f",        "display_name": "Agent02",        "avatar_url": "",        "first_name": "iMBRACE",        "last_name": "Agent02",        "gender": "",        "area_code": "852",        "phone_number": "99999999",        "language": "en",        "status": "active",        "is_bot": false,        "is_active": true,        "is_archived": false,        "created_at": "2022-06-06T05:08:31.168Z",        "updated_at": "2023-06-08T09:40:10.730Z",        "organization_id": "org_imbrace",        "email": "agent02@imbrace.co",        "role": "user"    },    "team": {        "object_name": "team",        "id": "t_imbrace_default_team",        "organization_id": "org_imbrace",        "business_unit_id": "bu_imbrace_testing",        "name": "general",        "mode": "public",        "icon_url": "",        "description": "Default iMBRACE team, auto create by system for testing purpose",        "is_default": true,        "created_at": "2022-06-22T09:19:58.929Z",        "updated_at": "2023-06-19T09:47:06.218Z",        "is_disabled": false    }}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 10,    "message": "team user accept"}
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
  {    "code": 40004,    "message": "not found team user"}
  ```
* **Example:**

  ```
  curl --location --request POST 'https://app-gateway.dev.imbrace.co/v2/backend/teams/t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9/user/u_09173225-d34e-4f1b-8b80-9e97a608db07/accept' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [14. Delete Team](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#14-delete-team)

Delete an existing team from the organization.

This API allows you to permanently delete a team and all its associated data. It's useful for team management interfaces where administrators need to remove teams that are no longer needed.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/v2/backend/teams/{team_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/v2/backend/teams/{team_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/v2/backend/teams/{team_id}`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `team_id` (string, required): The unique identifier of the team to delete
* **Request Body:**

  * No request body required
* **Result:**

  * **Status code: 200 OK** (when successful)

  ```
  {    "message": "Team deleted successfully"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 8,    "field": "team",    "message": "is default team, refuse to delete"}
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
  {    "code": 40004,    "field": "team",    "message": "team not found"}
  ```
* **Example:**

  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/v2/backend/teams/t_35d4663e-ace7-4698-9348-dc30d5638c99' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [15. Remove Multiple Users from Team](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#15-remove-multiple-users-from-team)

Remove multiple users from a team in a single operation.

This API allows you to remove multiple users from a team simultaneously. It's useful for team management interfaces where administrators need to perform bulk user removal operations.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v2/backend/teams/_remove_users`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v2/backend/teams/_remove_users`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v2/backend/teams/_remove_users`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "team_id": "t_imbrace_team2",    "user_ids": [        "u_imbrace_agent1",        "u_imbrace_agent2",        "u_imbrace_admin"    ]}
  ```
* **Request Parameters:**

  * `team_id` (string, required): The unique identifier of the team
  * `user_ids` (array, required): Array of user IDs to remove from the team
* **Result:**

  * **Status code: 200 OK** (when successful)

  ```
      {        "object_name": "team",        "id": "t_imbrace_team2",        "organization_id": "org_imbrace",        "business_unit_id": "bu_imbrace_testing",        "name": "team2",        "icon_url": "",        "description": "iMBRACE team 2, auto create by system for testing purpose",        "is_default": false,        "created_at": "2022-04-04T07:04:50.821Z",        "updated_at": "2022-04-04T07:04:50.821Z",        "team_user_ids": [            "tu_imbrace_admin_team2"        ],        "team_users": [            {                "object_name": "team_user",                "id": "tu_imbrace_admin_team2",                "organization_id": "org_imbrace",                "business_unit_id": "bu_imbrace_testing",                "user_id": "u_imbrace_admin",                "role": "admin",                "created_at": "2022-04-04T07:04:50.828Z",                "updated_at": "2022-04-04T07:04:50.828Z",                "user": {                    "object_name": "user",                    "id": "u_imbrace_admin",                    "display_name": "imbrace owner",                    "avatar_url": "",                    "first_name": "",                    "last_name": "",                    "gender": "",                    "area_code": "",                    "phone_number": "",                    "language": "en",                    "is_bot": false,                    "is_active": true,                    "is_archived": false,                    "is_email_verified": false,                    "created_at": "2022-04-04T07:04:50.797Z",                    "updated_at": "2022-04-04T07:04:50.797Z",                    "organization_id": "org_imbrace",                    "email": "admin@imbrace.co",                    "role": "owner"                }            }        ]    }
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 11,    "message": "is last admin, forbidden"}
  ```

  ```
  {    "code": 40000,    "message": "Invalid team_id"}
  ```

  ```
  {    "code": 12,    "message": "is own, forbidden"}
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
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/teams/_remove_users' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "team_id": "t_imbrace_team2",    "user_ids": [        "u_imbrace_agent1",        "u_imbrace_agent2",        "u_imbrace_admin"    ]}'
  ```

## [16. Leave Team](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#16-leave-team)

Allow the current user to leave a team.

This API allows authenticated users to voluntarily leave a team they are currently a member of. It's useful for team management interfaces where users need to remove themselves from teams.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v2/backend/teams/_leave`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v2/backend/teams/_leave`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v2/backend/teams/_leave`
* **Headers:**

  * `Content-Type`: `application/json`
  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Request Body (JSON)**

  ```
  {    "team_id": "t_imbrace_team3"}
  ```
* **Request Parameters:**

  * `team_id` (string, required): The unique identifier of the team to leave
* **Result:**

  * **Status code: 200 OK** (when successful)

  ```
  {    "message": "Successfully left the team"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 11,    "message": "is last admin, forbidden"}
  ```

  ```
  {    "code": 40000,    "message": "You are not in the team"}
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
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/teams/_leave' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--header 'Content-Type: application/json' \--data '{    "team_id": "t_imbrace_team3"}'
  ```

## [17. Approve Team User with Role](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#17-approve-team-user-with-role)

Approve a team user request and assign a specific role.

This API allows team administrators to approve pending team user requests and assign a specific role to the user. It's useful for team management workflows where join requests require approval and role assignment.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v2/backend/teams/{team_id}/user/{team_user_id}/approve`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v2/backend/teams/{team_id}/user/{team_user_id}/approve`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v2/backend/teams/{team_id}/user/{team_user_id}/approve`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `team_id` (string, required): The unique identifier of the team
  * `team_user_id` (string, required): The unique identifier of the team user relationship
* **Request Body (JSON)**

  ```
  {    "role": "admin"}
  ```
* **Request Parameters:**

  * `role` (string, required): The role to assign to the user (e.g., "admin", "member")
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "object_name": "team_user",    "id": "tu_6071c67b-a3de-4e20-8856-e51a1e63d43f",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "team_id": "t_af167c32-ea4f-4c15-bb38-15b97b4223cd",    "user_id": "u_5e336d97-e26d-4c6b-9452-36c90bd0769f",    "role": "admin",    "state": "join",    "user": {        "object_name": "user",        "id": "u_5e336d97-e26d-4c6b-9452-36c90bd0769f",        "display_name": "Agent02",        "avatar_url": "",        "first_name": "iMBRACE",        "last_name": "Agent02",        "gender": "",        "area_code": "852",        "phone_number": "99999999",        "language": "en",        "status": "active",        "is_bot": false,        "is_active": true,        "is_archived": false,        "created_at": "2022-06-06T05:08:31.168Z",        "updated_at": "2023-06-08T09:40:10.730Z",        "organization_id": "org_imbrace",        "email": "agent02@imbrace.co",        "role": "user"    },    "team": {        "object_name": "team",        "id": "t_af167c32-ea4f-4c15-bb38-15b97b4223cd",        "organization_id": "org_imbrace",        "business_unit_id": "bu_imbrace_testing",        "name": "Grab3",        "mode": "grab",        "icon_url": "",        "description": "",        "is_default": false,        "created_at": "2023-06-16T03:10:52.591Z",        "updated_at": "2023-07-03T01:15:38.942Z",        "is_disabled": false    }}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "code": 40000,    "message": "Invalid team_user_id"}
  ```

  ```
  {    "code": 3,    "field": "role",    "message": "role format error"}
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
  {    "code": 40004,    "message": "Team user not found"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v2/backend/teams/t_af167c32-ea4f-4c15-bb38-15b97b4223cd/user/tu_6071c67b-a3de-4e20-8856-e51a1e63d43f/approve' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9' \--data '{    "role": "admin"}'
  ```

## [18. Get All Teams for Assignment](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#18-get-all-teams-for-assignment)

Retrieve all teams available for assignment to a specific conversation.

This API allows you to fetch all teams that can be assigned to a conversation, including their assignment status. It's useful for conversation management interfaces where you need to show available teams for assignment.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/assign/teams/all?conversation_id=conv_d9337f16-b206-4e9a-be6e-accced8e8ecc`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/assign/teams/all?conversation_id=conv_d9337f16-b206-4e9a-be6e-accced8e8ecc`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/assign/teams/all?conversation_id=conv_d9337f16-b206-4e9a-be6e-accced8e8ecc`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Query Parameters:**

  * `conversation_id` (string, required): The unique identifier of the conversation
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "_id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9",        "doc_name": "team",        "public_id": "t_17f35e4f-7fb1-4096-a5cc-e90f9ece4be9",        "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd",        "business_unit_id": "bu_be188361-fbec-4505-9a05-d9d34a5d5961",        "icon_url": "",        "name": "Admin",        "mode": "public",        "description": "",        "is_default": true,        "is_disabled": false,        "created_at": "2025-06-19T01:39:42.765Z",        "updated_at": "2025-06-19T01:39:42.765Z",        "is_delete": false,        "deleted_by": "",        "deleted_at": "",        "isAssign": false    }]
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/assign/teams/all?conversation_id=conv_d9337f16-b206-4e9a-be6e-accced8e8ecc' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [19. Get Team Observers for Conversation](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#19-get-team-observers-for-conversation)

Retrieve all team members who can observe a specific conversation.

This API allows you to fetch all team members who have observer access to a specific conversation. It's useful for conversation management interfaces where you need to show which team members can observe the conversation.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/assign/team/{team_id}/observers?conversation_id=conv_d9337f16-b206-4e9a-be6e-accced8e8ecc`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/assign/team/{team_id}/observers?conversation_id=conv_d9337f16-b206-4e9a-be6e-accced8e8ecc`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/assign/team/{team_id}/observers?conversation_id=conv_d9337f16-b206-4e9a-be6e-accced8e8ecc`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `team_id` (string, required): The unique identifier of the team
* **Query Parameters:**

  * `conversation_id` (string, required): The unique identifier of the conversation
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "_id": "tu_69886bbd-4004-4d46-9cf6-0f7e61442dbe",        "role": "member",        "user": {            "_id": "u_5e336d97-e26d-4c6b-9452-36c90bd0769f",            "doc_name": "user",            "public_id": "u_5e336d97-e26d-4c6b-9452-36c90bd0769f",            "organization_id": "org_imbrace",            "email": "agent02@imbrace.co",            "role": "user",            "display_name": "Agent02",            "avatar_url": "",            "gender": "",            "first_name": "iMBRACE",            "last_name": "Agent02",            "address_line1": "",            "address_line2": "",            "area_code": "852",            "phone_number": "99999999",            "language": "en",            "status": "active",            "is_active": true,            "is_archived": false,            "is_bot": false,            "is_admin": false,            "created_at": "2022-06-06T05:08:31.168Z",            "updated_at": "2024-05-07T10:00:39.535Z",            "_language": "en",            "on_boarded": true,            "is_deleted": false        }    }]
  ```
* **Example:**

  ```
  curl --request GET \--url 'https://app-gateway.dev.imbrace.co/v1/backend/assign/team/t_32c57386-a5fe-40e2-b9c5-b236adbfe1eb/observers?conversation_id=conv_d9337f16-b206-4e9a-be6e-accced8e8ecc' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```

## [20. Get Team Workflows](https://devportal.dev.imbrace.co/docs/api-document/app-apis/team#20-get-team-workflows)

Retrieve all workflows associated with a specific team.

This API allows you to fetch all workflows that are associated with a team, including their active status. It's useful for team management interfaces where you need to show which workflows are available for the team.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/teams/{team_id}/workflows`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/teams/{team_id}/workflows`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/teams/{team_id}/workflows`
* **Headers:**

  * `X-Access-Token`:
    **Your Access Token****Your Access Token**
* **Path Parameters:**

  * `team_id` (string, required): The unique identifier of the team
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "id": "755",        "name": "My workflow 45",        "active": false    },    {        "id": "1019",        "name": "WhatsApp 852 5372 0898 - Default workflow",        "active": true    },    {        "id": "972",        "name": "Sam",        "active": true    }]
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/teams/t_imbrace_team3/workflows' \--header 'X-Access-Token: acc_7c769464-4577-49da-abc4-b27b3866fcb9'
  ```
