import requests, os
from bs4 import BeautifulSoup

def find_programs(field):
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
