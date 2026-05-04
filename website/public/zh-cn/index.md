# Imbrace SDK

> Imbrace Gateway 官方 TypeScript 和 Python SDK — 类型安全、功能完整、生产就绪。

## 为什么选择 Imbrace SDK？

  ### 类型安全设计

覆盖 27+ 资源命名空间的完整 TypeScript 定义和 Python 类型注解。在编译时捕获错误，而非运行时。

  ### 自动重试与弹性

针对 429 和 5xx 响应内置指数退避重试。无需配置 — 高负载下应用依然稳定运行。

  ### 三层身份验证

API Key、JWT Bearer 和 legacy access token — 全部透明处理。无需更改业务逻辑即可切换认证策略。

  ### Python 异步优先

`AsyncImbraceClient` 与同步客户端并行存在。一行导入即可接入 FastAPI、asyncio 或 Django。

## 快速安装

  
    
      TypeScript
    

    ```bash
    npm install @imbrace/sdk
    ```

    ```ts
    import { ImbraceClient } from "@imbrace/sdk";
    const client = new ImbraceClient();
    const me = await client.platform.getMe();
    ```

  
  
    
      Python
    

    ```bash
    pip install imbrace
    ```

    ```python
    from imbrace import ImbraceClient
    client = ImbraceClient()
    me = client.platform.get_me()
    ```

  

## 探索文档

  - [SDK 概览](sdk/overview/): 架构、资源命名空间、身份验证策略。TypeScript 和 Python 在同一处。
  - [快速入门](sdk/quick-start/): 在 60 秒内完成首次 API 调用 — 在 TypeScript 和 Python 之间切换。
  - [身份验证](sdk/authentication/): API 密钥 vs 访问令牌、OTP 登录流程，以及如何选择。
  - [完整流程指南](sdk/full-flow-guide/): 四个主要工作流程的端到端演练。
  - [测试指南](guides/testing/): 单元测试、模拟、集成测试模式。
  - [常见问题](guides/troubleshooting/): 常见错误、调试技巧、已知问题。
