#!/usr/bin/env python
from app.database import SessionLocal
from app.models.admin import Admin

db = SessionLocal()
admins = db.query(Admin).all()

print(f"\n{'='*60}")
print(f"Total admins in database: {len(admins)}")
print(f"{'='*60}\n")

if admins:
    for admin in admins:
        print(f"Email: {admin.email}")
        print(f"Full Name: {admin.full_name}")
        print(f"Is Active: {admin.is_active}")
        print(f"Created At: {admin.created_at}")
        print(f"-" * 40)
else:
    print("No admin accounts found in database!")
    print("\nPlease register an admin account first using the registration page.")

db.close()
