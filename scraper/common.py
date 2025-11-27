KEYWORDS = ["intern", "new grad", "graduate", "university", "entry"]

def is_india(loc: str):
    if not loc:
        return False
    loc = loc.lower()
    return any(k in loc for k in [
        "india", "bangalore", "bengaluru", "hyderabad",
        "gurgaon", "gurugram", "mumbai", "delhi",
        "noida", "pune", "chennai"
    ])
