[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Server Gateway](https://devportal.dev.imbrace.co/docs/api-document/server-gateways)

# Channel Server APIs

Channel Server APIs provide functionality to manage and retrieve channel information across different communication platforms. These APIs allow you to access channel configurations, settings, and metadata for various channel types including web, email, WhatsApp, and more.

---

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/channelserver#overview)

The Channel Server APIs enable you to retrieve and manage channel configurations within your organization. Channels represent different communication platforms and their associated settings, including visual customization, bot configurations, and welcome messages.

---

## [1. Get Channel by ID](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/channelserver#1-get-channel-by-id)

Retrieve detailed information about a specific channel including its configuration, settings, and metadata.

This API allows you to fetch complete channel details by providing the channel ID. It returns comprehensive information about the channel including type, colors, bot settings, email configurations, and more.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/channels/{channel_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/channels/{channel_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/channels/{channel_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `channel_id` (string, required): The unique identifier of the channel
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "_id": "ch_c18b8867-5e88-469b-a17c-ba332231c931",    "doc_name": "channel",    "public_id": "ch_c18b8867-5e88-469b-a17c-ba332231c931",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "welcome_message_id": "",    "bot_id": "u_imbrace_bot",    "type": "web",    "name": "Test if bot added",    "icon_url": "",    "primary_color": "#d316f2",    "secondary_color": "#7f748f",    "description": "",    "is_disabled": false,    "welcome_message": "",    "fallback_url": "https://app.prod.imbrace.co/channels/web_widget",    "created_at": "2022-09-06T06:31:08.223Z",    "updated_at": "2022-09-06T06:31:08.223Z",    "active": true,    "config": {        "email_config": {            "email": null,            "subject_title": null,            "profile_name": null,            "action_button_text": null,            "button_url": null,            "e_signature_name": null,            "e_signature_information": null,            "e_signature_logo": null,            "show_powered_by": false,            "legal_disclaimer": null        },        "type": "web",        "window_name": null,        "window_logo": null,        "chatbot_name": null,        "chatbot_avatar": null,        "welcome_message": null,        "primary_color": null,        "secondary_color": null,        "_id": "6613adb609763afdf1b7f419"    },    "is_deleted": true,    "is_init": true,    "id": "ch_c18b8867-5e88-469b-a17c-ba332231c931"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "channel id is required"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "no channel found with id :channel_id"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/channels/ch_0a0eeedd-5581-4549-9b35-7a5e003fce2f' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```

---

## [2. Get Channel by Organization and Channel ID](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/channelserver#2-get-channel-by-organization-and-channel-id)

Retrieve detailed information about a specific channel within an organization.

This API allows you to fetch complete channel details by providing both the organization ID and channel ID. It returns the same comprehensive information as API #1 but with organization-specific context.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/organization/{organization_id}/channels/{channel_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/channels/{channel_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/channels/{channel_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `channel_id` (string, required): The unique identifier of the channel
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "_id": "ch_c18b8867-5e88-469b-a17c-ba332231c931",    "doc_name": "channel",    "public_id": "ch_c18b8867-5e88-469b-a17c-ba332231c931",    "organization_id": "org_imbrace",    "business_unit_id": "bu_imbrace_testing",    "welcome_message_id": "",    "bot_id": "u_imbrace_bot",    "type": "web",    "name": "Test if bot added",    "icon_url": "",    "primary_color": "#d316f2",    "secondary_color": "#7f748f",    "description": "",    "is_disabled": false,    "welcome_message": "",    "fallback_url": "https://app.prod.imbrace.co/channels/web_widget",    "created_at": "2022-09-06T06:31:08.223Z",    "updated_at": "2022-09-06T06:31:08.223Z",    "active": true,    "config": {        "email_config": {            "email": null,            "subject_title": null,            "profile_name": null,            "action_button_text": null,            "button_url": null,            "e_signature_name": null,            "e_signature_information": null,            "e_signature_logo": null,            "show_powered_by": false,            "legal_disclaimer": null        },        "type": "web",        "window_name": null,        "window_logo": null,        "chatbot_name": null,        "chatbot_avatar": null,        "welcome_message": null,        "primary_color": null,        "secondary_color": null,        "_id": "6613adb609763afdf1b7f419"    },    "is_deleted": true,    "is_init": true,    "id": "ch_c18b8867-5e88-469b-a17c-ba332231c931"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "channel id is required"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "no channel found with id :channel_id"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/organization/org_imbrace/channels/ch_0a0eeedd-5581-4549-9b35-7a5e003fce2f' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```
