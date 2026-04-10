# DAILY SCRUM REPORT | 2026-04-09
**Reporter:** Hoàng Junfeng  
**Team:** SDK Core  
**Last updated:** 22:39 UTC+7

---

## ✅ WHAT I DID TODAY
| Task | Status | Notes |
|------|--------|-------|
| Identify & fix TypeScript SDK authentication bugs | ✅ DONE | 2 critical bugs found in HttpTransport layer |
| Fix apiKey header mapping | ✅ DONE | `x-api-key` → `x-access-token` (http.ts:47) |
| Fix accessToken header format | ✅ DONE | `x-access-token` → `Authorization: Bearer <token>` |
| Fix cascading timeout bug | ✅ RESOLVED | setAccessToken test 5000ms timeout auto fixed after header correction |
| Update test assertions | ✅ DONE | 3 test files updated (account, agent, messages) |
| TypeScript Unit Tests | ✅ PASSING | 98/98 tests ✔️ |
| Write bug analysis documentation | ✅ DONE | `docs/bug_TS_fix.md` |

---

## 🔄 IN PROGRESS
- [ ] Full audit HttpTransport class for other misnamed headers
- [ ] Review remaining test files → validate all header assertions
- [ ] Scan Python integration tests for similar header naming issues

---

## 🚩 BLOCKERS
| ID | Issue | Impact | Action Required |
|----|-------|--------|-----------------|
| 1 | API Key expired `2025-10-04` | ❌ ALL integration tests return 401 Unauthorized | 🔴 Backend team → issue new valid API key |
| 2 | Token endpoint not found | `POST /private/backend/v1/thrid_party_token` returns 404 | 🔴 Backend team → confirm correct endpoint path |
| 3 | Python integration test bugs | 2 method name mismatches found | ⏳ Pending API key for real server verification |

> **Note:** Cannot confirm SDK works correctly against real server until blockers #1 & #2 are resolved.

---

## 📋 NEXT PLAN
1. 🔑 Receive new API key from backend team
2. ✅ Run full integration test suite (TypeScript + Python)
3. 🐛 Fix 2 minor Python test bugs:
    - `client.channels.list()` → `client.channel.list()`
    - Missing `client.account.get_account()` method
4. 🤝 Confirm token endpoint with PM / Tech Lead
5. 🎥 Prepare demo flow: `Init SDK → Authenticate → Call API` for branch review

---

## 💡 TECHNICAL NOTES
**Root Cause Analysis:**
> Unit tests were passing successfully *while production authentication was completely broken*.
>
> Tests were asserting against the same incorrect header names that were being set in code.
> Both implementation and tests were wrong in exactly the same way, creating a false positive test result.

---

**Commit summary:**
```
fix(auth): correct header names for authentication

- apiKey now correctly set to x-access-token
- accessToken now correctly uses Authorization: Bearer format
- update all test assertions to match correct header names
- fixes silent authentication failure while tests passing

Closes #SDK-147
```

---

## 🎤 SPEAKING SCRIPT / SCRIPT NÓI TRONG MEETING

### 🇻🇳 Tiếng Việt
> *Buổi sáng hôm nay tôi đã phát hiện và fix được 2 bug nghiêm trọng ở lớp authentication trong TypeScript SDK. Cả 2 header xác thực đều đang được set sai tên, dẫn đến toàn bộ flow đăng nhập bị hỏng hoàn toàn mà unit test vẫn chạy ngon lành do cả code và test đều bị sai giống hệt nhau.*
>
> *Đã sửa xong cả 2 bug, cập nhật 3 file test, bây giờ toàn bộ 98 test TypeScript đều pass 100%. Bug timeout 5 giây ở test setAccessToken cũng tự hết luôn sau khi fix header.*
>
> *Hiện tại bị chặn bởi API key đã hết hạn từ tháng 10 năm ngoái, nên chưa thể chạy integration test được. Còn 2 lỗi nhỏ ở Python test sẽ fix sau khi có key mới.*
>
> *Tiếp theo tôi sẽ rà soát hết lớp HttpTransport rồi chờ backend team cấp key mới để test hoàn chỉnh.*

---

### 🇬🇧 English
> *Today I identified and fixed two critical authentication bugs in the TypeScript SDK. Both auth headers were being set with incorrect names, which completely broke the entire authentication flow while unit tests were still passing perfectly - because both the implementation and tests had the exact same mistake.*
>
> *All bugs are fixed, 3 test files updated. All 98 TypeScript tests are now passing 100%. The 5000ms timeout bug in the setAccessToken test also resolved itself automatically after fixing the headers.*
>
> *We are currently blocked: API key expired last October, so we cannot run any integration tests. There are also 2 minor issues found in Python tests which I will fix once we have a valid key.*
>
> *Next I will finish auditing the full HttpTransport class, then waiting for backend team to provide a new API key for complete testing.*
