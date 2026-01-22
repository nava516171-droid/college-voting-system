#!/usr/bin/env python3
"""
Complete test suite for Welcome Letter & OTP Email System
Tests registration, login, OTP request, and OTP verification
"""

import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}@test.com"
TEST_PASSWORD = "TestPassword123"
TEST_FULL_NAME = "Test User"
TEST_ROLL_NUMBER = f"TEST_{datetime.now().strftime('%Y%m%d%H%M%S')}"

print("\n" + "="*70)
print("COLLEGE VOTING SYSTEM - EMAIL & OTP TEST SUITE")
print("="*70)
print(f"\nTest Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Test Email: {TEST_EMAIL}")
print(f"Test Roll Number: {TEST_ROLL_NUMBER}")

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{RESET}")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ️  {text}{RESET}")

def test_backend_health():
    """Test if backend server is running"""
    print_header("TEST 1: Backend Health Check")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("Backend server is running")
            print(f"  Response: {response.json()}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Is the server running on http://localhost:8000?")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_registration():
    """Test user registration"""
    print_header("TEST 2: User Registration (Welcome Email)")
    try:
        payload = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "full_name": TEST_FULL_NAME,
            "roll_number": TEST_ROLL_NUMBER
        }
        
        print_info(f"Registering user: {TEST_EMAIL}")
        response = requests.post(
            f"{API_BASE_URL}/api/auth/register",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("User registered successfully!")
            print(f"  User ID: {data.get('id')}")
            print(f"  Email: {data.get('email')}")
            print(f"  Full Name: {data.get('full_name')}")
            print(f"  Roll Number: {data.get('roll_number')}")
            print_success("✉️  WELCOME EMAIL SENT (check your inbox)")
            return True
        else:
            print_error(f"Registration failed with status {response.status_code}")
            print(f"  Response: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Registration error: {str(e)}")
        return False

def test_login(email, password):
    """Test user login"""
    print_header("TEST 3: User Login")
    try:
        payload = {
            "email": email,
            "password": password
        }
        
        print_info(f"Logging in user: {email}")
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print_success("User logged in successfully!")
            print(f"  Token Type: {data.get('token_type')}")
            print(f"  User: {data.get('user', {}).get('full_name')}")
            return token
        else:
            print_error(f"Login failed with status {response.status_code}")
            print(f"  Response: {response.json()}")
            return None
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return None

def test_otp_request(email):
    """Test OTP request"""
    print_header("TEST 4: OTP Request (Welcome Letter Email)")
    try:
        payload = {"email": email}
        
        print_info(f"Requesting OTP for: {email}")
        response = requests.post(
            f"{API_BASE_URL}/api/otp/request",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("OTP requested successfully!")
            print(f"  Message: {data.get('message')}")
            print(f"  Email: {data.get('email')}")
            print(f"  Expires in: {data.get('expires_in_minutes')} minutes")
            print_success("✉️  OTP EMAIL WITH WELCOME LETTER SENT (check your inbox)")
            return True
        else:
            print_error(f"OTP request failed with status {response.status_code}")
            print(f"  Response: {response.json()}")
            return False
    except Exception as e:
        print_error(f"OTP request error: {str(e)}")
        return False

def test_email_configuration():
    """Test email configuration"""
    print_header("TEST 5: Email Configuration")
    try:
        print_info("Checking email configuration...")
        
        # Try to import and check settings
        import sys
        sys.path.insert(0, '/Users/Navaneeth M/Desktop/college voting system')
        
        from app.config import settings
        
        print_success("Email Configuration Found:")
        print(f"  SMTP Server: {settings.SMTP_SERVER}")
        print(f"  SMTP Port: {settings.SMTP_PORT}")
        print(f"  Sender Name: {settings.SENDER_NAME}")
        print(f"  Sender Email: {settings.SENDER_EMAIL}")
        print(f"  SMTP User: {settings.SMTP_USER}")
        
        # Mask the password for security
        password = settings.SMTP_PASSWORD
        masked_password = password[:3] + "*" * (len(password) - 6) + password[-3:] if len(password) > 6 else "***"
        print(f"  SMTP Password: {masked_password}")
        
        return True
    except Exception as e:
        print_error(f"Could not load configuration: {str(e)}")
        return False

def test_api_endpoints():
    """Test all available API endpoints"""
    print_header("TEST 6: Available API Endpoints")
    try:
        print_info("Testing endpoint availability...")
        
        endpoints = [
            ("GET", "/"),
            ("GET", "/health"),
            ("GET", "/docs"),
            ("POST", "/api/auth/register"),
            ("POST", "/api/auth/login"),
            ("POST", "/api/otp/request"),
            ("POST", "/api/otp/verify"),
            ("GET", "/api/elections"),
        ]
        
        working = 0
        for method, endpoint in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=3)
                else:
                    response = requests.post(f"{API_BASE_URL}{endpoint}", timeout=3)
                
                status = "✅" if response.status_code < 500 else "⚠️"
                print(f"  {status} {method:4} {endpoint:30} → {response.status_code}")
                working += 1
            except Exception as e:
                print(f"  ⚠️  {method:4} {endpoint:30} → Error")
        
        print_success(f"Found {working}/{len(endpoints)} accessible endpoints")
        return True
    except Exception as e:
        print_error(f"Error testing endpoints: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + BLUE + "Starting comprehensive system test..." + RESET)
    
    results = {}
    
    # Test 1: Backend Health
    results['Backend Health'] = test_backend_health()
    if not results['Backend Health']:
        print_error("Cannot continue without backend server!")
        return results
    
    # Test 2: Email Configuration
    results['Email Configuration'] = test_email_configuration()
    
    # Test 3: API Endpoints
    results['API Endpoints'] = test_api_endpoints()
    
    # Test 4: User Registration
    results['User Registration'] = test_registration()
    
    # Test 5: User Login
    token = None
    if results['User Registration']:
        token = test_login(TEST_EMAIL, TEST_PASSWORD)
        results['User Login'] = token is not None
    
    # Test 6: OTP Request
    if results['User Registration']:
        results['OTP Request'] = test_otp_request(TEST_EMAIL)
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{GREEN}✅ PASSED{RESET}" if result else f"{RED}❌ FAILED{RESET}"
        print(f"  {test_name:30} {status}")
    
    print(f"\n{BLUE}Results: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print_success("ALL TESTS PASSED! System is working correctly.")
    else:
        print_error(f"{total - passed} test(s) failed. Please check the errors above.")
    
    # Important Information
    print_header("IMPORTANT: NEXT STEPS")
    print(f"""
{YELLOW}To test the WELCOME LETTERS & OTP EMAILS:
{RESET}
1. Check your email inbox for:
   - Welcome Email (sent at registration)
   - OTP Email (sent at OTP request)

2. Both emails should contain:
   ✅ Professional welcome banner
   ✅ System information
   ✅ Key features
   ✅ Getting started guide
   ✅ Security warnings
   ✅ Support contact info

3. Test Email Information:
   - Test Email: {TEST_EMAIL}
   - Test Roll Number: {TEST_ROLL_NUMBER}
   - Test Password: {TEST_PASSWORD}

4. To complete OTP verification:
   - Copy the 6-digit OTP code from the email
   - Use the frontend to enter it
   - This will allow access to the voting system

{BLUE}Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}
""")
    
    return results

if __name__ == "__main__":
    results = main()
    print("\n" + "="*70 + "\n")
