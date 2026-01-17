"""
Tamil Ashtakavarga Interpretation Engine
Implements traditional Tamil Ashtakavarga predictions and interpretations
"""

from typing import Dict, List, Tuple
from ashtakavarga_calculator_final import AshtakavargaCalculator

class TamilAshtakavargaInterpreter:
    """Tamil Ashtakavarga Interpretation Engine"""
    
    def __init__(self):
        self.tamil_rasis = [
            "மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்", "சிம்மம்", "கன்னி",
            "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்", "கும்பம்", "மீனம்"
        ]
        
        # Direction mappings for houses
        self.direction_houses = {
            'east': [1, 12, 11],      # கிழக்கு
            'south': [10, 9, 8],      # தெற்கு  
            'west': [7, 6, 5],        # மேற்கு
            'north': [4, 3, 2]        # வடக்கு
        }
        
        # Age period mappings
        self.age_periods = {
            'young': [1, 2, 3, 4],           # இளம் வயது
            'middle': [5, 6, 7, 8],          # நடு வயது
            'old': [9, 10, 11, 12]           # முது வயது
        }
        
        # Rasi age periods
        self.rasi_age_periods = {
            'young': [12, 1, 2, 3],          # மீனம் to மிதுனம்
            'middle': [4, 5, 6, 7],          # கடகம் to துலாம்
            'old': [8, 9, 10, 11]            # விருச்சிகம் to கும்பம்
        }
    
    def calculate_longevity_analysis(self, sarva_values: List[int], ascendant_rasi: int) -> Dict:
        """Calculate longevity based on Lagna vs 8th house comparison"""
        # sarva_values is already mapped based on Ascendant:
        # Index 0 = House 1 (Lagna), Index 7 = House 8 (8th house)
        lagna_value = sarva_values[0]  # House 1 (Lagna)
        eighth_value = sarva_values[7]  # House 8 (8th house)
        
        if lagna_value < eighth_value:
            longevity = "மத்திம ஆயுள்"  # Medium longevity
        elif lagna_value > eighth_value:
            longevity = "நீண்ட ஆயுள்"  # Long longevity
        else:
            longevity = "சாதாரண ஆயுள்"  # Normal longevity
            
        return {
            'lagna_value': lagna_value,
            'eighth_value': eighth_value,
            'longevity': longevity,
            'interpretation': f"லக்னத்திற்கு 8ஆம் வீட்டில் உள்ள பரல்களை விட லக்னத்தில் உள்ள பரல்கள் {'குறைவாக' if lagna_value < eighth_value else 'அதிகமாக'} இருப்பதால் ஜாதகருக்கு {longevity}."
        }
    
    def calculate_agam_puram(self, sarva_values: List[int], ascendant_rasi: int) -> Dict:
        """Calculate Agam (internal happiness) vs Puram (external happiness)"""
        # sarva_values is already mapped based on Ascendant:
        # Agam houses: 1-4-7-10, 5-9 (indices 0, 3, 6, 9, 4, 8)
        agam_indices = [0, 3, 6, 9, 4, 8]  # Houses 1, 4, 7, 10, 5, 9
        agam_total = sum(sarva_values[i] for i in agam_indices)
        
        # Puram houses: 2-6-8-12, 3-11 (indices 1, 5, 7, 11, 2, 10)
        puram_indices = [1, 5, 7, 11, 2, 10]  # Houses 2, 6, 8, 12, 3, 11
        puram_total = sum(sarva_values[i] for i in puram_indices)
        
        if agam_total > puram_total:
            happiness = "வாழ்கையில் எல்லா விதத்திலும் மனதிருப்தி உண்டாகும்"
        elif puram_total > agam_total:
            happiness = "வெளிப்புற விஷயங்களில் மனதிருப்தி உண்டாகும்"
        else:
            happiness = "சமநிலையான மனதிருப்தி உண்டாகும்"
            
        return {
            'agam_total': agam_total,
            'puram_total': puram_total,
            'happiness': happiness,
            'interpretation': f"இந்த ஜாதகத்தில் புறப்பரல்களை ({puram_total}) விட அகப்பரல்கள் ({agam_total}) {'அதிகமாக' if agam_total > puram_total else 'குறைவாக'} இருப்பதால் ஜாதகருக்கு {happiness}."
        }
    
    def calculate_srisuram(self, sarva_values: List[int], ascendant_rasi: int) -> Dict:
        """Calculate Srisuram (wealth vs expenses)"""
        # sarva_values is already mapped based on Ascendant:
        # Srisuram houses: 1-2-4-9-10-11 (indices 0, 1, 3, 8, 9, 10)
        srisuram_indices = [0, 1, 3, 8, 9, 10]  # Houses 1, 2, 4, 9, 10, 11
        srisuram_total = sum(sarva_values[i] for i in srisuram_indices)
        
        if srisuram_total > 164:
            wealth_status = "செலவை விட வரவு அதிகமாக இருக்கும்"
        else:
            wealth_status = "செலவு அதிகமாக இருக்கும்"
            
        return {
            'srisuram_total': srisuram_total,
            'wealth_status': wealth_status,
            'interpretation': f"லக்னத்திற்கு 1-2-4-9-10-11 ஆம் இடங்களில் உள்ள பரல்களை ஒன்றாக கூட்டவும். இதற்கு ஸ்ரீசுரம் ({srisuram_total}) என்று பெயர். இவ்வாறு கூட்டி வந்த தொகை 164 க்கு {'மேல்' if srisuram_total > 164 else 'கீழ்'} இருப்பதால் {wealth_status}."
        }
    
    def calculate_asrisuram(self, sarva_values: List[int], ascendant_rasi: int) -> Dict:
        """Calculate Asrisuram (expenses vs income)"""
        # sarva_values is already mapped based on Ascendant:
        # Asrisuram houses: 6-8-12 (indices 5, 7, 11)
        asrisuram_indices = [5, 7, 11]  # Houses 6, 8, 12
        asrisuram_total = sum(sarva_values[i] for i in asrisuram_indices)
        
        if asrisuram_total < 76:
            expense_status = "வரவை விட செலவு குறைவாக இருக்கும்"
        else:
            expense_status = "செலவு அதிகமாக இருக்கும்"
            
        return {
            'asrisuram_total': asrisuram_total,
            'expense_status': expense_status,
            'interpretation': f"லக்னத்திற்கு 6-8-12 ஆம் இடங்களில் உள்ள பரல்களை ஒன்றாக கூட்டவும். இதற்கு அஸ்ரீசுரம் ({asrisuram_total}) என்று பெயர். இவ்வாறு கூட்டி வந்த தொகை 76 க்கு {'குறைவாக' if asrisuram_total < 76 else 'அதிகமாக'} இருந்தால் {expense_status}."
        }
    
    def find_beneficial_rasis(self, sarva_values: List[int], ascendant_rasi: int) -> Dict:
        """Find most and least beneficial Rasis for relationships"""
        # Calculate total points for each Rasi based on Ascendant
        rasi_totals = {}
        
        for i, value in enumerate(sarva_values):
            # Calculate which Rasi this house corresponds to
            rasi_index = (ascendant_rasi + i - 1) % 12
            rasi_name = self.tamil_rasis[rasi_index]
            
            if rasi_name not in rasi_totals:
                rasi_totals[rasi_name] = 0
            rasi_totals[rasi_name] += value
        
        # Find most and least beneficial
        most_beneficial = max(rasi_totals.items(), key=lambda x: x[1])
        least_beneficial = min(rasi_totals.items(), key=lambda x: x[1])
        
        return {
            'most_beneficial': {
                'rasi': most_beneficial[0],
                'points': most_beneficial[1],
                'interpretation': f"இந்த ஜாதகருக்கு {most_beneficial[0]} ராசியில் அதிக பரல்கள் இருப்பதால் அந்த ராசியை ஜென்ம ராசியாகவோ அல்லது ஜென்ம லக்னமாகவோ கொண்டவர்கள் வாழ்க்கை துணையாக அமைந்தால் வாழ்க்கை சிறப்பாக இருக்கும்"
            },
            'least_beneficial': {
                'rasi': least_beneficial[0],
                'points': least_beneficial[1],
                'interpretation': f"இந்த ஜாதகருக்கு {least_beneficial[0]} ராசியில் குறைவான பரல்கள் இருப்பதால் அந்த ராசியை ஜென்ம ராசியாகவோ அல்லது ஜென்ம லக்னமாகவோ கொண்டவர்களுடன் கூட்டு சேரகூடாது"
            }
        }
    
    def calculate_age_periods(self, sarva_values: List[int], ascendant_rasi: int) -> Dict:
        """Calculate happiness in different age periods"""
        # sarva_values is already mapped based on Ascendant:
        # Method 1: House-based age periods (indices 0-3, 4-7, 8-11)
        young_indices = [0, 1, 2, 3]  # Houses 1, 2, 3, 4
        middle_indices = [4, 5, 6, 7]  # Houses 5, 6, 7, 8
        old_indices = [8, 9, 10, 11]  # Houses 9, 10, 11, 12
        
        young_total = sum(sarva_values[i] for i in young_indices)
        middle_total = sum(sarva_values[i] for i in middle_indices)
        old_total = sum(sarva_values[i] for i in old_indices)
        
        # Find the period with maximum points
        periods = {
            'இளம் வயது': young_total,
            'நடு வயது': middle_total,
            'முது வயது': old_total
        }
        best_period = max(periods.items(), key=lambda x: x[1])
        
        # Method 2: Rasi-based age periods (using the actual Rasi mapping)
        # For Rasi-based, we need to map the actual Rasis to house indices
        rasi_young_total = 0
        rasi_middle_total = 0
        rasi_old_total = 0
        
        for i, value in enumerate(sarva_values):
            # Calculate which Rasi this house corresponds to
            rasi_index = (ascendant_rasi + i - 1) % 12
            rasi_num = rasi_index + 1  # Convert to 1-based Rasi number
            
            if rasi_num in self.rasi_age_periods['young']:
                rasi_young_total += value
            elif rasi_num in self.rasi_age_periods['middle']:
                rasi_middle_total += value
            elif rasi_num in self.rasi_age_periods['old']:
                rasi_old_total += value
        
        rasi_periods = {
            'இளம் வயது': rasi_young_total,
            'நடு வயது': rasi_middle_total,
            'முது வயது': rasi_old_total
        }
        rasi_best_period = max(rasi_periods.items(), key=lambda x: x[1])
        
        return {
            'house_based': {
                'young': young_total,
                'middle': middle_total,
                'old': old_total,
                'best_period': best_period[0],
                'interpretation': f"இந்த ஜாதகத்தில் {best_period[0]} ஜாதகன் அதிக சந்தோசத்தை அனுபவிப்பார்"
            },
            'rasi_based': {
                'young': rasi_young_total,
                'middle': rasi_middle_total,
                'old': rasi_old_total,
                'best_period': rasi_best_period[0],
                'interpretation': f"இந்த ஜாதகத்தில் {rasi_best_period[0]} ஜாதகன் அதிக சந்தோசத்தை அனுபவிப்பார்"
            }
        }
    
    def calculate_lucky_directions(self, sarva_values: List[int], ascendant_rasi: int) -> Dict:
        """Calculate lucky directions based on Sarvashtakavarga"""
        direction_totals = {}
        
        # sarva_values is already mapped based on Ascendant:
        # Convert house numbers to indices (house - 1)
        for direction, houses in self.direction_houses.items():
            indices = [house - 1 for house in houses]  # Convert to 0-based indices
            total = sum(sarva_values[i] for i in indices)
            direction_totals[direction] = total
        
        # Find the luckiest direction
        luckiest_direction = max(direction_totals.items(), key=lambda x: x[1])
        
        # Tamil direction names
        direction_names = {
            'east': 'கிழக்கு',
            'south': 'தெற்கு',
            'west': 'மேற்கு',
            'north': 'வடக்கு'
        }
        
        return {
            'directions': {
                'கிழக்கு': direction_totals['east'],
                'தெற்கு': direction_totals['south'],
                'மேற்கு': direction_totals['west'],
                'வடக்கு': direction_totals['north']
            },
            'luckiest': {
                'direction': direction_names[luckiest_direction[0]],
                'points': luckiest_direction[1],
                'interpretation': f"இந்த ஜாதகருக்கு {direction_names[luckiest_direction[0]]} திசை அதிர்ஷ்டமானதாகும்"
            }
        }
    
    def calculate_relationship_dynamics(self, sarva_values: List[int], ascendant_rasi: int) -> Dict:
        """Calculate relationship dynamics and family relationships"""
        lagna_value = sarva_values[0]  # House 1
        seventh_value = sarva_values[6]  # House 7
        fifth_value = sarva_values[4]   # House 5
        fourth_value = sarva_values[3]  # House 4
        sixth_value = sarva_values[5]   # House 6
        eleventh_value = sarva_values[10]  # House 11
        twelfth_value = sarva_values[11]   # House 12
        tenth_value = sarva_values[9]      # House 10
        second_value = sarva_values[1]     # House 2
        
        relationships = []
        
        # Spouse relationship
        if lagna_value < seventh_value:
            relationships.append("லக்னதில் உள்ள பரல்களைவிட ஏழாம் வீட்டில் உள்ள பரல்கள் அதிகமாக இருப்பதால் மனைவிக்கு(வாழ்க்கைதுணைவர்) ஜாதகர் அடங்கி நடப்பார்.")
        else:
            relationships.append("லக்னத்தில் உள்ள பரல்களைவிட ஏழாம் வீட்டில் உள்ள பரல்கள் குறைவாக இருப்பதால் ஜாதகர் மனைவிக்கு(வாழ்க்கைதுணைவர்) அடங்கி நடக்கமாட்டார்.")
        
        # Spouse dominance
        if fifth_value > seventh_value:
            relationships.append("ஐந்தாம் வீட்டில் உள்ள பரல்களைவிட ஏழாம் வீட்டில் உள்ள பரல்கள் குறைவாக இருப்பதால் மனைவி(வாழ்க்கைதுணைவர்) ஜாதகருக்கு அடங்கி நடப்பார்.")
        else:
            relationships.append("ஐந்தாம் வீட்டில் உள்ள பரல்களைவிட ஏழாம் வீட்டில் உள்ள பரல்கள் அதிகமாக இருப்பதால் மனைவி(வாழ்க்கைதுணைவர்) ஜாதகருக்கு அடங்கி நடக்கமாட்டார்.")
        
        # Family support
        if fourth_value > sixth_value:
            relationships.append("நாலாம் வீட்டில் உள்ள பரல்களை விட ஆறாம் வீட்டில் உள்ள பரல்கள் குறைவாக இருப்பதால் உறவினர்களின் உதவி அதிகம் கிடைக்கும்.")
        else:
            relationships.append("நாலாம் வீட்டில் உள்ள பரல்களை விட ஆறாம் வீட்டில் உள்ள பரல்கள் அதிகமாக இருப்பதால் உறவினர்களின் உதவி குறைவாக கிடைக்கும்.")
        
        # Income vs expenses
        if eleventh_value > twelfth_value:
            relationships.append("பதினோராம் வீட்டில் உள்ள பரல்கள், பன்னிரெண்டாம் வீட்டின் பரல்களை விட அதிகமாக இருப்பதால் வரவு அதிகம் செலவு குறைவு.")
        else:
            relationships.append("பதினோராம் வீட்டில் உள்ள பரல்கள், பன்னிரெண்டாம் வீட்டின் பரல்களை விட குறைவாக இருப்பதால் செலவு அதிகம் வரவு குறைவு.")
        
        # Work and income
        if eleventh_value > tenth_value:
            relationships.append("பதினோராம் வீட்டில் உள்ள பரல்கள், பத்தாம் வீட்டின் பரல்களை விட அதிகமாக இருப்பதால் உழைபுக்கேற்ப ஊதியம் கிடைக்கும்.")
        else:
            relationships.append("பதினோராம் வீட்டில் உள்ள பரல்கள், பத்தாம் வீட்டின் பரல்களை விட குறைவாக இருப்பதால் உழைபுக்கேற்ப ஊதியம் கிடைக்காது.")
        
        # Ancestral property
        if second_value > 25 and fourth_value > 25:
            relationships.append("இரண்டாம் வீட்டிலும், நாலாம் வீட்டிலும் பரல்கள் அதிகமாக இருப்பதால் பூர்வீக சொத்து கிடைக்க / அனுபவிக்க வாய்ப்பு உள்ளது.")
        else:
            relationships.append("இரண்டாம் வீட்டிலும், நாலாம் வீட்டிலும் பரல்கள் குறைவாக இருப்பதால் பூர்வீக சொத்து கிடைக்க / அனுபவிக்க வாய்ப்பு குறைவு.")
        
        return {
            'relationships': relationships,
            'values': {
                'lagna': lagna_value,
                'seventh': seventh_value,
                'fifth': fifth_value,
                'fourth': fourth_value,
                'sixth': sixth_value,
                'eleventh': eleventh_value,
                'twelfth': twelfth_value,
                'tenth': tenth_value,
                'second': second_value
            }
        }
    
    def generate_comprehensive_tamil_interpretation(self, sarva_values: List[int], ascendant_rasi: int) -> Dict:
        """Generate comprehensive Tamil Ashtakavarga interpretation"""
        return {
            'longevity': self.calculate_longevity_analysis(sarva_values, ascendant_rasi),
            'agam_puram': self.calculate_agam_puram(sarva_values, ascendant_rasi),
            'srisuram': self.calculate_srisuram(sarva_values, ascendant_rasi),
            'asrisuram': self.calculate_asrisuram(sarva_values, ascendant_rasi),
            'beneficial_rasis': self.find_beneficial_rasis(sarva_values, ascendant_rasi),
            'age_periods': self.calculate_age_periods(sarva_values, ascendant_rasi),
            'lucky_directions': self.calculate_lucky_directions(sarva_values, ascendant_rasi),
            'relationships': self.calculate_relationship_dynamics(sarva_values, ascendant_rasi)
        }

def main():
    """Test the Tamil interpretation engine"""
    # Test with sample data
    sarva_values = [32, 36, 34, 30, 28, 16, 24, 28, 33, 28, 24, 24]  # Sample values
    ascendant_rasi = 11  # Kumbha
    
    interpreter = TamilAshtakavargaInterpreter()
    interpretation = interpreter.generate_comprehensive_tamil_interpretation(sarva_values, ascendant_rasi)
    
    print("Tamil Ashtakavarga Interpretation:")
    print("=" * 50)
    print(f"Longevity: {interpretation['longevity']['interpretation']}")
    print(f"Agam vs Puram: {interpretation['agam_puram']['interpretation']}")
    print(f"Srisuram: {interpretation['srisuram']['interpretation']}")
    print(f"Asrisuram: {interpretation['asrisuram']['interpretation']}")

if __name__ == "__main__":
    main()
