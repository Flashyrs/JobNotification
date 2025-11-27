import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://boards-api.greenhouse.io/v1/boards/spacex/jobs?content=true"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []

    for job in data.get("jobs", []):
        title = job.get("title", "")
        loc = job.get("location", {}).get("name", "")

        if not is_india(loc):
            continue  # no SpaceX India roles exist

        if any(k in title.lower() for k in KEYWORDS):
            jobs.append({
                "id": job.get("id"),
                "title": title,
                "company": "SpaceX",
                "url": job.get("absolute_url")
            })

    return jobs
