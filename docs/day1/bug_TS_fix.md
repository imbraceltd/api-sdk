# Bug Report & Fix — TypeScript SDK (iMBrace)

> **Ngày:** 2026-04-09  
> **Phạm vi:** `ts/src/http.ts`  
> **Test runner:** Vitest v1.6.1  
> **Kết quả trước fix:** 3 failed / 98 tests, 1 unhandled error  
> **Kết quả sau fix:** 98 passed / 98 tests, 0 errors

---

## Tóm tắt lỗi

| # | File | Dòng | Mô tả | Mức độ |
|---|------|------|-------|--------|
| 1 | `http.ts` | 47 | `apiKey` được gán vào header `x-access-token` thay vì `x-api-key` | Cao |
| 2 | `http.ts` | 52 | `accessToken` được gán vào `x-access-token` thay vì `authorization: Bearer <token>` | Cao |
| 3 | `client.test.ts` | 71 | Test `setAccessToken` timeout 5000ms — cascading từ Bug 2 | Cascading |

---

## Chi tiết từng bug

### Bug 1 — Header `x-api-key` bị ghi sai tên

**File:** `ts/src/http.ts:47`

**Code lỗi:**
```ts
if (this.opts.apiKey) {
  headers.set("x-access-token", this.opts.apiKey);  // ❌
}
```

**Code đúng:**
```ts
if (this.opts.apiKey) {
  headers.set("x-api-key", this.opts.apiKey);  // ✅
}
```

**Test fail:**
```
FAIL src/__tests__/http.test.ts > HttpTransport > sets X-Api-Key header when apiKey provided
AssertionError: expected undefined to be 'key_test'
  capturedHeaders["x-api-key"]  →  undefined   (nhận)
                                →  "key_test"   (mong đợi)
```

**Nguyên nhân:** Developer dùng sai tên header. API gateway iMBrace yêu cầu API key qua header `x-api-key`, không phải `x-access-token`.

---

### Bug 2 — Header `Authorization` bị ghi sai tên và sai format

**File:** `ts/src/http.ts:52`

**Code lỗi:**
```ts
const token = this.opts.tokenManager.getToken();
if (token) {
  headers.set("x-access-token", token);  // ❌ sai tên + sai format (thiếu "Bearer ")
}
```

**Code đúng:**
```ts
const token = this.opts.tokenManager.getToken();
if (token) {
  headers.set("authorization", `Bearer ${token}`);  // ✅
}
```

**Test fail:**
```
FAIL src/__tests__/http.test.ts > HttpTransport > sets Authorization header when token set
AssertionError: expected undefined to be 'Bearer tok_test'
  capturedHeaders["authorization"]  →  undefined         (nhận)
                                    →  "Bearer tok_test"  (mong đợi)
```

**Nguyên nhân:** 
1. Tên header sai: dùng `x-access-token` thay vì header chuẩn HTTP `authorization`
2. Thiếu prefix `Bearer ` theo chuẩn Bearer Token (RFC 6750)
3. Cả `apiKey` và `token` đều set cùng `x-access-token` → token sẽ overwrite apiKey nếu cả hai được cung cấp

---

### Bug 3 — Test timeout (cascading từ Bug 2)

**File:** `ts/src/__tests__/client.test.ts:58–74`

**Mô tả:** Test `setAccessToken updates the token manager` timeout sau 5000ms.

**Cơ chế:**
```ts
it("setAccessToken updates the token manager", () => {
  // ...
  client.sessions.list()
  return new Promise<void>(resolve => setTimeout(() => {
    expect(capturedHeaders["authorization"]).toBe("Bearer tok_new")  // ❌ throws vì header undefined
    resolve()  // ← không bao giờ được gọi khi expect throws
  }, 0))
  // Promise không bao giờ resolve/reject → Vitest timeout sau 5000ms
})
```

**Nguyên nhân gốc rễ:** Vì Bug 2 chưa được fix, header `authorization` là `undefined`. Khi `expect()` throw, `resolve()` không chạy, Promise treo vô tận → timeout.

**Lưu ý:** Đây là lỗi cascading — test code không cần sửa. Khi Bug 2 được fix, test này tự pass.

---

## Fix đã áp dụng

**Files sửa:**
| File | Loại thay đổi |
|------|---------------|
| `ts/src/http.ts` | Fix source — tên header sai |
| `ts/src/__tests__/resources/account.test.ts` | Fix test — assertion dùng tên header cũ |
| `ts/src/__tests__/resources/agent.test.ts` | Fix test — assertion dùng tên header cũ |
| `ts/src/__tests__/resources/messages.test.ts` | Fix test — assertion dùng tên header cũ |

```diff
- if (this.opts.apiKey) {
-   headers.set("x-access-token", this.opts.apiKey);
- }
- 
- const token = this.opts.tokenManager.getToken();
- if (token) {
-   headers.set("x-access-token", token);
- }

+ if (this.opts.apiKey) {
+   headers.set("x-api-key", this.opts.apiKey);
+ }
+ 
+ const token = this.opts.tokenManager.getToken();
+ if (token) {
+   headers.set("authorization", `Bearer ${token}`);
+ }
```

---

## Hướng dẫn chạy test

### Yêu cầu
- Node.js ≥ 18
- Đã cài dependencies: `npm install` trong `ts/`

### Chạy toàn bộ test
```bash
cd ts
npm test
```

### Chạy chỉ các test liên quan đến bug này
```bash
cd ts
npx vitest run src/__tests__/http.test.ts src/__tests__/client.test.ts
```

### Kết quả mong đợi sau fix
```
✓ src/__tests__/http.test.ts (9)
  ✓ sets X-Api-Key header when apiKey provided
  ✓ sets Authorization header when token set
  ✓ does not set Authorization header when no token
  ✓ throws AuthError on 401
  ✓ throws AuthError on 403
  ✓ throws ApiError on 404
  ✓ retries on 500 and throws after max retries
  ✓ throws NetworkError when fetch throws
  ✓ returns response on 200

✓ src/__tests__/client.test.ts (10)
  ✓ setAccessToken updates the token manager

Test Files  0 failed | 16 passed (16)
     Tests  0 failed | 98 passed (98)
```

### Chạy toàn bộ suite với verbose
```bash
cd ts
npx vitest run --reporter=verbose
```

### Chạy integration test (cần API key thật)
```bash
cd ts
IMBRACE_API_KEY=your_key_here npm test
```

---

## Checklist kiểm tra thủ công sau fix

- [ ] `npm test` chạy 0 failed
- [ ] Không còn "Unhandled Errors" trong output
- [ ] Test `sets X-Api-Key header` pass
- [ ] Test `sets Authorization header` pass
- [ ] Test `setAccessToken updates the token manager` không còn timeout
- [ ] Các test khác vẫn pass (không regression)

---

## Lưu ý về thiết kế

### Phân biệt `x-api-key` và `authorization`

| Header | Dùng cho | Giá trị |
|--------|----------|---------|
| `x-api-key` | API Key tĩnh (backend-to-backend) | `key_xxxxx` |
| `authorization` | Access Token động (user session) | `Bearer tok_xxxxx` |

Khi cả hai được cung cấp, header `authorization` (Bearer token) sẽ được ưu tiên xử lý bởi gateway (vì được set sau). Đây là hành vi hợp lý cho dual-auth flow của iMBrace SDK.
