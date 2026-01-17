#!/usr/bin/env python3
"""
Debug script for native chart issue
"""

from ashtakavarga_calculator_final import AshtakavargaCalculator

def debug_native_chart():
    """Debug the native chart calculation"""
    print("🔍 Debugging Native Chart Calculation")
    print("=" * 50)
    
    birth_data = {
        'name': 'Test User',
        'dob': '1978-09-18',
        'tob': '17:35',
        'place': 'Chennai',
        'latitude': 13.0827,
        'longitude': 80.2707,
        'tz_offset': 5.5
    }
    
    calculator = AshtakavargaCalculator(birth_data)
    
    print("1. Testing calculate_positions()...")
    positions = calculator.calculate_positions()
    print(f"   Planetary positions: {positions}")
    
    print("\n2. Testing calculate_all_charts()...")
    charts = calculator.calculate_all_charts()
    
    print("\n3. Testing get_native_chart()...")
    native_chart = calculator.get_native_chart()
    
    print(f"   Native chart length: {len(native_chart)}")
    print("\n   Native Chart Details:")
    for house in native_chart:
        planets = house.get('planets', [])
        planets_str = ', '.join(planets) if planets else 'Empty'
        print(f"      House {house['house']:2d} - {house['rasi_name']:8s}: {planets_str}")
    
    print("\n4. Testing get_display_data()...")
    display_data = calculator.get_display_data()
    print(f"   Display data keys: {list(display_data.keys())}")
    print(f"   Native chart in display data: {len(display_data.get('native_chart', []))}")
    
    # Check if planets are in the right positions
    print("\n5. Checking planet positions...")
    for planet, position in positions.items():
        print(f"   {planet}: House {position}")
    
    print("\n🎉 Debug completed!")

if __name__ == "__main__":
    debug_native_chart()
