PS D:\HUANGJUNFENG\sdk\ts> npm test

> @imbrace/sdk@1.0.0 test
> vitest run

 RUN  v1.6.1 D:/HUANGJUNFENG/sdk/ts

stderr | src/__tests__/integration.test.ts
IMBRACE_API_KEY not set — skipping integration tests

 ✓ src/__tests__/auth.test.ts (4)
 ✓ src/__tests__/errors.test.ts (6)
 ✓ src/__tests__/resources/settings.test.ts (8)
 ✓ src/__tests__/resources/account.test.ts (2)
 ✓ src/__tests__/resources/agent.test.ts (6)
 ❯ src/__tests__/http.test.ts (9)
   ❯ HttpTransport (9)
     × sets X-Api-Key header when apiKey provided
     × sets Authorization header when token set
     ✓ does not set Authorization header when no token
     ✓ throws AuthError on 401
     ✓ throws AuthError on 403
     ✓ throws ApiError on 404
     ✓ retries on 500 and throws after max retries
     ✓ throws NetworkError when fetch throws
     ✓ returns response on 200
 ✓ src/__tests__/resources/contacts.test.ts (7)
 ✓ src/__tests__/resources/conversations.test.ts (4)
 ✓ src/__tests__/resources/sessions.test.ts (5)
 ✓ src/__tests__/resources/channel.test.ts (6)
 ✓ src/__tests__/resources/ai.test.ts (4)
 ✓ src/__tests__/resources/teams.test.ts (4)
 ✓ src/__tests__/resources/boards.test.ts (7)
 ✓ src/__tests__/resources/messages.test.ts (5)
 ✓ src/__tests__/integration.test.ts (11)
 ❯ src/__tests__/client.test.ts (10) 5047ms
   ❯ ImbraceClient (10) 5046ms
     ✓ defaults to the production base URL
     ✓ strips trailing slash from baseUrl
     ✓ reads IMBRACE_API_KEY from env
     ✓ reads IMBRACE_BASE_URL from env
     ✓ initialises all 9 domain resources
     × setAccessToken updates the token manager 5021ms
     ✓ clearAccessToken removes the token
     ✓ init() pings health when checkHealth=true
     ✓ init() is a no-op when checkHealth=false
     ✓ createImbraceClient returns an ImbraceClient

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ Failed Tests 3 ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/__tests__/client.test.ts > ImbraceClient > setAccessToken updates the token manager
Error: Test timed out in 5000ms.
If this is a long-running test, pass a timeout value as the last argument or configure it globally with "testTimeout".
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/3]⎯

 FAIL  src/__tests__/http.test.ts > HttpTransport > sets X-Api-Key header when apiKey providedAssertionError: expected undefined to be 'key_test' // Object.is equality

- Expected:
  "key_test"

+ Received:
  undefined

 ❯ src/__tests__/http.test.ts:38:42
     36|
     37|     await transport.getFetch()(BASE + "/health", { method: "GET" })
     38|     expect(capturedHeaders["x-api-key"]).toBe("key_test")
       |                                          ^
     39|   })
     40|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/3]⎯

 FAIL  src/__tests__/http.test.ts > HttpTransport > sets Authorization header when token setAssertionError: expected undefined to be 'Bearer tok_test' // Object.is equality

- Expected:
  "Bearer tok_test"

+ Received:
  undefined

 ❯ src/__tests__/http.test.ts:52:46
     50|
     51|     await transport.getFetch()(BASE + "/health", { method: "GET" })
     52|     expect(capturedHeaders["authorization"]).toBe("Bearer tok_test")
       |                                              ^
     53|   })
     54|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/3]⎯

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ Unhandled Errors ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

Vitest caught 1 unhandled error during the test run.
This might cause false positive tests. Resolve unhandled errors to make sure your tests are not affected.

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ Uncaught Exception ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
AssertionError: expected undefined to be 'Bearer tok_new' // Object.is equality

- Expected:
  "Bearer tok_new"

+ Received:
  undefined

 ❯ Timeout._onTimeout src/__tests__/client.test.ts:71:48
     69|     // Allow microtasks to run
     70|     return new Promise`<void>`(resolve => setTimeout(() => {
     71|       expect(capturedHeaders["authorization"]).toBe("Bearer tok_new")
       |                                                ^
     72|       resolve()
     73|     }, 0))
 ❯ listOnTimeout node:internal/timers:608:17
 ❯ processTimers node:internal/timers:543:7

This error originated in "src/__tests__/client.test.ts" test file. It doesn't mean the error was thrown inside the file itself, but while it was running.
The latest test that might've caused the error is "setAccessToken updates the token manager". It might mean one of the following:

- The error was thrown, while Vitest was running this test.
- If the error occurred after the test had been completed, this was the last documented test before it was thrown.
  ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

 Test Files  2 failed | 14 passed (16)
      Tests  3 failed | 95 passed (98)
     Errors  1 error
   Start at  21:54:09
   Duration  7.83s (transform 7.13s, setup 0ms, collect 24.82s, tests 5.29s, environment 4ms, prepare 9.07s)
