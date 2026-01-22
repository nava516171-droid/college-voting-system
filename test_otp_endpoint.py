import requests
import json
import time

BASE_URL = "http://localhost:8000"

# Test user data
email = "test.user@example.com"
password = "Test@123"
full_name = "Test User"
roll_number = "12345"

try:
    # Step 1: Register a user
    print("=" * 60)
    print("Step 1: Registering user...")
    print("=" * 60)
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": full_name,
            "roll_number": roll_number
        }
    )
    print(f"Register response: {response.status_code}")
    reg_data = response.json()
    print(json.dumps(reg_data, indent=2))

    if response.status_code == 200:
        # Step 2: Login
        print("\n" + "=" * 60)
        print("Step 2: Logging in...")
        print("=" * 60)
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": email, "password": password}
        )
        print(f"Login response: {response.status_code}")
        login_data = response.json()
        print(json.dumps(login_data, indent=2))
        
        if response.status_code == 200:
            token = login_data.get("access_token")
            
            # Step 3: Request OTP
            print("\n" + "=" * 60)
            print("Step 3: Requesting OTP...")
            print("=" * 60)
            response = requests.post(
                f"{BASE_URL}/api/otp/request",
                json={"email": email},
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"OTP request response: {response.status_code}")
            otp_data = response.json()
            print(json.dumps(otp_data, indent=2))
            
            if response.status_code != 200:
                print("\n⚠️  ERROR: OTP request failed!")
                print("Check the backend console for error details")
            else:
                print("\n✓ OTP sent successfully!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
