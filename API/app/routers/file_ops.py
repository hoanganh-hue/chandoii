from fastapi import APIRouter, Path, Query, Body, HTTPException
from typing import Optional, List, Dict, Any
from app.services import file_service
from app.utils.common import create_response
from pydantic import BaseModel

router = APIRouter()

class FileCreateRequest(BaseModel):
    path: str
    content: Optional[str] = ""

class DirectoryCreateRequest(BaseModel):
    path: str

class FileOperationRequest(BaseModel):
    path: str

class FileMoveRequest(BaseModel):
    source_path: str
    destination_path: str

@router.get("/list", summary="Liệt kê nội dung thư mục")
async def list_directory(path: str = Query(..., description="Đường dẫn đến thư mục cần liệt kê")):
    """
    Liệt kê tất cả các file và thư mục trong đường dẫn được chỉ định.
    """
    result = file_service.list_dir(path)
    return create_response(True, "Directory listed successfully", result)

@router.post("/create/file", summary="Tạo file mới")
async def create_file(request: FileCreateRequest):
    """
    Tạo một file mới với nội dung tùy chọn.
    """
    result = file_service.create_file(request.path, request.content)
    return create_response(True, "File created successfully", result)

@router.post("/create/directory", summary="Tạo thư mục mới")
async def create_directory(request: DirectoryCreateRequest):
    """
    Tạo một thư mục mới.
    """
    result = file_service.create_directory(request.path)
    return create_response(True, "Directory created successfully", result)

@router.get("/read", summary="Đọc nội dung file")
async def read_file(path: str = Query(..., description="Đường dẫn đến file cần đọc")):
    """
    Đọc và trả về nội dung của file.
    """
    result = file_service.read_file(path)
    return create_response(True, "File read successfully", result)

@router.delete("/delete", summary="Xóa file hoặc thư mục")
async def delete_item(path: str = Query(..., description="Đường dẫn đến file/thư mục cần xóa")):
    """
    Xóa file hoặc thư mục được chỉ định.
    """
    result = file_service.delete_item(path)
    return create_response(True, f"{result['type']} deleted successfully", result)

@router.post("/move", summary="Di chuyển file hoặc thư mục")
async def move_item(request: FileMoveRequest):
    """
    Di chuyển file hoặc thư mục từ vị trí nguồn đến đích.
    """
    result = file_service.move_item(request.source_path, request.destination_path)
    return create_response(True, f"{result['type']} moved successfully", result)

@router.post("/copy", summary="Sao chép file hoặc thư mục")
async def copy_item(request: FileMoveRequest):
    """
    Sao chép file hoặc thư mục từ vị trí nguồn đến đích.
    """
    result = file_service.copy_item(request.source_path, request.destination_path)
    return create_response(True, f"{result['type']} copied successfully", result)

@router.get("/info", summary="Lấy thông tin chi tiết về file/thư mục")
async def get_file_info(path: str = Query(..., description="Đường dẫn đến file/thư mục cần lấy thông tin")):
    """
    Lấy thông tin chi tiết về file hoặc thư mục.
    """
    result = file_service.get_file_info(path)
    return create_response(True, "File info retrieved successfully", result) 