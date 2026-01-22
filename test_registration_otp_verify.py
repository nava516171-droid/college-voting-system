"""
Test script to verify OTP email sending after registration
This script will:
1. Create a test user account
2. Check if OTP is created in the database
3. Verify if OTP email sending works
4. Check the database for OTP records
"""

import requests
import json
import sys
from datetime import datetime
import sqlite3

# Configuration
API_BASE_URL = "http://localhost:8001/api"
DB_PATH = "voting_system.db"

# Colors for output
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

def test_registration_with_otp():
    """Test user registration and verify OTP is sent"""
    print_section("TEST 1: USER REGISTRATION WITH OTP VERIFICATION")
    
    # Test user data
    test_email = f"test_otp_{datetime.now().strftime('%Y%m%d_%H%M%S')}@test.com"
    test_data = {
        "email": test_email,
        "full_name": "OTP Test User",
        "roll_number": f"TEST{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "password": "TestPassword123!"
    }
    
    print_info(f"Registering user with email: {test_email}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json=test_data,
            timeout=30
        )
        
        print_info(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print_success("User registration successful!")
            print(f"  User ID: {user_data.get('id')}")
            print(f"  Email: {user_data.get('email')}")
            print(f"  Full Name: {user_data.get('full_name')}")
            return user_data.get('id'), test_email
        else:
            print_error(f"Registration failed: {response.text}")
            return None, test_email
            
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to API server")
        print_info("Make sure the server is running with: python main.py")
        return None, test_email
    except Exception as e:
        print_error(f"Error during registration: {str(e)}")
        return None, test_email

def check_otp_in_database(user_id):
    """Check if OTP exists in database for the user"""
    print_section("TEST 2: CHECKING OTP IN DATABASE")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Query OTP table
        cursor.execute("""
            SELECT id, user_id, otp_code, is_verified, created_at, expires_at 
            FROM otp 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        """, (user_id,))
        
        otp_record = cursor.fetchone()
        conn.close()
        
        if otp_record:
            print_success("OTP record found in database!")
            otp_id, uid, otp_code, is_verified, created_at, expires_at = otp_record
            print(f"  OTP ID: {otp_id}")
            print(f"  User ID: {uid}")
            print(f"  OTP Code: {otp_code}")
            print(f"  Is Verified: {is_verified}")
            print(f"  Created At: {created_at}")
            print(f"  Expires At: {expires_at}")
            return otp_code
        else:
            print_error("No OTP record found in database!")
            return None
            
    except Exception as e:
        print_error(f"Error checking database: {str(e)}")
        return None

def test_otp_request(email):
    """Test requesting OTP for an email"""
    print_section("TEST 3: REQUEST OTP ENDPOINT")
    
    test_data = {
        "email": email
    }
    
    print_info(f"Requesting OTP for email: {email}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/otp/request",
            json=test_data,
            timeout=30
        )
        
        print_info(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print_success("OTP request successful!")
            print(f"  Message: {result.get('message')}")
            print(f"  Email: {result.get('email')}")
            print(f"  Expires In: {result.get('expires_in_minutes')} minutes")
            return True
        else:
            print_error(f"OTP request failed: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error requesting OTP: {str(e)}")
        return False

def check_email_configuration():
    """Check if email configuration is valid"""
    print_section("TEST 4: EMAIL CONFIGURATION CHECK")
    
    try:
        # Try to import settings
        sys.path.insert(0, '.')
        from app.config import settings
        
        print_info("Email Configuration:")
        print(f"  SMTP Server: {settings.SMTP_SERVER}")
        print(f"  SMTP Port: {settings.SMTP_PORT}")
        
        smtp_user = settings.SMTP_USER if settings.SMTP_USER else "NOT CONFIGURED"
        smtp_password = "***" if settings.SMTP_PASSWORD else "NOT CONFIGURED"
        sender_email = settings.SENDER_EMAIL if settings.SENDER_EMAIL else "NOT CONFIGURED"
        
        print(f"  SMTP User: {smtp_user}")
        print(f"  SMTP Password: {smtp_password}")
        print(f"  Sender Email: {sender_email}")
        
        # Validate configuration
        if not settings.SMTP_USER or settings.SMTP_USER == "your-email@gmail.com":
            print_error("SMTP_USER is not properly configured!")
            return False
        
        if not settings.SMTP_PASSWORD or settings.SMTP_PASSWORD == "your-app-password":
            print_error("SMTP_PASSWORD is not properly configured!")
            return False
        
        if not settings.SENDER_EMAIL or settings.SENDER_EMAIL == "your-email@gmail.com":
            print_error("SENDER_EMAIL is not properly configured!")
            return False
        
        print_success("Email configuration appears to be valid!")
        return True
        
    except Exception as e:
        print_error(f"Error checking configuration: {str(e)}")
        return False

def test_email_connection():
    """Test SMTP connection"""
    print_section("TEST 5: SMTP CONNECTION TEST")
    
    try:
        import smtplib
        from app.config import settings
        
        print_info(f"Attempting to connect to {settings.SMTP_SERVER}:{settings.SMTP_PORT}")
        
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10) as server:
            print_success("Connected to SMTP server")
            
            print_info("Starting TLS encryption...")
            server.starttls()
            print_success("TLS encryption started")
            
            print_info(f"Attempting to login with: {settings.SMTP_USER}")
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            print_success("SMTP authentication successful!")
            
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print_error(f"SMTP Authentication Error: {str(e)}")
        print_warning("Check if SMTP_USER and SMTP_PASSWORD are correct")
        return False
    except smtplib.SMTPException as e:
        print_error(f"SMTP Error: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Connection Error: {str(e)}")
        return False

def main():
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║      OTP EMAIL VERIFICATION TEST SUITE                            ║")
    print("║      College Digital Voting System                                ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    results = {}
    
    # Test 1: Email Configuration
    print_info("Starting test sequence...\n")
    results['email_config'] = check_email_configuration()
    
    # Test 2: SMTP Connection
    results['smtp_connection'] = test_email_connection()
    
    # Test 3: User Registration
    user_id, test_email = test_registration_with_otp()
    results['user_registration'] = user_id is not None
    
    # Test 4: Check OTP in Database
    if user_id:
        otp_code = check_otp_in_database(user_id)
        results['otp_created'] = otp_code is not None
        
        # Test 5: Request OTP
        results['otp_request'] = test_otp_request(test_email)
    
    # Summary
    print_section("TEST SUMMARY")
    
    for test_name, result in results.items():
        status = f"{Colors.OKGREEN}PASSED{Colors.ENDC}" if result else f"{Colors.FAIL}FAILED{Colors.ENDC}"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print("\n" + "="*70)
    
    if all(results.values()):
        print_success("ALL TESTS PASSED! OTP EMAIL SYSTEM IS WORKING CORRECTLY")
    else:
        print_error("Some tests failed. Please check the configuration and try again.")
        print("\n" + Colors.WARNING + "TROUBLESHOOTING STEPS:" + Colors.ENDC)
        if not results.get('email_config'):
            print("1. Check your .env file for correct SMTP credentials")
        if not results.get('smtp_connection'):
            print("2. Verify Gmail App Password is correctly set")
            print("   - Go to: https://myaccount.google.com/apppasswords")
            print("   - Select Mail and Windows Computer")
            print("   - Copy the 16-character password to SMTP_PASSWORD in .env")
        if not results.get('user_registration'):
            print("3. Ensure the backend server is running: python main.py")
        if not results.get('otp_created'):
            print("4. Check the database for OTP table structure")

if __name__ == "__main__":
    main()
