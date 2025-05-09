# Remote Ops API System

## 1. Giới thiệu

Tài liệu này hướng dẫn chi tiết cách xây dựng một hệ thống API cho phép bạn thực thi các thao tác trên máy chủ từ xa thông qua các lệnh HTTP gửi đến URL cố định (được expose qua ngrok). Hệ thống sẽ hỗ trợ:

* **File Operations**: di chuyển, mở, xóa, tạo file và thư mục ở bất kỳ vị trí nào trên server.
* **Data Scanning & Analysis**: quét, đọc và phân tích dữ liệu từ nhiều định dạng file văn phòng (Word, Excel, PDF...) và mã nguồn (HTML, CSS, Java, Kotlin...).
* **Command Execution**: chạy lệnh shell (bash) hoặc PowerShell trực tiếp trên server.

> **Chú ý**: Hệ thống này không có cơ chế xác thực (authentication), chỉ sử dụng riêng cho mục đích cá nhân.

---

## 2. Ngôn ngữ & Thư viện

* **Ngôn ngữ**: Python 3.10+
* **Web Framework**: FastAPI
* **Server**: Uvicorn
* **Tunnel**: ngrok

### Các thư viện chính

| Tính năng        | Thư viện                                              |
| ---------------- | ----------------------------------------------------- |
| Web API          | `fastapi`, `uvicorn`                                  |
| File ops         | tiêu chuẩn `os`, `shutil`, `pathlib`                  |
| Quét & phân tích | `python-docx`, `openpyxl`, `PyPDF2`, `tika`, `pandas` |
| Command exec     | tiêu chuẩn `subprocess`                               |
| Biến môi trường  | `python-dotenv`                                       |

---

## 3. Cấu trúc thư mục

```text
remote-ops-api/
├── app/
│   ├── main.py             # Khởi tạo FastAPI, include routers
│   ├── routers/
│   │   ├── file_ops.py     # Endpoints File Operations
│   │   ├── scan_ops.py     # Endpoints Data Scanning
│   │   └── exec_ops.py     # Endpoints Command Execution
│   ├── services/
│   │   ├── file_service.py # Logic thao tác file & thư mục
│   │   ├── scan_service.py # Logic quét & phân tích file
│   │   └── exec_service.py # Logic chạy lệnh shell/Powershell
│   └── utils/
│       └── common.py       # Các hàm/wrapper chung
├── .env                    # Cấu hình môi trường (NGROK_URL, PATH gốc...)
├── requirements.txt        # Danh sách thư viện Python
└── README.md               # Tài liệu hướng dẫn này
```

---

## 4. Thiết lập môi trường

1. **Clone repo**

   ```bash
   git clone https://github.com/yourusername/remote-ops-api.git
   cd remote-ops-api
   ```

2. **Tạo virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\\Scripts\\activate  # Windows (PowerShell)
   ```

3. **Cài đặt dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Cấu hình biến môi trường** Tạo file `.env` với nội dung:

   ```dotenv
  ngrok config add-authtoken 2rLzNrcOqbQVc9AiRMkcQeVFGjD_6Wkix5eeBiSscWBJwd2Cs

ngrok http --url=climbing-lioness-factual.ngrok-free.app 
   BASE_PATH=/home/username        # Thư mục gốc thao tác file
   ```

5. **Chạy ngrok**

   ```bash
   ngrok http 8000
   # copy URL HTTPS, dán vào NGROK_URL
   ```

6. **Khởi động API server**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

## 5. Nội dung chi tiết từng file

### 5.1 `app/main.py`

```python
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.routers import file_ops, scan_ops, exec_ops

load_dotenv()
app = FastAPI(title="Remote Ops API")

# Đăng ký các router
app.include_router(file_ops.router, prefix="/files", tags=["FileOps"])
app.include_router(scan_ops.router, prefix="/scan", tags=["ScanOps"])
app.include_router(exec_ops.router, prefix="/exec", tags=["ExecOps"])
```

### 5.2 `app/routers/file_ops.py`

* Các endpoint: `POST /create`, `DELETE /delete`, `GET /list`, `POST /move`...
* Sử dụng `file_service.py` để thực thi.

### 5.3 `app/services/file_service.py`

* Hàm `create_file(path)`, `delete_file(path)`, `move(path_src, path_dst)`, `list_dir(path)`...
* Dùng `os`, `shutil`, `pathlib`.

### 5.4 `app/routers/scan_ops.py` & `app/services/scan_service.py`

* Endpoint `POST /read` đọc file theo đường dẫn và định dạng:

  * Word: `python-docx`
  * Excel: `openpyxl` + `pandas`
  * PDF: `PyPDF2` hoặc `tika`
* Trả về JSON chứa nội dung/text thô.

### 5.5 `app/routers/exec_ops.py` & `app/services/exec_service.py`

* Endpoint `POST /cmd` nhận JSON `{ "command": "ls -la" }` hoặc PowerShell.
* Dùng `subprocess.run(..., shell=True)` để chạy.
* Trả về stdout và stderr.

### 5.6 `app/utils/common.py`

* Hàm parse path an toàn, wrapper xử lý lỗi, logging.

---

## 6. Ví dụ sử dụng API

1. **Tạo thư mục**

   ```bash
   curl -X POST $NGROK_URL/files/create -H 'Content-Type: application/json' \
     -d '{"path": "/home/username/new_folder"}'
   ```

2. **Đọc file Excel**

   ```bash
   curl -X POST $NGROK_URL/scan/read -H 'Content-Type: application/json' \
     -d '{"path": "/home/username/data.xlsx"}'
   ```

3. **Chạy lệnh shell**

   ```bash
   curl -X POST $NGROK_URL/exec/cmd -H 'Content-Type: application/json' \
     -d '{"command": "apt update && apt install jq -y"}'
   ```

---

## 7. Lưu ý bảo mật

* **Chỉ dùng cho mục đích cá nhân**, không expose public.
* Đảm bảo server chỉ mở cổng 8000 và chỉ chạy ngrok trong phiên làm việc.
* Có thể bổ sung Basic Auth hoặc token nếu cần mở rộng.

---

## 8. Kết luận

Với hướng dẫn trên, bạn đã có một hệ thống API toàn diện để thực thi thao tác file, quét dữ liệu và chạy lệnh từ xa trên server của mình. Chúc bạn thành công!
