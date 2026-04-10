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
