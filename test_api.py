#!/usr/bin/env python3
"""
Quick test script for FastAPI endpoints
Run this after starting api_server.py to test the endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_full_calculation():
    """Test full calculation endpoint"""
    print("Testing /api/v1/calculate/full endpoint...")
    payload = {
        "name": "Test User",
        "dob": "1978-09-18",
        "tob": "17:35",
        "place": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "tz_offset": 5.5
    }
    response = requests.post(f"{BASE_URL}/api/v1/calculate/full", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"SAV Total: {data['sav_total']}")
        print(f"Sun BAV Total: {data['bav_totals']['SUN']}")
        print(f"Sun BAV Chart: {data['bav_charts']['SUN']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_bav_calculation():
    """Test individual BAV calculation"""
    print("Testing /api/v1/calculate/bav/SUN endpoint...")
    payload = {
        "dob": "1978-09-18",
        "tob": "17:35",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "tz_offset": 5.5
    }
    response = requests.post(f"{BASE_URL}/api/v1/calculate/bav/SUN", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Planet: {data['planet']}")
        print(f"Total: {data['total']}")
        print(f"BAV Chart: {data['bav_chart']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_sav_calculation():
    """Test SAV calculation"""
    print("Testing /api/v1/calculate/sav endpoint...")
    payload = {
        "dob": "1978-09-18",
        "tob": "17:35",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "tz_offset": 5.5
    }
    response = requests.post(f"{BASE_URL}/api/v1/calculate/sav", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"SAV Total: {data['total']}")
        print(f"House Strengths: {data['house_strengths']}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("FastAPI Endpoint Tests")
    print("=" * 60)
    print("Make sure api_server.py is running on port 8000\n")
    
    try:
        test_health()
        test_full_calculation()
        test_bav_calculation()
        test_sav_calculation()
        print("✅ All tests completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API server.")
        print("   Make sure api_server.py is running: python api_server.py")
    except Exception as e:
        print(f"❌ Error: {e}")

