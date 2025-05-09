import os
import pathlib
from typing import Union, Dict, Any
from fastapi import HTTPException
import logging
from dotenv import load_dotenv

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("remote-ops-api")

# Load biến môi trường
load_dotenv()
BASE_PATH = os.getenv("BASE_PATH", "/")
DISABLE_PATH_SECURITY = os.getenv("DISABLE_PATH_SECURITY", "false").lower() == "true"

def normalize_path(path: str) -> str:
    """
    Chuẩn hóa đường dẫn và đảm bảo nằm trong BASE_PATH
    """
    # Chuyển đổi dấu / thành dấu \ trên Windows nếu cần
    path = os.path.normpath(path)
    
    # Nếu là đường dẫn tương đối, thêm BASE_PATH
    if not os.path.isabs(path):
        path = os.path.join(BASE_PATH, path)
    
    # Chuyển đổi thành đường dẫn tuyệt đối
    abs_path = os.path.abspath(path)
    
    # Kiểm tra xem đường dẫn có nằm trong BASE_PATH không - chỉ kiểm tra nếu không disabled security
    if not DISABLE_PATH_SECURITY and not abs_path.startswith(BASE_PATH):
        logger.warning(f"Access attempt outside of BASE_PATH: {path}")
        raise HTTPException(
            status_code=403, 
            detail=f"Path {path} is outside of allowed base directory"
        )
    
    return abs_path

def handle_exceptions(func):
    """
    Decorator để xử lý các ngoại lệ chung
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            # Truyền qua HTTPException
            raise
        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
        except PermissionError as e:
            logger.error(f"Permission denied: {str(e)}")
            raise HTTPException(status_code=403, detail=f"Permission denied: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    return wrapper

def create_response(status: bool, message: str, data: Any = None) -> Dict[str, Any]:
    """
    Tạo response chuẩn cho API
    """
    response = {
        "success": status,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
        
    return response 