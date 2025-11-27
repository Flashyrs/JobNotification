import json
import os

FILE = "seen.json"

def load_seen():
    if not os.path.exists(FILE):
        return set()
    try:
        return set(json.load(open(FILE)))
    except:
        return set()

def save_seen(seen):
    with open(FILE, "w") as f:
        json.dump(list(seen), f)
