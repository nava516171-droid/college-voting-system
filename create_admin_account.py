#!/usr/bin/env python
from app.database import SessionLocal
from app.models.admin import Admin
from app.utils.security import get_password_hash

db = SessionLocal()

# Create admin account
email = "boxkali123@gmail.com"
password = "admin123"  # You can change this to your desired password
full_name = "Admin User"

# Check if admin already exists
existing = db.query(Admin).filter(Admin.email == email).first()
if existing:
    print(f"Admin with email {email} already exists!")
else:
    # Create new admin
    hashed_password = get_password_hash(password)
    admin = Admin(
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print(f"\n{'='*60}")
    print(f"✅ Admin account created successfully!")
    print(f"{'='*60}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Full Name: {full_name}")
    print(f"{'='*60}\n")

db.close()
