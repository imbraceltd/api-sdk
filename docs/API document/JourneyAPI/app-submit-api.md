# App Submit API

API to submit application information, which may be related to registration or status updates.

## [7. App Submit](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/submitApp#7-app-submit)

Submit application information, which may be related to registration or status updates.

* **Endpoint:** `POST https://app-gateway.dev.imbrace.co/journeys/v2/apps/submit/{app_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "name": "marketing grgdf",  "apply_to": "email-template",  "app_id": "app_fede1969-6ac9-4149-b76c-1800c9242d7b"}
  ```
* **Example:**
  ```
  curl --location 'https://app-gateway.dev.imbrace.co/journeys/v1/board' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{    "name": "marketing grgdf",    "apply_to": "email-template",    "app_id": "app_fede1969-6ac9-4149-b76c-1800c9242d7b"}'
  ```


# Update App Settings API

API to update settings for a specific application.

## [6. Update App Setting](https://devportal.dev.imbrace.co/docs/api-document/journeyAPIReference/updateAppSetting#6-update-app-setting)

Update settings for a specific application (app).

* **Endpoint:** `PUT https://app-gateway.dev.imbrace.co/journeys/v2/apps/settings/{app_id}`
* **Headers:**
  * `x-temp-token`:
    **Your token**
  * `Content-Type`: `application/json`
* **Body:**
  ```
  {  "channel": {    "id": "860",    "name": "Telegram Api 01",    "channel_type": "telegramApi"  },  "options": {    "interaction": {      "type": "IFRAME",      "data": {        "type": "telegram_outbound",        "url": "https://wcs.dev.imbrace.co/app/telegram-outbound/send"      }    },    "sendMessage": true  },  "user_progress": {    "steps": 1,    "finished": true  }}
  ```
* **Example:**
  ```
  curl --location --request PUT 'https://app-gateway.dev.imbrace.co/journeys/v2/apps/settings/app_7674022f-4a51-42e7-a321-63627fa1cd66' \--header 'x-temp-token: api_2d599e6d-2694-4389-b585-1d5a2a5ec8c1' \--header 'Content-Type: application/json' \--data '{    "channel": {      "id": "860",      "name": "Telegram Api 01",      "channel_type": "telegramApi"    },    "options": {      "interaction": {        "type": "IFRAME",        "data": {          "type": "telegram_outbound",          "url": "https://wcs.dev.imbrace.co/app/telegram-outbound/send"        }      },      "sendMessage": true    },    "user_progress": {      "steps": 1,      "finished": true    }}'
  ```
