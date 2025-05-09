from fastapi import APIRouter, Query, Body, HTTPException
from typing import Optional, Dict, Any
from app.services import exec_service
from app.utils.common import create_response
from pydantic import BaseModel

router = APIRouter()

class CommandRequest(BaseModel):
    command: str
    timeout: Optional[int] = None

@router.post("/cmd", summary="Thực thi lệnh shell/bash")
async def execute_command(request: CommandRequest):
    """
    Thực thi lệnh shell/bash và trả về kết quả.
    Ví dụ: ls -la, cat file.txt, mkdir folder, ...
    """
    result = exec_service.execute_command(request.command, request.timeout)
    
    message = "Command executed successfully"
    if not result["success"]:
        message = "Command execution failed"
    
    return create_response(result["success"], message, result)

@router.post("/powershell", summary="Thực thi lệnh PowerShell (Windows)")
async def execute_powershell(request: CommandRequest):
    """
    Thực thi lệnh PowerShell (chỉ trên hệ điều hành Windows) và trả về kết quả.
    Ví dụ: Get-Process, Get-ChildItem, New-Item, ...
    """
    result = exec_service.execute_powershell(request.command, request.timeout)
    
    message = "PowerShell command executed successfully"
    if not result["success"]:
        message = "PowerShell command execution failed"
    
    return create_response(result["success"], message, result)

@router.post("/cmd/windows", summary="Thực thi lệnh CMD (Windows)")
async def execute_cmd(request: CommandRequest):
    """
    Thực thi lệnh CMD (chỉ trên hệ điều hành Windows) và trả về kết quả.
    Ví dụ: dir, type file.txt, ...
    """
    result = exec_service.execute_cmd(request.command, request.timeout)
    
    message = "CMD command executed successfully"
    if not result["success"]:
        message = "CMD command execution failed"
    
    return create_response(result["success"], message, result)

@router.post("/bash", summary="Thực thi lệnh Bash (Unix/Linux)")
async def execute_bash(request: CommandRequest):
    """
    Thực thi lệnh Bash (chỉ trên hệ điều hành Unix/Linux) và trả về kết quả.
    Ví dụ: ls -la, cat file.txt, mkdir folder, ...
    """
    result = exec_service.execute_bash(request.command, request.timeout)
    
    message = "Bash command executed successfully"
    if not result["success"]:
        message = "Bash command execution failed"
    
    return create_response(result["success"], message, result)

@router.get("/system-info", summary="Lấy thông tin hệ thống")
async def get_system_info():
    """
    Lấy thông tin chi tiết về hệ thống đang chạy API.
    """
    result = exec_service.get_system_info()
    return create_response(True, "System information retrieved successfully", result) 