import requests
from scraper.common import KEYWORDS

def scrape():
    url = "https://boards-api.greenhouse.io/v1/boards/atlassian/jobs?content=true"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []

    for job in data.get("jobs", []):
        title = job.get("title", "")
        t = title.lower()

        if any(k in t for k in KEYWORDS):
            jobs.append({
                "id": job.get("id"),
                "title": title,
                "company": "Atlassian",
                "url": job.get("absolute_url")
            })

    return jobs
