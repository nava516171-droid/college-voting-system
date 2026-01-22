#!/usr/bin/env python3
"""
Update candidate names in the database
Changes existing candidates to: DINESH RANGAPPA, RAMESH, NIRMALA HIREMANI
"""

import sys
sys.path.insert(0, 'c:\\Users\\Navaneeth M\\Desktop\\college voting system')

from app.database import SessionLocal
from app.models.candidate import Candidate
from sqlalchemy.orm import Session

# New candidate names
NEW_CANDIDATES = [
    {"id": 1, "name": "DINESH RANGAPPA"},
    {"id": 2, "name": "RAMESH"},
    {"id": 3, "name": "NIRMALA HIREMANI"}
]

def update_candidates():
    """Update candidate names in database"""
    db: Session = SessionLocal()
    
    try:
        print("\n" + "="*70)
        print("UPDATING CANDIDATE NAMES")
        print("="*70 + "\n")
        
        # Get all candidates
        candidates = db.query(Candidate).all()
        
        if not candidates:
            print("❌ No candidates found in database!")
            return False
        
        print(f"Found {len(candidates)} candidate(s) in database\n")
        
        # Display current candidates
        print("CURRENT CANDIDATES:")
        print("-" * 70)
        for candidate in candidates:
            print(f"  ID: {candidate.id}")
            print(f"  Name: {candidate.name}")
            print(f"  Description: {candidate.description}")
            print(f"  Symbol Number: {candidate.symbol_number}")
            print(f"  Election ID: {candidate.election_id}")
            print()
        
        # Update first 3 candidates with new names
        print("\nUPDATING TO NEW NAMES:")
        print("-" * 70)
        
        updated_count = 0
        for i, new_data in enumerate(NEW_CANDIDATES):
            if i < len(candidates):
                candidate = candidates[i]
                old_name = candidate.name
                candidate.name = new_data["name"]
                db.add(candidate)
                
                print(f"✅ Updated Candidate {candidate.id}:")
                print(f"   Old Name: {old_name}")
                print(f"   New Name: {candidate.name}\n")
                
                updated_count += 1
        
        # Commit changes
        db.commit()
        
        print("\n" + "="*70)
        print(f"✅ SUCCESSFULLY UPDATED {updated_count} CANDIDATE(S)")
        print("="*70)
        
        # Display updated candidates
        print("\nUPDATED CANDIDATES:")
        print("-" * 70)
        updated_candidates = db.query(Candidate).all()
        for candidate in updated_candidates:
            print(f"  ID {candidate.id}: {candidate.name} (Election: {candidate.election_id})")
        
        print("\n✅ Candidates updated successfully!")
        print("   Refresh your browser to see the changes.\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error updating candidates: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = update_candidates()
    sys.exit(0 if success else 1)
