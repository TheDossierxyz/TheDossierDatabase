import os
import argparse
import sys
from datetime import datetime

# Configuration
CLAIMS_DIR = os.path.join(os.path.dirname(__file__), "..", "claims")
CONTRIBUTOR_HANDLE = os.getenv("CONTRIBUTOR_HANDLE", "Anonymous")

def claim_batch(batch_id: str):
    # Normalize batch ID
    batch_file = os.path.join(CLAIMS_DIR, f"{batch_id}.txt")
    
    # 1. Check if already claimed
    if os.path.exists(batch_file):
        with open(batch_file, 'r') as f:
            claimer = f.read().strip()
        print(f"[LOCKED] Batch {batch_id} is already claimed by: {claimer}")
        print("Please choose a different batch.")
        sys.exit(1)
    
    # 2. Claim it
    try:
        with open(batch_file, 'w') as f:
            f.write(f"{CONTRIBUTOR_HANDLE}\nClaimed on {datetime.now()}")
        print(f"[SUCCESS] Batch {batch_id} locked to you!")
        print("IMPORTANT: Run 'git add claims/ && git commit -m \"Claim batch {batch_id}\" && git push' immediately!")
    except Exception as e:
        print(f"[ERROR] Could not write claim file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Claim a batch to prevent duplicate work.")
    parser.add_argument("--batch", required=True, help="Batch ID to claim (e.g. 001)")
    args = parser.parse_args()
    
    if not os.path.exists(CLAIMS_DIR):
        print("[ERROR] claims/ directory not found.")
        sys.exit(1)

    claim_batch(args.batch)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    # Reload handle after dotenv
    globals()['CONTRIBUTOR_HANDLE'] = os.getenv("CONTRIBUTOR_HANDLE", "Anonymous")
    main()
