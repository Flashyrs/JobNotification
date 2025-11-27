import requests
from scraper.common import KEYWORDS, is_india

API = "https://prod-ms-hrz-search.search.windows.net/indexes/jobs/docs"
KEY = "B03F98FD8A7C441E8E67A004CD4A9F8B"

def scrape():
    try:
        data = requests.get(
            API,
            params={"api-version": "2021-04-30-Preview", "search": "software"},
            headers={"api-key": KEY},
            timeout=20
        ).json()
    except:
        return []

    jobs = []

    for j in data.get("value", []):
        title = j.get("title", "")
        loc = j.get("location", "")

        if not is_india(loc):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            job_id = j.get("jobId")
            jobs.append({
                "id": job_id,
                "title": title,
                "company": "Microsoft",
                "url": f"https://jobs.careers.microsoft.com/us/en/job/{job_id}"
            })
    return jobs
