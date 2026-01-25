"""
Populate Supabase Knowledge Base with Vedic Astrology Content
Run this script to populate the vector database with knowledge
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agent_app.rag.supabase_rag import SupabaseRAGSystem


# House Significations (12 houses)
HOUSE_SIGNIFICATIONS = [
    {
        "house": 1,
        "name": "Lagna / Ascendant",
        "content": """House 1 (Lagna) represents the self, physical body, personality, appearance, and overall vitality. 
        It is the most important house as it determines the entire chart. High SAV points (28+) indicate strong 
        personality, good health, and fame. Low points suggest health issues and weak constitution. Planets in Lagna 
        significantly influence the native's character and life path.""",
        "category": "house"
    },
    {
        "house": 2,
        "name": "Dhana / Wealth",
        "content": """House 2 represents wealth, family, speech, food, and accumulated resources. High SAV points 
        indicate financial stability and family harmony. Low points suggest financial difficulties and speech problems. 
        This house also governs the face, eyes, and right eye specifically. Strong 2nd house brings prosperity and 
        family support.""",
        "category": "house"
    },
    {
        "house": 3,
        "name": "Sahaja / Siblings",
        "content": """House 3 represents siblings, courage, communication, short journeys, and writing. High SAV points 
        indicate good relationships with siblings, courage, and communication skills. Low points suggest conflicts with 
        siblings and lack of courage. This house also governs the arms, shoulders, and ears. Strong 3rd house brings 
        success through communication and short travels.""",
        "category": "house"
    },
    {
        "house": 4,
        "name": "Sukha / Home",
        "content": """House 4 represents mother, home, property, education, vehicles, and happiness. High SAV points 
        indicate property gains, good relationship with mother, and domestic happiness. Low points suggest property 
        losses and domestic troubles. This house also governs the chest, heart, and lungs. Strong 4th house brings 
        property, vehicles, and emotional stability.""",
        "category": "house"
    },
    {
        "house": 5,
        "name": "Putra / Children",
        "content": """House 5 represents children, education, intelligence, creativity, and speculation. High SAV points 
        indicate good children, educational success, and creative abilities. Low points suggest difficulties with 
        children and education. This house also governs the stomach and intelligence. Strong 5th house brings progeny, 
        wisdom, and success in education.""",
        "category": "house"
    },
    {
        "house": 6,
        "name": "Ripu / Enemies",
        "content": """House 6 represents enemies, diseases, debts, service, and obstacles. Interestingly, low SAV points 
        in 6th house are actually beneficial as it weakens enemies and diseases. High points can indicate strong enemies 
        and health issues. This house also governs the intestines and lower abdomen. Strong 6th house (low points) brings 
        victory over enemies and good health.""",
        "category": "house"
    },
    {
        "house": 7,
        "name": "Kalatra / Spouse",
        "content": """House 7 represents spouse, marriage, partnerships, and business. High SAV points indicate delayed 
        but stable marriage. Low points suggest early marriage or marital discord. This house also governs the genitals 
        and lower back. Strong 7th house brings harmonious partnerships and successful marriage. Zero points in 7th 
        house or 7th lord indicates denial of marriage.""",
        "category": "house"
    },
    {
        "house": 8,
        "name": "Ayush / Longevity",
        "content": """House 8 represents longevity, sudden events, transformations, and occult knowledge. Like 6th house, 
        low SAV points are beneficial here as they reduce obstacles to longevity. High points can indicate sudden 
        changes and transformations. This house also governs the anus and reproductive organs. Strong 8th house (low 
        points) brings longevity and protection from sudden events.""",
        "category": "house"
    },
    {
        "house": 9,
        "name": "Bhagya / Fortune",
        "content": """House 9 represents fortune, father, higher education, spirituality, and long journeys. High SAV 
        points indicate good fortune, spiritual growth, and support from father. Low points suggest lack of fortune and 
        spiritual obstacles. This house also governs the thighs and hips. Strong 9th house brings fortune, wisdom, and 
        spiritual progress.""",
        "category": "house"
    },
    {
        "house": 10,
        "name": "Karma / Career",
        "content": """House 10 represents career, profession, reputation, authority, and status in society. High SAV 
        points indicate successful career and high status. Low points suggest career difficulties and lack of recognition. 
        This house also governs the knees and back. Strong 10th house brings professional success, authority, and fame.""",
        "category": "house"
    },
    {
        "house": 11,
        "name": "Labha / Gains",
        "content": """House 11 represents gains, income, friends, elder siblings, and fulfillment of desires. High SAV 
        points indicate financial gains, good friendships, and fulfillment of desires. Low points suggest financial 
        losses and lack of support from friends. This house also governs the legs and ankles. Strong 11th house brings 
        wealth, gains, and supportive friendships.""",
        "category": "house"
    },
    {
        "house": 12,
        "name": "Vyaya / Expenses",
        "content": """House 12 represents expenses, losses, foreign lands, spirituality, and liberation. High SAV points 
        can indicate high expenses and losses. Low points are beneficial here as they reduce expenses. This house also 
        governs the feet and left eye. Strong 12th house (low points) brings reduced expenses and spiritual progress.""",
        "category": "house"
    }
]

# Dasha Interpretations
DASHA_INTERPRETATIONS = [
    {
        "planet": "Sun",
        "content": """Sun Dasha (6 years) brings authority, recognition, and leadership. The native gains respect, 
        government support, and success in career. However, Sun can cause health issues related to heart, eyes, and 
        bones. Father's health may be affected. Remedies include wearing ruby, chanting Surya mantras, and offering water 
        to Sun.""",
        "category": "dasha"
    },
    {
        "planet": "Moon",
        "content": """Moon Dasha (10 years) brings emotional stability, mother's blessings, and mental peace. The native 
        gains popularity, travels, and success in water-related professions. However, Moon can cause mental stress, 
        emotional instability, and water-related issues. Remedies include wearing pearl, chanting Chandra mantras, and 
        offering milk to Shiva.""",
        "category": "dasha"
    },
    {
        "planet": "Mars",
        "content": """Mars Dasha (7 years) brings courage, energy, and success in competitive fields. The native gains 
        property, vehicles, and success through courage. However, Mars can cause accidents, blood-related issues, and 
        conflicts. Remedies include wearing red coral, chanting Mangal mantras, and performing Hanuman puja.""",
        "category": "dasha"
    },
    {
        "planet": "Mercury",
        "content": """Mercury Dasha (17 years) brings intelligence, communication skills, and success in business and 
        education. The native gains through writing, trading, and intellectual pursuits. However, Mercury can cause 
        speech problems and nervous disorders. Remedies include wearing emerald, chanting Budh mantras, and performing 
        Vishnu puja.""",
        "category": "dasha"
    },
    {
        "planet": "Jupiter",
        "content": """Jupiter Dasha (16 years) brings wisdom, spirituality, and prosperity. The native gains through 
        knowledge, teaching, and spiritual pursuits. This is generally a very beneficial period. However, Jupiter can 
        cause issues related to liver and fat accumulation. Remedies include wearing yellow sapphire, chanting Guru 
        mantras, and performing Vishnu puja.""",
        "category": "dasha"
    },
    {
        "planet": "Venus",
        "content": """Venus Dasha (20 years) brings luxury, relationships, and artistic success. The native gains through 
        marriage, partnerships, and creative pursuits. This is generally a very beneficial period. However, Venus can 
        cause issues related to reproductive organs and urinary system. Remedies include wearing diamond or white sapphire, 
        chanting Shukra mantras, and performing Lakshmi puja.""",
        "category": "dasha"
    },
    {
        "planet": "Saturn",
        "content": """Saturn Dasha (19 years) brings discipline, hard work, and delayed but lasting results. The native 
        gains through perseverance and service. However, Saturn can cause delays, obstacles, and health issues related 
        to bones and joints. Remedies include wearing blue sapphire, chanting Shani mantras, and performing Shani puja.""",
        "category": "dasha"
    },
    {
        "planet": "Rahu",
        "content": """Rahu Dasha (18 years) brings sudden changes, material gains, and foreign connections. The native gains 
        through unconventional means and technology. However, Rahu can cause confusion, addictions, and mental stress. 
        Remedies include wearing gomedh, chanting Rahu mantras, and performing Durga puja.""",
        "category": "dasha"
    },
    {
        "planet": "Ketu",
        "content": """Ketu Dasha (7 years) brings spirituality, detachment, and liberation. The native gains through 
        spiritual pursuits and research. However, Ketu can cause sudden losses, accidents, and health issues. Remedies 
        include wearing cat's eye, chanting Ketu mantras, and performing Ganesha puja.""",
        "category": "dasha"
    }
]

# Gochara/Transit Interpretations
GOCHARA_INTERPRETATIONS = [
    {
        "content": """Planetary transits through houses activate those houses and their significations. When a planet 
        transits a house with high SAV points (30+), it produces benefic results. When transiting a house with low SAV 
        points (<22), it produces malefic results. Slow-moving planets (Saturn, Jupiter, Rahu, Ketu) have longer-lasting 
        effects.""",
        "category": "gochara"
    },
    {
        "content": """Saturn's transit through 7th, 8th, and 9th houses from Moon is called Sade Sati (7.5 years). This 
        period brings challenges, delays, and obstacles. However, if the transited houses have high SAV points (>30), the 
        negative effects are mitigated. Remedies include Shani puja, wearing blue sapphire, and charity.""",
        "category": "gochara"
    },
    {
        "content": """Jupiter's transit through beneficial houses (5th, 7th, 9th, 11th) brings prosperity, wisdom, and 
        spiritual growth. Jupiter's transit through 1st house brings overall prosperity. However, Jupiter's transit 
        through 6th, 8th, or 12th houses can bring challenges. Remedies include Guru puja and wearing yellow sapphire.""",
        "category": "gochara"
    },
    {
        "content": """Mars transit through 1st, 4th, 7th, 8th, or 12th houses can cause Mangal Dosha effects including 
        accidents, conflicts, and health issues. However, if these houses have high SAV points, the negative effects are 
        reduced. Remedies include Mangal puja and wearing red coral.""",
        "category": "gochara"
    }
]

# BAV/SAV Rules
BAV_SAV_RULES = [
    {
        "content": """SAV (Sarvashtakavarga) points indicate house strength. Houses with 28+ points are considered 
        strong and produce benefic results. Houses with 30+ points are very strong. Houses with less than 22 points are 
        weak and produce malefic results. The total SAV points across all 12 houses is always 337.""",
        "category": "bav_sav"
    },
    {
        "content": """BAV (Bhinnashtakavarga) shows individual planetary contributions to each house. Each planet's BAV 
        has a fixed total: Sun (48), Moon (49), Mars (39), Mercury (54), Jupiter (56), Venus (52), Saturn (39), 
        Ascendant (49). High BAV points in a house indicate strong planetary support for that house's significations.""",
        "category": "bav_sav"
    },
    {
        "content": """For marriage analysis, check 7th house SAV points and Venus BAV. Low points (0-3) indicate early 
        marriage. High points (6-8) indicate delayed marriage. Zero points in 7th house or 7th lord indicates denial of 
        marriage. Mars in 7th house or aspecting 7th house can cause Mangal Dosha.""",
        "category": "bav_sav"
    },
    {
        "content": """For health analysis, check 1st house (Lagna) and 6th house SAV points. High points in 1st house 
        indicate good health. Low points in 6th house are beneficial (weakens enemies and diseases). High points in 6th 
        house can indicate health issues.""",
        "category": "bav_sav"
    },
    {
        "content": """For career analysis, check 10th house SAV points. High points (30+) indicate successful career, 
        authority, and recognition. Low points indicate career difficulties. Also check 10th lord placement and Dasha 
        period.""",
        "category": "bav_sav"
    }
]

# Remedies
REMEDIES = [
    {
        "content": """Gemstones (Ratnas) are powerful remedies for planetary afflictions. Sun: Ruby, Moon: Pearl, Mars: 
        Red Coral, Mercury: Emerald, Jupiter: Yellow Sapphire, Venus: Diamond/White Sapphire, Saturn: Blue Sapphire, 
        Rahu: Gomedh, Ketu: Cat's Eye. Gemstones should be worn after proper consultation and on auspicious days.""",
        "category": "remedy"
    },
    {
        "content": """Mantras are spiritual remedies. Chanting planetary mantras daily can reduce negative effects and 
        enhance positive results. Sun: Om Suryaya Namah, Moon: Om Somaya Namah, Mars: Om Mangalaya Namah, Mercury: Om 
        Budhaya Namah, Jupiter: Om Gurave Namah, Venus: Om Shukraya Namah, Saturn: Om Shanaye Namah.""",
        "category": "remedy"
    },
    {
        "content": """Charity (Dana) is a powerful remedy. Donating items related to afflicted planets on their days 
        can reduce negative effects. Sun: Wheat, copper, Moon: Rice, silver, Mars: Red lentils, copper, Mercury: Green 
        gram, Jupiter: Yellow items, Venus: White items, Saturn: Black items, iron.""",
        "category": "remedy"
    },
    {
        "content": """Fasting on planetary days can reduce negative effects. Sun: Sunday, Moon: Monday, Mars: Tuesday, 
        Mercury: Wednesday, Jupiter: Thursday, Venus: Friday, Saturn: Saturday. Fasting should be done with devotion and 
        proper prayers.""",
        "category": "remedy"
    },
    {
        "content": """Perform remedies for a planet when it transits a house where it has 0 or 1 point to mitigate negative energy.""",
        "category": "remedy"
    }
]

# Advanced Ashtakavarga Rules
ADVANCED_RULES = [
    {
        "content": """A house with 28 points in Sarvashtakavarga is considered the baseline for a balanced and good life area. 
        This is the standard threshold for evaluating house strength.""",
        "category": "bav_sav",
        "metadata": {"min_points": 28, "threshold_type": "baseline"}
    },
    {
        "content": """Planets transiting through a house with less than 22 points yield negative results or significant challenges. 
        Such transits should be approached with caution and remedies may be necessary.""",
        "category": "gochara",
        "metadata": {"max_points": 22, "effect": "negative"}
    },
    {
        "content": """Having more than 30 points in a house is highly beneficial and yields auspicious results. Houses with 30+ 
        points are considered very strong and produce excellent outcomes.""",
        "category": "bav_sav",
        "metadata": {"min_points": 31, "effect": "highly_beneficial"}
    },
    {
        "content": """When the Karaka (significator) and the Lord of the Bhava transit a house with high points simultaneously, 
        excellent results are produced. This combination creates powerful positive effects.""",
        "category": "gochara",
        "metadata": {"min_points": 28, "combination": "karaka_and_lord"}
    },
    {
        "content": """Even if Dasha or Bhukti planets are naturally malefic, they will yield auspicious results if they are in 
        a house with high points (28+). High SAV points can transform malefic periods into beneficial ones.""",
        "category": "dasha",
        "metadata": {"min_points": 28, "effect": "transforms_malefic"}
    },
    {
        "content": """Slow-moving planets like Saturn, Jupiter, Rahu, and Ketu do not cause harm when transiting a house with 
        more than 30 points. High points provide protection even from slow-moving malefic planets.""",
        "category": "gochara",
        "metadata": {"min_points": 30, "planets": "slow_moving", "effect": "protection"}
    },
    {
        "content": """In Bhinnashtakavarga (individual planet charts), a house can receive a maximum of 8 points. This is the 
        technical limit for BAV calculations.""",
        "category": "bav_sav",
        "metadata": {"max_points": 8, "type": "bav_maximum"}
    },
    {
        "content": """If a planet has more than 4 points in its individual Bhinnashtakavarga chart for a house, its strength is 
        considered good. This indicates strong planetary support for that house.""",
        "category": "bav_sav",
        "metadata": {"min_points": 5, "strength": "good"}
    },
    {
        "content": """If a planet has less than 4 points in its individual chart for a house, its strength is considered low or 
        weak. This indicates weak planetary support.""",
        "category": "bav_sav",
        "metadata": {"max_points": 3, "strength": "weak"}
    },
    {
        "content": """If the Sun has 0 points and Mars transits that position, there is a high risk of accidents or health crises 
        for the father. This is a critical combination requiring immediate attention and remedies.""",
        "category": "gochara",
        "metadata": {"planet": "Sun", "trigger": "Mars", "risk": "high", "affected": "father"}
    },
    {
        "content": """High points in the Lagna (Ascendant) indicate a person who is famous, influential, and possesses leadership 
        qualities. Lagna with 30+ points creates a strong personality and public recognition.""",
        "category": "house",
        "house_number": 1,
        "metadata": {"min_points": 30, "qualities": ["fame", "influence", "leadership"]}
    },
    {
        "content": """If the Lagna has 54 points, the native will be extremely arrogant; however, this is a very rare occurrence. 
        This extreme score creates excessive pride and ego.""",
        "category": "house",
        "house_number": 1,
        "metadata": {"points": 54, "trait": "arrogance", "rarity": "very_rare"}
    },
    {
        "content": """High points in the Lagna combined with low points in the 6th house ensures a healthy body; otherwise, frequent 
        illness occur. This combination is ideal for health.""",
        "category": "house",
        "house_number": 1,
        "metadata": {"houses": [1, 6], "condition": "H1_high_H6_low", "effect": "good_health"}
    },
    {
        "content": """It is considered beneficial for the 6th and 8th houses to have low points as it reduces enemies and obstacles. 
        Low points in these houses weaken malefic influences.""",
        "category": "house",
        "house_number": 6,
        "metadata": {"houses": [6, 8], "effect": "reduces_enemies_obstacles"}
    },
    {
        "content": """If the house where Mars is placed has 0 points, the native will face blood-related issues or accidents. 
        This is a critical indicator requiring preventive measures.""",
        "category": "house",
        "metadata": {"planet": "Mars", "points": 0, "risks": ["blood_issues", "accidents"]}
    },
    {
        "content": """If Mars has 0 points, there is a high probability of accidents during travel. Caution is advised when 
        traveling during Mars-related periods.""",
        "category": "gochara",
        "metadata": {"planet": "Mars", "points": 0, "risk": "travel_accidents"}
    },
    {
        "content": """A house with more than 30 points prevents major suffering during Sade Sati (7.5 years of Saturn). High points 
        provide protection even during challenging Saturn transits.""",
        "category": "gochara",
        "metadata": {"min_points": 31, "planet": "Saturn", "period": "sade_sati", "effect": "protection"}
    },
    {
        "content": """Fewer points in the 7th house indicate early marriage, while high points indicate a delayed marriage. 
        The point count directly correlates with marriage timing.""",
        "category": "house",
        "house_number": 7,
        "metadata": {"effect": "marriage_timing", "low_points": "early", "high_points": "delayed"}
    },
    {
        "content": """If the 7th house, Venus, and Mars all have 0 points, marriage is unlikely to take place. This is a strong 
        indicator of denial of marriage.""",
        "category": "house",
        "house_number": 7,
        "metadata": {"points": 0, "planets": ["Venus", "Mars"], "effect": "marriage_denial"}
    },
    {
        "content": """If the 7th Lord has 0 points in its BAV, there will be frequent and intense quarrels in marriage. 
        This indicates marital discord and relationship challenges.""",
        "category": "house",
        "house_number": 7,
        "metadata": {"lord_points": 0, "effect": "marital_discord"}
    },
    {
        "content": """If the total points in the 11th house (Gains) are greater than the 10th house (Action), the native earns 
        more with less effort. This indicates effortless gains and prosperity.""",
        "category": "house",
        "house_number": 11,
        "metadata": {"houses": [10, 11], "condition": "H11 > H10", "effect": "effortless_gains"}
    },
    {
        "content": """If the 11th house points are higher than the 12th house (Expenses), financial stability and savings are 
        assured. This creates a positive financial flow.""",
        "category": "house",
        "house_number": 11,
        "metadata": {"houses": [11, 12], "condition": "H11 > H12", "effect": "financial_stability"}
    },
    {
        "content": """If the 12th house has significantly more points than the 11th house, the native may face persistent debt. 
        This indicates expenses exceeding gains.""",
        "category": "house",
        "house_number": 12,
        "metadata": {"houses": [11, 12], "condition": "H12 > H11", "effect": "debt"}
    },
    {
        "content": """If the sum of points in houses 1, 2, 4, 9, 10, and 11 exceeds 164, the native will be very wealthy. 
        These houses represent key wealth indicators.""",
        "category": "house",
        "metadata": {"houses": [1, 2, 4, 9, 10, 11], "min_sum": 165, "effect": "great_wealth"}
    },
    {
        "content": """If the sum of malefic houses (6, 8, 12) is greater than 76, expenses will consistently exceed income. 
        This creates financial challenges.""",
        "category": "house",
        "metadata": {"houses": [6, 8, 12], "max_sum": 76, "effect": "expenses_exceed_income"}
    },
    {
        "content": """If the 11th house contains 36 points or more, the person attains wealth with very little hard work. 
        This is an exceptional indicator of effortless prosperity.""",
        "category": "house",
        "house_number": 11,
        "metadata": {"min_points": 36, "effect": "effortless_wealth"}
    },
    {
        "content": """If the 10th house points exceed the 11th house points, the native is suited for business or high authority 
        roles. This indicates career-oriented success.""",
        "category": "house",
        "house_number": 10,
        "metadata": {"houses": [10, 11], "condition": "H10 > H11", "effect": "business_authority"}
    },
    {
        "content": """If the 10th house is strong (above 28) but the 11th is weak, the native has prestige but financial fluctuations. 
        This creates status without consistent income.""",
        "category": "house",
        "house_number": 10,
        "metadata": {"houses": [10, 11], "condition": "H10_strong_H11_weak", "effect": "prestige_without_stability"}
    },
    {
        "content": """The 5th house points should be less than the 10th house points to avoid hidden obstacles in professional growth. 
        This balance is important for career success.""",
        "category": "house",
        "house_number": 5,
        "metadata": {"houses": [5, 10], "condition": "H5 < H10", "effect": "career_growth"}
    },
    {
        "content": """A planet transiting a house with 30+ SAV points and 5+ BAV points triggers a major professional promotion. 
        This combination creates exceptional career opportunities.""",
        "category": "gochara",
        "metadata": {"min_sav": 30, "min_bav": 5, "effect": "major_promotion"}
    },
    {
        "content": """In matchmaking, if both partners have 30+ points in their Moon signs, married life will be exceptionally happy. 
        This is an excellent indicator for marital harmony.""",
        "category": "house",
        "metadata": {"planet": "Moon", "min_points": 30, "context": "matchmaking", "effect": "happy_marriage"}
    },
    {
        "content": """If both marriage partners have 25 or fewer points in their Moon signs, the marriage is likely to face severe 
        instability. This indicates relationship challenges.""",
        "category": "house",
        "metadata": {"planet": "Moon", "max_points": 25, "context": "matchmaking", "effect": "marital_instability"}
    },
    {
        "content": """If the 7th house has higher points than the 1st house, the spouse will be more dominant in the relationship. 
        This indicates spouse's influence.""",
        "category": "house",
        "house_number": 7,
        "metadata": {"houses": [1, 7], "condition": "H7 > H1", "effect": "spouse_dominance"}
    },
    {
        "content": """The cardinal direction of the sign with the highest SAV points is the most auspicious direction for success. 
        This can guide important decisions and activities.""",
        "category": "general",
        "metadata": {"logic": "direction_of_max_sav", "effect": "auspicious_direction"}
    },
    {
        "content": """If the 4th house has 30+ points and benefic influence, the native will own multiple luxury properties and vehicles. 
        This indicates material prosperity in property and transportation.""",
        "category": "house",
        "house_number": 4,
        "metadata": {"min_points": 30, "effect": "luxury_properties_vehicles"}
    },
    {
        "content": """Avoid starting journeys when the transiting Moon is in a sign with less than 25 points to ensure safety. 
        This timing consideration can prevent travel-related issues.""",
        "category": "gochara",
        "metadata": {"planet": "Moon", "max_points": 25, "context": "travel", "effect": "safety"}
    },
    {
        "content": """If the 8th house has below 20 points, any sudden windfall or inheritance will likely be lost quickly. 
        Low points in 8th house create instability in sudden gains.""",
        "category": "house",
        "house_number": 8,
        "metadata": {"max_points": 19, "effect": "unstable_inheritance"}
    },
    {
        "content": """High score in the Dharma Trikona (1, 5, 9) indicates strong support from family and a righteous nature. 
        These houses represent dharma and moral strength.""",
        "category": "house",
        "metadata": {"houses": [1, 5, 9], "trikona": "dharma", "effect": "family_support_righteousness"}
    },
    {
        "content": """High score in the Artha Trikona (2, 6, 10) indicates success through professional labor and service. 
        These houses represent material success through work.""",
        "category": "house",
        "metadata": {"houses": [2, 6, 10], "trikona": "artha", "effect": "professional_success"}
    },
    {
        "content": """High score in the Kama Trikona (3, 7, 11) indicates success through social networking and partnerships. 
        These houses represent desires and relationships.""",
        "category": "house",
        "metadata": {"houses": [3, 7, 11], "trikona": "kama", "effect": "social_networking_success"}
    },
    {
        "content": """A planet's results are activated only when moving through the specific 3.75-degree Kaksha where it contributed 
        a point. This technical detail is important for precise timing.""",
        "category": "bav_sav",
        "metadata": {"technical": "kaksha", "precision": "3.75_degrees"}
    },
    {
        "content": """Even an exalted planet in Mahadasha will fail if its BAV score in its current house is less than 3. 
        BAV points are crucial even for exalted planets.""",
        "category": "dasha",
        "metadata": {"max_points": 2, "condition": "exalted_planet", "effect": "failure_despite_exaltation"}
    },
    {
        "content": """If a planet is Vargottama and has 6+ points in its BAV, it produces extraordinary, king-like results. 
        This combination creates exceptional outcomes.""",
        "category": "bav_sav",
        "metadata": {"condition": "vargottama", "min_points": 6, "effect": "extraordinary_results"}
    },
    {
        "content": """If the 9th house has more points than any other house, the native is protected by divine luck. 
        This indicates exceptional fortune and divine protection.""",
        "category": "house",
        "house_number": 9,
        "metadata": {"condition": "max_points", "effect": "divine_luck"}
    },
    {
        "content": """If the 6th house (Competition) has more points than the 5th (Intelligence), the native succeeds through 
        persistence rather than intelligence. This indicates hard work over natural talent.""",
        "category": "house",
        "house_number": 6,
        "metadata": {"houses": [5, 6], "condition": "H6 > H5", "effect": "persistence_over_intelligence"}
    },
    {
        "content": """A 5th house with 30+ points indicates potential for specialized higher education or research. 
        This creates opportunities for advanced learning.""",
        "category": "house",
        "house_number": 5,
        "metadata": {"min_points": 30, "effect": "specialized_education"}
    },
    {
        "content": """If the 9th house has 28+ points, the native will have a smooth journey toward PhD or post-graduate studies. 
        This indicates success in higher education.""",
        "category": "house",
        "house_number": 9,
        "metadata": {"min_points": 28, "effect": "higher_education_success"}
    },
    {
        "content": """If the 9th house points are greater than the 12th house, the native is likely to receive scholarships for 
        study. This creates financial support for education.""",
        "category": "house",
        "house_number": 9,
        "metadata": {"houses": [9, 12], "condition": "H9 > H12", "effect": "scholarships"}
    },
    {
        "content": """In Jupiter's BAV, if the sign occupied by Jupiter has 5+ points, the native is blessed with successful children. 
        This indicates progeny success.""",
        "category": "house",
        "metadata": {"planet": "Jupiter", "min_points": 5, "effect": "successful_children"}
    },
    {
        "content": """If the 11th house points are greater than the 5th house, the native's children will be more successful than 
        the parent. This indicates generational progress.""",
        "category": "house",
        "house_number": 11,
        "metadata": {"houses": [5, 11], "condition": "H11 > H5", "effect": "children_more_successful"}
    },
    {
        "content": """If the 5th and 12th houses have 28+ points and exchange lords, education will be completed in a foreign land. 
        This indicates foreign education.""",
        "category": "house",
        "metadata": {"houses": [5, 12], "min_points": 28, "condition": "lord_exchange", "effect": "foreign_education"}
    },
    {
        "content": """If the 12th house has more points than the 1st house, permanent foreign settlement is indicated. 
        This indicates foreign residence.""",
        "category": "house",
        "house_number": 12,
        "metadata": {"houses": [1, 12], "condition": "H12 > H1", "effect": "foreign_settlement"}
    },
    {
        "content": """If the 10th house and 12th house combined exceed 60 points, the native travels abroad for work but returns. 
        This indicates temporary foreign work assignments.""",
        "category": "house",
        "metadata": {"houses": [10, 12], "min_sum": 61, "effect": "temporary_foreign_work"}
    },
    {
        "content": """If the 7th house has 30+ points and the 2nd house is strong, business partnerships will be lucrative. 
        This combination creates successful business relationships.""",
        "category": "house",
        "house_number": 7,
        "metadata": {"houses": [2, 7], "min_points": 30, "effect": "lucrative_partnerships"}
    },
    {
        "content": """Launch a business when the Moon transits a sign where it has 6 to 8 points in its own BAV chart. 
        This timing ensures business success.""",
        "category": "gochara",
        "metadata": {"planet": "Moon", "min_points": 6, "max_points": 8, "context": "business_launch"}
    },
    {
        "content": """A 2nd house with 31+ points suggests a career in teaching, lecturing, or public speaking. 
        This indicates communication-based professions.""",
        "category": "house",
        "house_number": 2,
        "metadata": {"min_points": 31, "effect": "teaching_speaking_career"}
    },
    {
        "content": """If the 10th house has more points than the 9th house, the native is famous for their hard work rather than 
        luck. This indicates earned success.""",
        "category": "house",
        "house_number": 10,
        "metadata": {"houses": [9, 10], "condition": "H10 > H9", "effect": "hard_work_fame"}
    },
    {
        "content": """If the 3rd house has 30+ points, the native will find massive success in social media or digital marketing. 
        This indicates modern communication-based success.""",
        "category": "house",
        "house_number": 3,
        "metadata": {"min_points": 30, "effect": "social_media_success"}
    },
    {
        "content": """If the 1, 4, 7, and 10 houses (Kendras) all have 30+ points, the native lives like a King. 
        This is an exceptional combination indicating royal-like status and success.""",
        "category": "house",
        "metadata": {"houses": [1, 4, 7, 10], "kendras": True, "min_points": 30, "effect": "royal_life"}
    }
]


def populate_knowledge_base():
    """Populate Supabase with all Vedic astrology knowledge"""
    
    print("Initializing RAG system...")
    rag_system = SupabaseRAGSystem()
    
    print("\nPopulating House Significations...")
    for house_data in HOUSE_SIGNIFICATIONS:
        try:
            rag_system.store_knowledge(
                content=house_data["content"],
                category=house_data["category"],
                house_number=house_data["house"],
                metadata={
                    "house_name": house_data["name"],
                    "house_number": house_data["house"]
                }
            )
            print(f"  ✓ Stored House {house_data['house']} ({house_data['name']})")
        except Exception as e:
            print(f"  ✗ Error storing House {house_data['house']}: {e}")
    
    print("\nPopulating Dasha Interpretations...")
    for dasha_data in DASHA_INTERPRETATIONS:
        try:
            rag_system.store_knowledge(
                content=dasha_data["content"],
                category=dasha_data["category"],
                planet=dasha_data["planet"],
                metadata={
                    "planet": dasha_data["planet"],
                    "type": "dasha"
                }
            )
            print(f"  ✓ Stored {dasha_data['planet']} Dasha")
        except Exception as e:
            print(f"  ✗ Error storing {dasha_data['planet']} Dasha: {e}")
    
    print("\nPopulating Gochara Interpretations...")
    for gochara_data in GOCHARA_INTERPRETATIONS:
        try:
            rag_system.store_knowledge(
                content=gochara_data["content"],
                category=gochara_data["category"],
                metadata={"type": "gochara"}
            )
            print(f"  ✓ Stored Gochara content")
        except Exception as e:
            print(f"  ✗ Error storing Gochara: {e}")
    
    print("\nPopulating BAV/SAV Rules...")
    for bav_sav_data in BAV_SAV_RULES:
        try:
            rag_system.store_knowledge(
                content=bav_sav_data["content"],
                category=bav_sav_data["category"],
                metadata={"type": "bav_sav"}
            )
            print(f"  ✓ Stored BAV/SAV rule")
        except Exception as e:
            print(f"  ✗ Error storing BAV/SAV: {e}")
    
    print("\nPopulating Remedies...")
    for remedy_data in REMEDIES:
        try:
            rag_system.store_knowledge(
                content=remedy_data["content"],
                category=remedy_data["category"],
                metadata={"type": "remedy"}
            )
            print(f"  ✓ Stored Remedy content")
        except Exception as e:
            print(f"  ✗ Error storing Remedy: {e}")
    
    print("\nPopulating Advanced Ashtakavarga Rules...")
    for rule_data in ADVANCED_RULES:
        try:
            metadata = rule_data.get("metadata", {})
            metadata["type"] = "advanced_rule"
            metadata["logic"] = rule_data.get("logic", "")
            
            rag_system.store_knowledge(
                content=rule_data["content"],
                category=rule_data["category"],
                house_number=rule_data.get("house_number"),
                planet=rule_data.get("planet"),
                metadata=metadata
            )
            house_info = f" (House {rule_data['house_number']})" if rule_data.get("house_number") else ""
            planet_info = f" ({rule_data['planet']})" if rule_data.get("planet") else ""
            print(f"  ✓ Stored Advanced Rule{house_info}{planet_info}")
        except Exception as e:
            print(f"  ✗ Error storing Advanced Rule: {e}")
    
    print("\n✅ Knowledge base population completed!")


if __name__ == "__main__":
    populate_knowledge_base()

