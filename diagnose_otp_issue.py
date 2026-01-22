"""
OTP Registration Issue - Diagnostic Report and Fix
This script tests OTP generation manually and provides detailed diagnostics
"""

import sys
sys.path.insert(0, '.')

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.otp import OTP
from app.database import Base
from app.utils.otp import create_otp_for_user, generate_otp
from app.utils.email import send_otp_email
import sqlite3

# Database setup
DATABASE_URL = "sqlite:///voting_system.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

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

def test_otp_generation():
    """Test OTP generation function directly"""
    print_section("TEST 1: OTP GENERATION")
    
    try:
        otp = generate_otp()
        print_success(f"OTP generated successfully: {otp}")
        
        if len(otp) == 6 and otp.isdigit():
            print_success("OTP format is valid (6 digits)")
            return True
        else:
            print_error(f"OTP format is invalid: {otp}")
            return False
            
    except Exception as e:
        print_error(f"Error generating OTP: {str(e)}")
        return False

def test_otp_creation_in_db():
    """Test OTP creation in database"""
    print_section("TEST 2: OTP CREATION IN DATABASE")
    
    try:
        db = SessionLocal()
        
        # Get a test user
        test_user = db.query(User).first()
        
        if not test_user:
            print_error("No test user found in database")
            print_info("Creating a test user for OTP testing...")
            
            from app.utils.security import get_password_hash
            test_user = User(
                email="otp_test@test.com",
                full_name="OTP Test",
                roll_number="OTP_TEST_001",
                hashed_password=get_password_hash("TestPassword123!")
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print_success(f"Test user created: {test_user.id}")
        
        print_info(f"Using test user: {test_user.email} (ID: {test_user.id})")
        
        # Try to create OTP
        print_info("Creating OTP for test user...")
        otp_code = create_otp_for_user(db, test_user.id)
        print_success(f"OTP created: {otp_code}")
        
        # Verify it was saved in database
        print_info("Verifying OTP was saved in database...")
        saved_otp = db.query(OTP).filter(
            OTP.user_id == test_user.id,
            OTP.otp_code == otp_code
        ).first()
        
        if saved_otp:
            print_success("✓ OTP was successfully saved to database")
            print_info(f"  OTP ID: {saved_otp.id}")
            print_info(f"  User ID: {saved_otp.user_id}")
            print_info(f"  Code: {saved_otp.otp_code}")
            print_info(f"  Created: {saved_otp.created_at}")
            print_info(f"  Expires: {saved_otp.expires_at}")
            db.close()
            return True
        else:
            print_error("✗ OTP was NOT saved to database")
            print_error("This suggests a database connection or commit issue")
            db.close()
            return False
            
    except Exception as e:
        print_error(f"Error creating OTP: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_otp_email():
    """Test OTP email sending"""
    print_section("TEST 3: OTP EMAIL SENDING")
    
    try:
        test_email = "test_otp@test.com"
        test_otp = "123456"
        test_name = "Test User"
        
        print_info(f"Attempting to send OTP email to {test_email}")
        result = send_otp_email(test_email, test_otp, test_name)
        
        if result:
            print_success("OTP email sent successfully!")
            return True
        else:
            print_error("OTP email sending failed!")
            return False
            
    except Exception as e:
        print_error(f"Error sending OTP email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def analyze_registration_code():
    """Analyze the registration code to find issues"""
    print_section("CODE ANALYSIS")
    
    print_info("Checking app/routes/auth.py registration endpoint...")
    
    try:
        with open('app/routes/auth.py', 'r') as f:
            content = f.read()
        
        if 'create_otp_for_user' in content:
            print_success("✓ create_otp_for_user() is called in registration")
        else:
            print_error("✗ create_otp_for_user() is NOT called in registration")
            return False
        
        if 'send_otp_email' in content:
            print_success("✓ send_otp_email() is called in registration")
        else:
            print_error("✗ send_otp_email() is NOT called in registration")
            return False
        
        # Check for exception handling
        if 'try:' in content and 'except' in content:
            print_warning("⚠ Code has exception handling - errors might be silent")
        else:
            print_info("✓ No broad exception handling detected")
        
        return True
        
    except Exception as e:
        print_error(f"Error analyzing code: {str(e)}")
        return False

def check_imports():
    """Verify all required imports are available"""
    print_section("IMPORT VERIFICATION")
    
    imports_ok = True
    
    try:
        from app.models.otp import OTP
        print_success("✓ OTP model imported successfully")
    except Exception as e:
        print_error(f"✗ Failed to import OTP model: {str(e)}")
        imports_ok = False
    
    try:
        from app.utils.otp import create_otp_for_user
        print_success("✓ create_otp_for_user function imported successfully")
    except Exception as e:
        print_error(f"✗ Failed to import create_otp_for_user: {str(e)}")
        imports_ok = False
    
    try:
        from app.utils.email import send_otp_email
        print_success("✓ send_otp_email function imported successfully")
    except Exception as e:
        print_error(f"✗ Failed to import send_otp_email: {str(e)}")
        imports_ok = False
    
    return imports_ok

def main():
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║      OTP REGISTRATION ISSUE - DIAGNOSTIC REPORT                    ║")
    print("║      College Digital Voting System                                ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    results = {}
    
    # Run tests
    results['imports'] = check_imports()
    results['otp_generation'] = test_otp_generation()
    results['otp_creation'] = test_otp_creation_in_db()
    results['otp_email'] = test_otp_email()
    results['code_analysis'] = analyze_registration_code()
    
    # Summary
    print_section("DIAGNOSTIC SUMMARY")
    
    for test_name, result in results.items():
        status = f"{Colors.OKGREEN}PASSED{Colors.ENDC}" if result else f"{Colors.FAIL}FAILED{Colors.ENDC}"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print("\n" + "="*70)
    
    # Recommendations
    print(f"\n{Colors.BOLD}FINDINGS AND RECOMMENDATIONS:{Colors.ENDC}\n")
    
    if all(results.values()):
        print_success("ALL TESTS PASSED!")
        print_info("OTP system components are working correctly")
        print_info("The issue may be related to API endpoint or request handling")
    else:
        if not results['imports']:
            print_error("Import issues detected - check model and utility files")
        if not results['otp_generation']:
            print_error("OTP generation failed - check generate_otp() function")
        if not results['otp_creation']:
            print_error("OTP creation failed - likely database connection issue")
        if not results['otp_email']:
            print_error("OTP email sending failed - check SMTP configuration")
        if not results['code_analysis']:
            print_error("Code analysis issues - registration may not call OTP functions")

if __name__ == "__main__":
    main()
