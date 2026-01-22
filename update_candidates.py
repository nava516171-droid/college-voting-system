#!/usr/bin/env python3
"""Update all candidates to Professor"""
from app.database import SessionLocal
from app.models.candidate import Candidate

db = SessionLocal()
candidates = db.query(Candidate).all()

print(f'Updating {len(candidates)} candidates...')
for candidate in candidates:
    old_desc = candidate.description
    candidate.description = 'Professor'
    print(f'  {candidate.name}: {old_desc} -> Professor')

db.commit()
print(f'\n✓ All {len(candidates)} candidates updated to Professor')
db.close()
