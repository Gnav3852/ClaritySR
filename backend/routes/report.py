from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Optional
from services.gpt4_report import generate_damage_report

router = APIRouter()

class Detection(BaseModel):
    class_id: int
    confidence: float
    bbox: List[float]  

class ReportRequest(BaseModel):
    detections: List[Detection]
    ndvi_url: Optional[str] = None

@router.post("/")
def get_report(payload: ReportRequest):
   
    formatted = [
        {"class": d.class_id, "confidence": d.confidence, "bbox": d.bbox}
        for d in payload.detections
    ]
    
    report = generate_damage_report(formatted, payload.ndvi_url)
    return {"report": report}
