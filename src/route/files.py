from fastapi import File, UploadFile, APIRouter
from fastapi.responses import FileResponse
import os
import shutil

upload_folder = "uploads"

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "location": file_path}


@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(upload_folder, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}