#!/usr/bin/env python3
"""
Direct email test - Check if SMTP is working (Non-interactive version)
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "College Voting System")

# Use test email from command line or default
recipient_email = sys.argv[1] if len(sys.argv) > 1 else "thankyounava09@gmail.com"

print("=" * 70)
print("EMAIL CONFIGURATION TEST")
print("=" * 70)
print(f"SMTP Server: {SMTP_SERVER}")
print(f"SMTP Port: {SMTP_PORT}")
print(f"Sender Email: {SMTP_USER}")
print(f"Recipient Email: {recipient_email}")
print(f"Sender Name: {SENDER_NAME}")
print("=" * 70)

try:
    print(f"\n🔄 Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    
    # Create SMTP connection
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        print("✅ Connected to SMTP server")
        
        print("🔒 Starting TLS encryption...")
        server.starttls()
        print("✅ TLS encryption started")
        
        print(f"🔐 Logging in with {SMTP_USER}...")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("✅ Logged in successfully")
        
        # Create test email
        test_otp = "123456"
        subject = "TEST: College Voting System - OTP Verification"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px;">
                    <h2 style="color: #2196F3;">TEST EMAIL - OTP Verification</h2>
                    <p>This is a test email to verify SMTP is working correctly.</p>
                    
                    <div style="background-color: #f0f8ff; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0;">
                        <h1 style="color: #2196F3; letter-spacing: 8px; text-align: center; font-size: 32px;">{test_otp}</h1>
                    </div>
                    
                    <p style="color: #d32f2f; font-weight: bold;">⏱️ This OTP expires in 10 minutes</p>
                    <p style="color: #666;">If you receive this email, SMTP is working correctly!</p>
                </div>
            </body>
        </html>
        """
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message["To"] = recipient_email
        message.attach(MIMEText(html_body, "html"))
        
        print(f"\n📨 Sending test email to {recipient_email}...")
        server.send_message(message)
        print("✅ Email sent successfully!")
        
        print("\n" + "=" * 70)
        print("✅ SUCCESS! SMTP IS WORKING CORRECTLY")
        print("=" * 70)
        print(f"Email sent to: {recipient_email}")
        print("Check your inbox (and spam folder) for the test email")
        print("=" * 70)

except smtplib.SMTPAuthenticationError as e:
    print("\n" + "=" * 70)
    print("❌ AUTHENTICATION FAILED")
    print("=" * 70)
    print("Possible causes:")
    print("1. Gmail account doesn't have 2-Step Verification enabled")
    print("2. App Password is incorrect or has spaces")
    print("3. SMTP_USER is not set in .env file")
    print("4. Using regular Gmail password instead of App Password")
    print("\nFix: Use Gmail App Password (16 characters, no spaces)")
    print("=" * 70)

except smtplib.SMTPException as e:
    print(f"\n❌ SMTP Error: {str(e)}")
    print("Check your SMTP configuration")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
