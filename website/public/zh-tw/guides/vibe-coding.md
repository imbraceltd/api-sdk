# Vibe Coding

> 透過將 llms.txt 匯入 AI 程式助手（Claude、Cursor、Copilot 或任何支援 LLM 的 IDE），更高效地使用 Imbrace SDK。

**Vibe Coding** 是指透過與 AI 助手協作來撰寫程式碼——以自然語言描述需求，讓 AI 生成、解釋或重構程式碼。Imbrace SDK 提供了 [`llms.txt`](https://imbraceltd.github.io/api-sdk/llms.txt) 檔案，使任何 AI 工具都能立即理解 SDK，不會憑空捏造方法名稱或參數結構。

## 什麼是 `llms.txt`？

`llms.txt` 是一個純文字檔案（類似 `robots.txt`），為 AI 模型提供函式庫的簡潔、準確摘要——包括客戶端、資源、認證和常見模式。將其貼入 AI 的上下文視窗後，模型便已了解 SDK，可以一次寫出正確的程式碼。

**檔案 URL：** [`https://imbraceltd.github.io/api-sdk/llms.txt`](https://imbraceltd.github.io/api-sdk/llms.txt)

## 如何使用

### Claude（claude.ai 或 Claude Code）

1. 開啟新對話。
2. 將 `llms.txt` 的內容貼到訊息開頭，再描述你的任務：

```
<context>
[在此貼上 llms.txt 內容]
</context>

寫一段 TypeScript 程式碼，從 assistant "asst_abc" 串流獲取聊天回應，
並將每個文字增量輸出到主控台。
```

### Cursor / VS Code Copilot

透過 IDE 中的 **@ docs** 或「新增上下文」功能將 URL 加入 AI 上下文。Cursor 直接支援 `@URL`：

```
@https://imbraceltd.github.io/api-sdk/llms.txt

如何上傳檔案並觸發 embedding 處理？
```

### 其他 LLM

複製檔案的原始內容，貼到提問前的 prompt 開頭。大多數擁有 32k+ 上下文視窗的 LLM 都能完整讀取該檔案而不會遺失資訊。

## 範例提示詞

為 AI 提供 `llms.txt` 上下文後，可以嘗試如下提示：

- *「用 Python 示範如何建立 AI 助手並串流獲取聊天回應。」*
- *「生成 TypeScript 程式碼，列出所有 embedding 檔案並刪除狀態為 `error` 的檔案。」*
- *「`streamChat` 和 `streamSubAgentChat` 有什麼區別？」*
- *「參照 Integrations 指南，撰寫一個用於 Chat Client 的 Express.js 驗證代理。」*

> 在長時間的會話中，將 `llms.txt` 固定為 **系統提示詞** 或 **專案指令**，使其自動套用於每則訊息。

## 保持更新

該檔案在每次發布時重新生成。升級 SDK 後請重新取得該 URL，以獲取新增方法或已變更的簽章。
