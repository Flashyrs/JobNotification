import requests
from bs4 import BeautifulSoup
from scraper.common import KEYWORDS, is_india

def scrape():
    url = "https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2"
    try:
        html = requests.get(url, timeout=20).text
    except:
        return []

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if not text:
            continue

        if not is_india(text):
            continue

        if any(k in text.lower() for k in KEYWORDS):
            href = a["href"]
            if isinstance(href, str) and href.startswith("/"):
                href = url.rstrip("/") + href

            jobs.append({
                "id": href,
                "title": text,
                "company": "Morgan Stanley",
                "url": href
            })

    return jobs
