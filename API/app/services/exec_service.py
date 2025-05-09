import os
import subprocess
import platform
import sys
from typing import Dict, Any, List, Union
from app.utils.common import handle_exceptions, logger
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()
SHELL_TIMEOUT = int(os.getenv("SHELL_TIMEOUT", "60"))  # Timeout mặc định 60 giây

@handle_exceptions
def execute_command(command: str, timeout: int = None, shell_type: str = None) -> Dict[str, Any]:
    """
    Thực thi lệnh shell/bash và trả về kết quả
    
    Params:
        command: Lệnh cần thực thi
        timeout: Thời gian chờ tối đa (giây)
        shell_type: Loại shell (cmd, powershell, bash)
    """
    logger.info(f"Executing command: {command}")
    
    # Nếu không chỉ định timeout, dùng giá trị mặc định
    if timeout is None:
        timeout = SHELL_TIMEOUT
    
    # Xác định shell dựa vào hệ điều hành và tham số
    system = platform.system().lower()
    
    shell_cmd = None
    if shell_type:
        if shell_type.lower() == "powershell":
            shell_cmd = f'powershell -Command "{command}"'
        elif shell_type.lower() == "cmd" and system == "windows":
            shell_cmd = f'cmd /c "{command}"'
        elif shell_type.lower() == "bash" and system != "windows":
            shell_cmd = f'bash -c "{command}"'
    
    if not shell_cmd:
        # Mặc định
        if system == "windows":
            shell_cmd = command
            shell = True  # Sử dụng cmd.exe trên Windows
        else:
            shell_cmd = command
            shell = True  # Sử dụng /bin/sh trên Unix/Linux
    else:
        shell = True
    
    # Thực thi lệnh
    try:
        process = subprocess.run(
            shell_cmd, 
            shell=shell, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            timeout=timeout
        )
        
        # Lấy kết quả
        return {
            "command": command,
            "return_code": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "success": process.returncode == 0,
            "system": system
        }
    except subprocess.TimeoutExpired:
        logger.error(f"Command execution timed out after {timeout} seconds: {command}")
        return {
            "command": command,
            "return_code": -1,
            "stdout": "",
            "stderr": f"Command execution timed out after {timeout} seconds",
            "success": False,
            "timed_out": True
        }
    except Exception as e:
        logger.error(f"Error executing command '{command}': {str(e)}")
        return {
            "command": command,
            "return_code": -1,
            "stdout": "",
            "stderr": str(e),
            "success": False
        }

@handle_exceptions
def execute_powershell(command: str, timeout: int = None) -> Dict[str, Any]:
    """
    Thực thi lệnh PowerShell (Windows) và trả về kết quả
    """
    logger.info(f"Executing PowerShell command: {command}")
    
    # Kiểm tra xem có phải Windows không
    if platform.system().lower() != "windows":
        return {
            "command": command,
            "return_code": -1,
            "stdout": "",
            "stderr": "PowerShell commands are only supported on Windows",
            "success": False
        }
    
    # Gọi hàm execute_command với shell_type là powershell
    return execute_command(command, timeout, shell_type="powershell")

@handle_exceptions
def execute_cmd(command: str, timeout: int = None) -> Dict[str, Any]:
    """
    Thực thi lệnh qua CMD (Windows) và trả về kết quả
    """
    logger.info(f"Executing CMD command: {command}")
    
    # Kiểm tra xem có phải Windows không
    if platform.system().lower() != "windows":
        return {
            "command": command,
            "return_code": -1,
            "stdout": "",
            "stderr": "CMD commands are only supported on Windows",
            "success": False
        }
    
    # Gọi hàm execute_command với shell_type là cmd
    return execute_command(command, timeout, shell_type="cmd")

@handle_exceptions
def execute_bash(command: str, timeout: int = None) -> Dict[str, Any]:
    """
    Thực thi lệnh qua Bash (Linux/macOS) và trả về kết quả
    """
    logger.info(f"Executing Bash command: {command}")
    
    # Kiểm tra xem có phải hệ điều hành Unix-like không
    if platform.system().lower() == "windows":
        return {
            "command": command,
            "return_code": -1,
            "stdout": "",
            "stderr": "Bash commands are only supported on Unix-like systems",
            "success": False
        }
    
    # Gọi hàm execute_command với shell_type là bash
    return execute_command(command, timeout, shell_type="bash")

@handle_exceptions
def get_system_info() -> Dict[str, Any]:
    """
    Lấy thông tin hệ thống
    """
    info = {
        "platform": platform.platform(),
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "processor": platform.processor(),
        "architecture": platform.architecture(),
        "python_version": platform.python_version(),
        "python_path": sys.executable,
        "current_dir": os.getcwd(),
        "user_home": os.path.expanduser("~"),
        "environment_vars": {k: v for k, v in os.environ.items() if not k.startswith("_")}
    }
    
    # Thêm thông tin cụ thể hệ điều hành
    if platform.system().lower() == "linux":
        # Lấy thông tin Linux distribution
        try:
            distro_info = execute_command("cat /etc/os-release")
            info["os_details"] = distro_info["stdout"]
        except:
            pass
    elif platform.system().lower() == "windows":
        # Lấy thêm thông tin Windows
        try:
            win_ver = platform.win32_ver()
            info["windows_version"] = {
                "version": win_ver[0],
                "build": win_ver[1],
                "service_pack": win_ver[2],
                "os_type": win_ver[3]
            }
            
            # Lấy danh sách ổ đĩa
            drives = []
            try:
                drive_result = execute_command("wmic logicaldisk get caption", shell_type="cmd")
                if drive_result["success"]:
                    drives = [line.strip() for line in drive_result["stdout"].split("\n") 
                             if line.strip() and "Caption" not in line]
            except:
                pass
            
            info["available_drives"] = drives
        except:
            pass
    
    return info 