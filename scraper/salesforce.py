import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://salesforce.wd1.myworkdayjobs.com/wday/cxs/salesforce/External_Careers/jobs"
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
            path = j.get("externalPath", "")
            jobs.append({
                "id": path,
                "title": title,
                "company": "Salesforce",
                "url": "https://salesforce.wd1.myworkdayjobs.com/en-US/External_Careers" + path
            })
    return jobs
