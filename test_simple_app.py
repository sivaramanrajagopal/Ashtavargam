#!/usr/bin/env python3
"""
Test script for the simplified Ashtakavarga app
"""

import requests
import json

def test_simple_app():
    """Test the simplified app functionality"""
    base_url = "http://localhost:5003"
    
    print("🧪 Testing Simplified Ashtakavarga App")
    print("=" * 50)
    
    # Test 1: Home page
    print("1. Testing home page...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Home page loads successfully")
        else:
            print(f"   ❌ Home page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Home page error: {e}")
    
    # Test 2: Calculation
    print("2. Testing calculation...")
    try:
        data = {
            'name': 'Test User',
            'dob': '1978-09-18',
            'tob': '17:35',
            'place': 'Chennai',
            'latitude': 13.0827,
            'longitude': 80.2707,
            'tz_offset': 5.5
        }
        
        response = requests.post(f"{base_url}/calculate", data=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Calculation successful")
                print(f"   📊 Sarvashtakavarga Total: {result['data']['sarva_total']}")
                
                # Store data for matrix view test
                global test_data
                test_data = result['data']
            else:
                print(f"   ❌ Calculation failed: {result.get('error')}")
        else:
            print(f"   ❌ Calculation request failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Calculation error: {e}")
    
    # Test 3: Results page
    print("3. Testing results page...")
    try:
        response = requests.get(f"{base_url}/results")
        if response.status_code == 200:
            print("   ✅ Results page loads successfully")
        else:
            print(f"   ❌ Results page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Results page error: {e}")
    
    # Test 4: Dashboard page
    print("4. Testing dashboard page...")
    try:
        response = requests.get(f"{base_url}/dashboard")
        if response.status_code == 200:
            print("   ✅ Dashboard page loads successfully")
        else:
            print(f"   ❌ Dashboard page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Dashboard page error: {e}")
    
    # Test 5: Matrix view page
    print("5. Testing matrix view page...")
    try:
        response = requests.get(f"{base_url}/matrix-view")
        if response.status_code == 200:
            print("   ✅ Matrix view page loads successfully")
        else:
            print(f"   ❌ Matrix view page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Matrix view page error: {e}")
    
    # Test 6: Tamil interpretations page
    print("6. Testing Tamil interpretations page...")
    try:
        response = requests.get(f"{base_url}/tamil-interpretations")
        if response.status_code == 200:
            print("   ✅ Tamil interpretations page loads successfully")
        else:
            print(f"   ❌ Tamil interpretations page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Tamil interpretations page error: {e}")
    
    print("\n🎉 Testing completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_simple_app()
