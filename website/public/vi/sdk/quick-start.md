# Bắt Đầu Nhanh

> Thực hiện API call đầu tiên với Imbrace trong dưới một phút.

### 1. Khởi Tạo Client

  
    ```typescript
    import { ImbraceClient } from "@imbrace/sdk"

    const client = new ImbraceClient({
      accessToken: "your-access-token",
      baseUrl: "https://app-gatewayv2.imbrace.co",
    })
    ```
  
  
    ```python
    import os
    from dotenv import load_dotenv
    from imbrace import ImbraceClient

    load_dotenv()

    client = ImbraceClient(
        access_token=os.environ["IMBRACE_ACCESS_TOKEN"],
        base_url="https://app-gatewayv2.imbrace.co",
    )
    ```
  

> Chuyển dropdown **Auth** trong header để chuyển đổi giữa API Key và Access Token trên toàn trang. Xem [Xác Thực](/vi/sdk/authentication/) để biết nên chọn loại nào.

---

### 2. Lấy Danh Sách Boards

Boards là CRM pipelines — leads, deals, tasks, hoặc bất kỳ dữ liệu có cấu trúc nào. Call này chỉ cần credential của bạn.

  
    ```typescript
    const { data: boards } = await client.boards.list()

    for (const board of boards) {
      console.log(board._id, board.doc_name)
    }
    ```
  
  
    ```python
    boards = client.boards.list()

    for board in boards.get("data", []):
        print(board["_id"], board.get("doc_name"))
    ```
  

Nếu bạn thấy danh sách boards, SDK đã kết nối và xác thực thành công.

---

### 3. Bước Tiếp Theo

[Hướng Dẫn Luồng Đầy Đủ](/vi/sdk/full-flow-guide/) đi qua bốn luồng chính từ đầu đến cuối. Nhảy thẳng đến phần cần dùng:

- **AI Assistant + streamChat** → [Hướng Dẫn Luồng Đầy Đủ §1](/vi/sdk/full-flow-guide/#1-tạo-ai-assistant-và-bắt-đầu-chat)
- **Activepieces workflows** → [Hướng Dẫn Luồng Đầy Đủ §2](/vi/sdk/full-flow-guide/#2-tạo-workflow-với-activepieces-và-liên-kết-với-assistant)
- **Knowledge Hub (folders, RAG)** → [Hướng Dẫn Luồng Đầy Đủ §3](/vi/sdk/full-flow-guide/#3-quản-lý-knowledge-hub-và-gắn-vào-assistant)
- **Boards & Items (CRM)** → [Hướng Dẫn Luồng Đầy Đủ §4](/vi/sdk/full-flow-guide/#4-quản-lý-data-boards-và-items-crm-pipeline)

Để xem tham chiếu API theo namespace, xem [Resources](/vi/sdk/resources/).
