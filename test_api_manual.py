import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("COLLEGE VOTING SYSTEM API - VERIFICATION TEST")
print("=" * 70)

# Test 1: Health Check
print("\n✓ Test 1: Health Check")
response = requests.get(f"{BASE_URL}/health")
print(f"  Status Code: {response.status_code}")
print(f"  Response: {response.json()}")
assert response.status_code == 200

# Test 2: Register User
print("\n✓ Test 2: Register User")
register_data = {
    "roll_number": "CS2024001",
    "email": "student1@college.edu",
    "full_name": "Alice Johnson",
    "password": "SecurePass123"
}
response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
print(f"  Status Code: {response.status_code}")
print(f"  Response: {json.dumps(response.json(), indent=2)}")
assert response.status_code == 200
user_id = response.json()["id"]

# Test 3: Login User
print("\n✓ Test 3: Login User")
login_data = {
    "email": "student1@college.edu",
    "password": "SecurePass123"
}
response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
print(f"  Status Code: {response.status_code}")
data = response.json()
print(f"  User: {data['user']['full_name']}")
print(f"  Token Type: {data['token_type']}")
assert response.status_code == 200
token = data["access_token"]

# Test 4: Request OTP
print("\n✓ Test 4: Request OTP")
otp_data = {"email": "student1@college.edu"}
response = requests.post(f"{BASE_URL}/api/otp/request", json=otp_data)
print(f"  Status Code: {response.status_code}")
print(f"  Response: {response.json()}")
assert response.status_code == 200

# Test 5: Get Elections
print("\n✓ Test 5: Get All Elections")
response = requests.get(f"{BASE_URL}/api/elections/")
print(f"  Status Code: {response.status_code}")
elections = response.json()
print(f"  Total Elections: {len(elections)}")
assert response.status_code == 200

# Test 6: Get OTP Status
print("\n✓ Test 6: Check OTP Status")
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/api/otp/status", headers=headers)
print(f"  Status Code: {response.status_code}")
print(f"  Response: {response.json()}")
assert response.status_code == 200

# Test 7: Register Another User
print("\n✓ Test 7: Register Another User")
register_data2 = {
    "roll_number": "CS2024002",
    "email": "student2@college.edu",
    "full_name": "Bob Smith",
    "password": "AnotherPass456"
}
response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data2)
print(f"  Status Code: {response.status_code}")
print(f"  Response: {response.json()['full_name']}")
assert response.status_code == 200

# Test 8: Duplicate Email Prevention
print("\n✓ Test 8: Duplicate Email Prevention")
response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
print(f"  Status Code: {response.status_code}")
print(f"  Error Message: {response.json()['detail']}")
assert response.status_code == 400

# Test 9: Wrong Password
print("\n✓ Test 9: Wrong Password Handling")
wrong_login = {
    "email": "student1@college.edu",
    "password": "WrongPassword"
}
response = requests.post(f"{BASE_URL}/api/auth/login", json=wrong_login)
print(f"  Status Code: {response.status_code}")
print(f"  Error Message: {response.json()['detail']}")
assert response.status_code == 401

# Test 10: Get Root Endpoint
print("\n✓ Test 10: Root Endpoint")
response = requests.get(f"{BASE_URL}/")
print(f"  Status Code: {response.status_code}")
print(f"  Response: {response.json()}")
assert response.status_code == 200

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED - API IS WORKING CORRECTLY!")
print("=" * 70)
print("\nAPI Summary:")
print("  ✅ Health Check: Working")
print("  ✅ User Registration: Working")
print("  ✅ User Login: Working")
print("  ✅ OTP Generation: Working")
print("  ✅ OTP Status Check: Working")
print("  ✅ Error Handling: Working")
print("  ✅ Authorization: Working")
print("  ✅ Database Operations: Working")
print("\nServer is running at: http://localhost:8000")
print("Interactive API Docs: http://localhost:8000/docs")
print("=" * 70)
