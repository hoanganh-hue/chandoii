from fastapi import APIRouter, Query, Body, HTTPException
from typing import Optional, Dict, Any
from app.services import scan_service
from app.utils.common import create_response
from pydantic import BaseModel

router = APIRouter()

class ScanFileRequest(BaseModel):
    path: str
    sheet_name: Optional[str] = None
    delimiter: Optional[str] = ","

@router.post("/read", summary="Đọc và phân tích file")
async def read_file_auto(request: ScanFileRequest):
    """
    Tự động nhận diện loại file và đọc nội dung với phương thức thích hợp.
    Hỗ trợ các định dạng: DOCX, XLSX, PDF, CSV, TXT, và nhiều loại file văn bản khác.
    """
    result = scan_service.read_file_auto(request.path)
    return create_response(True, "File analyzed successfully", result)

@router.post("/read/docx", summary="Đọc file Word")
async def read_docx(request: ScanFileRequest):
    """
    Đọc và phân tích file Microsoft Word (.docx).
    Trả về văn bản, nội dung và cấu trúc bảng.
    """
    result = scan_service.read_docx(request.path)
    return create_response(True, "Word document analyzed successfully", result)

@router.post("/read/excel", summary="Đọc file Excel")
async def read_excel(request: ScanFileRequest):
    """
    Đọc và phân tích file Microsoft Excel (.xlsx, .xls).
    Nếu không chỉ định sheet_name, sẽ đọc sheet đầu tiên.
    """
    result = scan_service.read_excel(request.path, request.sheet_name)
    return create_response(True, "Excel document analyzed successfully", result)

@router.post("/read/pdf", summary="Đọc file PDF")
async def read_pdf(request: ScanFileRequest):
    """
    Đọc và phân tích file PDF.
    Trả về thông tin metadata và nội dung text từ mỗi trang.
    """
    result = scan_service.read_pdf(request.path)
    return create_response(True, "PDF document analyzed successfully", result)

@router.post("/read/csv", summary="Đọc file CSV")
async def read_csv(request: ScanFileRequest):
    """
    Đọc và phân tích file CSV.
    Có thể chỉ định delimiter (mặc định là dấu phẩy).
    """
    result = scan_service.read_csv(request.path, request.delimiter)
    return create_response(True, "CSV file analyzed successfully", result)

@router.post("/read/text", summary="Đọc file văn bản")
async def read_text(request: ScanFileRequest):
    """
    Đọc file văn bản thông thường (.txt, .md, .py, .java, .html, ...).
    """
    result = scan_service.read_text_file(request.path)
    return create_response(True, "Text file analyzed successfully", result) 