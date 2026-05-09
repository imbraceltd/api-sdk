# Getting an API Key

An API key (`api_...`) lets your backend call Imbrace without user sessions. For when to use an API key versus an access token, see [Authentication](/sdk/authentication/).

---

## Option 1 â€” Imbrace Portal (recommended)

1. Log in to the Imbrace Portal.
2. Go to **Settings â†’ API Keys**.
3. Click **Create** and give the key a name.
4. Copy the `api_...` value â€” it is only shown once.

---

## Option 2 â€” SDK (programmatic)

Use this when you need to generate a key from code, for example during automated provisioning. You must be authenticated with an access token first (via [OTP](/sdk/authentication/#otp-login-flow) or [password](/sdk/authentication/#password-login)).

    ```typescript
    // Requires client initialized with an access token
    const res = await client.auth.getThirdPartyToken(30) // expires in 30 days
    const apiKey = res.apiKey.apiKey  // "api_..."
    ```
    ```python
    # Requires client initialized with an access token
    res = client.auth.get_third_party_token(expiration_days=30)
    api_key = res["apiKey"]["apiKey"]  # "api_..."
    ```

The response shape:

```json
{
  "apiKey": {
    "apiKey": "api_...",
    "expired_at": "2025-08-01T00:00:00.000Z",
    "is_active": true
  },
  "expires_in": 2592000
}
```

---

## Using the key

Pass the key to the client constructor:

    ```typescript
    import { ImbraceClient } from "@imbrace/sdk";

    const client = new ImbraceClient({
      apiKey: process.env.IMBRACE_API_KEY!,
      baseUrl: "https://app-gatewayv2.imbrace.co",
    });
    ```
    ```python
    import os
    from imbrace import ImbraceClient

    client = ImbraceClient(api_key=os.environ["IMBRACE_API_KEY"])
    ```