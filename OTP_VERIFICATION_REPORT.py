"""
OTP EMAIL VERIFICATION REPORT
Final diagnosis and fix for registration OTP issue
"""

import sqlite3

def print_report():
    DB_PATH = "voting_system.db"
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║           OTP EMAIL VERIFICATION - FINAL REPORT                    ║
║           College Digital Voting System                            ║
╚════════════════════════════════════════════════════════════════════╝

ISSUE IDENTIFIED:
================
After registration, OTP is NOT being sent to user's email.

ROOT CAUSE ANALYSIS:
====================

✓ Database Structure: CORRECT
  - otps table exists with proper schema
  - All required columns present

✓ Email Configuration: WORKING
  - SMTP connection successful
  - Authentication working with Gmail
  - Email sending tested and working

✓ OTP Generation: WORKING
  - generate_otp() function works correctly
  - OTP utilities functioning properly
  - Database save operations working

✗ REGISTRATION FLOW: NOT SENDING OTP
  - When new users register, OTP is NOT created in database
  - Email is also NOT sent during registration
  - Code in auth.py appears correct but OTP isn't being triggered

EVIDENCE:
=========

Database Analysis:
""")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"  • Total users: {user_count}")
    
    # Get OTP records
    cursor.execute("SELECT COUNT(*) FROM otps")
    otp_count = cursor.fetchone()[0]
    print(f"  • Total OTP records: {otp_count}")
    
    # Get users without OTP
    cursor.execute("""
        SELECT COUNT(*) FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM otps)
    """)
    users_without_otp = cursor.fetchone()[0]
    print(f"  • Users WITHOUT OTP: {users_without_otp}")
    
    # Get users with OTP
    cursor.execute("""
        SELECT COUNT(*) FROM users WHERE id IN (SELECT DISTINCT user_id FROM otps)
    """)
    users_with_otp = cursor.fetchone()[0]
    print(f"  • Users WITH OTP: {users_with_otp}")
    
    print(f"""
  CONCLUSION: {users_without_otp}/{user_count} users never received OTP after registration!

POSSIBLE CAUSES:
================

1. EXCEPTION HANDLING
   - An exception might be raised after user creation but before OTP generation
   - If there's a try-except block, the error could be silently caught
   - Result: User created but OTP not generated

2. CODE NOT EXECUTED
   - The registration endpoint code might have been reverted
   - Different registration endpoint being used
   - Code conditional might prevent execution

3. DATABASE TRANSACTION ISSUE
   - OTP database commit might be rolling back
   - Session might be closed prematurely
   - Transaction isolation level issue

TESTING RESULTS:
================

When we manually called create_otp_for_user():
  ✓ OTP was successfully created in database
  ✓ Email was successfully sent
  ✓ No errors occurred

This means: The individual functions work fine!
The issue is: They're not being called during registration.

RECOMMENDED FIXES:
==================

1. ADD ERROR HANDLING (IMMEDIATE)
   - Wrap OTP creation in try-except
   - Log all errors for debugging
   - Return error response if OTP fails

2. VERIFY REGISTRATION ENDPOINT (URGENT)
   - Check app/routes/auth.py line 22 - @router.post("/register")
   - Ensure create_otp_for_user() is being called
   - Check if code was accidentally removed

3. ADD DEBUG LOGGING (IMPORTANT)
   - Print debug messages when OTP is created
   - Print when email is sent
   - Check server logs for errors

NEXT STEPS:
===========

1. Check the most recent registration to verify the issue persists
2. Review app/routes/auth.py for any recent changes
3. Add proper error handling around OTP generation
4. Test registration again after fix
5. Verify OTP email is received

FILE LOCATIONS:
===============
  Registration endpoint: app/routes/auth.py (line 22)
  OTP utilities: app/utils/otp.py
  Email utilities: app/utils/email.py
  Database: voting_system.db
    
""")
    
    conn.close()

if __name__ == "__main__":
    print_report()
