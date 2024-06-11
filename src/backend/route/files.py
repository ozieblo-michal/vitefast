import os
import shutil
import boto3

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

upload_folder = "uploads"

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed_extensions = {"txt", "csv", "jpg", "png", "pdf"}

    if file.filename.split(".")[-1] not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file extension.")

    contents = await file.read()
    file_size = len(contents)

    file.file.seek(0)

    if file_size > 2 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File size too large (up to 2 MB).")

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

@router.post("/uploads3/")
async def upload_to_s3(file: UploadFile = File(...)):
    allowed_extensions = {"txt", "csv", "jpg", "png", "pdf"}

    if file.filename.split(".")[-1] not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file extension.")

    bucket_name = os.getenv("S3_BUCKET_NAME")
    file_name_in_s3 = "folder/" + file.filename
    content = await file.read()

    file_size = len(content)

    file.file.seek(0)

    if file_size > 2 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File size too large (up to 2 MB).")

    if os.getenv("USE_LOCALSTACK") == "true":
        s3 = boto3.client(
            "s3",
            endpoint_url="http://localhost:4566",
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
    else:
        s3 = boto3.client("s3")

    s3.put_object(Bucket=bucket_name, Key=file_name_in_s3, Body=content)

    return {"message": "The file has been successfully uploaded to S3"}

@router.get("/download_s3/{filename}")
async def download_from_s3(filename: str):
    bucket_name = os.getenv("S3_BUCKET_NAME")
    file_name_in_s3 = "folder/" + filename

    if os.getenv("USE_LOCALSTACK") == "true":
        s3 = boto3.client(
            "s3",
            endpoint_url="http://localhost:4566",
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
    else:
        s3 = boto3.client("s3")

    try:
        s3_response = s3.get_object(Bucket=bucket_name, Key=file_name_in_s3)
        return StreamingResponse(s3_response['Body'], media_type='application/octet-stream', headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })
    except s3.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found in S3")

@router.get("/list_s3_files")
async def list_s3_files():
    bucket_name = os.getenv("S3_BUCKET_NAME")

    if os.getenv("USE_LOCALSTACK") == "true":
        s3 = boto3.client(
            "s3",
            endpoint_url="http://localhost:4566",
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
    else:
        s3 = boto3.client("s3")

    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix="folder/")
        files = [obj['Key'].split("folder/")[1] for obj in response.get('Contents', [])]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
