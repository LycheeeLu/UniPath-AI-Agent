from backend.services.bedrock_service import call_bedrock
import requests, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def match_faculty(field, university):
    """
    Use Google Custom Search to find faculty pages for a given field and university,
    then summarize potential research matches via Bedrock.
    """
    query = f"{university} {field} faculty OR professors site:.edu"

    url = (
        f"https://www.googleapis.com/customsearch/v1"
        f"?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
    )

    res = requests.get(url)
    data = res.json()

    links = [item["link"] for item in data.get("items", [])[:5]]
    if not links:
        return {"faculty_matches": "No faculty pages found.", "links": []}

    prompt = f"""
    You are an expert academic matching assistant.
    Based on the following faculty or department web pages, identify professors from corresponding university whose research overlaps with the field "{field}".
    For each professor (3 in total), return:
    - name
    - title/position
    - main research topics (1 sentence)

    Faculty pages:
    {links}

    Return results as a clean JSON list like:
    do not add anything extra else to ur response!!
    [
      {{"name": "...", "title": "...", "research": "..."}}
    ]
    """

    result = call_bedrock(prompt)
    return {"faculty_matches": result, "links": links}