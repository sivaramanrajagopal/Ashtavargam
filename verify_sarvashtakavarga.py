#!/usr/bin/env python3
"""
Verify Sarvashtakavarga (Combined Total) against trusted production values
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ashtavargam_calculator import TamilAshtakavargaCalculator

def verify_sarvashtakavarga():
    """Verify Sarvashtakavarga against trusted production values"""
    print("🌟 VERIFYING SARVASTHAKAVARGA (COMBINED TOTAL)")
    print("=" * 60)
    
    # Trusted production values from user
    trusted_sarvashtakavarga = [32, 36, 34, 30, 28, 16, 24, 28, 33, 28, 24, 24]
    trusted_total = 337
    
    # Rasi names
    rasis = [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ]
    
    print(f"Trusted Sarvashtakavarga values: {trusted_sarvashtakavarga}")
    print(f"Trusted total: {trusted_total}")
    print()
    
    # Create calculator and calculate
    calculator = TamilAshtakavargaCalculator()
    calculator.calculate_planetary_positions()
    calculator.calculate_all_ashtakavarga_tamil()
    
    # Get our calculated Sarvashtakavarga values
    if hasattr(calculator, 'sarvashtakavarga') and calculator.sarvashtakavarga:
        our_sarvashtakavarga = calculator.sarvashtakavarga
        our_total = sum(our_sarvashtakavarga)
        
        print(f"Our Sarvashtakavarga values: {our_sarvashtakavarga}")
        print(f"Our total:                  {our_total}")
        print()
        
        # Compare house by house
        print("📊 HOUSE-BY-HOUSE COMPARISON:")
        print("-" * 50)
        print(f"{'House':<8} {'Rasi':<12} {'Trusted':<8} {'Our':<8} {'Status':<10}")
        print("-" * 50)
        
        all_match = True
        for i, (trusted, our) in enumerate(zip(trusted_sarvashtakavarga, our_sarvashtakavarga)):
            status = "✅ MATCH" if trusted == our else "❌ DIFF"
            if trusted != our:
                all_match = False
            
            print(f"{i+1:<8} {rasis[i]:<12} {trusted:<8} {our:<8} {status}")
        
        print("-" * 50)
        print(f"{'TOTAL':<8} {'':<12} {trusted_total:<8} {our_total:<8} {'✅ MATCH' if trusted_total == our_total else '❌ DIFF'}")
        
        print(f"\n{'='*60}")
        if all_match and trusted_total == our_total:
            print("🎉 PERFECT MATCH!")
            print("✅ All house values match exactly")
            print("✅ Total matches exactly")
            print("✅ Sarvashtakavarga is CORRECT")
        else:
            print("⚠️  MISMATCH DETECTED")
            print("❌ Some values don't match")
            print("❌ Sarvashtakavarga needs correction")
        
        return all_match and trusted_total == our_total
    else:
        print("❌ SARVASTHAKAVARGA not found in calculations")
        return False

def display_detailed_breakdown():
    """Display detailed breakdown of Sarvashtakavarga calculation"""
    print(f"\n📋 DETAILED SARVASTHAKAVARGA BREAKDOWN:")
    print("-" * 80)
    
    calculator = TamilAshtakavargaCalculator()
    calculator.calculate_planetary_positions()
    calculator.calculate_all_ashtakavarga_tamil()
    
    rasis = [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ]
    
    # Display individual planet totals
    print("Individual Planet Totals:")
    print("-" * 40)
    planets = ['SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN']
    for planet in planets:
        if planet in calculator.binnashtakavarga:
            total = sum(calculator.binnashtakavarga[planet])
            print(f"{planet:8}: {total:2d} points")
    
    print(f"\nSarvashtakavarga by House:")
    print("-" * 80)
    print(f"{'House':<6} {'Rasi':<12} {'Total':<6} {'Breakdown':<50}")
    print("-" * 80)
    
    for i, rasi in enumerate(rasis):
        house_total = calculator.sarvashtakavarga[i]
        breakdown = []
        
        for planet in planets:
            if planet in calculator.binnashtakavarga:
                planet_value = calculator.binnashtakavarga[planet][i]
                if planet_value > 0:
                    breakdown.append(f"{planet[:3]}:{planet_value}")
        
        breakdown_str = ', '.join(breakdown) if breakdown else 'None'
        print(f"{i+1:<6} {rasi:<12} {house_total:<6} {breakdown_str:<50}")

def verify_individual_planet_totals():
    """Verify individual planet totals match expected values"""
    print(f"\n🔍 VERIFYING INDIVIDUAL PLANET TOTALS:")
    print("-" * 50)
    
    # Expected totals from trusted data
    expected_totals = {
        'SUN': 48,
        'MOON': 49,
        'MERCURY': 54,
        'VENUS': 52,
        'MARS': 39,
        'JUPITER': 56,
        'SATURN': 39
    }
    
    calculator = TamilAshtakavargaCalculator()
    calculator.calculate_planetary_positions()
    calculator.calculate_all_ashtakavarga_tamil()
    
    print(f"{'Planet':<10} {'Expected':<10} {'Our':<8} {'Status':<10}")
    print("-" * 50)
    
    all_planets_match = True
    for planet, expected in expected_totals.items():
        if planet in calculator.binnashtakavarga:
            our_total = sum(calculator.binnashtakavarga[planet])
            status = "✅ MATCH" if expected == our_total else "❌ DIFF"
            if expected != our_total:
                all_planets_match = False
            print(f"{planet:<10} {expected:<10} {our_total:<8} {status}")
    
    return all_planets_match

if __name__ == "__main__":
    # Verify individual planets first
    planets_match = verify_individual_planet_totals()
    
    # Then verify Sarvashtakavarga
    success = verify_sarvashtakavarga()
    display_detailed_breakdown()
    
    if success and planets_match:
        print(f"\n🏆 VERIFICATION RESULT: COMPLETE SUCCESS")
        print("✅ All individual planets match exactly")
        print("✅ Sarvashtakavarga matches trusted production values exactly!")
        print("✅ Complete Tamil Ashtakavarga system is 100% accurate!")
    else:
        print(f"\n⚠️  VERIFICATION RESULT: NEEDS CORRECTION")
        if not planets_match:
            print("❌ Some individual planet totals don't match")
        if not success:
            print("❌ Sarvashtakavarga doesn't match trusted values")
