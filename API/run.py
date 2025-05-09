import os
import sys
import subprocess
import threading
import time
import signal
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Cấu hình
HOST = "0.0.0.0"
PORT = os.getenv("PORT", "8080")
NGROK_DOMAIN = os.getenv("NGROK_URL", "climbing-lioness-factual.ngrok-free.app")
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN", "2rLzNrcOqbQVc9AiRMkcQeVFGjD_6Wkix5eeBiSscWBJwd2Cs")

# Biến toàn cục để theo dõi các process
processes = []

def run_uvicorn():
    """Chạy Uvicorn server"""
    cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", HOST, "--port", PORT]
    print(f"Khởi động API server: {' '.join(cmd)}")
    process = subprocess.Popen(cmd)
    processes.append(process)
    return process

def run_ngrok():
    """Chạy ngrok tunnel"""
    # Cấu hình ngrok auth token nếu chưa cấu hình
    subprocess.run(["ngrok", "config", "add-authtoken", NGROK_AUTH_TOKEN], 
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Chạy ngrok với domain cố định
    cmd = ["ngrok", "http", "--domain", NGROK_DOMAIN, PORT]
    print(f"Khởi động ngrok: {' '.join(cmd)}")
    process = subprocess.Popen(cmd)
    processes.append(process)
    return process

def cleanup(signum=None, frame=None):
    """Dọn dẹp khi kết thúc"""
    print("\nĐang dừng các process...")
    for process in processes:
        try:
            if sys.platform == "win32":
                process.kill()
            else:
                process.terminate()
        except:
            pass
    sys.exit(0)

def display_info():
    """Hiển thị thông tin kết nối"""
    print("\n" + "="*50)
    print(f"API đang chạy tại địa chỉ nội bộ: http://{HOST}:{PORT}")
    print(f"API được public qua ngrok: https://{NGROK_DOMAIN}")
    print("="*50)
    print("\nÁp dụng các đường dẫn API:")
    print("✅ GET  /                     - API chính")
    print("✅ GET  /files/list?path=C:/  - Liệt kê thư mục")
    print("✅ GET  /files/info?path=C:/file.txt - Thông tin file")
    print("✅ POST /files/create/file    - Tạo file")
    print("✅ POST /files/create/directory - Tạo thư mục")
    print("✅ GET  /files/read?path=C:/file.txt - Đọc file")
    print("✅ POST /files/move           - Di chuyển file/thư mục")
    print("✅ POST /files/copy           - Sao chép file/thư mục")
    print("✅ DEL  /files/delete?path=C:/file.txt - Xóa file/thư mục")
    print("✅ POST /scan/read            - Quét & phân tích file tự động")
    print("✅ POST /scan/read/docx       - Đọc file Word")
    print("✅ POST /scan/read/excel      - Đọc file Excel")
    print("✅ POST /scan/read/pdf        - Đọc file PDF")
    print("✅ POST /scan/read/csv        - Đọc file CSV")
    print("✅ POST /scan/read/text       - Đọc file văn bản")
    print("✅ POST /exec/cmd             - Thực thi lệnh shell/bash")
    print("✅ POST /exec/powershell      - Thực thi lệnh PowerShell")
    print("✅ POST /exec/cmd/windows     - Thực thi lệnh CMD")
    print("✅ POST /exec/bash            - Thực thi lệnh Bash")
    print("✅ GET  /exec/system-info     - Lấy thông tin hệ thống")
    print("="*50)
    print("\nỨng dụng đã sẵn sàng sử dụng! Nhấn Ctrl+C để dừng.")
    print("="*50 + "\n")

def main():
    # Đăng ký signal handler để dọn dẹp khi kết thúc
    if sys.platform != "win32":
        signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)
    
    try:
        # Khởi động Uvicorn
        uvicorn_process = run_uvicorn()
        
        # Đợi Uvicorn khởi động
        time.sleep(2)
        
        # Khởi động ngrok
        ngrok_process = run_ngrok()
        
        # Hiển thị thông tin
        time.sleep(3)
        display_info()
        
        # Giữ cho script chạy
        uvicorn_process.wait()
    except KeyboardInterrupt:
        cleanup()
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        cleanup()

if __name__ == "__main__":
    main() 