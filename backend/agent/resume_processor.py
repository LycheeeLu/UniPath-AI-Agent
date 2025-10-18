import os
import tempfile
import boto3
from dotenv import load_dotenv
from backend.services.db_service import add_user_item
from backend.services.bedrock_service import call_bedrock

load_dotenv()

# initialize s3
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

S3_BUCKET = os.getenv("S3_BUCKET")


async def process_resume(file):
    """
    upload resume/sv to S3 → store metadata to DynamoDB → call on Bedrock to summarize → return results
    """

    # 1 temp file storage
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # 2 upoad to S3
    s3_key = f"uploads/{file.filename}"
    s3.upload_file(tmp_path, S3_BUCKET, s3_key)
    s3_url = f"s3://{S3_BUCKET}/{s3_key}"
    print(f"✅ Uploaded to {s3_url}")

    # remove temp file
    os.remove(tmp_path)

    # 3️ store metadata to DynamoDB
    user_id = "demo_user"
    add_user_item(user_id, file.filename, s3_url)

    # use bedrock to summarize
    summary_prompt = f"""
    You are an admissions assistant AI.
    Summarize the key academic and professional strengths in this resume.
    Highlight likely target programs (CS, AI, Business, etc.) and offer short reasons.
    """

    # let Bedrock extract resume text
    # for future optimization, we can use Textract OCR to extract texts
    resume_text = f"Resume file name: {file.filename}"
    prompt = f"{summary_prompt}\n\nResume:\n{resume_text}"

    bedrock_response = call_bedrock(prompt)

    # 5️ return results
    return {
        "status": "success",
        "user_id": user_id,
        "file": file.filename,
        "s3_path": s3_url,
        "summary": bedrock_response
    }
