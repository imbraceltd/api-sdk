# Imbrace SDK

> Imbrace Gateway 官方 TypeScript 和 Python SDK — 類型安全、功能完整、生產就緒。

## 為什麼選擇 Imbrace SDK？

  ### 類型安全設計

覆蓋 27+ 資源命名空間的完整 TypeScript 定義和 Python 型別提示。在編譯時捕獲錯誤，而非執行時。

  ### 自動重試與彈性

針對 429 和 5xx 回應內建指數退避重試。無需配置 — 高負載下應用依然穩定運行。

  ### 三層身份驗證

API Key、JWT Bearer 和 legacy access token — 全部透明處理。無需更改業務邏輯即可切換認證策略。

  ### Python 非同步優先

`AsyncImbraceClient` 與同步客戶端並行存在。一行匯入即可接入 FastAPI、asyncio 或 Django。

## 快速安裝

  
    
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

  

## 探索文件

  - [SDK 總覽](sdk/overview/): 架構、資源命名空間、身份驗證策略。TypeScript 和 Python 在同一處。
  - [快速入門](sdk/quick-start/): 在 60 秒內完成首次 API 呼叫 — 在 TypeScript 和 Python 之間切換。
  - [身份驗證](sdk/authentication/): API 金鑰 vs 存取令牌、OTP 登入流程，以及如何選擇。
  - [完整流程指南](sdk/full-flow-guide/): 四個主要工作流程的端到端演練。
  - [測試指南](guides/testing/): 單元測試、模擬、整合測試模式。
  - [常見問題](guides/troubleshooting/): 常見錯誤、除錯技巧、已知問題。
