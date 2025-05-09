# Remote Ops API System

Hệ thống API cho phép thực thi các thao tác trên máy chủ từ xa thông qua các lệnh HTTP.

## Tính năng chính

* **File Operations**: di chuyển, mở, xóa, tạo file và thư mục từ xa
* **Data Scanning & Analysis**: quét, đọc và phân tích dữ liệu từ nhiều định dạng file
* **Command Execution**: chạy lệnh shell hoặc PowerShell trực tiếp trên server

## Cài đặt

1. **Clone repository**

```bash
git clone https://github.com/yourusername/remote-ops-api.git
cd remote-ops-api
```

2. **Tạo môi trường ảo Python**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Cài đặt các thư viện**

```bash
pip install -r requirements.txt
```

4. **Cấu hình ngrok**

Tạo tài khoản ngrok và lấy auth token từ [ngrok.com](https://ngrok.com).
Cấu hình token:

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

5. **Tạo file .env**

```
NGROK_AUTH_TOKEN=your_token_here
NGROK_URL=your_ngrok_url
BASE_PATH=/path/to/base/directory
```

## Chạy ứng dụng

1. **Khởi động API server**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

2. **Chạy ngrok để expose API**

```bash
ngrok http 8000
```

3. **Truy cập API**

- API Docs: `http://localhost:8000/docs`
- Ngrok URL: URL từ terminal ngrok

## Sử dụng API

### Ví dụ

1. **Tạo thư mục**

```bash
curl -X POST http://localhost:8000/files/create/directory -H "Content-Type: application/json" -d '{"path": "/đường/dẫn/thư-mục-mới"}'
```

2. **Đọc file Excel**

```bash
curl -X POST http://localhost:8000/scan/read/excel -H "Content-Type: application/json" -d '{"path": "/đường/dẫn/file.xlsx"}'
```

3. **Chạy lệnh shell**

```bash
curl -X POST http://localhost:8000/exec/cmd -H "Content-Type: application/json" -d '{"command": "ls -la"}'
```

## Cấu trúc dự án

```
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
│   │   └── exec_service.py # Logic chạy lệnh shell/PowerShell
│   └── utils/
│       └── common.py       # Các hàm/wrapper chung
├── .env                    # Cấu hình môi trường
├── requirements.txt        # Danh sách thư viện Python
└── README.md               # Tài liệu này
```

## Lưu ý bảo mật

Hệ thống này không có cơ chế xác thực (authentication), chỉ nên sử dụng trong môi trường đáng tin cậy hoặc cho mục đích cá nhân. 