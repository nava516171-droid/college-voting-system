import requests
import json

BASE_URL = "http://localhost:8000"

print('=' * 80)
print(' VOTING ENDPOINTS TEST')
print('=' * 80)
print()

# Step 1: Login to get JWT token
print('[1] Logging in as voter...')
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "email": "voter4399@college.com",
        "password": "password123"
    }
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f'✅ Login successful!')
    print(f'   Token: {token[:30]}...')
else:
    print(f'❌ Login failed: {login_response.status_code}')
    print(f'   Response: {login_response.text}')
    exit(1)

print()

# Step 2: Cast a vote
print('[2] Casting a vote for Raj Kumar...')
headers = {"Authorization": f"Bearer {token}"}
vote_data = {
    "election_id": 1,
    "candidate_id": 1
}

vote_response = requests.post(
    f"{BASE_URL}/api/votes/",
    json=vote_data,
    headers=headers
)

if vote_response.status_code == 200:
    print(f'✅ Vote cast successfully!')
    vote_info = vote_response.json()
    print(f'   Vote ID: {vote_info.get("id")}')
    print(f'   Candidate ID: {vote_info.get("candidate_id")}')
    print(f'   Election ID: {vote_info.get("election_id")}')
else:
    print(f'❌ Vote failed: {vote_response.status_code}')
    print(f'   Response: {vote_response.text}')

print()

# Step 3: Get election results
print('[3] Getting election results...')
results_response = requests.get(
    f"{BASE_URL}/api/votes/election/1"
)

if results_response.status_code == 200:
    print(f'✅ Results retrieved successfully!')
    results = results_response.json()
    print(f'   Results:')
    if isinstance(results, list):
        for result in results:
            print(f'     - {result.get("candidate_name", "Unknown")}: {result.get("vote_count", 0)} votes')
    else:
        print(f'   Total votes: {results.get("total_votes", 0)}')
        for result in results.get("results", []):
            print(f'     - {result.get("candidate_name", "Unknown")}: {result.get("vote_count", 0)} votes')
else:
    print(f'❌ Results retrieval failed: {results_response.status_code}')
    print(f'   Response: {results_response.text}')

print()

# Step 4: Try to vote again (should fail)
print('[4] Attempting to vote again (should fail)...')
vote_response2 = requests.post(
    f"{BASE_URL}/api/votes/",
    json=vote_data,
    headers=headers
)

if vote_response2.status_code != 200:
    print(f'✅ Correctly prevented duplicate vote!')
    print(f'   Status: {vote_response2.status_code}')
    print(f'   Error: {vote_response2.json().get("detail", "Unknown error")}')
else:
    print(f'❌ Duplicate vote was allowed (unexpected)')

print()
print('=' * 80)
print(' VOTING TEST COMPLETE')
print('=' * 80)
