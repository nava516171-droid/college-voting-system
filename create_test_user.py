#!/usr/bin/env python3
"""Check database users and create test user if needed"""
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.utils.security import get_password_hash

db = SessionLocal()

# Check existing users
print("=" * 70)
print("USERS IN DATABASE")
print("=" * 70)
users = db.query(User).all()
if users:
    for user in users:
        print(f"ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.full_name}")
        print(f"  Roll: {user.roll_number}")
        print(f"  Role: {user.role}")
        print()
else:
    print("No users found in database")

# Create a test user
print("\nCreating test user...")
test_user = User(
    email="test@college.com",
    full_name="Test User",
    roll_number="2024001",
    hashed_password=get_password_hash("password123"),
    role=UserRole.STUDENT
)
db.add(test_user)
db.commit()
print(f"✅ Test user created: test@college.com / password123")

# Also create for the email mentioned
test_user2 = User(
    email="thankyounava09@gmail.com",
    full_name="Navaneeth M",
    roll_number="2024099",
    hashed_password=get_password_hash("password123"),
    role=UserRole.STUDENT
)
db.add(test_user2)
db.commit()
print(f"✅ Test user created: thankyounava09@gmail.com / password123")

db.close()
print("\n" + "=" * 70)
print("Try logging in with these credentials:")
print("  Email: test@college.com or thankyounava09@gmail.com")
print("  Password: password123")
print("=" * 70)
