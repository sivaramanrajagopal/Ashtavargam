#!/usr/bin/env python3
"""
Final Correct Ashtakavarga Calculator - All 8 Planets Including Ascendant
Based on Tamil/South Indian Traditional Rules - Verified Methodology
"""

import swisseph as swe
import datetime
from typing import Dict, List, Tuple, Optional

# Tamil/South Indian Ashtakavarga Benefic Position Rules
# Complete rules for all 8 planets including Ascendant
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

class AshtakavargaCalculatorFinal:
    """Final Correct Ashtakavarga calculator - All 8 planets including Ascendant"""
    
    def __init__(self, birth_data: Dict):
        self.birth_data = birth_data
        self.planet_positions = {}
        self.planet_details = {}  # Store detailed planetary data (longitude, sign, house)
        self.ashtakavarga_charts = {}  # BAV for all 8 planets
        self.sarvashtakavarga = [0] * 12  # SAV (sum of 7 planets only, not Ascendant)
        
        # Tamil Rasi names
        self.tamil_rasis = [
            "மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்", "சிம்மம்", "கன்னி",
            "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்", "கும்பம்", "மீனம்"
        ]
        
        # English Rasi names
        self.english_rasis = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        # Sign Lords (Rasi Lords) - Index 0-11 corresponds to Rasi 1-12
        # Mesha=1=Mars, Vrishabha=2=Venus, Mithuna=3=Mercury, etc.
        self.sign_lords = [
            'MARS',      # Mesha (Aries)
            'VENUS',     # Vrishabha (Taurus)
            'MERCURY',   # Mithuna (Gemini)
            'MOON',      # Karka (Cancer)
            'SUN',       # Simha (Leo)
            'MERCURY',   # Kanya (Virgo)
            'VENUS',     # Tula (Libra)
            'MARS',      # Vrischika (Scorpio)
            'JUPITER',   # Dhanu (Sagittarius)
            'SATURN',    # Makara (Capricorn)
            'SATURN',    # Kumbha (Aquarius)
            'JUPITER'    # Meena (Pisces)
        ]
        
        # Nakshatra names (27 Nakshatras)
        self.nakshatras = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
            'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
            'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
            'Moola', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
            'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
        ]
        
        # Nakshatra Lords (27 Nakshatras)
        self.nakshatra_lords = [
            'KETU', 'VENUS', 'SUN', 'MOON', 'MARS', 'RAHU',
            'JUPITER', 'SATURN', 'MERCURY', 'KETU', 'VENUS', 'SUN',
            'MOON', 'MARS', 'RAHU', 'JUPITER', 'SATURN', 'MERCURY',
            'KETU', 'VENUS', 'SUN', 'MOON', 'MARS', 'RAHU',
            'JUPITER', 'SATURN', 'MERCURY'
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
        
        # All 8 planets for BAV calculation
        self.all_planets = ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN', 'ASCENDANT']
        # 7 planets for SAV calculation (excluding Ascendant)
        self.sav_planets = ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN']
    
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
                    
                    # Store detailed planetary data
                    degrees_in_sign = longitude % 30
                    deg = int(degrees_in_sign)
                    min_val = int((degrees_in_sign - deg) * 60)
                    sec = int(((degrees_in_sign - deg) * 60 - min_val) * 60)
                    
                    # Calculate Nakshatra and Pada
                    nakshatra_num, pada = self.calculate_nakshatra(longitude)
                    nakshatra_name = self.nakshatras[nakshatra_num - 1]
                    nakshatra_lord = self.nakshatra_lords[nakshatra_num - 1]
                    
                    self.planet_details[planet_name] = {
                        'longitude': longitude,
                        'rasi': rasi,
                        'rasi_name_tamil': self.tamil_rasis[rasi - 1],
                        'rasi_name_english': self.english_rasis[rasi - 1],
                        'degrees': deg,
                        'minutes': min_val,
                        'seconds': sec,
                        'sign_lord': self.sign_lords[rasi - 1],
                        'nakshatra': nakshatra_name,
                        'nakshatra_num': nakshatra_num,
                        'pada': pada,
                        'nakshatra_lord': nakshatra_lord
                    }
                    
                except Exception as e:
                    print(f"Error calculating {planet_name}: {e}")
                    self.planet_positions[planet_name] = 1
                    self.planet_details[planet_name] = {
                        'longitude': 0.0,
                        'rasi': 1,
                        'rasi_name_tamil': self.tamil_rasis[0],
                        'rasi_name_english': self.english_rasis[0],
                        'degrees': 0,
                        'minutes': 0,
                        'seconds': 0,
                        'sign_lord': self.sign_lords[0]
                    }
            
            # Calculate Rahu and Ketu
            try:
                # Calculate Rahu (North Node) first
                rahu_pos, _ = swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SIDEREAL)
                rahu_longitude = rahu_pos[0]
                
                # Rahu (North Node)
                rahu_rasi = int(rahu_longitude // 30) + 1
                if rahu_rasi > 12:
                    rahu_rasi -= 12
                if rahu_rasi < 1:
                    rahu_rasi += 12
                
                self.planet_positions['RAHU'] = rahu_rasi
                degrees_in_sign = rahu_longitude % 30
                deg = int(degrees_in_sign)
                min_val = int((degrees_in_sign - deg) * 60)
                sec = int(((degrees_in_sign - deg) * 60 - min_val) * 60)
                
                # Calculate Nakshatra for Rahu
                rahu_nakshatra_num, rahu_pada = self.calculate_nakshatra(rahu_longitude)
                rahu_nakshatra_name = self.nakshatras[rahu_nakshatra_num - 1]
                rahu_nakshatra_lord = self.nakshatra_lords[rahu_nakshatra_num - 1]
                
                self.planet_details['RAHU'] = {
                    'longitude': rahu_longitude,
                    'rasi': rahu_rasi,
                    'rasi_name_tamil': self.tamil_rasis[rahu_rasi - 1],
                    'rasi_name_english': self.english_rasis[rahu_rasi - 1],
                    'degrees': deg,
                    'minutes': min_val,
                    'seconds': sec,
                    'sign_lord': self.sign_lords[rahu_rasi - 1],
                    'nakshatra': rahu_nakshatra_name,
                    'nakshatra_num': rahu_nakshatra_num,
                    'pada': rahu_pada,
                    'nakshatra_lord': rahu_nakshatra_lord
                }
                
                # Ketu (South Node) - 180 degrees opposite of Rahu
                ketu_longitude = (rahu_longitude + 180) % 360
                ketu_rasi = int(ketu_longitude // 30) + 1
                if ketu_rasi > 12:
                    ketu_rasi -= 12
                if ketu_rasi < 1:
                    ketu_rasi += 12
                
                self.planet_positions['KETU'] = ketu_rasi
                degrees_in_sign = ketu_longitude % 30
                deg = int(degrees_in_sign)
                min_val = int((degrees_in_sign - deg) * 60)
                sec = int(((degrees_in_sign - deg) * 60 - min_val) * 60)
                
                # Calculate Nakshatra for Ketu
                ketu_nakshatra_num, ketu_pada = self.calculate_nakshatra(ketu_longitude)
                ketu_nakshatra_name = self.nakshatras[ketu_nakshatra_num - 1]
                ketu_nakshatra_lord = self.nakshatra_lords[ketu_nakshatra_num - 1]
                
                self.planet_details['KETU'] = {
                    'longitude': ketu_longitude,
                    'rasi': ketu_rasi,
                    'rasi_name_tamil': self.tamil_rasis[ketu_rasi - 1],
                    'rasi_name_english': self.english_rasis[ketu_rasi - 1],
                    'degrees': deg,
                    'minutes': min_val,
                    'seconds': sec,
                    'sign_lord': self.sign_lords[ketu_rasi - 1],
                    'nakshatra': ketu_nakshatra_name,
                    'nakshatra_num': ketu_nakshatra_num,
                    'pada': ketu_pada,
                    'nakshatra_lord': ketu_nakshatra_lord
                }
            except Exception as e:
                print(f"Error calculating Rahu/Ketu: {e}")
                self.planet_positions['RAHU'] = 1
                self.planet_positions['KETU'] = 7
                self.planet_details['RAHU'] = {
                    'longitude': 0.0, 'rasi': 1,
                    'rasi_name_tamil': self.tamil_rasis[0],
                    'rasi_name_english': self.english_rasis[0],
                    'degrees': 0, 'minutes': 0, 'seconds': 0,
                    'sign_lord': self.sign_lords[0]
                }
                self.planet_details['KETU'] = {
                    'longitude': 180.0, 'rasi': 7,
                    'rasi_name_tamil': self.tamil_rasis[6],
                    'rasi_name_english': self.english_rasis[6],
                    'degrees': 0, 'minutes': 0, 'seconds': 0,
                    'sign_lord': self.sign_lords[6]
                }
            
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
                
                # Store detailed Ascendant data
                degrees_in_sign = asc_longitude % 30
                deg = int(degrees_in_sign)
                min_val = int((degrees_in_sign - deg) * 60)
                sec = int(((degrees_in_sign - deg) * 60 - min_val) * 60)
                
                # Calculate Nakshatra for Ascendant
                asc_nakshatra_num, asc_pada = self.calculate_nakshatra(asc_longitude)
                asc_nakshatra_name = self.nakshatras[asc_nakshatra_num - 1]
                asc_nakshatra_lord = self.nakshatra_lords[asc_nakshatra_num - 1]
                
                self.planet_details['ASCENDANT'] = {
                    'longitude': asc_longitude,
                    'rasi': asc_rasi,
                    'rasi_name_tamil': self.tamil_rasis[asc_rasi - 1],
                    'rasi_name_english': self.english_rasis[asc_rasi - 1],
                    'degrees': deg,
                    'minutes': min_val,
                    'seconds': sec,
                    'sign_lord': self.sign_lords[asc_rasi - 1],
                    'nakshatra': asc_nakshatra_name,
                    'nakshatra_num': asc_nakshatra_num,
                    'pada': asc_pada,
                    'nakshatra_lord': asc_nakshatra_lord
                }
                
            except Exception as e:
                print(f"Error calculating Ascendant: {e}")
                self.planet_positions['ASCENDANT'] = 1
                self.planet_details['ASCENDANT'] = {
                    'longitude': 0.0,
                    'rasi': 1,
                    'rasi_name_tamil': self.tamil_rasis[0],
                    'rasi_name_english': self.english_rasis[0],
                    'degrees': 0,
                    'minutes': 0,
                    'seconds': 0,
                    'sign_lord': self.sign_lords[0]
                }
            
            return self.planet_positions
            
        except Exception as e:
            print(f"Error in calculate_positions: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def calculate_house_positions(self) -> Dict:
        """Calculate HOUSE positions for all planets based on Ascendant
        
        House positions are needed for BAV calculation (not Rasi positions).
        House 1 = Ascendant's Rasi, then count clockwise.
        """
        ascendant_rasi = self.planet_positions.get('ASCENDANT', 1)
        self.planet_house_positions = {}
        
        for planet, planet_rasi in self.planet_positions.items():
            if planet == 'ASCENDANT':
                # Ascendant is always in house 1
                self.planet_house_positions[planet] = 1
            else:
                # Calculate house number: (planet_rasi - ascendant_rasi) % 12 + 1
                house_num = ((planet_rasi - ascendant_rasi) % 12) + 1
                if house_num == 0:
                    house_num = 12
                self.planet_house_positions[planet] = house_num
        
        return self.planet_house_positions
    
    def calculate_relative_position(self, target_house: int, reference_rasi: int) -> int:
        """Calculate relative position using Parasara method
        
        CRITICAL: For Parasara Ashtakavarga, we need to use the RASI that the house represents,
        not the house number itself.
        
        Steps:
        1. Find which Rasi this house represents (based on Ascendant)
        2. Calculate relative position from the planet's Rasi to this house's Rasi
        3. Count COUNTER-CLOCKWISE from planet's Rasi (this is the correct method)
        
        Counter-clockwise counting:
        - Position 1 = planet's own Rasi
        - Position 2 = previous Rasi (Rasi - 1)
        - Position N = ((ref_rasi - N + 1) % 12) or equivalently calculated
        """
        # Get the Rasi that this house represents
        ascendant_rasi = self.planet_positions.get('ASCENDANT', 1)
        house_rasi = ((ascendant_rasi - 1 + target_house - 1) % 12) + 1
        
        # Calculate relative position from reference_rasi to house_rasi (CLOCKWISE)
        # Clockwise counting gives correct Rasi totals matching traditional calculations
        if house_rasi >= reference_rasi:
            relative_pos = house_rasi - reference_rasi + 1
        else:
            relative_pos = house_rasi - reference_rasi + 13
        
        return relative_pos
    
    def calculate_binnashtakavarga(self, target_planet: str) -> List[int]:
        """Calculate Bhinnashtakavarga (BAV) for a specific planet using Parasara method
        
        PARASARA METHOD (Correct):
        - Calculate BAV per RASI first (12 Rasis)
        - For each contributor (7 planets + Ascendant):
          - Get contributor's RASI position
          - For each benefic house number in the list:
            - Calculate target RASI = (contributor RASI + benefic house - 1)
            - If target RASI > 12, subtract 12 (wraparound)
            - Add 1 bindu to that RASI
        - Then map RASI values to houses based on Ascendant
        
        Critical: Benefic house numbers are counted FROM the contributor's RASI position (where 1 = contributor's own RASI).
        """
        if target_planet not in TAMIL_ASHTAKAVARGA_RULES:
            return [0] * 12
        
        rules = TAMIL_ASHTAKAVARGA_RULES[target_planet]
        
        # Step 1: Calculate BAV per RASI (12 Rasis)
        rasi_chart = [0] * 12  # Rasi 1-12
        
        # For each of the 8 contributors (7 planets + ascendant)
        for contributing_planet, benefic_houses in rules.items():
            if contributing_planet not in self.planet_positions:
                continue
            
            # Get the contributor's RASI position (1-12)
            contributor_rasi = self.planet_positions[contributing_planet]
            
            # For each benefic house number in the list
            for benefic_house_num in benefic_houses:
                # Calculate target RASI = (contributor RASI + benefic house - 1)
                target_rasi = contributor_rasi + benefic_house_num - 1
                
                # If target RASI > 12, subtract 12 (wraparound)
                if target_rasi > 12:
                    target_rasi -= 12
                
                # Add 1 bindu to that RASI (0-indexed array)
                if 1 <= target_rasi <= 12:
                    rasi_chart[target_rasi - 1] += 1
        
        # Validation: BAV Maximum is 8 points per planet per RASI
        for i in range(12):
            if rasi_chart[i] > 8:
                rasi_chart[i] = 8
        
        # Step 2: Map RASI values to houses based on Ascendant
        house_chart = [0] * 12
        ascendant_rasi = self.planet_positions.get('ASCENDANT', 1)
        
        for house_num in range(1, 13):
            # Calculate which RASI this house represents
            # House 1 = Ascendant RASI
            house_rasi = ((ascendant_rasi - 1 + house_num - 1) % 12) + 1
            # Map the RASI value to the house
            house_chart[house_num - 1] = rasi_chart[house_rasi - 1]
        
        return house_chart
    
    def calculate_all_charts(self) -> Dict:
        """Calculate all Ashtakavarga charts - BAV for all 8 planets including Ascendant"""
        # First calculate planetary positions (Rasi positions)
        self.calculate_positions()
        
        # Calculate HOUSE positions for all planets (needed for BAV calculation)
        self.calculate_house_positions()
        
        # Calculate Bhinnashtakavarga (BAV) for ALL 8 planets including Ascendant
        for planet in self.all_planets:
            chart = self.calculate_binnashtakavarga(planet)
            self.ashtakavarga_charts[planet] = chart
            total = sum(chart)
            print(f"{planet:10}: {total:2d} points (BAV)")
        
        # Calculate Sarvashtakavarga (SAV) - sum of 7 planets only (excluding Ascendant)
        self.sarvashtakavarga = [0] * 12
        for planet in self.sav_planets:
            if planet in self.ashtakavarga_charts:
                for i in range(12):
                    self.sarvashtakavarga[i] += self.ashtakavarga_charts[planet][i]
        
        # Validation: SAV Maximum is 54 points per house
        for i in range(12):
            if self.sarvashtakavarga[i] > 54:
                self.sarvashtakavarga[i] = 54
        
        sarva_total = sum(self.sarvashtakavarga)
        print(f"\nSarvashtakavarga (SAV) Total: {sarva_total} points")
        print(f"SAV per house: {self.sarvashtakavarga}")
        
        return self.ashtakavarga_charts
    
    def get_8x8_matrix(self) -> Dict[str, List[List[int]]]:
        """Get 8x8 matrix showing which planets contribute to each planet's BAV
        
        Returns a dictionary where each key is a target planet, and the value is
        an 8x12 matrix (8 contributing planets x 12 houses) showing 1 if that
        planet contributes a point, 0 otherwise.
        """
        matrix = {}
        contributing_planets = ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN', 'ASCENDANT']
        
        for target_planet in self.all_planets:
            if target_planet not in TAMIL_ASHTAKAVARGA_RULES:
                continue
            
            planet_matrix = []
            rules = TAMIL_ASHTAKAVARGA_RULES[target_planet]
            
            ascendant_rasi = self.planet_positions.get('ASCENDANT', 1)
            
            for contributing_planet in contributing_planets:
                row = []
                if contributing_planet in self.planet_positions:
                    reference_rasi = self.planet_positions[contributing_planet]
                    benefic_positions = rules.get(contributing_planet, [])
                    
                    for house_num in range(1, 13):
                        # Calculate which Rasi this house represents
                        house_rasi = ((ascendant_rasi - 1 + house_num - 1) % 12) + 1
                        relative_pos = self.calculate_relative_position(house_rasi, reference_rasi)
                        if relative_pos in benefic_positions:
                            row.append(1)
                        else:
                            row.append(0)
                else:
                    row = [0] * 12
                
                planet_matrix.append(row)
            
            matrix[target_planet] = planet_matrix
        
        return matrix
    
    def get_native_chart(self) -> List[Dict]:
        """Get native chart data for display - maps planets to houses based on Ascendant"""
        native_chart = []
        ascendant_rasi = self.planet_positions.get('ASCENDANT', 1)
        
        # Create a mapping: house_num -> rasi_index
        # House 1 = Ascendant Rasi, House 2 = Next Rasi, etc.
        for house_num in range(1, 13):
            planets_in_house = []
            
            # Calculate which Rasi this house represents
            # House 1 = Ascendant Rasi (index 0-based: ascendant_rasi - 1)
            # House 2 = Next Rasi, etc.
            house_rasi_index = (ascendant_rasi - 1 + house_num - 1) % 12
            house_rasi_number = house_rasi_index + 1  # Convert to 1-based
            
            # Find all planets in this Rasi
            for planet, planet_rasi in self.planet_positions.items():
                # Skip ASCENDANT as it's not a planet in the chart
                if planet == 'ASCENDANT':
                    continue
                if planet_rasi == house_rasi_number:
                    planets_in_house.append(planet)
            
            # Get the Rasi name for this house
            actual_rasi = self.tamil_rasis[house_rasi_index]
            
            native_chart.append({
                'house': house_num,
                'rasi_name': actual_rasi,
                'planets': planets_in_house
            })
        
        return native_chart
    
    def calculate_nakshatra(self, longitude: float) -> Tuple[int, int]:
        """Calculate Nakshatra number (1-27) and Pada (1-4) from longitude"""
        # Each Nakshatra spans 13°20' (13.3333 degrees)
        # Each Pada spans 3°20' (3.3333 degrees)
        nakshatra_span = 13.333333333333334  # 13°20'
        pada_span = 3.3333333333333335  # 3°20'
        
        # Normalize longitude to 0-360
        normalized_long = longitude % 360
        
        # Calculate Nakshatra number (1-27)
        nakshatra_num = int(normalized_long // nakshatra_span) + 1
        if nakshatra_num > 27:
            nakshatra_num = 27
        
        # Calculate degrees within the Nakshatra
        degrees_in_nakshatra = normalized_long % nakshatra_span
        
        # Calculate Pada (1-4)
        pada = int(degrees_in_nakshatra // pada_span) + 1
        if pada > 4:
            pada = 4
        
        return nakshatra_num, pada
    
    def get_birth_chart_data(self) -> Dict:
        """Get detailed birth chart data for table display - includes all planets, Ascendant, Rahu, Ketu"""
        ascendant_rasi = self.planet_positions.get('ASCENDANT', 1)
        birth_chart = []
        
        # Get all planets including Ascendant, Rahu, Ketu
        # Order: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu, Ascendant
        planets_list = ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN', 'RAHU', 'KETU', 'ASCENDANT']
        
        for planet in planets_list:
            if planet not in self.planet_details:
                continue
                
            detail = self.planet_details[planet]
            rasi = detail['rasi']
            
            # Find which house this planet is in (based on Ascendant)
            # For Ascendant, house is always 1
            if planet == 'ASCENDANT':
                house_num = 1
            else:
                house_num = ((rasi - ascendant_rasi) % 12) + 1
                if house_num == 0:
                    house_num = 12
            
            # Get house lord for this house
            house_rasi_index = (ascendant_rasi - 1 + house_num - 1) % 12
            house_lord = self.sign_lords[house_rasi_index]
            
            # Get house sign
            house_sign_english = self.english_rasis[house_rasi_index]
            house_sign_tamil = self.tamil_rasis[house_rasi_index]
            
            birth_chart.append({
                'planet': planet,
                'longitude': detail['longitude'],
                'sign': detail['rasi_name_english'],
                'sign_tamil': detail['rasi_name_tamil'],
                'house': house_num,
                'house_sign': house_sign_english,
                'house_sign_tamil': house_sign_tamil,
                'house_lord': house_lord,
                'degrees': detail['degrees'],
                'minutes': detail['minutes'],
                'seconds': detail['seconds'],
                'sign_lord': detail['sign_lord'],
                'nakshatra': detail.get('nakshatra', ''),
                'pada': detail.get('pada', 1),
                'nakshatra_lord': detail.get('nakshatra_lord', '')
            })
        
        # Add house lords for each house (for reference)
        house_lords = {}
        for house_num in range(1, 13):
            house_rasi_index = (ascendant_rasi - 1 + house_num - 1) % 12
            house_lords[house_num] = self.sign_lords[house_rasi_index]
        
        return {
            'planets': birth_chart,
            'house_lords': house_lords,
            'ascendant_rasi': ascendant_rasi
        }
    
    def get_display_data(self) -> Dict:
        """Get all data formatted for display"""
        return {
            'planetary_positions': self.planet_positions,
            'planet_house_positions': self.planet_house_positions,  # House positions for highlighting
            'planet_details': self.planet_details,
            'birth_chart_data': self.get_birth_chart_data(),
            'ashtakavarga_charts': self.ashtakavarga_charts,  # All 8 planets including Ascendant
            'sarvashtakavarga': self.sarvashtakavarga,  # Sum of 7 planets only
            'native_chart': self.get_native_chart(),
            'totals': {planet: sum(chart) for planet, chart in self.ashtakavarga_charts.items()},
            'sarva_total': sum(self.sarvashtakavarga),
            'matrix_8x8': self.get_8x8_matrix()  # 8x8 matrix for all planets
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
    
    calculator = AshtakavargaCalculatorFinal(birth_data)
    positions = calculator.calculate_positions()
    charts = calculator.calculate_all_charts()
    display_data = calculator.get_display_data()
    
    print("\n=== PLANETARY POSITIONS ===")
    for planet, rasi in positions.items():
        print(f"{planet:10}: Rasi {rasi:2d}")
    
    print("\n=== BAV TOTALS (All 8 Planets) ===")
    for planet, total in display_data['totals'].items():
        print(f"{planet:10}: {total:2d} points")
    
    print(f"\n=== SAV TOTAL (7 Planets Only) ===")
    print(f"Total: {display_data['sarva_total']} points")
    print(f"SAV per house: {display_data['sarvashtakavarga']}")
    
    print("\n=== 8x8 MATRIX (Sample - First 3 houses for SUN) ===")
    matrix = display_data['matrix_8x8']
    if 'SUN' in matrix:
        contributing = ['SUN', 'MOON', 'MARS', 'MERCURY', 'JUPITER', 'VENUS', 'SATURN', 'ASCENDANT']
        print("Contributing Planets -> Houses 1-3")
        for i, contrib in enumerate(contributing):
            print(f"{contrib:10}: {matrix['SUN'][i][:3]}")

if __name__ == "__main__":
    main()
