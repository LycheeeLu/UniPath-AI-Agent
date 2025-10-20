import os
import boto3
import fitz #PyMuPDF
from dotenv import load_dotenv
import json
import re
from backend.services.s3_service import upload_file
from backend.services.bedrock_service import call_bedrock
from backend.agent.program_finder import find_programs
from backend.agent.faculty_matcher import match_faculty





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

    Rules:
    - Use double quotes for all keys and strings.
    - Identify the applicant's **academic field or major** precisely (e.g., 'Psychology and Marketing' instead of 'general').
    - Do NOT include markdown formatting, comments, or text before/after JSON.
    - Only output valid JSON.

    Return JSON like this:
    {{
    "field": "Psychology, Computer Science, Economics/Marketing",
    "education": ["Bachelor of Science in Computer Science, NYU, 2023"],
    "skills": ["Python", "Machine Learning", "Data Analysis"],
    "experience": ["Research Assistant at XYZ Lab", "Software Engineer Intern at Google"],
    "interests": ["AI Safety", "Human-Computer Interaction"],
    "publications": [...]

    Resume content:
    {resume_text}

    }}
    """

    # let Bedrock extract resume text
    # for future optimization, we can use Textract OCR to extract texts
    summary_raw = call_bedrock(prompt)
    text = summary_raw.strip()
    print("=== [DEBUG Bedrock text output] ===\n", text)

    """     if isinstance(summary_raw, dict) and "content" in summary_raw:
            text = summary_raw["content"][0].get("text", "")
        elif "text" in summary_raw:
            text = summary_raw["text"]
        else:
            text = str(summary_raw)
    """

    text = re.sub(r"^```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        cleaned = match.group(0)
    else:
        cleaned = text

    # deconstruct JSON
    try:
        summary = json.loads(cleaned)

    except json.JSONDecodeError as e:
        print("⚠️ JSONDecodeError:", e)
        print("RAW TEXT:\n", text[:2000])
        summary = {"field": "what"}


    field = summary.get("field", "general")

    programs = find_programs(field)
    first_uni = programs["recommended_programs"][0]["title"].split(":")[0]
    faculty_data = match_faculty(field, first_uni)



    return {
        "status": "success",
        "user_id": user_id,
        "file": file.filename,
        "s3_path": s3_path,
        "summary": summary,
        "recommendations": {
            "programs": programs,
            "faculty": faculty_data}
    }
