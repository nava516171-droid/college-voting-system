#!/usr/bin/env python3
import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.database import SessionLocal
    from app.models.candidate import Candidate
    
    db = SessionLocal()
    candidates = db.query(Candidate).all()
    
    print(f"\n{'='*60}")
    print(f"Total Candidates in Database: {len(candidates)}")
    print(f"{'='*60}\n")
    
    if candidates:
        for candidate in candidates:
            print(f"ID: {candidate.id}")
            print(f"Name: {candidate.name}")
            print(f"Election ID: {candidate.election_id}")
            print(f"Symbol Number: {candidate.symbol_number}")
            print(f"Description: {candidate.description}")
            print("-" * 40)
    else:
        print("No candidates found in database!")
        print("\nLooking for expected candidates: DINESH RANGAPPA, RAMESH, NIRMALA HIREMANI")
    
    db.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
