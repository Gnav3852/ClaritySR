import torch
from torchvision import transforms
from torchvision.models.segmentation import deeplabv3_resnet101
from PIL import Image
import os
from ultralytics import YOLO

device = "cuda" if torch.cuda.is_available() else "cpu"

yolo_model = YOLO("yolov8n.pt")  
deeplab_model = deeplabv3_resnet101(pretrained=True).to(device).eval()

def detect_damage(image_path: str) -> dict:
    results = {}


    yolo_preds = yolo_model(image_path)
    detections = []
    for box in yolo_preds[0].boxes.data:
        x1, y1, x2, y2, conf, cls = box.tolist()
        detections.append({
            "bbox": [x1, y1, x2, y2],
            "confidence": conf,
            "class": int(cls)
        })
    results["yolo_detections"] = detections


    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor()
    ])
    input_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = deeplab_model(input_tensor)['out'][0]
    seg_mask = output.argmax(0).byte().cpu().numpy()


    seg_out_path = image_path.replace(".png", "_mask.png")
    Image.fromarray(seg_mask * 255).convert("L").save(seg_out_path)
    results["deeplab_mask"] = seg_out_path

    return results
