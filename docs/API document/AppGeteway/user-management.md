# User management

Manage user authentication seamlessly with our OTP-based login system. These APIs allow users to log in securely using their email and a one-time password (OTP) without the need for traditional passwords. Learn how to integrate this simple and secure login flow into your application.

## [Login](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_userManagement#login)

Login with Email and OTP

### [1. Signin Email request](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_userManagement#1-signin-email-request)

This endpoint allows you to send a request to generate a One-Time Password (OTP) and send it to the provided email address. The user will need this OTP to authenticate.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/login/_signin_email_request`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/login/_signin_email_request`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/login/_signin_email_request`
* **Headers:**

  * `Content-Type`: `application/json`
* **Body:**

  ```
  {    "email": "example@gmail.com"}
  ```
* **Result:**

  * **Status code: 201 Created** - Indicates that the OTP has been successfully sent to the provided email.
  * **Status code: 400 Bad Request** – Occurs when the OTP generation limit has been exceeded, instructing the user to try again after a certain period.

  ```
  {"code": 40010,"message": "Generate otp over limit, please try again after 3 hours"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.imbrace.co/v1/login/_signin_email_request' \--header 'Content-Type: application/json' \--data-raw '{    "email": "vani.hoang@imbrace.co"}'
  ```

**Note:** OTPs are sent in limited quantities to prevent abuse. If a user exceeds the allowed limit, they will need to wait for a cooldown period

### [2. Signin with Email](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_userManagement#2-signin-with-email)

This endpoint verifies the OTP entered by the user for authentication. Once the user provides the OTP, it will be validated to grant access.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/login/_signin_with_email`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/login/_signin_with_email`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/login/_signin_with_email`
* **Headers:**

  * `Content-Type`: `application/json`
* **Body:**

  ```
  {    "email": "example@gmail.com",    "otp":"123456"}
  ```
* **Result:**

  * **Status code: 200 OK** – The OTP is valid, and the user is successfully authenticated. A login token is returned to the user.

  ```
  {"object_name": "login_access","id": "login_acc_example","token": "login_acc_example","email": "example@gmail.com","expired_at": "2025-09-04T04:45:11.723Z"}
  ```

  * **Status code: 400 Bad Request** – Occurs when the OTP provided by the user is invalid or expired.

  ```
  {"code": 40000,"message": "Invalid OTP"}
  ```
* **Example:**

  ```
  {curl --location 'https://app-gateway.imbrace.co/v1/login/_signin_with_email' \--header 'Content-Type: application/json' \--data-raw '{    "email": "example@gmail.com",    "otp":"123456"    }'}
  ```

**Note:** Once the OTP is successfully verified, the user is issued a token that can be used for further requests. The token will expire at the specified time (expired_at).

### [3. Get organization list](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_userManagement#3-get-organization-list)

This endpoint retrieves a list of organizations associated with the authenticated user. The user must provide a valid authentication token in the request header.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v2/backend/organizations?limit=10&skip=0`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v2/backend/organizations?limit=10&skip=0`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v2/backend/organizations?limit=10&skip=0`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`: `login_acc_example`
* **Result:**

  * **Status code: 200 OK** – The request is successful, and a list of organizations is returned.

  ```
  {
  "object_name": "list",
  "data": [
      {
          "object_name": "organization",
          "id": "org_example",
          "name": "Ẽxample Organization",
          "created_at": "2025-06-19T01:39:42.667Z",
          "updated_at": null,
      },
      {
          "object_name": "organization",
          "id": "org_example2",
          "name": "Example Organization 2",
          "created_at": "2025-06-19T01:39:42.667Z",
          "updated_at": null,
      }
  ],
      "nested": {},
      "has_more": false,
      "count": 1,
      "total": 1
  }{
  "object_name": "list",
  "data": [
      {
          "object_name": "organization",
          "id": "org_example",
          "name": "Ẽxample Organization",
          "created_at": "2025-06-19T01:39:42.667Z",
          "updated_at": null,
      },
      {
          "object_name": "organization",
          "id": "org_example2",
          "name": "Example Organization 2",
          "created_at": "2025-06-19T01:39:42.667Z",
          "updated_at": null,
      }
  ],
      "nested": {},
      "has_more": false,
      "count": 1,
      "total": 1
  }
  ```
* **Example:**

```
  curl --location 'https://app-gateway.imbrace.co/v1/backend/organizations' \--header 'Content-Type: application/json' \--header 'x-access-token: login_acc_example'
```

* **Note:** Ensure that the `x-access-token` header contains a valid token that starts with `login_acc_` obtained from the login process. If the token is invalid or expired, the request will fail with an appropriate error message.

### [4. Select organization (exchange access token)](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_userManagement#4-select-organization-exchange-access-token)

This endpoint exchanges the provided organization_id to select an organization and obtain a new access token tied to it.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/v1/backend/access/_exchange_access_token`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/v1/backend/access/_exchange_access_token`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/v1/backend/access/_exchange_access_token`
* **Headers:**
  * `Content-Type`: `application/json`
  * `x-access-token`: `login_acc_example`
* **Body:**

```
  {    "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd"}
```

* **Result:**

  * **Status code: 200 OK**

  ```
  {
      "object_name": "access",
      "id": "acc_a6ee0975-1fc7-463b-9d9c-504ae1d1203e",
      "token": "acc_a6ee0975-1fc7-463b-9d9c-504ae1d1203e",
      "refresh_token": "rtk_52a799d5-3522-4c4b-b9a6-a6c19dbcb29c",
      "user_id": "u_09173225-d34e-4f1b-8b80-9e97a608db07",
      "expired_at": "2025-10-17T03:04:58.473Z",
      "created_at": "2025-09-17T03:04:58.473Z",
      "updated_at": "2025-09-17T03:04:58.473Z",
      "creator": {
          "object_name": "user",
          "id": "u_09173225-d34e-4f1b-8b80-9e97a608db07",
          "display_name": "org owner",
          "avatar_url": "",
          "first_name": "agent01@imbrace.co",
          "last_name": "",
          "gender": "",
          "area_code": "",
          "phone_number": "",
          "language": "en",
          "status": "active",
          "email": "agent01@imbrace.co",
          "is_bot": false,
          "is_active": true,
          "is_archived": false,
          "is_deleted": false,
          "created_at": "2025-06-19T01:39:42.685Z",
          "updated_at": "2025-06-19T02:18:44.807Z"
      }
  }
  ```
* **Example:**

```
  curl --location 'https://app-gateway.dev.imbrace.co/v1/backend/access/_exchange_access_token' \--header 'x-access-token: login_acc_13ef66e6-c23e-428e-92f5-6bfcc0cb1658' \--header 'Content-Type: application/json' \--data '{    "organization_id": "org_e7e8fdb5-39a9-4599-80db-79ae6ff619fd"}'
```

* **Note:** Ensure that the `x-access-token` header contains a valid token that starts with `login_acc_` obtained from the login process. If the token is invalid or expired, the request will fail with an appropriate error message.

### [5. Get account info](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_userManagement#5-get-account-info)

This endpoint retrieves the account information of the authenticated user. The user must provide a valid authentication token in the request header.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/v1/backend/account`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/v1/backend/account`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/v1/backend/account`
* **Headers:**

  * `Content-Type`: `application/json`
  * `x-access-token`:
    **Your Access Token****Your Access Token**
* **Result:**

  * **Status code: 200 OK** – The request is successful, and the account information is returned.

  ```
  {
      "object_name": "account",
      "id": "u_imbrace_admin",
      "organization_id": "org_imbrace",
      "display_name": "imbrace owner",
      "avatar_url": "",
      "gender": "",
      "first_name": "",
      "last_name": "",
      "address_line1": "",
      "address_line2": "",
      "area_code": "",
      "phone_number": "",
      "email": "admin@imbrace.co",
      "language": "en",
      "role": "owner",
      "status": "active",
      "is_active": true,
      "is_archived": false,
      "created_at": "2022-05-20T07:30:41.296Z",
      "updated_at": "2022-05-20T07:30:41.296Z",
      "team_roles": [
          {
              "object_name": "team_user",
              "id": "tu_imbrace_admin",
              "organization_id": "org_imbrace",
              "business_unit_id": "bu_imbrace_testing",
              "team_id": "t_imbrace_default_team",
              "user_id": "u_imbrace_admin",
              "role": "admin",
              "team": {
                  "object_name": "team",
                  "id": "t_imbrace_default_team",
                  "organization_id": "org_imbrace",
                  "business_unit_id": "bu_imbrace_testing",
                  "name": "general",
                  "mode": "public",
                  "icon_url": "",
                  "description": "Default iMBRACE team, auto create by system for testing purpose",
                  "is_default": true,
                  "created_at": "2022-05-20T07:30:41.317Z",
                  "updated_at": "2022-05-20T07:30:41.317Z"
              }
          },
          {
              "object_name": "team_user",
              "id": "tu_imbrace_admin_team2",
              "organization_id": "org_imbrace",
              "business_unit_id": "bu_imbrace_testing",
              "team_id": "t_imbrace_team2",
              "user_id": "u_imbrace_admin",
              "role": "admin",
              "team": {
                  "object_name": "team",
                  "id": "t_imbrace_team2",
                  "organization_id": "org_imbrace",
                  "business_unit_id": "bu_imbrace_testing",
                  "name": "team2",
                  "mode": "public",
                  "icon_url": "",
                  "description": "iMBRACE team 2, auto create by system for testing purpose",
                  "is_default": false,
                  "created_at": "2022-05-20T07:30:41.317Z",
                  "updated_at": "2022-05-20T07:30:41.317Z"
              }
          },
          {
              "object_name": "team_user",
              "id": "tu_imbrace_admin_team3",
              "organization_id": "org_imbrace",
              "business_unit_id": "bu_imbrace_testing",
              "team_id": "t_imbrace_team3",
              "user_id": "u_imbrace_admin",
              "role": "admin",
              "team": {
                  "object_name": "team",
                  "id": "t_imbrace_team3",
                  "organization_id": "org_imbrace",
                  "business_unit_id": "bu_imbrace_testing",
                  "name": "Grab mode team",
                  "mode": "grab",
                  "icon_url": "",
                  "description": "iMBRACE team 3, auto create by system for testing purpose",
                  "is_default": false,
                  "created_at": "2022-05-20T07:30:41.317Z",
                  "updated_at": "2022-05-20T07:30:41.317Z"
              }
          }
      ]
  }
  ```
* **Example:**

```
  curl --location 'https://app-gateway.imbrace.co/v1/account' \--header 'Content-Type: application/json' \--header 'x-access-token: acc_token_example'
```

* **Note:** Ensure that the `x-access-token` header contains a valid token that starts with `acc_` obtained from the login process. If the token is invalid or expired, the request will fail with an appropriate error message.

### [Additional Notes for Developers](https://devportal.dev.imbrace.co/docs/api-document/app-apis/_userManagement#additional-notes-for-developers)

* The OTP sent to the user will expire after a short period (15 minutes). If the OTP expires, the user will need to request a new one.
* The expired_at field in the successful response indicates the expiration time of the authentication token.
* Make sure to handle the "Invalid OTP" error gracefully on the front end, prompting users to retry with the correct OTP.
