"""Test the candidates API endpoint"""

import requests
import json

def test_api():
    try:
        print("\n" + "="*80)
        print("TESTING CANDIDATES API ENDPOINT")
        print("="*80)
        
        url = "http://localhost:8001/api/candidates/all"
        print(f"\nURL: {url}")
        
        # Test without token
        print("\n1. Testing WITHOUT token (should work)...")
        response = requests.get(url, headers={"Content-Type": "application/json"}, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response Type: {type(response.text)}")
        print(f"Response Text: {response.text[:200]}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\n✅ SUCCESS! Got JSON response")
                print(f"Number of candidates: {len(data)}")
                for i, candidate in enumerate(data, 1):
                    print(f"\n{i}. {candidate.get('name', 'N/A')}")
                    print(f"   - ID: {candidate.get('id')}")
                    print(f"   - Election: {candidate.get('election_id')}")
                    print(f"   - Symbol: {candidate.get('symbol_number')}")
                    print(f"   - Description: {candidate.get('description')}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON Parse Error: {e}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Error Message: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_api()
