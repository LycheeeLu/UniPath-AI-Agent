from backend.services.bedrock_service import call_bedrock
import requests
from bs4 import BeautifulSoup

def match_faculty(field, university):
    query = f"{university} {field} faculty profiles"
    url = f"https://www.google.com/search?q={query}"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    links = [a["href"] for a in soup.find_all("a", href=True) if ".edu" in a["href"]][:5]
    prompt = f"""
    Based on the following faculty page URLs, identify professors whose research overlaps with {field}.
    Return name, position, and research summary.
    {links}
    """
    result = call_bedrock(prompt)
    return {"faculty_matches": result, "links": links}
