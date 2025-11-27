from utils.storage import load_seen, save_seen
from utils.telegram import send
from scraper.common import is_india
import datetime

# IMPORT SCRAPERS
from scraper.amazon import scrape as amazon
from scraper.google import scrape as google
from scraper.microsoft import scrape as microsoft
from scraper.salesforce import scrape as salesforce
from scraper.atlassian import scrape as atlassian
from scraper.uber import scrape as uber
from scraper.meta import scrape as meta
from scraper.linkedin import scrape as linkedin
from scraper.nvidia import scrape as nvidia
from scraper.oracle import scrape as oracle
from scraper.walmart import scrape as walmart
from scraper.adobe import scrape as adobe
from scraper.intuit import scrape as intuit
from scraper.stripe import scrape as stripe
from scraper.bloomberg import scrape as bloomberg
from scraper.amd import scrape as amd
from scraper.intel import scrape as intel
from scraper.qualcomm import scrape as qualcomm
from scraper.morgan import scrape as morgan
from scraper.goldman import scrape as goldman
from scraper.spacex import scrape as spacex


# MASTER SCRAPER LIST
SCRAPERS = [
    amazon, google, microsoft, salesforce, atlassian,
    uber, meta, linkedin, nvidia, oracle, walmart,
    adobe, intuit, stripe, bloomberg, amd, intel,
    qualcomm, morgan, goldman, spacex
]


def main():
    seen = load_seen()
    new_jobs = []

    print("========================================")
    print("     🚀 Job Scraper Started")
    print("========================================")

    for scraper in SCRAPERS:
        # readable scraper name
        scraper_module = scraper.__module__.split(".")[-1]
        scraper_name = scraper.__name__

        print(f"\n--- Running scraper: {scraper_module}.{scraper_name} ---")

        try:
            jobs = scraper()
            print(f"Jobs returned by {scraper_module}: {len(jobs)}")
        except Exception as e:
            print(f"❌ Error in {scraper_module}: {e}")
            continue

        for job in jobs:
            if not job or "id" not in job:
                continue

            job_id = job["id"]

            if job_id not in seen:
                new_jobs.append(job)
                seen.add(job_id)

    print(f"\n✨ New jobs found: {len(new_jobs)}")

    # SEND NOTIFICATIONS
    for job in new_jobs:
        location = job.get("location", "") or ""
        flag = "🇮🇳" if is_india(location) else "🌎"

        send(f"""
{flag} *New Job Alert!*
*Company:* {job['company']}
*Role:* {job['title']}
*Location:* {job.get("location", "N/A")}
*Apply:* {job['url']}
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
""")

    save_seen(seen)

    print("\n✔ Scraping completed.\n")


if __name__ == "__main__":
    main()
