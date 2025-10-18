
import boto3, os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

bucket = os.getenv("S3_BUCKET")

# Create a simple test file
test_file_name = "test_upload.txt"
with open(test_file_name, "w") as f:
    f.write("Hello from UniPathAI!")

s3.upload_file(test_file_name, bucket, test_file_name)
print(f"✅ Uploaded '{test_file_name}' to bucket '{bucket}' successfully!")
