"""
Direct database check for OTP functionality
This script checks the database directly without needing the API to be running
"""

import sqlite3
from datetime import datetime, timedelta
import sys

DB_PATH = "voting_system.db"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_section(title):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{title:^70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

def print_success(message):
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def check_database_structure():
    """Check if database and tables exist"""
    print_section("CHECKING DATABASE STRUCTURE")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print_info(f"Database file: {DB_PATH}")
        print_success(f"Database connected successfully")
        print_info(f"Found {len(tables)} tables:\n")
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"  • {table_name}")
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                print(f"      - {col_name} ({col_type})")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Error checking database: {str(e)}")
        return False

def check_users():
    """Check users in database"""
    print_section("CHECKING USERS")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, email, full_name, is_active, created_at FROM users ORDER BY created_at DESC LIMIT 5")
        users = cursor.fetchall()
        
        if users:
            print_success(f"Found {len(users)} recent users:")
            for user in users:
                user_id, email, full_name, is_active, created_at = user
                status = "✓ Active" if is_active else "✗ Inactive"
                print(f"\n  ID: {user_id}")
                print(f"  Email: {email}")
                print(f"  Name: {full_name}")
                print(f"  Status: {status}")
                print(f"  Created: {created_at}")
        else:
            print_warning("No users found in database")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Error checking users: {str(e)}")
        return False

def check_otps():
    """Check OTP records in database"""
    print_section("CHECKING OTP RECORDS")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if OTP table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='otps'")
        if not cursor.fetchone():
            print_error("OTP table does not exist in database!")
            
            # Show alternatives
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%otp%'")
            alternatives = cursor.fetchall()
            if alternatives:
                print_warning(f"Found similar tables: {[t[0] for t in alternatives]}")
            conn.close()
            return False
        
        # Get recent OTP records
        cursor.execute("""
            SELECT id, user_id, otp_code, is_verified, created_at, expires_at 
            FROM otps 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        otps = cursor.fetchall()
        
        if otps:
            print_success(f"Found {len(otps)} recent OTP records:")
            for otp in otps:
                otp_id, user_id, otp_code, is_verified, created_at, expires_at = otp
                
                # Check if expired
                expires_at_dt = datetime.fromisoformat(expires_at) if expires_at else None
                is_expired = expires_at_dt < datetime.utcnow() if expires_at_dt else True
                
                status = "✓ Verified" if is_verified else "✗ Not Verified"
                expiry = "✓ Valid" if not is_expired else "✗ Expired"
                
                print(f"\n  OTP ID: {otp_id}")
                print(f"  User ID: {user_id}")
                print(f"  Code: {otp_code}")
                print(f"  Verification Status: {status}")
                print(f"  Expiry Status: {expiry}")
                print(f"  Created: {created_at}")
                print(f"  Expires: {expires_at}")
        else:
            print_warning("No OTP records found in database")
            print_info("This means OTP hasn't been generated for any user yet")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Error checking OTPs: {str(e)}")
        return False

def check_registration_flow():
    """Check if registration flow is working by looking at recent data"""
    print_section("ANALYZING REGISTRATION FLOW")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get the most recent user
        cursor.execute("""
            SELECT id, email, full_name, created_at 
            FROM users 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        latest_user = cursor.fetchone()
        
        if not latest_user:
            print_warning("No users in database to analyze")
            conn.close()
            return False
        
        user_id, email, full_name, user_created = latest_user
        print_info(f"Latest user: {full_name} ({email})")
        print_info(f"User created at: {user_created}")
        
        # Check if OTP was created for this user
        cursor.execute("""
            SELECT id, otp_code, created_at, expires_at, is_verified
            FROM otps
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        otp_record = cursor.fetchone()
        
        if otp_record:
            otp_id, otp_code, otp_created, expires_at, is_verified = otp_record
            print_success(f"✓ OTP was created for user {user_id}")
            print_info(f"  OTP Code: {otp_code}")
            print_info(f"  Created: {otp_created}")
            print_info(f"  Verification Status: {'Verified' if is_verified else 'Awaiting Verification'}")
            
            # Check if OTP is expired
            expires_at_dt = datetime.fromisoformat(expires_at) if expires_at else None
            if expires_at_dt and expires_at_dt > datetime.utcnow():
                print_success(f"✓ OTP is still valid (expires at {expires_at})")
            else:
                print_warning(f"⚠ OTP has expired")
        else:
            print_error(f"✗ NO OTP WAS CREATED for user {user_id}")
            print_warning("This indicates the registration process didn't trigger OTP generation")
            print_info("Check the registration endpoint in auth.py")
        
        conn.close()
        return otp_record is not None
        
    except Exception as e:
        print_error(f"Error analyzing registration: {str(e)}")
        return False

def main():
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║      OTP SYSTEM DATABASE VERIFICATION                             ║")
    print("║      College Digital Voting System                                ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    results = {}
    
    # Run checks
    results['database'] = check_database_structure()
    results['users'] = check_users()
    results['otps'] = check_otps()
    results['registration_flow'] = check_registration_flow()
    
    # Summary
    print_section("VERIFICATION SUMMARY")
    
    for test_name, result in results.items():
        status = f"{Colors.OKGREEN}PASSED{Colors.ENDC}" if result else f"{Colors.FAIL}FAILED{Colors.ENDC}"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print("\n" + "="*70)
    
    # Recommendations
    print(f"\n{Colors.BOLD}RECOMMENDATIONS:{Colors.ENDC}\n")
    
    if results['database']:
        print_success("Database structure is correct")
    else:
        print_error("Database has issues - check the database file")
    
    if results['users']:
        print_success("Users are being created")
    else:
        print_warning("No users in database - registration hasn't been tested yet")
    
    if results['otps']:
        print_success("OTP records are being created")
    else:
        print_error("OTP is NOT being created - CHECK REGISTRATION CODE")
    
    if results['registration_flow']:
        print_success("Registration flow appears to be working correctly")
    else:
        print_error("Registration flow may have issues with OTP generation")

if __name__ == "__main__":
    main()
