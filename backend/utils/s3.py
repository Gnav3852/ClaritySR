import boto3
import os
from uuid import uuid4

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-west-1")
)

def upload_to_s3(file_path: str, bucket: str) -> str:
    ext = os.path.splitext(file_path)[1]
    key = f"{uuid4()}{ext}"

    s3.upload_file(file_path, bucket, key)

    url = f"https://{bucket}.s3.amazonaws.com/{key}"
    return url
