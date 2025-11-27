import json
import os

DATA_DIR = "utils/data"
SUB_FILE = f"{DATA_DIR}/subscribers.json"
SEEN_FILE = f"{DATA_DIR}/seen.json"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)

# ========== INTERNAL HELPERS ==========

def _load(path):
    if not os.path.exists(path):
        return set()
    try:
        with open(path, "r") as f:
            return set(json.load(f))
    except:
        return set()

def _save(path, data):
    with open(path, "w") as f:
        json.dump(list(data), f, indent=2)


# ========== SUBSCRIBERS ==========

def load_subscribers():
    return _load(SUB_FILE)

def save_subscribers(subs):
    _save(SUB_FILE, subs)

def add_subscriber(chat_id):
    subs = load_subscribers()
    subs.add(str(chat_id))
    save_subscribers(subs)

def remove_subscriber(chat_id):
    subs = load_subscribers()
    subs.discard(str(chat_id))
    save_subscribers(subs)


# ========== SEEN JOBS ==========

def load_seen():
    return _load(SEEN_FILE)

def save_seen(seen):
    _save(SEEN_FILE, seen)
