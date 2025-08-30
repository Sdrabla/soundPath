#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints are working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration"""
    url = f"{BASE_URL}/api/register"
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Register Status: {response.status_code}")
        print(f"Register Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Register Error: {e}")
        return False

def test_login():
    """Test user login"""
    url = f"{BASE_URL}/api/login"
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Login Error: {e}")
        return False

def test_ping():
    """Test health check"""
    url = f"{BASE_URL}/ping"
    
    try:
        response = requests.get(url)
        print(f"Ping Status: {response.status_code}")
        print(f"Ping Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Ping Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("=" * 50)
    
    # Test health check
    print("1. Testing health check...")
    ping_success = test_ping()
    
    # Test registration
    print("\n2. Testing user registration...")
    register_success = test_register()
    
    # Test login
    print("\n3. Testing user login...")
    login_success = test_login()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Health Check: {'✅ PASS' if ping_success else ' FAIL'}")
    print(f"Registration: {'✅ PASS' if register_success else ' FAIL'}")
    print(f"Login: {'✅ PASS' if login_success else ' FAIL'}")
    
    if all([ping_success, register_success, login_success]):
        print("\n All tests passed!")
    else:
        print("\n  Some tests failed. Check the output above.")
