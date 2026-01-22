#!/usr/bin/env python
"""
Quick API Test - Run this while server is running
"""
import subprocess
import time
import sys

print("Starting API verification tests...")
print("Make sure the server is running on port 8000\n")

# Start the actual pytest tests
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_api.py", "-v", "--tb=short"],
    capture_output=False,
    text=True
)

sys.exit(result.returncode)
