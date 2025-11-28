import json
import os
from datetime import datetime, timedelta

DATA_DIR = "utils/data"
SUB_FILE = f"{DATA_DIR}/subscribers.json"
SEEN_FILE = f"{DATA_DIR}/seen_jobs.json"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)

# ========== INTERNAL HELPERS ==========

def _load_json(path, default=None):
    """Load JSON file with default fallback"""
    if default is None:
        default = {}
    
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default

def _save_json(path, data):
    """Save data to JSON file"""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ========== SUBSCRIBERS ==========

def load_subscribers():
    """Load subscriber list"""
    data = _load_json(SUB_FILE, default=[])
    return set(data) if isinstance(data, list) else set()

def save_subscribers(subs):
    """Save subscriber list"""
    _save_json(SUB_FILE, list(subs))

def add_subscriber(chat_id):
    """Add a subscriber"""
    subs = load_subscribers()
    subs.add(str(chat_id))
    save_subscribers(subs)

def remove_subscriber(chat_id):
    """Remove a subscriber"""
    subs = load_subscribers()
    subs.discard(str(chat_id))
    save_subscribers(subs)


# ========== SEEN JOBS (PER-SUBSCRIBER) ==========

def load_seen_jobs():
    """
    Load seen jobs structure.
    Format: {
        "chat_id": {
            "job_id": {
                "seen_at": "2025-01-15T10:30:00",
                "title": "Software Engineer",
                "company": "Google"
            }
        }
    }
    """
    return _load_json(SEEN_FILE, default={})

def save_seen_jobs(seen_data):
    """Save seen jobs structure"""
    _save_json(SEEN_FILE, seen_data)

def is_job_seen(chat_id, job_id):
    """Check if a specific user has seen a job"""
    seen_data = load_seen_jobs()
    chat_id = str(chat_id)
    return job_id in seen_data.get(chat_id, {})

def mark_job_seen(chat_id, job_id, job_info=None):
    """Mark a job as seen for a specific user"""
    seen_data = load_seen_jobs()
    chat_id = str(chat_id)
    
    if chat_id not in seen_data:
        seen_data[chat_id] = {}
    
    seen_data[chat_id][job_id] = {
        "seen_at": datetime.now().isoformat(),
        "title": job_info.get("title", "") if job_info else "",
        "company": job_info.get("company", "") if job_info else ""
    }
    
    save_seen_jobs(seen_data)

def get_unseen_jobs_for_user(chat_id, all_jobs):
    """
    Filter jobs to only those not seen by this user.
    Returns list of jobs the user hasn't seen.
    """
    seen_data = load_seen_jobs()
    chat_id = str(chat_id)
    user_seen = seen_data.get(chat_id, {})
    
    unseen = []
    for job in all_jobs:
        job_id = job.get("id")
        if job_id and job_id not in user_seen:
            unseen.append(job)
    
    return unseen

def cleanup_old_seen_jobs(days=30):
    """
    Remove seen jobs older than specified days to prevent file bloat.
    Call this periodically (e.g., once a day).
    """
    seen_data = load_seen_jobs()
    cutoff_date = datetime.now() - timedelta(days=days)
    
    cleaned = {}
    for chat_id, jobs in seen_data.items():
        cleaned[chat_id] = {}
        for job_id, info in jobs.items():
            try:
                seen_at = datetime.fromisoformat(info.get("seen_at", ""))
                if seen_at > cutoff_date:
                    cleaned[chat_id][job_id] = info
            except:
                # Keep if we can't parse date (safety)
                cleaned[chat_id][job_id] = info
    
    save_seen_jobs(cleaned)
    return cleaned


# ========== LEGACY SUPPORT (for backward compatibility) ==========

def load_seen():
    """
    Legacy function - returns global seen set.
    Used for tracking which jobs have been scraped (not per-user).
    """
    # Load all unique job IDs across all users
    seen_data = load_seen_jobs()
    all_seen = set()
    for user_jobs in seen_data.values():
        all_seen.update(user_jobs.keys())
    return all_seen

def save_seen(seen):
    """
    Legacy function - not used anymore.
    Per-subscriber tracking is handled by mark_job_seen().
    """
    # This is now a no-op since we use per-subscriber tracking
    pass
