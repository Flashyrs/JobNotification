#!/usr/bin/env python3
"""
Migration script to reset seen jobs for per-subscriber tracking.

This script:
1. Backs up old seen.json files
2. Creates new per-subscriber seen_jobs.json structure
3. Ensures all subscribers start fresh

Run this once before deploying the new version.
"""

import json
import os
from datetime import datetime

def migrate():
    print("🔄 Migrating to per-subscriber seen jobs system...")
    
    # Backup old files
    old_files = ["seen.json", "utils/data/seen.json"]
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for old_file in old_files:
        if os.path.exists(old_file):
            backup_file = f"{backup_dir}/{os.path.basename(old_file)}.{timestamp}.backup"
            print(f"  📦 Backing up {old_file} to {backup_file}")
            
            try:
                with open(old_file, 'r') as f:
                    data = json.load(f)
                with open(backup_file, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"    ✅ Backed up {len(data)} entries")
            except Exception as e:
                print(f"    ⚠️  Could not backup {old_file}: {e}")
    
    # Create new per-subscriber structure
    new_file = "utils/data/seen_jobs.json"
    os.makedirs("utils/data", exist_ok=True)
    
    print(f"\n  🆕 Creating new per-subscriber seen jobs file: {new_file}")
    
    # Initialize with empty structure
    new_structure = {}
    
    with open(new_file, 'w') as f:
        json.dump(new_structure, f, indent=2)
    
    print(f"    ✅ Created new structure (empty - all users will see all jobs)")
    
    # Remove old seen.json files (optional - keep backups)
    print("\n  🗑️  Removing old seen.json files...")
    for old_file in old_files:
        if os.path.exists(old_file):
            try:
                os.remove(old_file)
                print(f"    ✅ Removed {old_file}")
            except Exception as e:
                print(f"    ⚠️  Could not remove {old_file}: {e}")
    
    print("\n✅ Migration complete!")
    print("\n📋 Summary:")
    print("  - Old seen jobs backed up to backups/ directory")
    print("  - New per-subscriber system initialized")
    print("  - All subscribers will now receive all available jobs")
    print("  - Each subscriber will only see each job once")
    print("\n🚀 You can now deploy the updated code!")

if __name__ == "__main__":
    migrate()
