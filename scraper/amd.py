import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://amd.wd3.myworkdayjobs.com/wday/cxs/External/jobs"
    try:
        data = requests.get(url, timeout=20).json()
    except:
        return []

    jobs = []

    for j in data.get("jobPostings", []):
        info = j.get("jobPostingInfo", {})
        title = info.get("title", "")
        loc = info.get("location", "")

        if not is_india(loc):
            continue

        if any(k in title.lower() for k in KEYWORDS):
            jobs.append({
                "id": j.get("externalPath"),
                "title": title,
                "company": "AMD",
                "url": "https://amd.wd3.myworkdayjobs.com/en-US/External" + j.get("externalPath")
            })
    return jobs
