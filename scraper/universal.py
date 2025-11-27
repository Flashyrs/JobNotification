import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

KEYWORDS = ["intern", "new grad", "graduate", "university", "entry"]


def scrape_site(url, company):
    try:
        res = requests.get(url, headers=HEADERS, timeout=25)
        html = res.text
    except Exception as e:
        print(f"[{company}] request error:", e)
        return []

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if not text:
            continue

        title = text.lower()
        if not any(k in title for k in KEYWORDS):
            continue

        href = a["href"]

        # ensure href is string
        if not isinstance(href, str):
            continue

        # normalize URL safely
        if href.startswith("/"):
            href = url.rstrip("/") + href
        elif not href.startswith("http"):
            href = url.rstrip("/") + "/" + href

        jobs.append({
            "id": href,
            "title": text,
            "company": company,
            "url": href
        })

    return jobs
