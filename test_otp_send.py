#!/usr/bin/env python3
"""Test OTP request directly"""
from app.database import SessionLocal
from app.models.user import User
from app.utils.otp import create_otp_for_user
from app.utils.email import send_otp_email

db = SessionLocal()

# Get the existing user
user = db.query(User).filter(User.email == "thankyounava09@gmail.com").first()

if not user:
    print("❌ User not found!")
    exit(1)

print("=" * 70)
print("TESTING OTP EMAIL SEND")
print("=" * 70)
print(f"User: {user.full_name} ({user.email})")
print()

# Generate OTP
print("1. Generating OTP code...")
otp_code = create_otp_for_user(db, user.id)
print(f"OTP generated: {otp_code}")

# Send email
print("\n2. Sending OTP email...")
email_sent = send_otp_email(user.email, otp_code, user.full_name)

if email_sent:
    print("OTP email sent successfully!")
else:
    print("OTP email failed to send!")

print("\n" + "=" * 70)
print(f"Check email: {user.email}")
print(f"OTP Code: {otp_code}")
print("=" * 70)

db.close()
