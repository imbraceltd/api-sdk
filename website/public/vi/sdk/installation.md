# Cài Đặt

> Cài đặt Imbrace SDK cho TypeScript hoặc Python.

### Cài Đặt

  
    ```bash
    npm install @imbrace/sdk
    # hoặc
    yarn add @imbrace/sdk
    # hoặc
    pnpm add @imbrace/sdk
    ```

    Yêu cầu Node.js 18+ (hoặc bất kỳ trình duyệt nào hỗ trợ native `fetch` và `ReadableStream`).
  
  
    ```bash
    pip install imbrace
    # hoặc
    uv add imbrace
    ```

    Yêu cầu Python 3.9+.
  

### Khởi Tạo Client

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"

    // Build on Imbrace — Imbrace IS your backend, end-users log in via OTP
    const client = new ImbraceClient({
      accessToken: "acc_your_token",
      baseUrl: "https://app-gatewayv2.imbrace.co",
    })
    ```

    Client có trạng thái — tạo một lần và tái sử dụng trong toàn bộ ứng dụng.
  
  
    ```python
    from imbrace import ImbraceClient

    # Build on Imbrace — Imbrace IS your backend, end-users log in via OTP
    with ImbraceClient(access_token="acc_your_token") as client:
        ...
    ```

    Python cũng export `AsyncImbraceClient` (`async with ...`) cho các stack async như FastAPI.

    Context manager tự đóng HTTP connection pool bên dưới.
  

Để biết khi nào dùng loại credential nào, xem [Xác Thực](/vi/sdk/authentication/). Để thiết lập credentials từng bước (env vars, dotenv, secrets), xem [Hướng Dẫn Cài Đặt](/vi/getting-started/setup/#configure-credentials).

### Kiểm Tra

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"
    console.log("SDK loaded:", typeof ImbraceClient) // "function"
    ```
  
  
    ```python
    from imbrace import ImbraceClient
    print("SDK ready:", ImbraceClient)
    ```
  

### Biến Môi Trường

SDK **không** tự đọc biến môi trường. Truyền credentials trực tiếp vào constructor và dùng loader (`dotenv` / cách xử lý env của framework) nếu bạn lưu chúng trong `.env`.

| Biến | Mục đích |
|---|---|
| `IMBRACE_API_KEY` | API key của bạn (org-level credential) |
| `IMBRACE_ACCESS_TOKEN` | Access token của user (per-session credential) |
| `IMBRACE_BASE_URL` | Override gateway URL (mặc định: `https://app-gatewayv2.imbrace.co`) |

Org id được mã hoá trong cả API keys và access tokens — bạn không bao giờ cần truyền `organizationId`/`organization_id` cho SDK. Xem [Xác Thực](/vi/sdk/authentication/) để biết thêm chi tiết.
