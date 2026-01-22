#!/usr/bin/env python
"""
Send OTP verification email to a specific user
"""

import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.utils.otp import create_otp_for_user
from app.utils.email import send_otp_email

DATABASE_URL = "sqlite:///voting_system.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def send_otp_to_email(email: str):
    """Send OTP to specified email"""
    
    print("\n" + "="*70)
    print("OTP VERIFICATION EMAIL SENDER")
    print("="*70 + "\n")
    
    try:
        db = SessionLocal()
        
        # Find user by email
        print(f"[1/4] Looking up user with email: {email}")
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"✗ ERROR: User not found with email: {email}")
            db.close()
            return False
        
        print(f"✓ User found: {user.full_name} (ID: {user.id})")
        
        # Generate OTP
        print(f"\n[2/4] Generating OTP for {user.email}...")
        otp_code = create_otp_for_user(db, user.id)
        print(f"✓ OTP Generated: {otp_code}")
        print(f"  Valid for: 10 minutes")
        
        # Send email
        print(f"\n[3/4] Sending OTP email to {user.email}...")
        email_sent = send_otp_email(user.email, otp_code, user.full_name)
        
        if email_sent:
            print(f"✓ OTP Email sent successfully!")
            print(f"\n[4/4] Verification complete")
            print(f"\nEmail Details:")
            print(f"  To: {user.email}")
            print(f"  Name: {user.full_name}")
            print(f"  OTP Code: {otp_code}")
            print(f"  Expires: 10 minutes from now")
            
            db.close()
            print("\n" + "="*70)
            print("✓ OTP SENT SUCCESSFULLY - CHECK YOUR EMAIL")
            print("="*70 + "\n")
            return True
        else:
            print(f"✗ Failed to send OTP email")
            db.close()
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Replace with actual email address to test
    email = input("Enter email address to send OTP: ").strip()
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║        SEND OTP VERIFICATION EMAIL                                ║")
    print("║        College Digital Voting System                              ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    success = send_otp_to_email(email)
    
    if success:
        print("✓ Task completed successfully!")
        print("  The user should receive the OTP email shortly.")
        print("  OTP is valid for 10 minutes.")
    else:
        print("✗ Failed to send OTP email")
        print("  Please check the error messages above.")
