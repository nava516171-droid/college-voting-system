"""
Test the registration endpoint directly and check if OTP is created
"""

import sqlite3
from datetime import datetime
import time

DB_PATH = "voting_system.db"

def get_latest_user():
    """Get the latest user from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, email, full_name, created_at 
        FROM users 
        ORDER BY created_at DESC 
        LIMIT 1
    """)
    
    result = cursor.fetchone()
    conn.close()
    return result

def check_otp_for_user(user_id):
    """Check if OTP exists for user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, otp_code, created_at, expires_at 
        FROM otps 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    """)
    
    result = cursor.fetchone()
    conn.close()
    return result

def test_registration():
    """Test registration flow"""
    print("\n" + "="*70)
    print("REGISTRATION OTP SENDING TEST")
    print("="*70 + "\n")
    
    # Check initial state
    print("[1/4] Checking initial state...")
    user_before = get_latest_user()
    if user_before:
        print(f"   ✓ Latest user: {user_before[1]} (ID: {user_before[0]})")
    else:
        print("   ✗ No users in database")
    
    # Simulate registration (you would do this through API in real scenario)
    print("\n[2/4] Registering new user...")
    print("   → Use your registration form to create a new account")
    print("   → Wait 5 seconds after registration...")
    
    for i in range(5, 0, -1):
        print(f"\r   ⏳ Waiting... {i}s", end='')
        time.sleep(1)
    print("\r   ✓ Wait complete                  ")
    
    # Check if new user was created
    print("\n[3/4] Checking if user was created...")
    user_after = get_latest_user()
    
    if user_after and user_before and user_after[0] != user_before[0]:
        print(f"   ✓ NEW USER CREATED!")
        print(f"      Email: {user_after[1]}")
        print(f"      Name: {user_after[2]}")
        print(f"      ID: {user_after[0]}")
        print(f"      Created At: {user_after[3]}")
        new_user_id = user_after[0]
    else:
        print("   ✗ No new user was created")
        print("   ✗ Registration may have failed")
        return False
    
    # Check if OTP was created
    print("\n[4/4] Checking if OTP was created...")
    otp = check_otp_for_user(new_user_id)
    
    if otp:
        otp_id, otp_code, created_at, expires_at = otp
        print(f"   ✓ OTP WAS CREATED!")
        print(f"      OTP ID: {otp_id}")
        print(f"      OTP Code: {otp_code}")
        print(f"      Created: {created_at}")
        print(f"      Expires: {expires_at}")
        return True
    else:
        print(f"   ✗ NO OTP WAS CREATED for user {new_user_id}")
        print("   ✗ THIS IS THE ISSUE!")
        print("\n   PROBLEM:")
        print("      The registration endpoint is not calling create_otp_for_user()")
        print("      OR an exception is being raised before OTP generation")
        return False

if __name__ == "__main__":
    print(Colors.BOLD + Colors.OKBLUE + """
╔════════════════════════════════════════════════════════════════════╗
║      MANUAL REGISTRATION OTP TEST                                  ║
║      College Digital Voting System                                ║
╚════════════════════════════════════════════════════════════════════╝
""" + Colors.ENDC)
    
    class Colors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
    
    result = test_registration()
    
    print("\n" + "="*70)
    if result:
        print("✓ TEST PASSED: OTP is being sent after registration!")
    else:
        print("✗ TEST FAILED: OTP is NOT being sent after registration!")
    print("="*70 + "\n")
