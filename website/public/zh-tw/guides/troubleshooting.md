# 常見問題

> 使用 Imbrace SDK 時的常見錯誤及解決方法。

## `AuthError: Invalid or expired access token.`（HTTP 401）

`.env` 中的 API key 已過期。

```bash
# 更新 .env
IMBRACE_API_KEY=api_xxx_new
```

---

## `ApiError: [400] {"message":"must have required property 'type'"}`

呼叫 `channel.list()` 時缺少必填參數。

```python
# 錯誤
client.channel.list()

# 正確
client.channel.list(type="web")
```

---

## `ApiError: [404]` 且 URL 路徑重複

`IMBRACE_BASE_URL` 被錯誤地設為完整的 endpoint 路徑，導致 URL 重複。

```env
# 錯誤
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co/private/backend/v1/third_party_token

# 正確
IMBRACE_BASE_URL=https://app-gatewayv2.imbrace.co
```

---

## 整合測試全部被略過

`IMBRACE_API_KEY` 未設置。

```bash
# 執行時臨時設置
IMBRACE_API_KEY=api_xxx pytest tests/integration -v -m integration

# 或添加到 .env
echo "IMBRACE_API_KEY=api_xxx" >> py/.env
```

---

## `Cannot find module`（TypeScript 測試）

測試檔案中的匯入路徑需要正確的目錄層級：

| 測試檔案位置                     | 匯入路徑                          |
| -------------------------------- | --------------------------------- |
| `tests/unit/*.test.ts`           | `../../src/client.js`             |
| `tests/unit/resources/*.test.ts` | `../../../src/app/resources/x.js` |
| `tests/integration/*.test.ts`    | `../../src/client.js`             |

---

## `mypy` 回報 `Pattern matching is only supported in Python 3.10`

mypy 錯誤地掃描了 `site-packages`。已在 `pyproject.toml` 中配置。若仍然回報錯誤：

```bash
mypy src/imbrace --exclude site-packages
```
