import os
import boto3
import fitz #PyMuPDF
from dotenv import load_dotenv
from backend.services.s3_service import upload_file
from backend.services.bedrock_service import call_bedrock




async def process_resume(file):
    """
    upload resume/sv to S3 → store metadata to DynamoDB → call on Bedrock to summarize → return results
    """
    user_id = "demo_user"
    filename = file.filename
    local_path = f"uploads/{filename}"

    # 1 temp file storage
    os.makedirs("uploads", exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(await file.read())


    # 2 upoad to S3
    s3_path = upload_file(local_path, f"uploads/{filename}")


    # extract texts from PDF
    resume_text = ""
    with fitz.open(local_path) as pdf:
        for page in pdf:
            resume_text += page.get_text()

    if not resume_text.strip():
        resume_text = "This resume appears empty or unscannable."


    # use bedrock to summarize
    prompt = (
        "Please summarize the following university application resume and "
        "suggest 5 suitable academic programs with reasoning:\n\n"
        f"{resume_text}"
    )

    # let Bedrock extract resume text
    # for future optimization, we can use Textract OCR to extract texts
    summary = call_bedrock(prompt)

    # 5️ return results
    return {
        "status": "success",
        "user_id": user_id,
        "file": file.filename,
        "s3_path": s3_path,
        "summary": summary
    }
