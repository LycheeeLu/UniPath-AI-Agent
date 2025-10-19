from fastapi import FastAPI, UploadFile
from backend.agent.resume_processor import process_resume
from backend.agent.program_finder import recommend_programs
from backend.agent.requirement_parser import parse_requirements
from backend.agent.faculty_matcher import match_faculty
from backend.agent.tracker import generate_tracker

app = FastAPI()

@app.post("/upload-resume")
async def upload_resume(file: UploadFile):
    return await process_resume(file)

@app.get("/recommend-programs")
def recommend_programs(field: str):
    return recommend_programs(field)

@app.get("/parse-requirements")
def requirements(url: str):
    return parse_requirements(url)

@app.get("/faculty-match")
def faculty(field: str, university: str):
    return match_faculty(field, university)

@app.get("/generate-tracker")
def tracker(user_id: str):
    return generate_tracker(user_id)

@app.get("/")
def home():
    return {"status": "UniPathAI backend is running"}
