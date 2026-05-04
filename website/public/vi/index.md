# Imbrace SDK

> Bộ SDK TypeScript và Python chính thức cho Imbrace Gateway — type-safe, đầy đủ tính năng, sẵn sàng cho production.

## Tại Sao Chọn Imbrace SDK?

  ### Type-safe Theo Thiết Kế

Định nghĩa TypeScript đầy đủ và type hints Python trên 27+ resource
    namespace. Bắt lỗi lúc compile, không phải lúc chạy.

  ### Tự Động Retry & Độ Bền

Exponential backoff tích hợp sẵn cho lỗi 429 và 5xx. Không cần cấu hình —
    ứng dụng vẫn hoạt động ổn định dưới tải cao.

  ### Xác Thực 3 Tầng

API Key, JWT Bearer, và legacy access token — tất cả được xử lý trong suốt.
    Đổi chiến lược xác thực mà không cần thay đổi logic nghiệp vụ.

  ### Python Async-first

`AsyncImbraceClient` song song với client đồng bộ. Tích hợp ngay vào
    FastAPI, asyncio, hoặc Django với một lệnh import.

## Cài Đặt Nhanh

  
    
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

  

## Khám Phá Tài Liệu

  - [Tổng Quan SDK](sdk/overview/): Kiến trúc, resource namespaces, chiến lược xác thực. TypeScript và Python trong cùng một nơi.
  - [Quick Start](sdk/quick-start/): Thực hiện cuộc gọi API đầu tiên trong 60 giây — chuyển đổi giữa TypeScript và Python.
  - [Xác Thực](sdk/authentication/): API key vs access token, luồng đăng nhập OTP, và cách chọn cái nào.
  - [Hướng Dẫn Flow Đầy Đủ](sdk/full-flow-guide/): Hướng dẫn từ đầu đến cuối của bốn quy trình làm việc chính.
  - [Hướng Dẫn Test](guides/testing/): Unit tests, mocking, integration test patterns.
  - [Xử Lý Lỗi](guides/troubleshooting/): Common errors, debugging tips, known issues.
