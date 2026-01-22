#!/usr/bin/env python3
"""
Email Configuration Test Script
Tests if OTP emails can be sent successfully
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.email import send_otp_email
from app.config import settings


def test_email_config():
    """Test email configuration and send a test OTP"""
    
    print("\n" + "="*70)
    print("📧 COLLEGE VOTING SYSTEM - EMAIL CONFIGURATION TEST")
    print("="*70 + "\n")
    
    # Check configuration
    print("✓ Checking Email Configuration...\n")
    print(f"  SMTP Server:    {settings.SMTP_SERVER}")
    print(f"  SMTP Port:      {settings.SMTP_PORT}")
    print(f"  SMTP User:      {settings.SMTP_USER}")
    print(f"  Sender Email:   {settings.SENDER_EMAIL}")
    print(f"  Sender Name:    {settings.SENDER_NAME}")
    
    # Validate configuration
    if settings.SMTP_USER == "your-email@gmail.com":
        print("\n" + "⚠️ "*35)
        print("\n❌ ERROR: Email not configured!")
        print("\nPlease follow these steps:")
        print("1. Open .env file in the project root")
        print("2. Replace 'your-email@gmail.com' with your actual Gmail address")
        print("3. Replace 'your-app-password' with your 16-character Gmail App Password")
        print("\n📖 For detailed setup instructions, see EMAIL_SETUP.md")
        print("\n" + "⚠️ "*35 + "\n")
        return False
    
    # Send test OTP
    print("\n" + "-"*70)
    print("✓ Attempting to send test OTP...\n")
    
    test_email = "test@votingsystem.example.com"
    test_otp = "123456"
    test_name = "Test User"
    
    result = send_otp_email(test_email, test_otp, test_name)
    
    print("-"*70)
    
    if result:
        print("\n✅ EMAIL CONFIGURATION SUCCESSFUL!")
        print("\nYour OTP email system is ready to use:")
        print("  • OTP requests will send emails to users")
        print("  • OTP verification will work as expected")
        print("  • All authentication flows with OTP are active")
        print("\n📝 Test Details:")
        print(f"  • Recipient: {test_email}")
        print(f"  • OTP Code: {test_otp}")
        print(f"  • Recipient Name: {test_name}")
        print("\n📖 Next Steps:")
        print("  1. Start your server: python main.py")
        print("  2. Test OTP endpoint via Swagger: http://localhost:8000/docs")
        print("  3. Use /api/otp/request endpoint to send real OTPs")
        return True
    else:
        print("\n❌ EMAIL CONFIGURATION FAILED!")
        print("\nPossible issues:")
        print("  • Invalid SMTP credentials")
        print("  • 2-Factor Authentication not enabled on Gmail")
        print("  • Using regular password instead of App Password")
        print("  • Network connectivity issues")
        print("\n📖 For troubleshooting, see EMAIL_SETUP.md")
        return False


def test_live_email():
    """Send a real OTP to a specified email address"""
    print("\n" + "="*70)
    print("🚀 SEND LIVE TEST OTP")
    print("="*70 + "\n")
    
    try:
        email = input("Enter recipient email address: ").strip()
        name = input("Enter recipient name (optional): ").strip() or "User"
        
        # Generate random OTP for testing
        import random
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        print(f"\n📧 Sending OTP '{otp}' to {email}...\n")
        
        result = send_otp_email(email, otp, name)
        
        if result:
            print("\n✅ Test OTP sent successfully!")
            print(f"📧 Check {email} for the OTP code")
        else:
            print("\n❌ Failed to send test OTP")
            
    except KeyboardInterrupt:
        print("\n\nTest cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    # Run configuration test
    success = test_email_config()
    
    if success:
        # Ask if user wants to send a live test
        print("\nWould you like to send a live test OTP? (y/n): ", end="")
        if input().lower().strip() == 'y':
            test_live_email()
    
    print("\n" + "="*70 + "\n")
