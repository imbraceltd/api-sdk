# Vibe Coding

> 通过将 llms.txt 导入 AI 编程助手（Claude、Cursor、Copilot 或任何支持 LLM 的 IDE），更高效地使用 Imbrace SDK。

**Vibe Coding** 是指通过与 AI 助手协作来编写代码——用自然语言描述需求，让 AI 生成、解释或重构代码。Imbrace SDK 提供了 [`llms.txt`](https://imbraceltd.github.io/api-sdk/llms.txt) 文件，使任何 AI 工具都能立即理解 SDK，不会凭空捏造方法名或参数结构。

## 什么是 `llms.txt`？

`llms.txt` 是一个纯文本文件（类似 `robots.txt`），为 AI 模型提供库的简洁、准确摘要——包括客户端、资源、认证和常见模式。将其粘贴到 AI 的上下文窗口后，模型便已了解 SDK，可以一次性写出正确的代码。

**文件 URL：** [`https://imbraceltd.github.io/api-sdk/llms.txt`](https://imbraceltd.github.io/api-sdk/llms.txt)

## 如何使用

### Claude（claude.ai 或 Claude Code）

1. 打开新对话。
2. 将 `llms.txt` 的内容粘贴到消息开头，然后描述你的任务：

```
<context>
[在此粘贴 llms.txt 内容]
</context>

写一段 TypeScript 代码，从 assistant "asst_abc" 流式获取聊天响应，
并将每个文本增量输出到控制台。
```

### Cursor / VS Code Copilot

通过 IDE 中的 **@ docs** 或"添加上下文"功能将 URL 添加到 AI 上下文中。Cursor 直接支持 `@URL`：

```
@https://imbraceltd.github.io/api-sdk/llms.txt

如何上传文件并触发 embedding 处理？
```

### 其他 LLM

复制文件的原始内容，粘贴到提问前的 prompt 开头。大多数拥有 32k+ 上下文窗口的 LLM 都能完整读取该文件而不会丢失信息。

## 示例提示词

为 AI 提供 `llms.txt` 上下文后，可以尝试如下提示：

- *"用 Python 演示如何创建 AI 助手并流式获取聊天响应。"*
- *"生成 TypeScript 代码，列出所有 embedding 文件并删除状态为 `error` 的文件。"*
- *"`streamChat` 和 `streamSubAgentChat` 有什么区别？"*
- *"参照 Integrations 指南，编写一个用于 Chat Client 的 Express.js 鉴权代理。"*

> 在长时间会话中，将 `llms.txt` 固定为 **系统提示词** 或 **项目指令**，使其自动应用于每条消息。

## 保持更新

该文件在每次发布时重新生成。升级 SDK 后请重新获取该 URL，以获取新增方法或已更改的签名。
