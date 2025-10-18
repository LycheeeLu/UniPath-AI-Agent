import requests
from bs4 import BeautifulSoup
from services.bedrock_service import call_bedrock

def parse_requirements(url):
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text(separator="\n")

    prompt = f"""
    Extract and summarize key graduate application requirements from the following text:
    - Application deadline
    - GPA / Degree requirements on course curriculum
    - GRE / TOEFL / IELTS
    - Documents (transcript, personal statement, recommendation letters, resume, and more files)
    - Tuition or fees
    - Program ranking if mentioned
    - Output in structured JSON
    Text: {text[:8000]}
    """

    summary = call_bedrock(prompt)
    return json.loads(summary) if "{" in summary else {"summary": summary}
