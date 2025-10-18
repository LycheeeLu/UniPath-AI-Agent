import json, tempfile
from backend.services.s3_service import upload_file
from backend.services.bedrock_service import call_bedrock

def process_resume(file):
    contents = file.file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    # upload resume to S3
    s3_path = upload_file(contents, f"resumes/{file.filename}")

    prompt = f"""
    You are an expert in academic admissions. Read the following resume text (PDF extracted text):
    Summarize the applicant’s:
    - Field of study
    - Research interests
    - Professional or academic achievements
    - Recommended target programs or specializations
    """

    summary = call_bedrock(prompt)
    return {"summary": summary, "resume_s3": s3_path}
