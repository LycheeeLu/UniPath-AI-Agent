from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.agent.resume_processor import process_resume
from backend.agent.program_finder import find_programs
from backend.agent.requirement_parser import parse_requirements
from backend.agent.faculty_matcher import match_faculty
from backend.agent.tracker import generate_tracker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload-resume")
async def upload_resume(file: UploadFile):
    return await process_resume(file)

@app.get("/recommend-programs")
def find_programs(field: str):
    return find_programs(field)

@app.get("/parse-requirements")
def requirements(url: str):
    print(f"🌐 Parsing requirements from {url}")
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
