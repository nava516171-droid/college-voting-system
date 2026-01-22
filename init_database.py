#!/usr/bin/env python3
"""Initialize database with sample data"""
from app.database import SessionLocal, Base, engine
from app.models.election import Election
from app.models.candidate import Candidate
from app.models.user import User
from app.utils.security import get_password_hash
from datetime import datetime, timedelta

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create election
election = Election(
    id=1,
    title="College Student Council Elections 2026",
    description="Annual student council elections",
    status="active",
    start_time=datetime.utcnow(),
    end_time=datetime.utcnow() + timedelta(days=7),
    is_active=True
)
db.add(election)
db.commit()
print("✓ Created election")

# Create candidates with campaign info
candidates_data = [
    {
        "name": "DINESH RANGAPPA",
        "symbol_number": 1,
        "description": "Professor",
        "email": "dinesh.rangappa@college.com",
        "campaign_message": "Focused on improving student welfare and academic excellence",
        "about": "Experienced in student affairs with 5+ years of dedication to college development"
    },
    {
        "name": "RAMESH",
        "symbol_number": 2,
        "description": "Professor",
        "email": "ramesh@college.com",
        "campaign_message": "Committed to infrastructure development and student engagement",
        "about": "Dedicated leader working for campus modernization and better student life"
    },
    {
        "name": "NIRMALA HIREMANI",
        "symbol_number": 3,
        "description": "Professor",
        "email": "nirmala.hiremani@college.com",
        "campaign_message": "Working towards gender equality and inclusive college policies",
        "about": "Advocate for student rights and inclusive campus environment"
    }
]

for cand_data in candidates_data:
    candidate = Candidate(
        election_id=1,
        name=cand_data["name"],
        symbol_number=cand_data["symbol_number"],
        description=cand_data["description"],
        email=cand_data["email"],
        hashed_password=get_password_hash("candidate123"),
        campaign_message=cand_data["campaign_message"],
        about=cand_data["about"]
    )
    db.add(candidate)
    print(f"✓ Created candidate: {cand_data['name']}")
    print(f"  Email: {cand_data['email']}")
    print(f"  Password: candidate123")

db.commit()

# Create sample user for testing
user = User(
    id=1,
    roll_number="2024001",
    email="nava2588ka@gmail.com",
    full_name="salman",
    hashed_password=get_password_hash("password123"),
    is_active=True
)
db.add(user)
db.commit()
print("\n✓ Created test user")
print(f"  Email: nava2588ka@gmail.com")
print(f"  Password: password123")

print("\n" + "="*60)
print("DATABASE INITIALIZATION COMPLETE!")
print("="*60)
print("\n📚 Candidate Login Credentials:")
for cand_data in candidates_data:
    print(f"  Email: {cand_data['email']}")
print(f"  Password: candidate123 (same for all)")

print("\n👥 Test User Credentials:")
print(f"  Email: nava2588ka@gmail.com")
print(f"  Password: password123")

db.close()
