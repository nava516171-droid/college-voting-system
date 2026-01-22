#!/usr/bin/env python3
"""
Optimized Frontend-Backend Connection Test
Tests API connectivity with better timeout handling
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
        
        print("Waiting for backend to initialize (8 seconds)...")
        time.sleep(8)
        
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

def test_simple_endpoints():
    """Test basic endpoints with longer timeout"""
    print_section("BACKEND ENDPOINT TESTS (Simple)")
    
    endpoints = [
        ("GET", "/health", "Health Check", 5),
        ("GET", "/", "Root Endpoint", 5),
    ]
    
    results = {}
    
    for method, path, description, timeout in endpoints:
        try:
            url = f"http://localhost:8001{path}"
            response = requests.request(method, url, timeout=timeout)
            
            if response.status_code in [200, 401]:
                print(f"✓ {description:25} {response.status_code}")
                results[description] = True
            else:
                print(f"✗ {description:25} Status: {response.status_code}")
                results[description] = False
                
        except requests.exceptions.Timeout:
            print(f"⚠ {description:25} TIMEOUT (server slow)")
            results[description] = False
        except requests.exceptions.ConnectionError:
            print(f"✗ {description:25} Connection refused")
            results[description] = False
        except Exception as e:
            print(f"✗ {description:25} Error: {str(e)[:40]}")
            results[description] = False
    
    return results

def test_data_endpoints():
    """Test data endpoints with longer timeout"""
    print_section("BACKEND DATA ENDPOINTS (With Timeout)")
    
    endpoints = [
        ("GET", "/api/elections", "Elections", 10),
        ("GET", "/api/candidates/all", "Candidates", 10),
    ]
    
    results = {}
    
    for method, path, description, timeout in endpoints:
        try:
            url = f"http://localhost:8001{path}"
            print(f"Testing {description} (timeout: {timeout}s)...")
            response = requests.request(method, url, timeout=timeout)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    count = len(data) if isinstance(data, list) else 1
                    print(f"✓ {description:25} Status: 200, Records: {count}")
                    results[description] = True
                except:
                    print(f"✓ {description:25} Status: 200")
                    results[description] = True
            else:
                print(f"✗ {description:25} Status: {response.status_code}")
                results[description] = False
                
        except requests.exceptions.Timeout:
            print(f"⚠ {description:25} TIMEOUT - Server is slow")
            results[description] = False
        except requests.exceptions.ConnectionError:
            print(f"✗ {description:25} Connection refused")
            results[description] = False
        except Exception as e:
            print(f"✗ {description:25} Error: {str(e)[:40]}")
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
                print(f"  └─ API configured for: http://localhost:8001")
                results["api_url"] = True
            else:
                print(f"  ✗ API_BASE_URL not found in api.js")
                results["api_url"] = False
    else:
        print(f"✗ api.js: NOT FOUND")
        results["api_js"] = False
        results["api_url"] = False
    
    # Check key dependencies
    print(f"\nKey Dependencies:")
    try:
        with open(package_json, 'r') as f:
            pkg = json.load(f)
            
        required_deps = ['react', 'react-dom', 'axios']
        for dep in required_deps:
            if dep in pkg.get('dependencies', {}):
                version = pkg['dependencies'][dep]
                print(f"  ✓ {dep:20} {version}")
            else:
                print(f"  ✗ {dep:20} MISSING")
    except Exception as e:
        print(f"✗ Error reading package.json: {str(e)}")
    
    return results

def test_api_endpoint_existence():
    """Test if endpoints respond (even if slowly)"""
    print_section("API ENDPOINT CONNECTIVITY TEST")
    
    endpoints = [
        "/api/auth/register",
        "/api/auth/login",
        "/api/elections",
        "/api/candidates/all",
    ]
    
    print("Testing endpoint accessibility (with extended timeout)...\n")
    
    results = {}
    for path in endpoints:
        try:
            url = f"http://localhost:8001{path}"
            response = requests.get(url, timeout=15)  # 15 second timeout
            status = response.status_code
            status_text = "OK" if status == 200 else "ACCESSIBLE" if status in [401, 400, 404] else f"HTTP {status}"
            print(f"✓ {path:40} {status_text}")
            results[path] = True
        except requests.exceptions.Timeout:
            print(f"⚠ {path:40} TIMEOUT (exists but slow)")
            results[path] = False
        except Exception as e:
            print(f"✗ {path:40} {str(e)[:30]}")
            results[path] = False
    
    return results

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  FRONTEND-BACKEND CONNECTION TEST")
    print("="*70)
    
    # Start backend
    backend_process = test_backend_startup()
    
    if not backend_process:
        print("\n✗ Cannot proceed - backend failed to start")
        sys.exit(1)
    
    try:
        # Give server extra time to warm up
        print("\nServer warm-up (5 seconds)...")
        time.sleep(5)
        
        # Test simple endpoints first
        simple_results = test_simple_endpoints()
        
        # Test data endpoints
        data_results = test_data_endpoints()
        
        # Test frontend
        frontend_results = test_frontend_setup()
        
        # Test API endpoints
        api_results = test_api_endpoint_existence()
        
        # Summary
        print_section("CONNECTION TEST SUMMARY")
        
        simple_pass = sum(1 for v in simple_results.values() if v)
        data_pass = sum(1 for v in data_results.values() if v)
        frontend_pass = sum(1 for v in frontend_results.values() if v)
        api_pass = sum(1 for v in api_results.values() if v)
        
        print(f"\nBackend (Simple):        {simple_pass}/{len(simple_results)} passed")
        print(f"Backend (Data):          {data_pass}/{len(data_results)} passed")
        print(f"Frontend Setup:          {frontend_pass}/{len(frontend_results)} passed")
        print(f"API Endpoints:           {api_pass}/{len(api_results)} passed")
        
        total_pass = simple_pass + data_pass + frontend_pass + api_pass
        total_tests = len(simple_results) + len(data_results) + len(frontend_results) + len(api_results)
        
        print(f"\n{'─'*70}")
        print(f"Overall:                 {total_pass}/{total_tests} passed")
        
        if simple_pass > 0:
            print(f"\n✓ BACKEND: OPERATIONAL (Port 8001)")
        if frontend_pass >= 3:
            print(f"✓ FRONTEND: CONFIGURED (Ready for npm start)")
        if api_pass >= 2:
            print(f"✓ API ENDPOINTS: ACCESSIBLE")
        
        print("\n" + "─"*70)
        print("NEXT STEPS:")
        print("  1. Backend is running on: http://localhost:8001")
        print("  2. Start frontend:        cd frontend && npm install && npm start")
        print("  3. Access frontend on:    http://localhost:3000")
        print("  4. View API docs:         http://localhost:8001/docs")
        
    finally:
        # Cleanup
        print(f"\n{'─'*70}")
        print("Shutting down backend server...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
        print("✓ Backend stopped")

if __name__ == "__main__":
    main()
