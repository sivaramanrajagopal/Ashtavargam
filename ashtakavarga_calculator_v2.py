#!/usr/bin/env python3
"""
Clean Ashtakavarga Calculator - Version 2
Simplified, reliable implementation with proper error handling
"""

import swisseph as swe
import datetime
from typing import Dict, List, Tuple, Optional

class AshtakavargaCalculator:
    """Clean, reliable Ashtakavarga calculator"""
    
    def __init__(self, birth_data: Dict):
        self.birth_data = birth_data
        self.planet_positions = {}
        self.ashtakavarga_charts = {}
        self.sarvashtakavarga = [0] * 12
        
        # Tamil Rasi names
        self.tamil_rasis = [
            "மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்", "சிம்மம்", "கன்னி",
            "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்", "கும்பம்", "மீனம்"
        ]
        
        # Tamil Rasi abbreviations
        self.tamil_rasi_abbr = [
            "மே", "ரி", "மி", "க", "சி", "க", "து", "வி", "த", "ம", "கு", "மீ"
        ]
        
        # Planet names
        self.planets = {
            'SUN': 'சூர்யன்',
            'MOON': 'சந்திரன்', 
            'MARS': 'செவ்வாய்',
            'MERCURY': 'புதன்',
            'JUPITER': 'குரு',
            'VENUS': 'சுக்ரன்',
            'SATURN': 'சனி',
            'ASCENDANT': 'லக்கினம்'
        }
        
        # Ashtakavarga rules (simplified and verified)
        self.rules = {
            'SUN': {
                'SUN': [1, 4, 7, 10, 8, 2, 9, 11],
                'MOON': [3, 6, 10, 11],
                'MARS': [1, 4, 7, 10, 8, 2, 9, 11],
                'MERCURY': [3, 6, 10, 11, 5, 9, 12],
                'JUPITER': [5, 6, 9, 11],
                'VENUS': [6, 7, 12],
                'SATURN': [1, 4, 7, 10, 8, 2, 9, 11],
                'ASCENDANT': [3, 4, 6, 10, 11, 12]
            },
            'MOON': {
                'SUN': [3, 6, 7, 8, 10, 11],
                'MOON': [1, 3, 6, 7, 10, 11],
                'MARS': [2, 3, 5, 6, 9, 10, 11],
                'MERCURY': [1, 3, 4, 5, 7, 8, 10, 11],
                'JUPITER': [1, 4, 7, 8, 10, 11, 12],
                'VENUS': [3, 4, 5, 7, 9, 10, 11],
                'SATURN': [3, 5, 6, 11],
                'ASCENDANT': [3, 6, 10, 11]
            },
            'MARS': {
                'SUN': [3, 5, 6, 10, 11],
                'MOON': [3, 6, 11],
                'MARS': [1, 2, 4, 7, 8, 10, 11],
                'MERCURY': [3, 5, 6, 11],
                'JUPITER': [6, 10, 11, 12],
                'VENUS': [6, 8, 11, 12],
                'SATURN': [1, 4, 7, 8, 9, 10, 11],
                'ASCENDANT': [1, 3, 6, 10, 11]
            },
            'MERCURY': {
                'SUN': [1, 3, 5, 6, 9, 10, 11, 12],
                'MOON': [2, 4, 6, 8, 10, 11],
                'MARS': [1, 2, 4, 7, 8, 9, 10, 11],
                'MERCURY': [1, 3, 5, 6, 9, 10, 11, 12],
                'JUPITER': [6, 8, 11, 12],
                'VENUS': [1, 2, 3, 4, 5, 9, 10, 11],
                'SATURN': [1, 2, 4, 7, 8, 9, 10, 11],
                'ASCENDANT': [1, 2, 4, 6, 8, 10, 11]
            },
            'JUPITER': {
                'SUN': [1, 2, 3, 4, 7, 8, 9, 10, 11],
                'MOON': [2, 5, 7, 9, 11],
                'MARS': [1, 2, 4, 7, 8, 10, 11],
                'MERCURY': [1, 2, 4, 5, 6, 9, 10, 11],
                'JUPITER': [1, 2, 3, 4, 7, 8, 10, 11],
                'VENUS': [2, 5, 6, 9, 10, 11],
                'SATURN': [3, 5, 6, 12],
                'ASCENDANT': [1, 2, 4, 5, 6, 7, 9, 10, 11]
            },
            'VENUS': {
                'SUN': [8, 11, 12],
                'MOON': [1, 2, 3, 4, 5, 8, 9, 11, 12],
                'MARS': [3, 5, 6, 9, 11, 12],
                'MERCURY': [3, 5, 6, 9, 11],
                'JUPITER': [5, 8, 9, 10, 11],
                'VENUS': [1, 2, 3, 4, 5, 8, 9, 10, 11],
                'SATURN': [3, 4, 5, 8, 9, 10, 11],
                'ASCENDANT': [1, 2, 3, 4, 5, 8, 9, 11]
            },
            'SATURN': {
                'SUN': [1, 2, 4, 7, 8, 10, 11],
                'MOON': [3, 6, 11],
                'MARS': [3, 5, 6, 10, 11, 12],
                'MERCURY': [6, 8, 9, 10, 11, 12],
                'JUPITER': [5, 6, 11, 12],
                'VENUS': [6, 11, 12],
                'SATURN': [3, 5, 6, 11],
                'ASCENDANT': [1, 3, 4, 6, 10, 11]
            },
            'ASCENDANT': {
                'SUN': [3, 4, 6, 10, 11, 12],
                'MOON': [3, 6, 10, 11],
                'MARS': [1, 3, 6, 10, 11],
                'MERCURY': [1, 2, 4, 6, 8, 10, 11],
                'JUPITER': [1, 2, 4, 5, 6, 7, 9, 10, 11],
                'VENUS': [1, 2, 3, 4, 5, 8, 9, 11],
                'SATURN': [1, 3, 4, 6, 10, 11],
                'ASCENDANT': [3, 6, 10, 11]
            }
        }
    
    def calculate_positions(self) -> Dict:
        """Calculate planetary positions with proper error handling"""
        try:
            # Parse birth data
            day, month, year = map(int, self.birth_data['dob'].split('-'))
            hour, minute = map(int, self.birth_data['tob'].split(':'))
            
            # Create datetime and convert to UTC
            local_dt = datetime.datetime(year, month, day, hour, minute)
            utc_dt = local_dt - datetime.timedelta(hours=self.birth_data['tz_offset'])
            
            # Calculate Julian Day
            jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                           utc_dt.hour + utc_dt.minute/60.0)
            
            # Set sidereal mode
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            
            print(f"Calculating positions for: {day:02d}-{month:02d}-{year} {hour:02d}:{minute:02d}")
            print(f"UTC: {utc_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Calculate planetary positions
            planet_ids = {
                'SUN': swe.SUN,
                'MOON': swe.MOON,
                'MARS': swe.MARS,
                'MERCURY': swe.MERCURY,
                'JUPITER': swe.JUPITER,
                'VENUS': swe.VENUS,
                'SATURN': swe.SATURN
            }
            
            for planet_name, planet_id in planet_ids.items():
                try:
                    planet_pos, _ = swe.calc_ut(jd, planet_id, swe.FLG_SIDEREAL)
                    longitude = planet_pos[0]
                    
                    # Convert to rasi (1-12)
                    rasi = int(longitude // 30) + 1
                    if rasi > 12:
                        rasi -= 12
                    if rasi < 1:
                        rasi += 12
                    
                    self.planet_positions[planet_name] = rasi
                    
                    degrees = longitude % 30
                    deg = int(degrees)
                    minutes = int((degrees - deg) * 60)
                    
                    print(f"{planet_name:8}: {longitude:7.2f}° | Rasi {rasi:2d} ({self.tamil_rasis[rasi-1]:10}) | {deg:2d}°{minutes:02d}'")
                    
                except Exception as e:
                    print(f"Error calculating {planet_name}: {e}")
                    self.planet_positions[planet_name] = 1
            
            # Calculate Ascendant
            try:
                cusps, ascmc = swe.houses_ex(jd, self.birth_data['lat'], self.birth_data['lon'],
                                            b'P', flags=swe.FLG_SIDEREAL)
                asc_longitude = ascmc[0]
                
                asc_rasi = int(asc_longitude // 30) + 1
                if asc_rasi > 12:
                    asc_rasi -= 12
                if asc_rasi < 1:
                    asc_rasi += 12
                
                self.planet_positions['ASCENDANT'] = asc_rasi
                
                degrees = asc_longitude % 30
                deg = int(degrees)
                minutes = int((degrees - deg) * 60)
                
                print(f"ASCENDANT: {asc_longitude:7.2f}° | Rasi {asc_rasi:2d} ({self.tamil_rasis[asc_rasi-1]:10}) | {deg:2d}°{minutes:02d}'")
                
            except Exception as e:
                print(f"Error calculating Ascendant: {e}")
                self.planet_positions['ASCENDANT'] = 1
            
            return self.planet_positions
            
        except Exception as e:
            print(f"Error in calculate_positions: {e}")
            return {}
    
    def calculate_ashtakavarga(self, target_planet: str) -> List[int]:
        """Calculate Ashtakavarga for a specific planet"""
        if target_planet not in self.rules:
            return [0] * 12
        
        chart = [0] * 12
        
        # For each contributing planet
        for contributor, houses in self.rules[target_planet].items():
            if contributor in self.planet_positions:
                # Get the contributor's position
                contributor_pos = self.planet_positions[contributor]
                
                # Apply the rules from that position
                for house_num in houses:
                    # Calculate relative position (1-based)
                    relative_pos = ((contributor_pos - 1 + house_num - 1) % 12) + 1
                    chart[relative_pos - 1] += 1
        
        return chart
    
    def calculate_all_charts(self) -> Dict:
        """Calculate all Ashtakavarga charts"""
        print("\nCalculating Ashtakavarga charts...")
        
        for planet in self.planets:
            chart = self.calculate_ashtakavarga(planet)
            self.ashtakavarga_charts[planet] = chart
            total = sum(chart)
            print(f"{planet:8}: {total:2d} points")
        
        # Calculate Sarvashtakavarga
        self.sarvashtakavarga = [0] * 12
        for planet in ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN']:
            if planet in self.ashtakavarga_charts:
                for i in range(12):
                    self.sarvashtakavarga[i] += self.ashtakavarga_charts[planet][i]
        
        sarva_total = sum(self.sarvashtakavarga)
        print(f"Sarvashtakavarga Total: {sarva_total}")
        
        return self.ashtakavarga_charts
    
    def get_native_chart(self) -> List[Dict]:
        """Get native chart data for display"""
        native_chart = []
        
        for house_num in range(1, 13):
            planets_in_house = []
            
            for planet, position in self.planet_positions.items():
                if position == house_num:
                    planets_in_house.append(planet)
            
            native_chart.append({
                'house': house_num,
                'rasi_name': self.tamil_rasis[house_num - 1],
                'planets': planets_in_house
            })
        
        return native_chart
    
    def get_display_data(self) -> Dict:
        """Get all data formatted for display"""
        return {
            'planetary_positions': self.planet_positions,
            'ashtakavarga_charts': self.ashtakavarga_charts,
            'sarvashtakavarga': self.sarvashtakavarga,
            'native_chart': self.get_native_chart(),
            'totals': {planet: sum(chart) for planet, chart in self.ashtakavarga_charts.items()},
            'sarva_total': sum(self.sarvashtakavarga)
        }

def main():
    """Test the calculator"""
    birth_data = {
        'name': 'Sivaraman R',
        'dob': '18-09-1978',
        'tob': '17:35',
        'lat': 13.0827,
        'lon': 80.2707,
        'place': 'Chennai',
        'tz_offset': 5.5
    }
    
    calculator = AshtakavargaCalculator(birth_data)
    positions = calculator.calculate_positions()
    charts = calculator.calculate_all_charts()
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    
    for planet, total in calculator.get_display_data()['totals'].items():
        print(f"{planet:8}: {total:2d} points")
    
    print(f"Sarvashtakavarga: {calculator.get_display_data()['sarva_total']}")

if __name__ == "__main__":
    main()
