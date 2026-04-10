[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Server Gateway](https://devportal.dev.imbrace.co/docs/api-document/server-gateways)

# Marketplace APIs

Marketplace APIs provide functionality to access and manage marketplace resources including email templates, message templates, and other shared assets within your organization.

---

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/marketplace#overview)

The Marketplace APIs enable you to retrieve and manage marketplace resources within your organization. These APIs provide access to various templates and assets that can be used across your organization, including email templates with customizable content, subjects, and attachments.

---

## [1. Get Email Template by ID](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/marketplace#1-get-email-template-by-id)

Retrieve detailed information about a specific email template from the marketplace.

This API allows you to fetch complete email template details by providing the organization ID and template ID. It returns comprehensive information about the template including name, subject, body content, status, and attachments.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/organization/{organization_id}/marketplaces/email-templates/{template_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/organization/{organization_id}/marketplaces/email-templates/{template_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/organization/{organization_id}/marketplaces/email-templates/{template_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
  * `template_id` (string, required): The unique identifier of the email template (format: `ema_*`)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "data": {        "_id": "ema_c8262ca3-fdd7-42b7-b8da-46f7df76fcc3",        "doc_name": "EmailTemplate",        "name": "All Subscribers",        "subject": "All Subscribers",        "body": "<p>All Subscribers</p>",        "status": "draft",        "organization_id": "org_ef3c3d5e-c1cf-49b4-8113-6d9196ec33dc",        "attachments": [],        "app_id": "app_cc2c15a5-1e22-4252-85a0-b390fc90597e",        "links": [],        "public_id": "ema_c8262ca3-fdd7-42b7-b8da-46f7df76fcc3",        "created_at": "2024-02-02T02:38:51.234Z",        "updated_at": "2024-07-23T04:34:30.313Z"    }}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "template id is required"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "no email template found with id :template_id"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/organization/org_ef3c3d5e-c1cf-49b4-8113-6d9196ec33dc/marketplaces/email-templates/ema_c8262ca3-fdd7-42b7-b8da-46f7df76fcc3' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```
