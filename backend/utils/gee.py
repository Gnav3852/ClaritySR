import ee
import os

if not ee.data._initialized:
    ee.Initialize() 

def get_ndvi_image(bbox: list, date: str = "2023-01-01") -> dict:
    """
    bbox: [x1, y1, x2, y2]
    Returns: download URL or image metadata
    """
    x1, y1, x2, y2 = bbox
    region = ee.Geometry.Rectangle([x1, y1, x2, y2])

    collection = (
        ee.ImageCollection("COPERNICUS/S2")
        .filterDate(date, "2023-12-31")
        .filterBounds(region)
        .sort("CLOUDY_PIXEL_PERCENTAGE")
    )

    image = collection.first().normalizedDifference(["B8", "B4"]).rename("NDVI")

    url = image.getThumbURL({
        "min": 0.0,
        "max": 1.0,
        "region": region.coordinates(),
        "dimensions": 512,
        "format": "png",
        "palette": ["white", "green"]
    })

    return {
        "bbox": bbox,
        "ndvi_url": url
    }
