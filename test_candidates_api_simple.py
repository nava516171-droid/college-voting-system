#!/usr/bin/env python
"""Test script to verify candidates API endpoint"""

import requests
import json

API_BASE_URL = "http://localhost:8001"

# Test 1: Get all elections
print("\n" + "="*60)
print("TEST 1: Getting all elections")
print("="*60)

response = requests.get(f"{API_BASE_URL}/api/elections")
print(f"Status: {response.status_code}")
elections = response.json()
print(f"Elections: {json.dumps(elections, indent=2)}")

if elections and len(elections) > 0:
    election_id = elections[0]['id']
    
    # Test 2: Get candidates for that election
    print("\n" + "="*60)
    print(f"TEST 2: Getting candidates for election {election_id}")
    print("="*60)
    
    response = requests.get(f"{API_BASE_URL}/api/elections/{election_id}/candidates")
    print(f"Status: {response.status_code}")
    candidates = response.json()
    print(f"Candidates: {json.dumps(candidates, indent=2)}")
else:
    print("\nNo elections found!")

print("\n" + "="*60)
