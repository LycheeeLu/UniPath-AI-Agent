import boto3, os
s3 = boto3.client("s3")
BUCKET = os.getenv("S3_BUCKET")

def upload_file(file, key):
    s3.put_object(Bucket=BUCKET, Key=key, Body=file)
    return f"s3://{BUCKET}/{key}"
