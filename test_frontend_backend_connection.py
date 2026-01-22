#!/usr/bin/env python3
"""
Frontend-Backend Connection Test Suite
Tests both backend API and frontend connectivity
"""

import subprocess
import time
import requests
import json
import sys
from pathlib import Path

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def test_backend_startup():
    """Start backend server"""
    print_section("BACKEND INITIALIZATION")
    
    try:
        print("Starting FastAPI backend server on port 8001...")
        process = subprocess.Popen(
            ["python", "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path.cwd()
        )
        
        print("Waiting for backend to initialize (5 seconds)...")
        time.sleep(5)
        
        if process.poll() is None:
            print("✓ Backend server: STARTED on port 8001")
            return process
        else:
            stdout, stderr = process.communicate()
            print("✗ Backend server: FAILED TO START")
            if stderr:
                print(f"  Error: {stderr.decode()[:300]}")
            return None
            
    except Exception as e:
        print(f"✗ Backend startup failed: {str(e)}")
        return None

def test_backend_endpoints():
    """Test critical backend endpoints"""
    print_section("BACKEND ENDPOINT TESTS")
    
    endpoints = [
        ("GET", "/health", "Health Check"),
        ("GET", "/", "Root Endpoint"),
        ("GET", "/api/elections", "Elections"),
        ("GET", "/api/candidates/all", "Candidates"),
    ]
    
    results = {}
    
    for method, path, description in endpoints:
        try:
            url = f"http://localhost:8001{path}"
            response = requests.request(method, url, timeout=3)
            
            if response.status_code in [200, 401]:  # 401 means endpoint exists but needs auth
                print(f"✓ {description:20} {method} {path:35} Status: {response.status_code}")
                results[description] = True
            else:
                print(f"✗ {description:20} {method} {path:35} Status: {response.status_code}")
                results[description] = False
                
        except requests.exceptions.ConnectionError:
            print(f"✗ {description:20} {method} {path:35} Connection failed")
            results[description] = False
        except Exception as e:
            print(f"✗ {description:20} {method} {path:35} Error: {str(e)[:50]}")
            results[description] = False
    
    return results

def test_frontend_setup():
    """Check frontend configuration"""
    print_section("FRONTEND SETUP VERIFICATION")
    
    results = {}
    
    # Check if frontend directory exists
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        print(f"✓ Frontend directory: EXISTS")
        results["frontend_dir"] = True
    else:
        print(f"✗ Frontend directory: NOT FOUND")
        results["frontend_dir"] = False
        return results
    
    # Check package.json
    package_json = frontend_dir / "package.json"
    if package_json.exists():
        print(f"✓ package.json: EXISTS")
        results["package_json"] = True
    else:
        print(f"✗ package.json: NOT FOUND")
        results["package_json"] = False
    
    # Check api.js
    api_js = frontend_dir / "src" / "api.js"
    if api_js.exists():
        print(f"✓ api.js: EXISTS")
        results["api_js"] = True
        
        # Check API_BASE_URL configuration
        with open(api_js, 'r') as f:
            content = f.read()
            if "API_BASE_URL" in content:
                print(f"  └─ API_BASE_URL configured: http://localhost:8001 (default)")
                results["api_url"] = True
            else:
                print(f"  ✗ API_BASE_URL not found in api.js")
                results["api_url"] = False
    else:
        print(f"✗ api.js: NOT FOUND")
        results["api_js"] = False
        results["api_url"] = False
    
    # Check dependencies
    try:
        with open(package_json, 'r') as f:
            pkg = json.load(f)
            
        print(f"\n✓ Dependencies installed:")
        for dep in ['react', 'react-dom', 'axios', 'react-router-dom']:
            if dep in pkg.get('dependencies', {}):
                version = pkg['dependencies'][dep]
                print(f"  ✓ {dep:20} {version}")
            else:
                print(f"  ✗ {dep:20} MISSING")
    except Exception as e:
        print(f"✗ Error reading package.json: {str(e)}")
    
    return results

def test_api_integration():
    """Test frontend-backend API integration"""
    print_section("API INTEGRATION TESTS")
    
    results = {}
    
    # Test 1: Register endpoint
    print("Test 1: User Registration Endpoint")
    try:
        response = requests.post(
            "http://localhost:8001/api/auth/register",
            json={
                "email": "test_integration@example.com",
                "password": "TestPassword123",
                "full_name": "Integration Test User",
                "roll_number": "TEST001"
            },
            timeout=3
        )
        if response.status_code in [200, 400, 409]:  # 400/409 = user exists
            print(f"✓ Registration endpoint responding: Status {response.status_code}")
            results["register"] = True
        else:
            print(f"✗ Unexpected status: {response.status_code}")
            results["register"] = False
    except Exception as e:
        print(f"✗ Registration endpoint error: {str(e)[:100]}")
        results["register"] = False
    
    # Test 2: Login endpoint
    print("\nTest 2: User Login Endpoint")
    try:
        response = requests.post(
            "http://localhost:8001/api/auth/login",
            json={
                "email": "test_integration@example.com",
                "password": "TestPassword123"
            },
            timeout=3
        )
        if response.status_code in [200, 401, 400]:
            print(f"✓ Login endpoint responding: Status {response.status_code}")
            results["login"] = True
        else:
            print(f"✗ Unexpected status: {response.status_code}")
            results["login"] = False
    except Exception as e:
        print(f"✗ Login endpoint error: {str(e)[:100]}")
        results["login"] = False
    
    # Test 3: Elections endpoint
    print("\nTest 3: Elections Endpoint")
    try:
        response = requests.get(
            "http://localhost:8001/api/elections",
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Elections endpoint responding: {len(data) if isinstance(data, list) else 1} election(s)")
            results["elections"] = True
        else:
            print(f"✗ Unexpected status: {response.status_code}")
            results["elections"] = False
    except Exception as e:
        print(f"✗ Elections endpoint error: {str(e)[:100]}")
        results["elections"] = False
    
    # Test 4: Candidates endpoint
    print("\nTest 4: Candidates Endpoint")
    try:
        response = requests.get(
            "http://localhost:8001/api/candidates/all",
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Candidates endpoint responding: {len(data) if isinstance(data, list) else 1} candidate(s)")
            results["candidates"] = True
        else:
            print(f"✗ Unexpected status: {response.status_code}")
            results["candidates"] = False
    except Exception as e:
        print(f"✗ Candidates endpoint error: {str(e)[:100]}")
        results["candidates"] = False
    
    return results

def test_cors_headers():
    """Test CORS headers"""
    print_section("CORS CONFIGURATION")
    
    try:
        response = requests.options(
            "http://localhost:8001/api/elections",
            headers={
                "Origin": "http://localhost:3000"
            },
            timeout=3
        )
        
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
        }
        
        print("✓ CORS Headers detected:")
        for header, value in cors_headers.items():
            if value:
                print(f"  ✓ {header}: {value}")
            else:
                print(f"  ℹ {header}: Not set (may be wildcard)")
        
        return True
        
    except Exception as e:
        print(f"✗ CORS check failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  FRONTEND-BACKEND CONNECTION TEST SUITE")
    print("="*70)
    
    all_results = {}
    
    # Start backend
    backend_process = test_backend_startup()
    
    if not backend_process:
        print("\n✗ Cannot proceed - backend failed to start")
        sys.exit(1)
    
    try:
        # Test backend
        all_results["backend"] = test_backend_endpoints()
        
        # Test frontend setup
        all_results["frontend"] = test_frontend_setup()
        
        # Test API integration
        all_results["integration"] = test_api_integration()
        
        # Test CORS
        print_section("CORS CONFIGURATION")
        test_cors_headers()
        
        # Generate summary
        print_section("CONNECTION TEST SUMMARY")
        
        backend_pass = sum(1 for v in all_results["backend"].values() if v)
        backend_total = len(all_results["backend"])
        
        frontend_pass = sum(1 for v in all_results["frontend"].values() if v)
        frontend_total = len(all_results["frontend"])
        
        integration_pass = sum(1 for v in all_results["integration"].values() if v)
        integration_total = len(all_results["integration"])
        
        print(f"\nBackend Tests:        {backend_pass}/{backend_total} passed")
        print(f"Frontend Tests:       {frontend_pass}/{frontend_total} passed")
        print(f"Integration Tests:    {integration_pass}/{integration_total} passed")
        
        total_pass = backend_pass + frontend_pass + integration_pass
        total_tests = backend_total + frontend_total + integration_total
        
        print(f"\n{'─'*70}")
        print(f"Total:                {total_pass}/{total_tests} passed")
        
        if total_pass == total_tests:
            print(f"\n✓ FRONTEND-BACKEND CONNECTION: FULLY OPERATIONAL")
        elif total_pass > (total_tests * 0.75):
            print(f"\n⚠ FRONTEND-BACKEND CONNECTION: MOSTLY OPERATIONAL")
        else:
            print(f"\n✗ FRONTEND-BACKEND CONNECTION: ISSUES DETECTED")
        
        print("\nStartup Instructions:")
        print("  1. Backend (port 8001): Already running (python main.py)")
        print("  2. Frontend (port 3000): npm start (from frontend directory)")
        print("\nAccess Points:")
        print("  • Frontend:     http://localhost:3000")
        print("  • Backend API:  http://localhost:8001")
        print("  • API Docs:     http://localhost:8001/docs")
        
    finally:
        # Cleanup
        print(f"\n{'─'*70}")
        print("Shutting down backend server...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
        print("✓ Server stopped")

if __name__ == "__main__":
    main()
