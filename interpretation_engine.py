#!/usr/bin/env python3
"""
Ashtakavarga Interpretation Engine
Provides quantified analysis and interpretations based on Parasara principles
"""

from typing import Dict, List, Tuple
import math

class AshtakavargaInterpreter:
    """Comprehensive interpretation engine for Ashtakavarga analysis"""
    
    def __init__(self):
        # House significations based on Parasara principles
        self.house_significations = {
            1: {
                'name': 'Lagna (Ascendant)',
                'tamil': 'லக்கினம்',
                'significations': [
                    'Physical appearance and constitution',
                    'Personality and character',
                    'Health and vitality',
                    'Head and face',
                    'Overall life direction',
                    'Self and identity'
                ],
                'body_parts': ['Head', 'Face', 'Brain', 'Hair'],
                'keywords': ['Self', 'Personality', 'Health', 'Appearance']
            },
            2: {
                'name': 'Dhana (Wealth)',
                'tamil': 'தனம்',
                'significations': [
                    'Wealth and financial resources',
                    'Family and domestic life',
                    'Speech and communication',
                    'Food and nourishment',
                    'Right eye',
                    'Banking and investments'
                ],
                'body_parts': ['Right Eye', 'Face', 'Mouth', 'Tongue'],
                'keywords': ['Wealth', 'Family', 'Speech', 'Food']
            },
            3: {
                'name': 'Sahaja (Siblings)',
                'tamil': 'சகோதரர்',
                'significations': [
                    'Siblings and relatives',
                    'Courage and valor',
                    'Communication and writing',
                    'Short journeys',
                    'Arms and shoulders',
                    'Mental strength'
                ],
                'body_parts': ['Arms', 'Shoulders', 'Hands', 'Chest'],
                'keywords': ['Siblings', 'Courage', 'Communication', 'Journeys']
            },
            4: {
                'name': 'Sukha (Happiness)',
                'tamil': 'சுகம்',
                'significations': [
                    'Mother and maternal relations',
                    'Home and property',
                    'Education and learning',
                    'Vehicles and conveyances',
                    'Chest and heart',
                    'Emotional security'
                ],
                'body_parts': ['Chest', 'Heart', 'Lungs', 'Breast'],
                'keywords': ['Mother', 'Home', 'Education', 'Vehicles']
            },
            5: {
                'name': 'Putra (Children)',
                'tamil': 'புத்திரர்',
                'significations': [
                    'Children and progeny',
                    'Intelligence and wisdom',
                    'Creativity and arts',
                    'Speculation and gambling',
                    'Stomach and liver',
                    'Romance and love affairs'
                ],
                'body_parts': ['Stomach', 'Liver', 'Spleen', 'Abdomen'],
                'keywords': ['Children', 'Intelligence', 'Creativity', 'Romance']
            },
            6: {
                'name': 'Ari (Enemies)',
                'tamil': 'அரி',
                'significations': [
                    'Enemies and obstacles',
                    'Diseases and health issues',
                    'Service and employment',
                    'Debts and losses',
                    'Waist and intestines',
                    'Legal disputes'
                ],
                'body_parts': ['Waist', 'Intestines', 'Kidneys', 'Lower Abdomen'],
                'keywords': ['Enemies', 'Diseases', 'Service', 'Debts']
            },
            7: {
                'name': 'Kalatra (Spouse)',
                'tamil': 'கலத்ரம்',
                'significations': [
                    'Marriage and spouse',
                    'Partnerships and relationships',
                    'Business and trade',
                    'Sexual life',
                    'Genitals and reproductive organs',
                    'Public relations'
                ],
                'body_parts': ['Genitals', 'Reproductive Organs', 'Lower Back'],
                'keywords': ['Marriage', 'Partnerships', 'Business', 'Relationships']
            },
            8: {
                'name': 'Ayu (Longevity)',
                'tamil': 'ஆயுள்',
                'significations': [
                    'Longevity and lifespan',
                    'Occult and mystical knowledge',
                    'Inheritance and legacies',
                    'Accidents and sudden events',
                    'Anus and excretory system',
                    'Transformation and regeneration'
                ],
                'body_parts': ['Anus', 'Excretory System', 'Rectum'],
                'keywords': ['Longevity', 'Occult', 'Inheritance', 'Transformation']
            },
            9: {
                'name': 'Bhagya (Fortune)',
                'tamil': 'பாக்யம்',
                'significations': [
                    'Fortune and luck',
                    'Father and paternal relations',
                    'Higher learning and philosophy',
                    'Long journeys and foreign lands',
                    'Hips and thighs',
                    'Spirituality and religion'
                ],
                'body_parts': ['Hips', 'Thighs', 'Buttocks'],
                'keywords': ['Fortune', 'Father', 'Philosophy', 'Spirituality']
            },
            10: {
                'name': 'Karma (Profession)',
                'tamil': 'கர்மம்',
                'significations': [
                    'Profession and career',
                    'Status and reputation',
                    'Authority and power',
                    'Government and administration',
                    'Knees and joints',
                    'Achievements and recognition'
                ],
                'body_parts': ['Knees', 'Joints', 'Legs'],
                'keywords': ['Career', 'Status', 'Authority', 'Achievements']
            },
            11: {
                'name': 'Labha (Gains)',
                'tamil': 'லாபம்',
                'significations': [
                    'Gains and profits',
                    'Friends and social circle',
                    'Aspirations and desires',
                    'Income and earnings',
                    'Ankles and calves',
                    'Hopes and wishes'
                ],
                'body_parts': ['Ankles', 'Calves', 'Shins'],
                'keywords': ['Gains', 'Friends', 'Aspirations', 'Income']
            },
            12: {
                'name': 'Vyaya (Expenses)',
                'tamil': 'வியயம்',
                'significations': [
                    'Expenses and losses',
                    'Foreign lands and travel',
                    'Bed pleasures and comforts',
                    'Spiritual liberation',
                    'Feet and toes',
                    'Charity and donations'
                ],
                'body_parts': ['Feet', 'Toes', 'Soles'],
                'keywords': ['Expenses', 'Foreign', 'Liberation', 'Charity']
            }
        }
        
        # Planet significations
        self.planet_significations = {
            'SUN': {
                'name': 'Sun',
                'tamil': 'சூர்யன்',
                'significations': [
                    'Soul and self',
                    'Father and authority',
                    'Government and administration',
                    'Health and vitality',
                    'Leadership and power',
                    'Eyes and vision'
                ],
                'keywords': ['Soul', 'Father', 'Authority', 'Leadership']
            },
            'MOON': {
                'name': 'Moon',
                'tamil': 'சந்திரன்',
                'significations': [
                    'Mind and emotions',
                    'Mother and maternal relations',
                    'Public and masses',
                    'Travel and movement',
                    'Fluids and water',
                    'Imagination and creativity'
                ],
                'keywords': ['Mind', 'Mother', 'Emotions', 'Public']
            },
            'MARS': {
                'name': 'Mars',
                'tamil': 'செவ்வாய்',
                'significations': [
                    'Energy and courage',
                    'Brothers and siblings',
                    'Land and property',
                    'Accidents and injuries',
                    'Surgery and operations',
                    'Weapons and tools'
                ],
                'keywords': ['Energy', 'Courage', 'Brothers', 'Land']
            },
            'MERCURY': {
                'name': 'Mercury',
                'tamil': 'புதன்',
                'significations': [
                    'Intelligence and communication',
                    'Business and trade',
                    'Education and learning',
                    'Writing and speaking',
                    'Nervous system',
                    'Mathematics and calculations'
                ],
                'keywords': ['Intelligence', 'Communication', 'Business', 'Education']
            },
            'JUPITER': {
                'name': 'Jupiter',
                'tamil': 'குரு',
                'significations': [
                    'Wisdom and knowledge',
                    'Teachers and gurus',
                    'Children and progeny',
                    'Wealth and prosperity',
                    'Religion and spirituality',
                    'Law and justice'
                ],
                'keywords': ['Wisdom', 'Teachers', 'Children', 'Wealth']
            },
            'VENUS': {
                'name': 'Venus',
                'tamil': 'சுக்ரன்',
                'significations': [
                    'Love and relationships',
                    'Beauty and arts',
                    'Marriage and spouse',
                    'Luxury and comforts',
                    'Vehicles and conveyances',
                    'Reproductive system'
                ],
                'keywords': ['Love', 'Beauty', 'Marriage', 'Luxury']
            },
            'SATURN': {
                'name': 'Saturn',
                'tamil': 'சனி',
                'significations': [
                    'Discipline and hard work',
                    'Longevity and old age',
                    'Servants and subordinates',
                    'Delays and obstacles',
                    'Chronic diseases',
                    'Spiritual practices'
                ],
                'keywords': ['Discipline', 'Longevity', 'Delays', 'Spirituality']
            },
            'ASCENDANT': {
                'name': 'Ascendant',
                'tamil': 'லக்கினம்',
                'significations': [
                    'Physical appearance',
                    'Personality and character',
                    'Health and vitality',
                    'Overall life direction',
                    'First impressions',
                    'Body constitution'
                ],
                'keywords': ['Appearance', 'Personality', 'Health', 'Direction']
            }
        }
    
    def get_strength_level(self, value: int, is_bav: bool = False) -> Tuple[str, str, str]:
        """Get strength level based on Ashtakavarga value
        
        For BAV: >4 is good strength, <4 is weak
        For SAV: Use thresholds from Vedic rules
        """
        if is_bav:
            # BAV strength: >4 is good, <4 is weak
            if value > 4:
                return 'Good Strength', 'success', '#28a745'  # Green
            elif value == 4:
                return 'Neutral', 'warning', '#ffc107'  # Orange
            else:
                return 'Weak', 'danger', '#dc3545'  # Red
        else:
            # SAV strength levels
            if value >= 30:
                return 'Benefic (Strong)', 'success', '#28a745'  # Green
            elif value >= 28:
                return 'Good (Baseline)', 'info', '#17a2b8'  # Blue
            elif value >= 22:
                return 'Average', 'warning', '#ffc107'  # Orange
            else:
                return 'Malefic (Weak)', 'danger', '#dc3545'  # Red
    
    def analyze_house_strength(self, sarva_values: List[int], ascendant_rasi: int = 1, bav_charts: Dict = None, planet_positions: Dict = None) -> List[Dict]:
        """Analyze strength of each house in Sarvashtakavarga with Vedic rules
        
        Rules applied:
        - Baseline (Good): 28 points
        - Malefic Threshold: <22 points (planets transiting produce malefic results)
        - Benefic Threshold: >30 points (yields benefic results)
        - Dusthanas (6th, 8th): Low points are beneficial
        """
        analysis = []
        bav_charts = bav_charts or {}
        planet_positions = planet_positions or {}
        
        # Tamil Rasi names
        tamil_rasis = [
            "மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்", "சிம்மம்", "கன்னி",
            "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்", "கும்பம்", "மீனம்"
        ]
        
        # Get Moon position for Sade Sati analysis
        moon_house = planet_positions.get('MOON', 1)
        
        for i, value in enumerate(sarva_values):
            house_num = i + 1
            strength, level, color = self.get_strength_level(value, is_bav=False)
            house_info = self.house_significations[house_num]
            
            # Calculate the actual Rasi for this house based on Ascendant
            actual_rasi_index = (ascendant_rasi + house_num - 2) % 12
            actual_rasi = tamil_rasis[actual_rasi_index]
            
            # Calculate percentage of maximum possible (28 is baseline, 54 is max)
            percentage = (value / 28) * 100
            max_percentage = (value / 54) * 100
            
            # Vedic interpretation rules
            interpretations = []
            warnings = []
            
            # Rule: Baseline (28 points is good)
            if value == 28:
                interpretations.append("Baseline good strength - average results expected")
            elif value > 28:
                interpretations.append("Above baseline - beneficial results expected")
            elif value < 28:
                interpretations.append("Below baseline - requires attention")
            
            # Rule: Malefic threshold (<22 points)
            if value < 22:
                warnings.append("Malefic threshold: Planets transiting this house may produce negative results")
            
            # Rule: Benefic threshold (>30 points)
            if value > 30:
                interpretations.append("Benefic threshold: Yields positive results and protects from negative transits")
            
            # Rule: Dusthanas (6th and 8th houses - low points are beneficial)
            if house_num in [6, 8]:
                if value < 22:
                    interpretations.append("Dusthana house with low points - beneficial for this house")
                elif value >= 28:
                    warnings.append("Dusthana house with high points - may create challenges")
            
            # Rule: Lagna (1st house) specific rules
            if house_num == 1:
                if value >= 45:
                    interpretations.append("Very high Lagna points - native may be famous and capable of dominating others")
                if value == 54:
                    warnings.append("Maximum Lagna points (54) - native may be extremely arrogant")
                # Check 6th house for health
                if len(sarva_values) >= 6:
                    sixth_house_points = sarva_values[5]  # 6th house (index 5)
                    if value >= 30 and sixth_house_points < 22:
                        interpretations.append("High Lagna with low 6th house - excellent health indicated")
                    elif value >= 30 and sixth_house_points >= 22:
                        warnings.append("High Lagna but 6th house not low - may face frequent illness")
            
            # Rule: Marriage (7th house) specific rules
            if house_num == 7:
                if value < 22:
                    interpretations.append("Low 7th house points - early marriage indicated")
                elif value > 30:
                    warnings.append("High 7th house points - delayed marriage indicated")
                # Check Venus and Mars BAV in 7th house
                if bav_charts:
                    venus_7th = bav_charts.get('VENUS', [0]*12)[6] if len(bav_charts.get('VENUS', [])) >= 7 else 0
                    mars_7th = bav_charts.get('MARS', [0]*12)[6] if len(bav_charts.get('MARS', [])) >= 7 else 0
                    if venus_7th == 0 or mars_7th == 0 or value == 0:
                        warnings.append("0 points in 7th house, Venus, or Mars - marriage may not occur")
            
            # Rule: Sade Sati protection (Moon house and adjacent houses)
            if house_num in [moon_house - 1, moon_house, moon_house + 1]:
                # Normalize to 1-12 range
                check_houses = [(moon_house - 2) % 12 + 1, moon_house, moon_house % 12 + 1]
                if house_num in check_houses and value > 30:
                    interpretations.append("Sade Sati protection: High points mitigate severe negative impact")
            
            # Rule: Transit protection for slow-moving planets
            if value > 30:
                interpretations.append("Slow-moving planets (Saturn, Jupiter, Rahu, Ketu) transiting will not produce bad results")
            
            analysis.append({
                'house': house_num,
                'name': house_info['name'],
                'tamil': actual_rasi,
                'value': value,
                'strength': strength,
                'level': level,
                'color': color,
                'percentage': round(percentage, 1),
                'max_percentage': round(max_percentage, 1),
                'significations': house_info['significations'],
                'body_parts': house_info['body_parts'],
                'keywords': house_info['keywords'],
                'interpretations': interpretations,
                'warnings': warnings,
                'is_benefic': value > 30,
                'is_malefic': value < 22,
                'is_dusthana': house_num in [6, 8]
            })
        
        return analysis
    
    def analyze_planet_strength(self, planet_totals: Dict[str, int], bav_charts: Dict = None) -> List[Dict]:
        """Analyze strength of each planet's Ashtakavarga (BAV)
        
        Rules applied:
        - >4 points in a house is good strength
        - <4 points in a house is weak
        - Check for 0 points (accident indicators)
        """
        analysis = []
        bav_charts = bav_charts or {}
        
        # Standard Vedic total bindu counts
        expected_totals = {
            'SUN': 48,
            'MOON': 49,
            'MARS': 39,
            'MERCURY': 54,
            'JUPITER': 56,
            'VENUS': 52,
            'SATURN': 39
        }
        
        for planet, total in planet_totals.items():
            if planet == 'ASCENDANT':
                continue  # Skip Ascendant for planet analysis
            
            # For BAV analysis, use BAV-specific strength levels
            strength, level, color = self.get_strength_level(total // 12, is_bav=True)  # Average per house
            planet_info = self.planet_significations[planet]
            
            # Calculate percentage (56 is highest for Jupiter)
            max_possible = 56
            percentage = (total / max_possible) * 100
            
            # Check for 0 points in houses (accident indicators)
            zero_points_houses = []
            accident_warnings = []
            
            if planet in bav_charts:
                chart = bav_charts[planet]
                for i, points in enumerate(chart):
                    if points == 0:
                        zero_points_houses.append(i + 1)
                
                # Rule: Mars with 0 points indicates blood-related issues and accidents
                if planet == 'MARS' and zero_points_houses:
                    accident_warnings.append(f"Mars has 0 points in houses {zero_points_houses} - indicates blood-related issues and accidents")
                
                # Rule: Sun with 0 points + Mars transit indicates accident to father
                if planet == 'SUN' and zero_points_houses:
                    accident_warnings.append(f"Sun has 0 points in houses {zero_points_houses} - if Mars transits these houses, risk of accident to father")
            
            # Check against expected totals
            expected = expected_totals.get(planet, total)
            total_status = "Standard" if abs(total - expected) <= 2 else "Varies"
            
            analysis.append({
                'planet': planet,
                'name': planet_info['name'],
                'tamil': planet_info['tamil'],
                'total': total,
                'expected_total': expected,
                'total_status': total_status,
                'strength': strength,
                'level': level,
                'color': color,
                'percentage': round(percentage, 1),
                'significations': planet_info['significations'],
                'keywords': planet_info['keywords'],
                'zero_points_houses': zero_points_houses,
                'accident_warnings': accident_warnings,
                'is_good_strength': total > 48,  # Rough threshold
                'average_per_house': round(total / 12, 2)
            })
        
        return sorted(analysis, key=lambda x: x['total'], reverse=True)
    
    def get_overall_analysis(self, sarva_total: int) -> Dict:
        """Get overall analysis of the chart"""
        if sarva_total >= 350:
            overall_strength = 'Exceptional Life Potential'
            color = '#28a745'
            description = f'Your Sarvashtakavarga total of {sarva_total} points indicates exceptional potential for success, prosperity, and fulfillment in life. You have strong planetary support across most life areas, suggesting natural talents, good fortune, and the ability to overcome challenges. This is considered an excellent chart for achieving life goals and experiencing overall happiness and success.'
            level = 'Very High'
        elif sarva_total >= 320:
            overall_strength = 'Strong Life Potential'
            color = '#20c997'
            description = f'Your Sarvashtakavarga total of {sarva_total} points indicates strong potential for success with some areas requiring focused attention. You have good planetary support in most life areas, suggesting natural abilities and the capacity to achieve your goals with proper effort and planning.'
            level = 'High'
        elif sarva_total >= 300:
            overall_strength = 'Moderate Life Potential'
            color = '#ffc107'
            description = f'Your Sarvashtakavarga total of {sarva_total} points indicates moderate potential with mixed results across different life areas. While you have some natural strengths, certain areas may require more effort and attention to achieve desired outcomes.'
            level = 'Moderate'
        elif sarva_total >= 280:
            overall_strength = 'Challenging Life Path'
            color = '#fd7e14'
            description = f'Your Sarvashtakavarga total of {sarva_total} points indicates potential challenges that require focused effort, strategic planning, and appropriate remedies. While this may seem challenging, it also presents opportunities for significant personal growth and spiritual development.'
            level = 'Below Average'
        else:
            overall_strength = 'Difficult Life Path'
            color = '#dc3545'
            description = f'Your Sarvashtakavarga total of {sarva_total} points indicates significant challenges that require dedicated effort, spiritual practices, and appropriate remedies. This chart presents opportunities for deep personal transformation and spiritual growth through overcoming obstacles.'
            level = 'Low'
        
        return {
            'total': sarva_total,
            'strength': overall_strength,
            'level': level,
            'color': color,
            'description': description,
            'interpretation': description,
            'average_per_house': round(sarva_total / 12, 1)
        }
    
    def get_recommendations(self, house_analysis: List[Dict], planet_analysis: List[Dict]) -> List[str]:
        """Get recommendations based on Vedic analysis"""
        recommendations = []
        
        # Find malefic houses (<22 points)
        malefic_houses = [h for h in house_analysis if h.get('is_malefic', False)]
        if malefic_houses:
            house_names = [f"{h['name']} ({h['value']} pts)" for h in malefic_houses]
            recommendations.append(f"Malefic houses (<22 points): {', '.join(house_names)} - planets transiting may produce negative results")
        
        # Find benefic houses (>30 points)
        benefic_houses = [h for h in house_analysis if h.get('is_benefic', False)]
        if benefic_houses:
            house_names = [f"{h['name']} ({h['value']} pts)" for h in benefic_houses]
            recommendations.append(f"Benefic houses (>30 points): {', '.join(house_names)} - yields positive results")
        
        # Find weak planets (<4 average per house)
        weak_planets = [p for p in planet_analysis if p.get('average_per_house', 0) < 4]
        if weak_planets:
            planet_names = [f"{p['name']} ({p['average_per_house']:.1f} avg)" for p in weak_planets]
            recommendations.append(f"Weak planets (<4 avg per house): {', '.join(planet_names)} - limited positive results")
        
        # Accident warnings
        accident_planets = [p for p in planet_analysis if p.get('accident_warnings')]
        if accident_planets:
            for planet in accident_planets:
                for warning in planet['accident_warnings']:
                    recommendations.append(f"⚠️ {warning}")
        
        # Transit timing recommendations
        if benefic_houses:
            recommendations.append("For auspicious timing, choose periods when strong planets transit houses with >30 SAV points")
        
        # Advanced validation notes
        recommendations.append("Note: Navamsa check recommended - High points in Rashi BAV may not be beneficial if planet has low points in Navamsa chart")
        recommendations.append("Note: Dasha analysis recommended - Planets in Dasha/Bhukti/Antardasha give benefic results even during transits if moving through high SAV houses")
        
        # General recommendations
        recommendations.append("Regular meditation and spiritual practices can help balance planetary influences")
        recommendations.append("High SAV points (>30) can protect from negative effects of Maraka and Pathaka lords")
        recommendations.append("Consult with a qualified Vedic astrologer for personalized remedies, Dasha analysis, and Navamsa verification")
        
        return recommendations
    
    def generate_comprehensive_analysis(self, sarva_values: List[int], planet_totals: Dict[str, int], sarva_total: int, ascendant_rasi: int = 1, bav_charts: Dict = None, planet_positions: Dict = None) -> Dict:
        """Generate comprehensive analysis with Vedic rules
        
        Includes:
        - SAV house strength interpretations
        - BAV planet strength analysis
        - Specific planet & house logic (Lagna, Marriage, Accidents)
        - Transit protections
        - Advanced validation rules
        """
        bav_charts = bav_charts or {}
        planet_positions = planet_positions or {}
        
        house_analysis = self.analyze_house_strength(sarva_values, ascendant_rasi, bav_charts, planet_positions)
        planet_analysis = self.analyze_planet_strength(planet_totals, bav_charts)
        overall_analysis = self.get_overall_analysis(sarva_total)
        recommendations = self.get_recommendations(house_analysis, planet_analysis)
        
        # Add specific interpretations based on rules
        specific_interpretations = self.get_specific_interpretations(sarva_values, bav_charts, planet_positions, ascendant_rasi)
        
        return {
            'overall': overall_analysis,
            'houses': house_analysis,
            'planets': planet_analysis,
            'recommendations': recommendations,
            'specific_interpretations': specific_interpretations
        }
    
    def get_specific_interpretations(self, sarva_values: List[int], bav_charts: Dict, planet_positions: Dict, ascendant_rasi: int) -> Dict:
        """Get specific interpretations based on Vedic rules"""
        interpretations = {
            'lagna': [],
            'marriage': [],
            'accidents': [],
            'transit_protections': [],
            'dasha_impacts': []
        }
        
        # Lagna (1st house) interpretations
        if len(sarva_values) >= 1:
            lagna_points = sarva_values[0]
            if lagna_points >= 45:
                interpretations['lagna'].append(f"High Lagna points ({lagna_points}) - native may be famous and capable of dominating others")
            if lagna_points == 54:
                interpretations['lagna'].append("Maximum Lagna points (54) - native may be extremely arrogant")
            
            # Health analysis (Lagna vs 6th house)
            if len(sarva_values) >= 6:
                sixth_points = sarva_values[5]
                if lagna_points >= 30 and sixth_points < 22:
                    interpretations['lagna'].append(f"High Lagna ({lagna_points}) with low 6th house ({sixth_points}) - excellent health indicated")
                elif lagna_points >= 30 and sixth_points >= 22:
                    interpretations['lagna'].append(f"High Lagna ({lagna_points}) but 6th house not low ({sixth_points}) - may face frequent illness")
        
        # Marriage (7th house) interpretations
        if len(sarva_values) >= 7:
            seventh_points = sarva_values[6]
            if seventh_points < 22:
                interpretations['marriage'].append(f"Low 7th house points ({seventh_points}) - early marriage indicated")
            elif seventh_points > 30:
                interpretations['marriage'].append(f"High 7th house points ({seventh_points}) - delayed marriage indicated")
            
            # Check Venus and Mars BAV in 7th house
            if bav_charts:
                venus_7th = bav_charts.get('VENUS', [0]*12)[6] if len(bav_charts.get('VENUS', [])) >= 7 else 0
                mars_7th = bav_charts.get('MARS', [0]*12)[6] if len(bav_charts.get('MARS', [])) >= 7 else 0
                
                if seventh_points == 0 or venus_7th == 0 or mars_7th == 0:
                    interpretations['marriage'].append("0 points in 7th house, Venus, or Mars - marriage may not occur")
                
                # Check 7th Lord (need to determine which planet rules 7th house)
                # This would require additional chart analysis
        
        # Accident indicators
        if bav_charts:
            # Mars 0 points
            mars_chart = bav_charts.get('MARS', [])
            mars_zero_houses = [i+1 for i, val in enumerate(mars_chart) if val == 0]
            if mars_zero_houses:
                interpretations['accidents'].append(f"Mars has 0 points in houses {mars_zero_houses} - indicates blood-related issues and accidents")
            
            # Sun 0 points
            sun_chart = bav_charts.get('SUN', [])
            sun_zero_houses = [i+1 for i, val in enumerate(sun_chart) if val == 0]
            if sun_zero_houses:
                interpretations['accidents'].append(f"Sun has 0 points in houses {sun_zero_houses} - if Mars transits these houses, risk of accident to father")
        
        # Transit protections
        for i, points in enumerate(sarva_values):
            if points > 30:
                interpretations['transit_protections'].append(f"House {i+1} has {points} points (>30) - slow-moving planets (Saturn, Jupiter, Rahu, Ketu) transiting will not produce bad results")
        
        # Sade Sati protection
        moon_house = planet_positions.get('MOON', 1)
        if len(sarva_values) >= moon_house:
            moon_house_points = sarva_values[moon_house - 1]
            if moon_house_points > 30:
                interpretations['transit_protections'].append(f"Moon's house ({moon_house}) has {moon_house_points} points (>30) - Sade Sati protection: severe negative impact mitigated")
        
        # Dasha impacts (general note)
        interpretations['dasha_impacts'].append("Planets in their Dasha, Bhukti, or Antardasha will give benefic results during transits if moving through houses with high SAV points (>30)")
        
        # Maraka/Pathaka protection
        high_sav_houses = [i+1 for i, val in enumerate(sarva_values) if val > 30]
        if high_sav_houses:
            interpretations['dasha_impacts'].append(f"High SAV points (>30) in houses {high_sav_houses} can protect from negative effects of Maraka and Pathaka lords")
        
        return interpretations

def main():
    """Test the interpretation engine"""
    interpreter = AshtakavargaInterpreter()
    
    # Test data
    sarva_values = [32, 36, 34, 30, 28, 16, 24, 28, 33, 28, 24, 24]
    planet_totals = {
        'SUN': 48, 'MOON': 49, 'MARS': 39, 'MERCURY': 54,
        'JUPITER': 56, 'VENUS': 52, 'SATURN': 39, 'ASCENDANT': 49
    }
    sarva_total = 337
    
    analysis = interpreter.generate_comprehensive_analysis(sarva_values, planet_totals, sarva_total)
    
    print("Comprehensive Ashtakavarga Analysis")
    print("=" * 50)
    print(f"Overall Strength: {analysis['overall']['strength']}")
    print(f"Total Points: {analysis['overall']['total']}")
    print(f"Description: {analysis['overall']['description']}")
    
    print("\nHouse Analysis:")
    for house in analysis['houses']:
        print(f"House {house['house']} ({house['name']}): {house['value']} points - {house['strength']}")
    
    print("\nPlanet Analysis:")
    for planet in analysis['planets']:
        print(f"{planet['name']}: {planet['total']} points - {planet['strength']}")
    
    print("\nRecommendations:")
    for rec in analysis['recommendations']:
        print(f"- {rec}")

if __name__ == "__main__":
    main()
