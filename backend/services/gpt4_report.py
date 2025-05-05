import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_damage_report(detections: list, ndvi_url: str = None) -> str:
    """
    detections: [
        {"class": 0, "confidence": 0.92, "bbox": [x1, y1, x2, y2]},
        ...
    ]
    """
    prompt = "You are an AI field analyst. Analyze the following detection data:\n\n"

    for i, det in enumerate(detections):
        prompt += f"Detection {i+1}:\n"
        prompt += f"- Class ID: {det['class']}\n"
        prompt += f"- Confidence: {det['confidence']:.2f}\n"
        prompt += f"- Bounding Box: {det['bbox']}\n\n"

    if ndvi_url:
        prompt += f"Also consider the vegetation index image available at: {ndvi_url}\n\n"

    prompt += (
        "Based on this data, write a detailed and professional 2-paragraph report summarizing the level of "
        "damage, types of features detected, and any geographical implications. Keep it clear and field-ready."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content
