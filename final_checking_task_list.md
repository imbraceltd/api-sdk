# Final Checking Task List

## AI Agent Request Description

Khi thực hiện mỗi task `check_X`, hãy làm theo các nguyên tắc sau:

1. **Chỉ dựa vào source truth** — tuyệt đối không suy diễn, không đoán, không bịa ra thông tin.
2. **Mỗi code block** trong file `.mdx` phải được đối chiếu với source truth tương ứng:
   - SDK files: so sánh với code thật trong `ts/src/` và `py/src/imbrace/`; tham khảo thêm test files ở `ts/tests/`, `py/tests/`, `test-npm-pkg/`, `test-local-pkg/`, `test-pip-pkg/`
   - CLI files: so sánh với code thật trong `C:\Users\onggi\Desktop\Projects\imbrace-cli`
3. **Mỗi nội dung text** (tên method, tên class, tên parameter, tên resource, URL, endpoint, kiểu dữ liệu, v.v.) cũng phải được kiểm tra với source truth.
4. **Ghi nhận các vấn đề**:
   - Code block bịa ra (không tồn tại trong source truth)
   - Code block sai (tên method/class/param sai, signature sai, kiểu trả về sai)
   - Nội dung text sai lệch so với source truth
   - Thiếu hoặc thừa thông tin so với source truth
5. **Output**: Với mỗi vấn đề tìm thấy, ghi rõ:
   - Dòng số trong file `.mdx`
   - Nội dung sai / bịa
   - Nội dung đúng theo source truth (kèm đường dẫn file source truth và dòng số)
6. **Sau khi kiểm tra xong một `check_X`**:
   - Nếu không có issue nào → ghi **"→ Đã khớp tất cả"** bên cạnh `check_X`.
   - Nếu có issue → ghi **"→ Issues:"** và liệt kê bên dưới.
   - Tick checkbox: đổi `[ ]` thành `[x]`.

## Source Truths
- **SDK**: `ts/src/` (TypeScript) và `py/src/imbrace/` (Python) — tham khảo thêm `ts/tests/`, `py/tests/`, `test-npm-pkg/`, `test-local-pkg/`, `test-pip-pkg/`
- **CLI**: `C:\Users\onggi\Desktop\Projects\imbrace-cli`

---

## EN — SDK (13 files)

- [x] `check_01` — `website/src/content/docs/sdk/overview.mdx`
- [x] `check_02` — `website/src/content/docs/sdk/quick-start.mdx`
- [x] `check_03` — `website/src/content/docs/sdk/installation.mdx`
- [x] `check_04` — `website/src/content/docs/sdk/authentication.mdx`
- [x] `check_05` — `website/src/content/docs/sdk/full-flow-guide.mdx`
- [x] `check_06` — `website/src/content/docs/sdk/workflows.mdx`
- [x] `check_07` — `website/src/content/docs/sdk/ai-agent.mdx`
- [x] `check_08` — `website/src/content/docs/sdk/document-ai.mdx`
- [x] `check_09` — `website/src/content/docs/sdk/databoard.mdx`
- [x] `check_10` — `website/src/content/docs/sdk/resources.mdx`
- [x] `check_11` — `website/src/content/docs/sdk/integrations.mdx`
- [x] `check_12` — `website/src/content/docs/sdk/error-handling.mdx`
- [x] `check_13` — `website/src/content/docs/sdk/local-testing.mdx`

## EN — CLI (4 files)

- [x] `check_14` — `website/src/content/docs/cli/overview.mdx`
- [x] `check_15` — `website/src/content/docs/cli/installation.mdx`
- [x] `check_16` — `website/src/content/docs/cli/commands.mdx`
- [x] `check_17` — `website/src/content/docs/cli/api-reference.mdx`

## EN — Getting Started (2 files)

- [x] `check_18` — `website/src/content/docs/getting-started/overview.mdx`
- [x] `check_19` — `website/src/content/docs/getting-started/setup.mdx`

## EN — Guides (4 files)

- [x] `check_20` — `website/src/content/docs/guides/api-key.mdx`
- [x] `check_21` — `website/src/content/docs/guides/testing.mdx`
- [x] `check_22` — `website/src/content/docs/guides/troubleshooting.mdx`
- [x] `check_23` — `website/src/content/docs/guides/vibe-coding.mdx`

## EN — Index (1 file)

- [x] `check_24` — `website/src/content/docs/index.mdx`

## EN - Reference (8 files)

- [x] `check_25` — `website/src/content/docs/reference/ai-agent.mdx`
- [x] `check_26` — `website/src/content/docs/reference/workflow.mdx`
- [x] `check_27` — `website/src/content/docs/reference/board.mdx`
- [x] `check_28` — `website/src/content/docs/reference/campaign.mdx`
- [x] `check_29` — `website/src/content/docs/reference/communication.mdx` 
- [x] `check_30` — `website/src/content/docs/reference/channel.mdx`
- [x] `check_31` — `website/src/content/docs/reference/contact.mdx`
- [x] `check_32` — `website/src/content/docs/reference/conversation.mdx`

## EN - Review

- Review sections and evaluate whether the current structure and content flow are intuitive for new users. Check if the order of sections (e.g. installation, authentication, initialization, first request) is logical, whether explanations are clear enough before code examples, and whether the content helps users quickly understand how to get started without confusion. Also identify any sections that should be reorganized, simplified, separated, or improved for better onboarding experience.

- [x] `check_33` — `website/src/content/docs/getting-started/setup.mdx`
  → Đã review + sửa:
  1. Swap Environments lên trước Configure Credentials
  2. Thay `baseUrl` → `env` trong các init examples
  3. Xoá `## Quick Usage Examples` (đã có sdk/quick-start)
  4. Move `### CLI Installation` xuống cuối (sau init, trước service URLs)
  5. 401: curl raw → link Dashboard + API Key guide
  6. Update intro + description matching new order
  7. Python async example: `sk-...` → `api_...` (dòng 209)
- [x] `check_34` — `website/src/content/docs/guides/testing.mdx`
  → Đã review + sửa (verify pass):
  1. `Updated:` hardcoded date → đã xóa
  2. "This runs vitest..." → blockquote ngắn gọn
  3. `npm run build` duplicate → xóa khỏi Lint section
  4. Frontmatter `------` → `---`
  5. Blank line thiếu trước `---` separator (dòng 126)
  6. Coverage TS: không thêm vì `@vitest/coverage-v8` chưa cài — giữ nguyên chỉ Python
- [x] `check_35` — `website/src/content/docs/sdk/overview.mdx`
  → Đã review + sửa:
  1. Removed syncKey blockquote meta comment (dòng 10 cũ)
  2. "Hello, world": `accessToken: "acc_your_token"` → `apiKey: "api_your_key"` (TS + Py)
  3. Resources table: thêm `client.documentAi` / `client.document_ai`
  4. "When to pick which credential": làm cụ thể hơn — thêm cột "How you get it", "Scope"
- [x] `check_36` — `website/src/content/docs/sdk/quick-start.mdx`
  → Đã review + sửa (verify pass):
  1. `baseUrl`/`base_url` hardcoded URL → `env: "stable"` / `env="stable"` (tất cả 4 block)
  2. apiKey examples: thêm `organizationId` / `organization_id` (access-token không cần)
  3. Dòng 69: blockquote meta UI → `<Aside type="tip">` với link Authentication
  4. Health-check: bỏ qua — boards.list() đã serve mục đích này
  5. Empty list note: thêm "An empty list (data: []) just means no boards exist yet — not an error"
  6. TS access-token: `"your-access-token"` literal → `process.env.IMBRACE_ACCESS_TOKEN`
  7. Python boards: `board["id"]` → `board.get("_id") or board.get("id")` (API trả về cả 2 dạng)
- [x] `check_37` — `website/src/content/docs/sdk/installation.mdx`
  → Đã review + sửa (verify pass):
  1. `baseUrl` hardcoded → `env: "stable"` (access-token + api-key TS blocks)
  2. Hardcoded credential strings → `process.env.*` (TS) / `os.environ` (Py) với `import os`
  3. api-key blocks: thêm `organizationId` / `organization_id`
  4. Python `...` placeholder → `me = client.platform.get_me()`
  5. Env vars table: thêm `IMBRACE_ORGANIZATION_ID` row
  6. Thêm "### Next steps" section ở cuối
  7. Verify: `acc_your_token` format là đúng — matches README và actual test tokens (`acc_xxx`)
- [x] `check_38` — `website/src/content/docs/sdk/full-flow-guide.mdx`
  → Đã review + sửa (verify pass):
  1. `baseUrl`/`base_url` → `env: "stable"` / `env="stable"` (tất cả 4 init block)
  2. Credential literals → `process.env.*` / `os.environ` với `import os`; api-key thêm `organizationId`
  3. Meta comment "Toggle the language tabs..." → đã xóa khỏi intro
  4. "The header dropdown swaps..." → `<Aside type="tip">` với link Authentication
  5. Python indent bug: `print` dư 1 space (line 103) → sửa
  6. TS second streamChat: thừa 1 space indent → sửa
  7. Python second stream_chat: thiếu 1 space indent → sửa
  8. Step 2.1: `listFlows` fragile → đổi thành "Get your project ID" với Option A (hardcode) + Option B (`resolveProjectId()` — cả 2 SDK đều có, throws nếu org chưa có flows)
  9. Section 3 `"org_your_org_id"` hardcoded → `process.env.IMBRACE_ORGANIZATION_ID` / `os.environ.get(...)`
  10. Thêm "### Next steps" section ở cuối
  11. `Dropdown` field type: không xác nhận được từ source truth (tests chỉ có ShortText, Number) — giữ nguyên, cần verify thủ công
- [x] `check_39` — `website/src/content/docs/sdk/local-testing.mdx`
  → Đã review + sửa (verify pass):
  1. File refs: `test-local.mjs` ✓, `test_guide_flow.py` ✓, `.env.example` ✓, `requirements.txt` ✓ — tất cả tồn tại đúng path
  2. `cd test-pip-pkg/py` — working dir ambiguous sau `cd py` → thêm "(run from the repo root)"
  3. Thêm "### Next steps" section ở cuối
  4. AWS/sops (dòng 14, 32): giữ nguyên — guide này dành cho SDK developer nội bộ
  5. Curl 401 (dòng 166-171): giữ nguyên — dev guide dùng curl là phù hợp, khác audience với setup.mdx
  6. "Org context encoded" (dòng 42): minor inconsistency với setup guide nhưng đúng trong context API key — giữ nguyên
  7. `test-local.mjs` (dòng 70): là main entry đúng — các `test-*.mjs` khác là individual modules
- [x] `check_40` — `website/src/content/docs/sdk/integrations.mdx`
  → Đã review + sửa (verify pass):
  1. `:::tip` (Docusaurus syntax) → `<Aside type="tip">` + thêm `Aside` vào import
  2. Node.js CLI `new ImbraceClient()` → thêm `apiKey: process.env.IMBRACE_API_KEY`
  3. OTP Python: `client.auth.signin_email_request` / `auth.signin_with_email` → `client.request_otp()` / `client.login_with_otp()` (public convenience API); return token dùng `.get("accessToken") or .get("token")`
  4. Thêm "### Next steps" section ở cuối
  5. React stale token + AbortController: giữ nguyên (design concern, không phải accuracy issue)
  6. Next.js API key only: intentional (server-side pattern) ✓
  7. `init()` — confirmed public method trên AsyncImbraceClient ✓
- [x] `check_41` — `website/src/content/docs/sdk/authentication.mdx`
  → Đã review + sửa (verify pass):
  1. `baseUrl` → `env: "stable"` (tất cả 4 block: API Key TS, Access Token TS, OTP TS, Password TS)
  2. API Key TS: `"api_xxx..."` literal → `process.env.IMBRACE_API_KEY`; thêm `organizationId: process.env.IMBRACE_ORGANIZATION_ID`
  3. API Key Python: thêm `organization_id=os.environ.get("IMBRACE_ORGANIZATION_ID")` + `env="stable"`
  4. Access Token TS: `"acc_xxxxxxxxxxxxx"` → `process.env.IMBRACE_ACCESS_TOKEN`; thêm `import { ImbraceClient }`; thêm `env: "stable"`
  5. Access Token Python: thêm `import os` + `from imbrace import ImbraceClient`; `"acc_xxxxxxxxxxxxx"` → `os.environ["IMBRACE_ACCESS_TOKEN"]`; thêm `env="stable"`
  6. OTP TS: `const loginRes = await ...` (unused var) → `await ...` với comment cập nhật
  7. OTP: `"org_your_org_id"` → `process.env.IMBRACE_ORGANIZATION_ID!` (TS) / `os.environ["IMBRACE_ORGANIZATION_ID"]` (Py, cả sync + async)
  8. Password Login Python: thêm `from imbrace import ImbraceClient`
  9. Context manager: `api_key="api_xxx"` → `os.environ["IMBRACE_API_KEY"]`; thêm `import os` + `from imbrace import ImbraceClient, AsyncImbraceClient`
  10. Thêm "### Next steps" section ở cuối
  11. OTP 4 steps vs 3 steps: giữ nguyên 4 steps — đây là correct flow; setup guide là simplified overview
- [x] `check_42` — `website/src/content/docs/guides/api-key.mdx`
  → Đã review + sửa:
  1. `baseUrl` → `env: "stable"` + thêm `organizationId`
  2. "Option 2" → "Generate via SDK"
  3. Python thêm `env="stable"` + `organization_id`

---

## Plan — AuthOnly Sync & Audit

### Phase 1 — AuthOnly code block audit (EN files)

Các file EN hiện có `<AuthOnly>`:
- `sdk/quick-start.mdx` ✅ done
- `sdk/installation.mdx` ✅ done
- `sdk/full-flow-guide.mdx` → sẽ làm trong check_38
- `sdk/ai-agent.mdx` → cần review layout riêng (check_07 chỉ pass accuracy, chưa review layout)

**Audit mục tiêu:** Trong tất cả EN files (kể cả các file không dùng `<AuthOnly>`), kiểm tra xem có code block nào đang hiển thị cả 2 credential (accessToken + apiKey) trong cùng 1 block không — nếu có thì đánh giá có nên tách ra `<AuthOnly>` không.

**Tiêu chí để tách:**
- Block đang init client với cả 2 credential (`apiKey` / `accessToken`) gộp chung → nên tách
- Block chỉ minh họa 1 loại credential cụ thể (ví dụ: OTP flow chỉ có accessToken) → giữ nguyên
- Block là API call thông thường (không liên quan đến credential) → không cần tách
- **Lưu ý:** Cần xác nhận xem behavior có đúng không trước khi tách — một số block gộp chung có thể là chủ đích (ví dụ: cả 2 đều work, không cần phân biệt)

- [x] `check_43` — Audit AuthOnly split cho `sdk/ai-agent.mdx`
  → Đã audit: ai-agent.mdx đã dùng AuthOnly đúng — không cần sửa.
- [x] `check_44` — Audit AuthOnly split cho toàn bộ EN files còn lại
  → Đã audit toàn bộ EN files. Chỉ `getting-started/setup.mdx` cần split. Các files khác không cần.
  → Chi tiết:
  - `auth.mdx`: separate sections — skip
  - `overview.mdx`: chỉ show 1 credential — skip
  - `integrations.mdx`: mỗi framework section riêng — skip
  - `setup.mdx`: **⚠️ Cần split** — "Initialize the Client" có cả 2 credential cùng block

### Phase 2 — Locale sync (sau khi EN hoàn chỉnh)

4 file EN dùng `<AuthOnly>` × 3 locale (`zh-tw`, `zh-cn`, `vi`) = 12 file cần sync.

**Scope sync:** Chỉ sync phần code blocks (credential format, `env: "stable"`, `os.environ`, `organizationId`). Không dịch lại text — text giữ nguyên theo bản locale hiện tại.

- [ ] `check_45` — Locale sync: `sdk/quick-start.mdx` → `zh-tw`, `zh-cn`, `vi`
- [ ] `check_46` — Locale sync: `sdk/installation.mdx` → `zh-tw`, `zh-cn`, `vi`
- [ ] `check_47` — Locale sync: `sdk/full-flow-guide.mdx` → `zh-tw`, `zh-cn`, `vi`
- [ ] `check_48` — Locale sync: `sdk/ai-agent.mdx` → `zh-tw`, `zh-cn`, `vi`
