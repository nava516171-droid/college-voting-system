#!/usr/bin/env python3
"""Setup candidate login credentials"""
from app.database import SessionLocal
from app.models.candidate import Candidate
from app.utils.security import get_password_hash

db = SessionLocal()

# Get all candidates
candidates = db.query(Candidate).all()

print(f'Setting up {len(candidates)} candidates with login credentials...')
print('=' * 60)

for candidate in candidates:
    # Set email based on candidate name
    email = f'{candidate.name.lower().replace(" ", ".")}@college.com'
    candidate.email = email
    candidate.hashed_password = get_password_hash('candidate123')
    print(f'✓ {candidate.name}')
    print(f'  Email: {email}')
    print(f'  Password: candidate123')
    print()

db.commit()
print('=' * 60)
print('✓ All candidates are ready to login!')
print('\nCandidate Login Credentials:')
print('Password: candidate123')
print('\nUse the "Candidate Login" option on the main login page.')
db.close()
