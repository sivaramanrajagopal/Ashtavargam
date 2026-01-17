#!/usr/bin/env python3
"""
Correct Ashtakavarga Calculator - Using Tamil/South Indian Traditional Rules
Based on verified traditional methodology
"""

import swisseph as swe
import datetime
from typing import Dict, List, Tuple, Optional

# Tamil/South Indian Ashtakavarga Benefic Position Rules
# These are the correct traditional rules
TAMIL_ASHTAKAVARGA_RULES = {
    'SUN': {
        'SUN': [1, 2, 4, 7, 8, 9, 10, 11],
        'MOON': [3, 6, 10, 11],
        'MARS': [1, 2, 4, 7, 8, 9, 10, 11],
        'MERCURY': [3, 5, 6, 9, 10, 11, 12],
        'JUPITER': [5, 6, 9, 11],
        'VENUS': [6, 7, 12],
        'SATURN': [1, 2, 4, 7, 8, 9, 10, 11],
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
        'SUN': [5, 6, 9, 11, 12],
        'MOON': [2, 4, 6, 8, 10, 11],
        'MARS': [1, 2, 4, 7, 8, 9, 10, 11],
        'MERCURY': [1, 3, 5, 6, 9, 10, 11, 12],
        'JUPITER': [6, 8, 11, 12],
        'VENUS': [1, 2, 3, 4, 5, 8, 9, 11],
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
    }
}

class AshtakavargaCalculatorCorrect:
    """Correct Ashtakavarga calculator using Tamil/South Indian traditional rules"""
    
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
    
    def calculate_positions(self) -> Dict:
        """Calculate planetary positions with proper error handling"""
        try:
            # Parse birth data (format: YYYY-MM-DD or DD-MM-YYYY)
            dob = self.birth_data['dob']
            if '-' in dob:
                parts = dob.split('-')
                if len(parts[0]) == 4:  # YYYY-MM-DD format
                    year, month, day = map(int, parts)
                else:  # DD-MM-YYYY format
                    day, month, year = map(int, parts)
            else:
                raise ValueError("Invalid date format")
            
            hour, minute = map(int, self.birth_data['tob'].split(':'))
            
            # Create datetime and convert to UTC
            local_dt = datetime.datetime(year, month, day, hour, minute)
            utc_dt = local_dt - datetime.timedelta(hours=self.birth_data['tz_offset'])
            
            # Calculate Julian Day
            jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                           utc_dt.hour + utc_dt.minute/60.0)
            
            # Set sidereal mode (Lahiri Ayanamsa)
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            
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
                    
                except Exception as e:
                    print(f"Error calculating {planet_name}: {e}")
                    self.planet_positions[planet_name] = 1
            
            # Calculate Ascendant
            try:
                cusps, ascmc = swe.houses_ex(jd, self.birth_data['latitude'], self.birth_data['longitude'],
                                            b'P', flags=swe.FLG_SIDEREAL)
                asc_longitude = ascmc[0]
                
                asc_rasi = int(asc_longitude // 30) + 1
                if asc_rasi > 12:
                    asc_rasi -= 12
                if asc_rasi < 1:
                    asc_rasi += 12
                
                self.planet_positions['ASCENDANT'] = asc_rasi
                
            except Exception as e:
                print(f"Error calculating Ascendant: {e}")
                self.planet_positions['ASCENDANT'] = 1
            
            return self.planet_positions
            
        except Exception as e:
            print(f"Error in calculate_positions: {e}")
            return {}
    
    def calculate_relative_position(self, target_house: int, reference_rasi: int) -> int:
        """Calculate relative position using Tamil method (forward counting)"""
        if target_house >= reference_rasi:
            relative_pos = target_house - reference_rasi + 1
        else:
            relative_pos = target_house - reference_rasi + 13
        
        return relative_pos
    
    def calculate_binnashtakavarga(self, target_planet: str) -> List[int]:
        """Calculate Bhinnashtakavarga for a specific planet using correct Tamil rules"""
        if target_planet not in TAMIL_ASHTAKAVARGA_RULES:
            return [0] * 12
        
        chart = [0] * 12
        rules = TAMIL_ASHTAKAVARGA_RULES[target_planet]
        
        for house_num in range(1, 13):
            total_points = 0
            
            # Check each contributing planet/ascendant
            for contributing_planet, benefic_positions in rules.items():
                if contributing_planet in self.planet_positions:
                    reference_rasi = self.planet_positions[contributing_planet]
                    
                    # Calculate relative position using Tamil method
                    relative_pos = self.calculate_relative_position(house_num, reference_rasi)
                    
                    # Check if this relative position gives points
                    if relative_pos in benefic_positions:
                        total_points += 1
            
            # Validation: BAV Maximum is 8 points per planet per house
            if total_points > 8:
                total_points = 8
            
            chart[house_num - 1] = total_points
        
        return chart
    
    def calculate_all_charts(self) -> Dict:
        """Calculate all Ashtakavarga charts"""
        # First calculate planetary positions
        self.calculate_positions()
        
        # Calculate Bhinnashtakavarga for each planet
        for planet in ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN']:
            chart = self.calculate_binnashtakavarga(planet)
            self.ashtakavarga_charts[planet] = chart
        
        # Calculate Sarvashtakavarga (sum of all 7 planets)
        self.sarvashtakavarga = [0] * 12
        for planet_chart in self.ashtakavarga_charts.values():
            for i in range(12):
                self.sarvashtakavarga[i] += planet_chart[i]
        
        # Validation: SAV Maximum is 54 points per house
        for i in range(12):
            if self.sarvashtakavarga[i] > 54:
                self.sarvashtakavarga[i] = 54
        
        return self.ashtakavarga_charts
    
    def get_native_chart(self) -> List[Dict]:
        """Get native chart data for display"""
        native_chart = []
        ascendant_rasi = self.planet_positions.get('ASCENDANT', 1)
        
        for house_num in range(1, 13):
            planets_in_house = []
            
            for planet, position in self.planet_positions.items():
                if position == house_num:
                    planets_in_house.append(planet)
            
            # Calculate the actual Rasi for this house based on Ascendant
            actual_rasi_index = (ascendant_rasi + house_num - 2) % 12
            actual_rasi = self.tamil_rasis[actual_rasi_index]
            
            native_chart.append({
                'house': house_num,
                'rasi_name': actual_rasi,
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
        'name': 'Test User',
        'dob': '1978-09-18',
        'tob': '17:35',
        'place': 'Chennai',
        'latitude': 13.0827,
        'longitude': 80.2707,
        'tz_offset': 5.5
    }
    
    calculator = AshtakavargaCalculatorCorrect(birth_data)
    positions = calculator.calculate_positions()
    charts = calculator.calculate_all_charts()
    display_data = calculator.get_display_data()
    
    print("\n=== PLANETARY POSITIONS ===")
    for planet, rasi in positions.items():
        print(f"{planet:10}: Rasi {rasi:2d}")
    
    print("\n=== BAV TOTALS ===")
    for planet, total in display_data['totals'].items():
        print(f"{planet:10}: {total:2d} points")
    
    print(f"\n=== SAV TOTAL ===")
    print(f"Total: {display_data['sarva_total']} points")
    print(f"SAV per house: {display_data['sarvashtakavarga']}")

if __name__ == "__main__":
    main()

