#!/usr/bin/env python3
"""Update user password"""
from app.database import SessionLocal
from app.models.user import User
from app.utils.security import get_password_hash

db = SessionLocal()

# Get the user
user = db.query(User).filter(User.email == "thankyounava09@gmail.com").first()

if not user:
    print("User not found!")
    exit(1)

print(f"Updating password for: {user.email}")

# Update password
user.hashed_password = get_password_hash("password123")
db.commit()

print("Password updated to: password123")
print("\nYou can now login with:")
print("  Email: thankyounava09@gmail.com")
print("  Password: password123")

db.close()
