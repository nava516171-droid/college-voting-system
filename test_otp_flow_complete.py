#!/usr/bin/env python3
"""
Complete OTP Flow Test
Tests: Login -> OTP Request -> OTP Verify
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("COMPLETE OTP FLOW TEST")
print("=" * 70)

# Test credentials
TEST_EMAIL = "thankyounava09@gmail.com"
TEST_PASSWORD = "password123"

# Step 1: Login
print("\n1️⃣  STEP 1: LOGIN")
print("-" * 70)
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
)
print(f"Status: {login_response.status_code}")
login_data = login_response.json()
print(f"Response: {json.dumps(login_data, indent=2)}")

if login_response.status_code != 200:
    print("❌ Login failed!")
    exit(1)

token = login_data.get("access_token")
print(f"✅ Logged in successfully. Token: {token[:20]}...")

# Step 2: Request OTP
print("\n2️⃣  STEP 2: REQUEST OTP")
print("-" * 70)
otp_request_response = requests.post(
    f"{BASE_URL}/api/otp/request",
    json={"email": TEST_EMAIL},
    headers={"Authorization": f"Bearer {token}"}
)
print(f"Status: {otp_request_response.status_code}")
otp_request_data = otp_request_response.json()
print(f"Response: {json.dumps(otp_request_data, indent=2)}")

if otp_request_response.status_code != 200:
    print("❌ OTP request failed!")
    exit(1)

print(f"✅ OTP requested successfully")
print(f"📧 OTP has been sent to: {otp_request_data.get('email')}")
print(f"⏱️  Valid for: {otp_request_data.get('expires_in_minutes')} minutes")

# Step 3: Manual input for OTP verification
print("\n3️⃣  STEP 3: VERIFY OTP")
print("-" * 70)
otp_code = input("📝 Enter the 6-digit OTP code you received in your email: ").strip()

if not otp_code or len(otp_code) != 6:
    print("❌ Invalid OTP format!")
    exit(1)

otp_verify_response = requests.post(
    f"{BASE_URL}/api/otp/verify",
    json={"otp_code": otp_code},
    headers={"Authorization": f"Bearer {token}"}
)
print(f"Status: {otp_verify_response.status_code}")
otp_verify_data = otp_verify_response.json()
print(f"Response: {json.dumps(otp_verify_data, indent=2)}")

if otp_verify_response.status_code != 200:
    print("❌ OTP verification failed!")
    exit(1)

print(f"✅ OTP verified successfully!")

# Summary
print("\n" + "=" * 70)
print("✅ COMPLETE OTP FLOW TEST PASSED")
print("=" * 70)
print("Summary:")
print(f"  ✓ Login: Successful")
print(f"  ✓ OTP Request: Sent to {TEST_EMAIL}")
print(f"  ✓ OTP Verify: {otp_code} verified successfully")
print(f"\nUser can now proceed to voting!")
print("=" * 70)
