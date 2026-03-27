# Lab 2 - Thêm Memory Cho Agent (Tiếng Việt)

Tài liệu này hướng dẫn bạn triển khai Lab 2 theo workshop AWS AgentCore: thêm bộ nhớ dài hạn để agent có thể ghi nhớ thông tin khách hàng và cá nhân hóa phản hồi.

## 1. Tài liệu tham chiếu

- Workshop Lab 2: https://catalog.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US/30-add-memory
- Notebook mẫu chính thức: https://github.com/awslabs/amazon-bedrock-agentcore-samples/blob/main/01-tutorials/09-AgentCore-E2E/strands-agents/lab-02-agentcore-memory.ipynb

## 2. Mục tiêu của Lab 2

Từ agent ở Lab 1 (chỉ phản hồi theo phiên hiện tại), bạn nâng cấp để agent có trí nhớ:

- Nhớ thông tin khách hàng qua nhiều lần hội thoại.
- Tự động trích xuất sở thích người dùng (USER_PREFERENCE).
- Lưu và truy hồi dữ kiện hội thoại (SEMANTIC).
- Cá nhân hóa câu trả lời khi khách hàng quay lại.

## 3. Cách tạo Memory thủ công trên AWS Console (không cần code)

Nếu bạn muốn tạo Memory bằng thao tác trên giao diện AWS thay vì gọi API trong code, làm theo các bước sau:

1. Vào dịch vụ Bedrock AgentCore Memory trong AWS Console.
2. Tạo Memory mới với tên gợi ý: `CustomerSupportMemory`.
3. Cấu hình 2 chiến lược:
   - USER_PREFERENCE với namespace `support/customer/{actorId}/preferences/`
   - SEMANTIC với namespace `support/customer/{actorId}/semantic/`
4. Chờ tài nguyên được tạo xong, sau đó lưu lại Memory ID để dùng cho các bước sau.

### Hình minh họa

Tạo Memory trên giao diện:

![Bước tạo Memory 1](./images/image0.png)

Thiết lập các thông tin Memory và strategy:

![Bước tạo Memory 2](./images/image1.png)

Memory đã tạo thành công trên AWS Console:

![Memory đã sẵn sàng](./images/image2.png)

## 4. Chuẩn bị môi trường chạy local

Yêu cầu:

- Python 3.10+
- AWS CLI đã cấu hình (`aws configure`)
- Tài khoản AWS có quyền Bedrock AgentCore Memory
- Model Bedrock mặc định: `amazon.nova-lite-v1:0`

Cài đặt và chạy (PowerShell):

```powershell
cd lab2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python index.py
```

Nếu gặp lỗi `No module named 'dotenv'`, thường là do chưa kích hoạt đúng `.venv` hoặc chưa cài dependencies.

## 5. Cấu hình model Bedrock

Code ưu tiên đọc biến môi trường `BEDROCK_MODEL_ID`. Nếu không có, script dùng mặc định `amazon.nova-lite-v1:0`.

Ví dụ:

```powershell
$env:BEDROCK_MODEL_ID="amazon.nova-lite-v1:0"
python index.py
```

## 6. Luồng xử lý trong index.py

File `index.py` chạy theo flow chuẩn Lab 2:

1. Nạp biến môi trường và kết nối AWS theo region hiện tại.
2. Tạo hoặc dùng lại Memory resource `CustomerSupportMemory`.
3. Cấu hình 2 strategy (USER_PREFERENCE, SEMANTIC).
4. Seed lịch sử hội thoại mẫu vào memory bằng `create_event`.
5. Chờ Long-Term Memory xử lý bất đồng bộ.
6. Truy hồi memories từ 2 namespace.
7. Khởi tạo Strands Agent với `AgentCoreMemorySessionManager`.
8. Chạy 2 câu test personalization.

## 7. Giải thích output thường gặp

Nếu bạn thấy:

`Memory already exists. Using existing memory ID: ...`

thì là đúng, nghĩa là memory đã được tạo từ lần chạy trước và hệ thống tái sử dụng.

Nếu thấy `Memory ID của bạn là: None`, đó là lỗi lấy sai trường khi in. Bản code hiện tại đã sửa để in đúng `memory_id`.

## 8. Troubleshooting nhanh

1. `ModuleNotFoundError: No module named 'dotenv'`
- Kích hoạt lại `.venv`
- Chạy lại `pip install -r requirements.txt`

2. Region bị `None`
- Thiết lập `AWS_REGION` hoặc `AWS_DEFAULT_REGION`
- Hoặc chạy lại `aws configure`

3. Chưa thấy long-term memory ngay
- Đây là xử lý async, chờ thêm 30-60 giây
- Chạy lại script sau khi memory service ổn định

4. Lỗi quyền truy cập
- Kiểm tra IAM policy cho Bedrock AgentCore Memory và Bedrock model access

## 9. Bước tiếp theo

Sau khi Lab 2 chạy ổn, bạn có thể sang Lab 3 (Gateway + Identity) để mở rộng khả năng tích hợp tool doanh nghiệp an toàn hơn.

