import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://careers.oracle.com/api/jobs?keywords=software"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []

    for j in data.get("jobs", []):
        title = j.get("title", "")
        loc = j.get("location", "")

        if not is_india(loc):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            jobs.append({
                "id": j.get("id"),
                "title": title,
                "company": "Oracle",
                "url": j.get("applyUrl")
            })
    return jobs
