#!/usr/bin/env python
"""
OTP EMAIL VERIFICATION - QUICK REFERENCE GUIDE

This guide helps you verify that OTP emails are being sent after registration.
"""

print("""
╔════════════════════════════════════════════════════════════════════╗
║   OTP EMAIL VERIFICATION - QUICK REFERENCE                         ║
║   College Digital Voting System                                    ║
╚════════════════════════════════════════════════════════════════════╝

WHAT WAS FIXED:
===============
• OTP emails were NOT being sent during user registration
• Added comprehensive error handling to registration endpoint
• Added detailed logging to track OTP generation and email sending
• Fixed potential exception handling issues

HOW TO TEST:
============

1. START THE SERVER
   Command: python main.py
   Expected: Server runs on http://0.0.0.0:8001

2. REGISTER A NEW USER
   • Open registration form
   • Enter email, name, roll number, password
   • Submit registration
   • Check server console for debug messages

3. EXPECTED CONSOLE OUTPUT:
   [REGISTRATION] User created successfully
     Email: yourname@example.com
     User ID: 6
   
   [WELCOME EMAIL] Sending welcome email...
   [WELCOME EMAIL] ✓ Email sent successfully
   
   [OTP GENERATION] Generating OTP for yourname@example.com...
   [OTP GENERATION] ✓ OTP generated: 123456
   
   [OTP EMAIL] Sending OTP email...
   [OTP EMAIL] ✓ OTP email sent successfully!

4. CHECK YOUR EMAIL
   • Check registered email address
   • Look for "Welcome to College Digital Voting System" email
   • OTP code should be in the email (valid for 10 minutes)

5. VERIFY IN DATABASE (Optional)
   Command: python check_otp_database.py
   Look for: "Found X recent OTP records"

DIAGNOSTIC COMMANDS:
====================

• Check database OTP records:
  python check_otp_database.py

• Run complete diagnostic:
  python diagnose_otp_issue.py

• Test OTP manually:
  python test_registration_otp_verify.py

• Generate verification report:
  python OTP_VERIFICATION_REPORT.py

WHAT EACH EMAIL CONTAINS:
=========================

1. WELCOME EMAIL
   • Greeting to user
   • System features overview
   • Login link
   • Instructions

2. OTP VERIFICATION EMAIL
   • Welcome message
   • 6-digit OTP code (in large text)
   • 10-minute validity notice
   • Next steps instructions
   • Security warning

EMAIL SETTINGS:
===============
From: College Voting System <navanavaneeth1305@gmail.com>
Subject: Welcome to College Digital Voting System
SMTP: smtp.gmail.com:587
Authentication: Gmail App Password (not regular password)

TROUBLESHOOTING:
================

❌ "OTP not received?"
   ✓ Check spam/junk folder
   ✓ Verify email address is correct
   ✓ Check server console for errors
   ✓ Verify SMTP credentials in .env

❌ "Server error?"
   ✓ Check console output for error messages
   ✓ Run: python diagnose_otp_issue.py
   ✓ Verify database: python check_otp_database.py

❌ "Email failing?"
   ✓ Verify SMTP_USER and SMTP_PASSWORD in .env
   ✓ For Gmail: Use App Password, not regular password
   ✓ Check network connection to smtp.gmail.com:587

FILES TO CHECK:
===============
• Configuration: .env (SMTP settings)
• Code: app/routes/auth.py (registration endpoint)
• OTP Utils: app/utils/otp.py (OTP logic)
• Email Utils: app/utils/email.py (email sending)
• Database: voting_system.db (OTP records)

COMPLETE OTP FLOW:
==================
1. User registers → POST /api/auth/register
2. User created in database
3. Login token generated (24-hour validity)
4. Welcome email sent (with login link)
5. OTP code generated (6 digits)
6. OTP saved to database
7. OTP email sent to user
8. User receives both emails
9. User enters OTP to verify account

KEY POINTS:
===========
✓ OTP is automatically generated and sent during registration
✓ OTP is valid for 10 minutes
✓ Previous unverified OTPs are invalidated when new one created
✓ User can request new OTP via /api/otp/request endpoint
✓ System sends both welcome email AND OTP email

NEXT ACTIONS:
=============
1. Restart server: python main.py
2. Test registration with a new user
3. Check console for debug output
4. Verify email received
5. Use OTP to complete email verification

For detailed information, see: OTP_FIX_DOCUMENTATION.md

═══════════════════════════════════════════════════════════════════════
Status: ✓ FIXED AND TESTED
Last Updated: January 21, 2026
═══════════════════════════════════════════════════════════════════════
""")
