import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Union
from app.utils.common import normalize_path, handle_exceptions, logger

@handle_exceptions
def list_dir(path: str) -> List[Dict[str, Any]]:
    """
    Liệt kê nội dung thư mục
    """
    norm_path = normalize_path(path)
    
    if not os.path.exists(norm_path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    if not os.path.isdir(norm_path):
        raise ValueError(f"Path is not a directory: {path}")
    
    items = []
    for item in os.listdir(norm_path):
        item_path = os.path.join(norm_path, item)
        item_info = {
            "name": item,
            "path": item_path,
            "type": "file" if os.path.isfile(item_path) else "directory",
            "size": os.path.getsize(item_path) if os.path.isfile(item_path) else None,
            "modified": os.path.getmtime(item_path)
        }
        items.append(item_info)
    
    return items

@handle_exceptions
def create_file(path: str, content: str = "") -> Dict[str, Any]:
    """
    Tạo file mới với nội dung
    """
    norm_path = normalize_path(path)
    
    # Kiểm tra xem thư mục cha có tồn tại không
    parent_dir = os.path.dirname(norm_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    
    # Tạo file
    with open(norm_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return {
        "path": norm_path,
        "size": len(content),
        "created": True
    }

@handle_exceptions
def create_directory(path: str) -> Dict[str, Any]:
    """
    Tạo thư mục mới
    """
    norm_path = normalize_path(path)
    
    if os.path.exists(norm_path):
        if os.path.isdir(norm_path):
            return {"path": norm_path, "created": False, "message": "Directory already exists"}
        else:
            raise ValueError(f"Path exists but is not a directory: {path}")
    
    os.makedirs(norm_path)
    
    return {
        "path": norm_path,
        "created": True
    }

@handle_exceptions
def read_file(path: str) -> Dict[str, Any]:
    """
    Đọc nội dung file
    """
    norm_path = normalize_path(path)
    
    if not os.path.exists(norm_path):
        raise FileNotFoundError(f"File does not exist: {path}")
    
    if not os.path.isfile(norm_path):
        raise ValueError(f"Path is not a file: {path}")
    
    # Đọc nội dung file
    with open(norm_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        "path": norm_path,
        "size": os.path.getsize(norm_path),
        "content": content
    }

@handle_exceptions
def read_file_binary(path: str) -> bytes:
    """
    Đọc nội dung file dưới dạng binary
    """
    norm_path = normalize_path(path)
    
    if not os.path.exists(norm_path):
        raise FileNotFoundError(f"File does not exist: {path}")
    
    if not os.path.isfile(norm_path):
        raise ValueError(f"Path is not a file: {path}")
    
    # Đọc nội dung file dưới dạng binary
    with open(norm_path, 'rb') as f:
        content = f.read()
    
    return content

@handle_exceptions
def delete_item(path: str) -> Dict[str, Any]:
    """
    Xóa file hoặc thư mục
    """
    norm_path = normalize_path(path)
    
    if not os.path.exists(norm_path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    if os.path.isfile(norm_path):
        os.remove(norm_path)
        item_type = "file"
    else:
        shutil.rmtree(norm_path)
        item_type = "directory"
    
    return {
        "path": norm_path,
        "deleted": True,
        "type": item_type
    }

@handle_exceptions
def move_item(src_path: str, dst_path: str) -> Dict[str, Any]:
    """
    Di chuyển file hoặc thư mục
    """
    norm_src = normalize_path(src_path)
    norm_dst = normalize_path(dst_path)
    
    if not os.path.exists(norm_src):
        raise FileNotFoundError(f"Source path does not exist: {src_path}")
    
    # Kiểm tra xem thư mục cha của destination có tồn tại không
    parent_dir = os.path.dirname(norm_dst)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    
    # Di chuyển item
    shutil.move(norm_src, norm_dst)
    
    return {
        "source": norm_src,
        "destination": norm_dst,
        "moved": True,
        "type": "file" if os.path.isfile(norm_dst) else "directory"
    }

@handle_exceptions
def copy_item(src_path: str, dst_path: str) -> Dict[str, Any]:
    """
    Sao chép file hoặc thư mục
    """
    norm_src = normalize_path(src_path)
    norm_dst = normalize_path(dst_path)
    
    if not os.path.exists(norm_src):
        raise FileNotFoundError(f"Source path does not exist: {src_path}")
    
    # Kiểm tra xem thư mục cha của destination có tồn tại không
    parent_dir = os.path.dirname(norm_dst)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    
    # Sao chép item
    if os.path.isfile(norm_src):
        shutil.copy2(norm_src, norm_dst)
        item_type = "file"
    else:
        shutil.copytree(norm_src, norm_dst)
        item_type = "directory"
    
    return {
        "source": norm_src,
        "destination": norm_dst,
        "copied": True,
        "type": item_type
    }

@handle_exceptions
def get_file_info(path: str) -> Dict[str, Any]:
    """
    Lấy thông tin chi tiết về file/thư mục
    """
    norm_path = normalize_path(path)
    
    if not os.path.exists(norm_path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    stat_info = os.stat(norm_path)
    
    info = {
        "path": norm_path,
        "name": os.path.basename(norm_path),
        "type": "file" if os.path.isfile(norm_path) else "directory",
        "size": stat_info.st_size if os.path.isfile(norm_path) else None,
        "created": stat_info.st_ctime,
        "modified": stat_info.st_mtime,
        "accessed": stat_info.st_atime,
        "permissions": stat_info.st_mode
    }
    
    return info 