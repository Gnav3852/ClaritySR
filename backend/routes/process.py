from fastapi import APIRouter, File, UploadFile
from services.super_resolve import enhance_image
from services.damage_detect import detect_damage
from services.gpt4_report import generate_damage_report
from utils.s3 import upload_to_s3
from utils.gee import get_ndvi_image
from utils.postgis import insert_detection

import os

router = APIRouter()

@router.post("/")
async def process_image(file: UploadFile = File(...)):
  
    raw_path = f"/tmp/{file.filename}"
    with open(raw_path, "wb") as f:
        f.write(await file.read())
    raw_url = upload_to_s3(raw_path, bucket="raw-images")

   
    enhanced_path = enhance_image(raw_path)
    enhanced_url = upload_to_s3(enhanced_path, bucket="enhanced-images")

    
    detections = detect_damage(enhanced_path)
    yolo_data = detections["yolo_detections"]
    mask_url = upload_to_s3(detections["deeplab_mask"], bucket="masks")

   
    if yolo_data:
        ndvi_overlay = get_ndvi_image(yolo_data[0]["bbox"])
        ndvi_url = ndvi_overlay["ndvi_url"]
    else:
        ndvi_url = None


    for d in yolo_data:
        insert_detection(enhanced_url, mask_url, d["bbox"], d["class"], d["confidence"])

    report = generate_damage_report(yolo_data, ndvi_url)

    return {
        "raw_url": raw_url,
        "enhanced_url": enhanced_url,
        "mask_url": mask_url,
        "ndvi_url": ndvi_url,
        "report": report,
        "detections": yolo_data
    }
