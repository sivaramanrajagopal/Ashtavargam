#!/usr/bin/env python3
"""
Test script for the traditional chart layout
"""

import requests
import json

def test_traditional_chart():
    """Test the traditional chart functionality"""
    base_url = "http://localhost:5003"
    
    print("🧪 Testing Traditional Chart Layout")
    print("=" * 50)
    
    # Test calculation
    print("1. Testing calculation...")
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
                
                # Check native chart data
                native_chart = result['data'].get('native_chart', [])
                print(f"   📊 Native chart has {len(native_chart)} houses")
                
                # Display the chart data
                print("\n   📋 Native Chart Data:")
                for house in native_chart:
                    planets = house.get('planets', [])
                    planets_str = ', '.join(planets) if planets else 'Empty'
                    print(f"      House {house['house']:2d} - {house['rasi_name']:8s}: {planets_str}")
                
                # Check if planets are properly placed
                total_planets = sum(len(house.get('planets', [])) for house in native_chart)
                print(f"   🌟 Total planets placed: {total_planets}")
                
                if total_planets > 0:
                    print("   ✅ Planets are properly placed in houses")
                else:
                    print("   ❌ No planets found in houses")
                
            else:
                print(f"   ❌ Calculation failed: {result.get('error')}")
        else:
            print(f"   ❌ Calculation request failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Calculation error: {e}")
    
    # Test results page
    print("\n2. Testing results page...")
    try:
        response = requests.get(f"{base_url}/results")
        if response.status_code == 200:
            print("   ✅ Results page loads successfully")
            
            # Check if traditional chart HTML is present
            if 'traditional-chart' in response.text:
                print("   ✅ Traditional chart layout found")
            else:
                print("   ❌ Traditional chart layout not found")
                
            if 'rasi-1' in response.text:
                print("   ✅ Chart elements found")
            else:
                print("   ❌ Chart elements not found")
                
        else:
            print(f"   ❌ Results page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Results page error: {e}")
    
    print("\n🎉 Traditional Chart Testing completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_traditional_chart()
