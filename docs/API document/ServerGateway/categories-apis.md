[API Documents](https://devportal.dev.imbrace.co/docs/api-document)/[Server Gateway](https://devportal.dev.imbrace.co/docs/api-document/server-gateways)

# Categories APIs

Categories APIs provide functionality to retrieve and manage categories within your organization. These APIs allow you to access category information and configurations.

---

## [Overview](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/categories#overview)

The Categories APIs enable you to retrieve category information within your organization. Categories help organize and classify various resources and data within the system.

---

## [1. Get Categories by Organization](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/categories#1-get-categories-by-organization)

Retrieve all categories associated with a specific organization.

This API allows you to fetch all categories for an organization by providing the organization ID as a query parameter. It returns a list of categories with their details and configurations.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/categories?organization_id={organization_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/categories?organization_id={organization_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/categories?organization_id={organization_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Query Parameters:**

  * `organization_id` (string, required): The unique identifier of the organization
* **Result:**

  * **Status code: 200 OK**

  ```
  [    {        "_id": "cat_17116811-71d3-48d5-819c-9b5ae1ad9aa1",        "doc_name": "category",        "name": "OnlyForMessages",        "apply_to": [            "email_templates",            "message_template"        ],        "is_default": false,        "organization_id": "org_imbrace",        "is_deleted": false,        "public_id": "cat_17116811-71d3-48d5-819c-9b5ae1ad9aa1",        "created_at": "2025-10-28T08:52:30.683Z",        "id": "cat_17116811-71d3-48d5-819c-9b5ae1ad9aa1"    },    {        "_id": "cat_67250f22-1555-4d96-8853-f96f35395ed5",        "doc_name": "category",        "name": "new category from msg temp",        "description": "new category from msg temp",        "apply_to": [],        "is_default": false,        "organization_id": "org_imbrace",        "is_deleted": false,        "public_id": "cat_67250f22-1555-4d96-8853-f96f35395ed5",        "created_at": "2024-08-09T03:08:17.175Z",        "id": "cat_67250f22-1555-4d96-8853-f96f35395ed5"    },    {        "_id": "cat_af8c8843-9ccc-4819-9a5e-a01183d8e8b2",        "doc_name": "category",        "name": "new category",        "description": "new category",        "apply_to": [],        "is_default": false,        "organization_id": "org_imbrace",        "is_deleted": false,        "public_id": "cat_af8c8843-9ccc-4819-9a5e-a01183d8e8b2",        "created_at": "2024-08-09T03:06:17.645Z",        "id": "cat_af8c8843-9ccc-4819-9a5e-a01183d8e8b2"    },    {        "_id": "cat_3a07820c-5d4b-457c-8742-a5b13331f9e9",        "doc_name": "category",        "name": "new cat cat",        "description": "",        "apply_to": [],        "is_default": false,        "organization_id": "org_imbrace",        "is_deleted": false,        "public_id": "cat_3a07820c-5d4b-457c-8742-a5b13331f9e9",        "created_at": "2024-07-17T07:35:44.602Z",        "id": "cat_3a07820c-5d4b-457c-8742-a5b13331f9e9"    }]
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "organization_id is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "Organization not found"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/categories?organization_id=org_imbrace' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```

---

## [2. Get Category by ID](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/categories#2-get-category-by-id)

Retrieve detailed information about a specific category.

This API allows you to fetch complete category details by providing the category ID. It returns comprehensive information about the category including name, description, applicable resources, and default status.

* **Endpoint for Product:** `GET https://app-gateway.imbrace.co/3rd/categories/{category_id}`
* **Endpoint for Demo:** `GET https://app-gateway.demo.imbrace.co/3rd/categories/{category_id}`
* **Endpoint for Dev:** `GET https://app-gateway.dev.imbrace.co/3rd/categories/{category_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `category_id` (string, required): The unique identifier of the category (format: `cat_*`)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "_id": "cat_imbrace_sales",    "doc_name": "category",    "apply_to": [],    "is_default": true,    "is_deleted": false,    "organization_id": "default",    "name": "Sales",    "description": "Sales",    "public_id": "cat_imbrace_sales",    "created_at": "2024-07-17T06:29:11.263Z",    "id": "cat_imbrace_sales"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "category id is required"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "no category found with id :category_id"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/categories/cat_imbrace_sales' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```

---

## [3. Create Category](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/categories#3-create-category)

Create a new category within an organization.

This API allows you to create a new category by providing the category name and the resource types it applies to. The category will be created within the specified organization.

* **Endpoint for Product:** `POST https://app-gateway.imbrace.co/3rd/categories`
* **Endpoint for Demo:** `POST https://app-gateway.demo.imbrace.co/3rd/categories`
* **Endpoint for Dev:** `POST https://app-gateway.dev.imbrace.co/3rd/categories`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
  * `organization_id`: The unique identifier of the organization
  * `Content-Type`: `application/json`
* **Body:**

  ```
  {    "apply_to": ["message_templates"],    "name": "OnlyForMessages1"}
  ```
* **Body Parameters:**

  * `name` (string, required): The name of the category
  * `apply_to` (array, optional): List of resource types this category applies to (e.g., "message_templates", "email_templates")
  * `description` (string, optional): Description of the category
* **Result:**

  * **Status code: 201 Created**

  ```
  {    "doc_name": "category",    "name": "OnlyForMessages1",    "apply_to": [        "message_templates"    ],    "is_default": false,    "organization_id": "org_imbrace",    "is_deleted": false,    "_id": "cat_a0952e63-73a5-4e26-b4da-33c43b8b0ab0",    "public_id": "cat_a0952e63-73a5-4e26-b4da-33c43b8b0ab0",    "created_at": "2025-10-29T01:39:59.144Z",    "id": "cat_a0952e63-73a5-4e26-b4da-33c43b8b0ab0"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "name is required"}
  ```

  ```
  {    "message": "organization_id header is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 409 Conflict**

  ```
  {    "message": "Category with this name already exists"}
  ```
* **Example:**

  ```
  curl --location 'https://app-gateway.dev.imbrace.co/3rd/categories' \--header 'organization_id: org_imbrace' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1' \--header 'Content-Type: application/json' \--data '{    "apply_to": ["message_templates"],    "name": "OnlyForMessages1"}'
  ```

---

## [4. Update Category](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/categories#4-update-category)

Update an existing category's information.

This API allows you to update a category by providing the category ID and the fields you want to modify. You can update the category name, description, and the resource types it applies to.

* **Endpoint for Product:** `PUT https://app-gateway.imbrace.co/3rd/categories/{category_id}`
* **Endpoint for Demo:** `PUT https://app-gateway.demo.imbrace.co/3rd/categories/{category_id}`
* **Endpoint for Dev:** `PUT https://app-gateway.dev.imbrace.co/3rd/categories/{category_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
  * `organization_id`: The unique identifier of the organization
  * `Content-Type`: `application/json`
* **Path Parameters:**

  * `category_id` (string, required): The unique identifier of the category (format: `cat_*`)
* **Body:**

  ```
  {    "apply_to": ["email_templates", "message_template"]}
  ```
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "_id": "cat_17116811-71d3-48d5-819c-9b5ae1ad9aa1",    "doc_name": "category",    "name": "OnlyForMessages",    "apply_to": [        "email_templates",        "message_template"    ],    "is_default": false,    "organization_id": "org_imbrace",    "is_deleted": false,    "public_id": "cat_17116811-71d3-48d5-819c-9b5ae1ad9aa1",    "created_at": "2025-10-28T08:52:30.683Z",    "id": "cat_17116811-71d3-48d5-819c-9b5ae1ad9aa1"}
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "category id is required"}
  ```

  ```
  {    "message": "organization_id header is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "no category found with id :category_id"}
  ```

  * **Status code: 409 Conflict**

  ```
  {    "message": "Category with this name already exists"}
  ```
* **Example:**

  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/3rd/categories/cat_17116811-71d3-48d5-819c-9b5ae1ad9aa1' \--header 'organization_id: org_imbrace' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1' \--header 'Content-Type: application/json' \--data '{    "apply_to": ["email_templates", "message_template"]}'
  ```

---

## [5. Delete Category](https://devportal.dev.imbrace.co/docs/api-document/server-gateways/categories#5-delete-category)

Delete a specific category by its ID.

This API allows you to delete a category by providing the category ID. Once deleted, the category will be marked as deleted in the system.

* **Endpoint for Product:** `DELETE https://app-gateway.imbrace.co/3rd/categories/{category_id}`
* **Endpoint for Demo:** `DELETE https://app-gateway.demo.imbrace.co/3rd/categories/{category_id}`
* **Endpoint for Dev:** `DELETE https://app-gateway.dev.imbrace.co/3rd/categories/{category_id}`
* **Headers:**

  * `x-access-token`: `Contact to iMBRACE`
* **Path Parameters:**

  * `category_id` (string, required): The unique identifier of the category (format: `cat_*`)
* **Result:**

  * **Status code: 200 OK**

  ```
  {    "message": "Category deleted successfully"}
  ```

  * **Status code: 204 No Content**

  ```
  (No response body)
  ```
* **Error Responses:**

  * **Status code: 400 Bad Request**

  ```
  {    "message": "category id is required"}
  ```

  * **Status code: 401 Unauthorized**

  ```
  {    "message": "Unauthorized"}
  ```

  * **Status code: 404 Not Found**

  ```
  {    "message": "no category found with id :category_id"}
  ```

  * **Status code: 403 Forbidden**

  ```
  {    "message": "Cannot delete default category"}
  ```
* **Example:**

  ```
  curl --location --request DELETE 'https://app-gateway.dev.imbrace.co/3rd/categories/cat_17116811-71d3-48d5-819c-9b5ae1ad9aa1' \--header 'x-access-token: api_2f576a7d-f7eb-4748-9ec0-b295d7204de1'
  ```
