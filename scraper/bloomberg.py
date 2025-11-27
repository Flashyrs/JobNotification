import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://boards-api.greenhouse.io/v1/boards/bloomberg/jobs?content=true"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []
    for j in data.get("jobs", []):
        title = j.get("title", "")
        loc = j.get("location", {}).get("name", "")

        if not is_india(loc):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            jobs.append({
                "id": j.get("id"),
                "title": title,
                "company": "Bloomberg",
                "url": j.get("absolute_url")
            })
    return jobs
