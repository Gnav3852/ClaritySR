from fastapi import APIRouter, File, UploadFile
from services.super_resolve import enhance_image
from utils.s3 import upload_to_s3

router = APIRouter()

@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    # Save original
    raw_path = f"/tmp/{file.filename}"
    with open(raw_path, "wb") as f:
        f.write(await file.read())

    # Upload raw image to S3
    raw_url = upload_to_s3(raw_path, bucket="raw-images")

    # Run super-resolution
    enhanced_path = enhance_image(raw_path)

    # Upload enhanced to S3
    enhanced_url = upload_to_s3(enhanced_path, bucket="enhanced-images")

    return {"raw_url": raw_url, "enhanced_url": enhanced_url}
