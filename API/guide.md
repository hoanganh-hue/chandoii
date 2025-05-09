# Hướng dẫn sử dụng Remote Ops API System

## 1. Cài đặt

### Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Cài đặt ngrok
Nếu chưa cài đặt ngrok, hãy tải từ trang chủ https://ngrok.com và đảm bảo nó nằm trong PATH.

## 2. Cấu hình môi trường

File `.env` đã được tạo với các thông số:
```
PORT=8080
NGROK_AUTH_TOKEN=2rLzNrcOqbQVc9AiRMkcQeVFGjD_6Wkix5eeBiSscWBJwd2Cs
NGROK_URL=climbing-lioness-factual.ngrok-free.app
BASE_PATH=/
DISABLE_PATH_SECURITY=true
SHELL_TIMEOUT=300
DEBUG=true
```

## 3. Chạy ứng dụng

### Chạy với chức năng tự động cấu hình ngrok (Khuyến nghị)
```bash
python run.py
```

Script này sẽ:
- Tự động khởi động API server
- Tự động cấu hình và chạy ngrok
- Hiển thị thông tin endpoints và URL

### Chạy riêng lẻ các thành phần

Nếu muốn chạy riêng lẻ:

```bash
# Terminal 1: Chạy API server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080

# Terminal 2: Chạy ngrok
ngrok http --domain=climbing-lioness-factual.ngrok-free.app 8080
```

## 4. Sử dụng API

### Endpoint chính

- API chính: `https://climbing-lioness-factual.ngrok-free.app/`

### Thao tác file

- **Liệt kê thư mục**:
  ```
  GET /files/list?path=C:/
  ```

- **Lấy thông tin file**:
  ```
  GET /files/info?path=C:/file.txt
  ```

- **Tạo file mới**:
  ```
  POST /files/create/file
  Body: {"path": "C:/folder/file.txt", "content": "Nội dung file"}
  ```

- **Tạo thư mục mới**:
  ```
  POST /files/create/directory
  Body: {"path": "C:/folder/new_folder"}
  ```

- **Đọc file**:
  ```
  GET /files/read?path=C:/folder/file.txt
  ```

- **Di chuyển file/thư mục**:
  ```
  POST /files/move
  Body: {"source_path": "C:/folder/source.txt", "destination_path": "C:/folder/dest.txt"}
  ```

- **Sao chép file/thư mục**:
  ```
  POST /files/copy
  Body: {"source_path": "C:/folder/source.txt", "destination_path": "C:/folder/dest.txt"}
  ```

- **Xóa file/thư mục**:
  ```
  DELETE /files/delete?path=C:/folder/file.txt
  ```

### Quét và phân tích file

- **Quét file tự động**:
  ```
  POST /scan/read
  Body: {"path": "C:/folder/file.ext"}
  ```

- **Đọc file Word**:
  ```
  POST /scan/read/docx
  Body: {"path": "C:/folder/document.docx"}
  ```

- **Đọc file Excel**:
  ```
  POST /scan/read/excel
  Body: {"path": "C:/folder/spreadsheet.xlsx", "sheet_name": "Sheet1"}
  ```

- **Đọc file PDF**:
  ```
  POST /scan/read/pdf
  Body: {"path": "C:/folder/document.pdf"}
  ```

- **Đọc file CSV**:
  ```
  POST /scan/read/csv
  Body: {"path": "C:/folder/data.csv", "delimiter": ","}
  ```

- **Đọc file văn bản**:
  ```
  POST /scan/read/text
  Body: {"path": "C:/folder/text.txt"}
  ```

### Thực thi lệnh

- **Thực thi lệnh shell/bash**:
  ```
  POST /exec/cmd
  Body: {"command": "dir", "timeout": 30}
  ```

- **Thực thi lệnh PowerShell (Windows)**:
  ```
  POST /exec/powershell
  Body: {"command": "Get-Process", "timeout": 30}
  ```

- **Thực thi lệnh CMD (Windows)**:
  ```
  POST /exec/cmd/windows
  Body: {"command": "ipconfig /all", "timeout": 30}
  ```

- **Thực thi lệnh Bash (Linux/Mac)**:
  ```
  POST /exec/bash
  Body: {"command": "ls -la", "timeout": 30}
  ```

- **Lấy thông tin hệ thống**:
  ```
  GET /exec/system-info
  ```

## 5. Bảo mật

Hệ thống không có cơ chế xác thực, vì vậy hãy chỉ sử dụng trong môi trường đáng tin cậy. Nếu cần hạn chế quyền truy cập:

1. Sửa file `.env`:
   ```
   DISABLE_PATH_SECURITY=false
   BASE_PATH=C:/limited_folder
   ```

2. Khởi động lại ứng dụng

## 6. Gỡ lỗi

Kiểm tra log trong terminal để biết thêm thông tin về lỗi.

Nếu ngrok không kết nối được, hãy kiểm tra:
1. Token ngrok có hợp lệ không
2. Domain ngrok có khả dụng không
3. Cổng 8080 có đang được sử dụng bởi ứng dụng khác không

## 7. Gỡ cài đặt

Để gỡ cài đặt, dừng ứng dụng và xóa thư mục project. 