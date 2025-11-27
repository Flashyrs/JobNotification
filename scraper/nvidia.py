import requests
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"
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
                "company": "NVIDIA",
                "url": "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite" + path
            })
    return jobs
