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

@app.get("/")
def read_root():
    return {"message": "Welcome to Remote Ops API"} 