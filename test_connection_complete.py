#!/usr/bin/env python3
"""
Comprehensive Backend and Database Connection Test
Verifies database connectivity, tables, and API endpoints
"""

import sys
import sqlite3
import subprocess
import time
import requests
import json
from pathlib import Path

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_database_connection():
    """Test SQLite database connection"""
    print_section("DATABASE CONNECTION TEST")
    
    try:
        conn = sqlite3.connect('voting_system.db')
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if tables:
            print("✓ Database connection: SUCCESSFUL")
            print(f"✓ Database file: voting_system.db")
            print(f"✓ Tables found: {len(tables)}")
            
            # Display table details
            print("\nTable Details:")
            for table in tables:
                table_name = table[0]
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    col_count = len(columns)
                    print(f"  ✓ {table_name}: {count} records, {col_count} columns")
                except Exception as e:
                    print(f"  ✗ {table_name}: Error reading table - {str(e)}")
            
            conn.close()
            return True
        else:
            print("✗ Database connection: FAILED - No tables found")
            conn.close()
            return False
            
    except Exception as e:
        print(f"✗ Database connection: FAILED")
        print(f"  Error: {str(e)}")
        return False

def test_database_schema():
    """Verify database schema integrity"""
    print_section("DATABASE SCHEMA VERIFICATION")
    
    try:
        conn = sqlite3.connect('voting_system.db')
        cursor = conn.cursor()
        
        expected_tables = ['users', 'elections', 'candidates', 'votes', 'otps', 'admins']
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        all_good = True
        for table_name in expected_tables:
            if table_name in existing_tables:
                print(f"✓ Table '{table_name}': EXISTS")
            else:
                print(f"✗ Table '{table_name}': MISSING")
                all_good = False
        
        conn.close()
        return all_good
        
    except Exception as e:
        print(f"✗ Schema verification failed: {str(e)}")
        return False

def test_api_startup():
    """Test if FastAPI backend can start"""
    print_section("BACKEND STARTUP TEST")
    
    try:
        # Start the API server in background
        print("Starting FastAPI server...")
        process = subprocess.Popen(
            ["python", "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path.cwd()
        )
        
        # Wait for server to start
        print("Waiting for server to initialize (5 seconds)...")
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ Backend server: STARTED")
            return process
        else:
            stdout, stderr = process.communicate()
            print("✗ Backend server: FAILED TO START")
            if stderr:
                print(f"  Error: {stderr.decode()[:200]}")
            return None
            
    except Exception as e:
        print(f"✗ Backend startup failed: {str(e)}")
        return None

def test_health_endpoint(max_retries=5):
    """Test the health check endpoint"""
    print_section("API HEALTH CHECK")
    
    url = "http://localhost:8001/health"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✓ Health endpoint: HEALTHY")
                print(f"  Response: {response.json()}")
                return True
            else:
                print(f"✗ Health endpoint returned status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                print(f"  Attempting connection ({attempt + 1}/{max_retries})...")
                time.sleep(1)
            else:
                print(f"✗ Health endpoint: CONNECTION FAILED")
                return False
        except Exception as e:
            print(f"✗ Health endpoint error: {str(e)}")
            return False

def test_root_endpoint():
    """Test the root endpoint"""
    print_section("API ROOT ENDPOINT TEST")
    
    url = "http://localhost:8001/"
    
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print(f"✓ Root endpoint: ACCESSIBLE")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Root endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Root endpoint error: {str(e)}")
        return False

def test_candidate_endpoint():
    """Test the candidates endpoint"""
    print_section("CANDIDATES ENDPOINT TEST")
    
    url = "http://localhost:8001/api/v1/candidates"
    
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            candidates = response.json()
            print(f"✓ Candidates endpoint: ACCESSIBLE")
            if isinstance(candidates, list):
                print(f"  Candidates found: {len(candidates)}")
                if candidates:
                    print(f"  Sample: {candidates[0].get('candidate_name', 'N/A')}")
            return True
        elif response.status_code == 401:
            print(f"✓ Candidates endpoint: ACCESSIBLE (requires auth)")
            return True
        else:
            print(f"✗ Candidates endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Candidates endpoint error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  COLLEGE VOTING SYSTEM - CONNECTION TEST SUITE")
    print("="*60)
    
    results = {}
    
    # Test database
    results['db_connection'] = test_database_connection()
    results['db_schema'] = test_database_schema()
    
    # Try to start the backend
    print_section("STARTING BACKEND SERVER")
    server_process = test_api_startup()
    
    if server_process:
        # Test API endpoints
        results['health'] = test_health_endpoint()
        results['root'] = test_root_endpoint()
        results['candidates'] = test_candidate_endpoint()
        
        # Cleanup
        print("\nShutting down server...")
        server_process.terminate()
        server_process.wait(timeout=5)
        print("✓ Server stopped")
    else:
        print("\n⚠ Cannot test API endpoints - server failed to start")
        results['health'] = False
        results['root'] = False
        results['candidates'] = False
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL SYSTEMS OPERATIONAL")
    else:
        print(f"\n⚠ {total - passed} test(s) failed - see details above")

if __name__ == "__main__":
    main()
