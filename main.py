from utils.storage import load_seen, save_seen
from scraper.common import is_india
from utils.telegram import send_jobs
from utils.formatter import format_job_message
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

SCRAPERS = [
    amazon, google, microsoft, salesforce, atlassian,
    uber, meta, linkedin, nvidia, oracle, walmart,
    adobe, intuit, stripe, bloomberg, amd, intel,
    qualcomm, morgan, goldman, spacex
]


def main():
    """
    Main scraper function.
    Now sends jobs per-subscriber - each user only gets jobs they haven't seen.
    """
    all_jobs = []

    print("========================================")
    print("     🚀 Job Scraper Started")
    print("========================================")

    for scraper in SCRAPERS:
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

            # Ensure missing location does NOT break anything
            job.setdefault("location", "")
            
            # Add scraper name to job for reference
            job["scraper"] = scraper_module
            
            # Add all jobs (per-subscriber filtering happens in send_jobs)
            all_jobs.append(job)

    print(f"\n✨ Total jobs found: {len(all_jobs)}")

    # Send notifications per-subscriber (each user gets only unseen jobs)
    if all_jobs:
        stats = send_jobs(all_jobs, format_job_message)
        
        # Print summary
        total_sent = sum(stats.values())
        print(f"\n📊 Summary: Sent {total_sent} total notifications across {len(stats)} subscriber(s)")
        for chat_id, count in stats.items():
            print(f"  - Subscriber {chat_id}: {count} job(s)")
    else:
        print("\n📭 No jobs found to notify")

    return all_jobs  # serve.py needs the full job list


if __name__ == "__main__":
    main()
