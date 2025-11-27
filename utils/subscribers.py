import json
import os

FILE = "subscribers.json"

def load_subscribers():
    if not os.path.exists(FILE):
        return set()
    try:
        return set(json.load(open(FILE)))
    except:
        return set()

def save_subscribers(s):
    json.dump(list(s), open(FILE, "w"))
