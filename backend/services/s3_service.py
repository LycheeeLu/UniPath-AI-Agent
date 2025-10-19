import boto3, os
from dotenv import load_dotenv
load_dotenv()

s3 = boto3.client("s3")
BUCKET = os.getenv("S3_BUCKET")

def upload_file(local_path, key):
    if not BUCKET:
        raise ValueError("Missing S3_Bucket environment variable")
    with open(local_path, "rb") as f:
        s3.put_object(Bucket=BUCKET, Key=key, Body=f)

    return f"s3://{BUCKET}/{key}"
