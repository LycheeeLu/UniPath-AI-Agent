import requests, os
from backend.services.bedrock_service import call_bedrock
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
cx = os.getenv("GOOGLE_CSE_ID")


def find_programs(field):
    """
    google custom search API relevant masters degree program
    """

    query = f"{field} graduate programs university"

    res = requests.get(
        "https://www.googleapis.com/customsearch/v1",
        params={"q": query, "key": key, "cx": cx},
    )
    data = res.json()
    items = data.get("items", [])
    print("DEBUG Google Search data:", data)

    results = []
    for item in items[:3]:
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })
    return {"recommended_programs": results}

