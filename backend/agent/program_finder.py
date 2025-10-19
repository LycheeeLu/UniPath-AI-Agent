import requests, os
from bs4 import BeautifulSoup
from backend.services.bedrock_service import call_bedrock

def find_programs_links(field):
    """
    crawl relevant masters degree program
    """
    query = f"{field} master's program site:.edu"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for link in soup.select("a"):
        href = link.get("href", "")
        if "http" in href and ".edu" in href:
            results.append(href.split("&")[0].replace("/url?q=", ""))
        if len(results) >= 5:
            break
    return {"recommended_programs": results}

def recommend_programs(resume_json):
    # claude extract academic field
    prompt_field = f"""
Given this applicant profile:
{resume_json}

Extract the most relevant academic field (e.g., "computer science", "data science", "business analytics", etc.).
Return only one short field name.
"""
    field = call_bedrock(prompt_field)
    if not field:
        field = "computer science"

    # 2. Google search for real program links
    program_links = find_programs_links(field)

    # 3. Claude generate reasons
    prompt_reason = f"""
The user is interested in {field}. Here are some program links:
{program_links}

Write 2-3 sentences for each link explaining why this program might be a good fit.
Return JSON like:
[
  {{
    "school": "Stanford University",
    "program": "MS in Computer Science - AI Track",
    "link": "https://cs.stanford.edu/admissions/masters",
    "reason": "Strong research focus on AI and interdisciplinary collaboration."
  }},
  ...
]
"""
    recommendations = call_bedrock(prompt_reason)
    return recommendations