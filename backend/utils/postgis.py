import psycopg2
import os
from psycopg2.extras import RealDictCursor

POSTGIS_CONN = {
    "dbname": os.getenv("POSTGIS_DB", "geo"),
    "user": os.getenv("POSTGIS_USER", "postgres"),
    "password": os.getenv("POSTGIS_PASSWORD", ""),
    "host": os.getenv("POSTGIS_HOST", "localhost"),
    "port": os.getenv("POSTGIS_PORT", 5432)
}

def connect():
    return psycopg2.connect(**POSTGIS_CONN, cursor_factory=RealDictCursor)

def insert_detection(image_url, mask_url, bbox_coords, class_id, confidence):
    """
    bbox_coords: [x1, y1, x2, y2] → will be used to create a polygon
    """
    x1, y1, x2, y2 = bbox_coords
    polygon = f"POLYGON(({x1} {y1}, {x2} {y1}, {x2} {y2}, {x1} {y2}, {x1} {y1}))"

    query = """
        INSERT INTO damage_detections (image_url, mask_url, bbox, class_id, confidence)
        VALUES (%s, %s, ST_GeomFromText(%s, 4326), %s, %s)
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (image_url, mask_url, polygon, class_id, confidence))

def query_detections():
    query = """
        SELECT id, image_url, mask_url, ST_AsGeoJSON(bbox) AS bbox, class_id, confidence, timestamp
        FROM damage_detections
        ORDER BY timestamp DESC
        LIMIT 100;
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
