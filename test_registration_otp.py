import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001"

# Test registration with a new user
test_user = {
    "full_name": "OTP Test User",
    "email": f"otptest{datetime.now().timestamp()}@example.com",
    "roll_number": f"TEST{int(datetime.now().timestamp())}",
    "password": "TestPassword123!",
    "confirm_password": "TestPassword123!"
}

print(f"\n{'='*60}")
print(f"[TEST] Registering user: {test_user['full_name']}")
print(f"[TEST] Email: {test_user['email']}")
print(f"{'='*60}\n")

response = requests.post(f"{BASE_URL}/api/auth/register", json=test_user)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    print(f"\n{'='*60}")
    print(f"[SUCCESS] User registered successfully!")
    print(f"[INFO] Check the backend logs for OTP sending details")
    print(f"{'='*60}\n")
else:
    print(f"\n{'='*60}")
    print(f"[ERROR] Registration failed!")
    print(f"{'='*60}\n")
