import os
import boto3
import fitz #PyMuPDF
from dotenv import load_dotenv
from backend.services.s3_service import upload_file
from backend.services.bedrock_service import call_bedrock
from backend.agent.program_finder import recommend_programs




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
    prompt = f"""
    You are an expert academic advisor.
    Analyze the following resume text and extract structured information in JSON format:

    Resume:
    {resume_text}

    Return JSON like this:
    {{
    "education": ["Bachelor of Science in Computer Science, NYU, 2023"],
    "skills": ["Python", "Machine Learning", "Data Analysis"],
    "experience": ["Research Assistant at XYZ Lab", "Software Engineer Intern at Google"],
    "interests": ["AI Safety", "Human-Computer Interaction"]
    }}
    """

    # let Bedrock extract resume text
    # for future optimization, we can use Textract OCR to extract texts
    summary = call_bedrock(prompt)

    programs = recommend_programs(summary)


    return {
        "status": "success",
        "user_id": user_id,
        "file": file.filename,
        "s3_path": s3_path,
        "summary": summary,
        "program_recommendations": programs
    }
