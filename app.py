#!/usr/bin/env python3
"""
Flask Web Application for Tamil Ashtakavarga Calculator
Beautiful UI with tabs for each planet and user input form
"""

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import sys
import os

# Add current directory to path to import our calculator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ashtavargam_calculator import TamilAshtakavargaCalculator

app = Flask(__name__)

# Tamil planet names and emojis for display
PLANET_INFO = {
    'SUN': {'tamil': 'சூர்யன்', 'emoji': '☀️', 'color': '#FF6B35'},
    'MOON': {'tamil': 'சந்திரன்', 'emoji': '🌙', 'color': '#4ECDC4'},
    'MARS': {'tamil': 'செவ்வாய்', 'emoji': '♂️', 'color': '#FF4757'},
    'MERCURY': {'tamil': 'புதன்', 'emoji': '☿️', 'color': '#2ED573'},
    'JUPITER': {'tamil': 'குரு', 'emoji': '♃', 'color': '#FFA502'},
    'VENUS': {'tamil': 'சுக்ரன்', 'emoji': '♀️', 'color': '#FF6348'},
    'SATURN': {'tamil': 'சனி', 'emoji': '♄', 'color': '#747D8C'},
    'ASCENDANT': {'tamil': 'லக்கினம்', 'emoji': '🕐', 'color': '#5352ED'}
}

# Tamil Rasi names
TAMIL_RASIS = [
    "மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்", "சிம்மம்", "கன்னி",
    "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்", "கும்பம்", "மீனம்"
]

@app.route('/')
def index():
    """Main page with birth data input form"""
    return render_template('index.html', 
                         planet_info=PLANET_INFO,
                         tamil_rasis=TAMIL_RASIS)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate Ashtakavarga based on user input"""
    try:
        # Get form data
        name = request.form.get('name', 'User')
        dob = request.form.get('dob')  # Format: YYYY-MM-DD
        tob = request.form.get('tob')  # Format: HH:MM
        place = request.form.get('place', 'Chennai')
        latitude = float(request.form.get('latitude', 13.0827))
        longitude = float(request.form.get('longitude', 80.2707))
        timezone = float(request.form.get('timezone', 5.5))
        
        # Convert date format from YYYY-MM-DD to DD-MM-YYYY
        dob_parts = dob.split('-')
        dob_formatted = f"{dob_parts[2]}-{dob_parts[1]}-{dob_parts[0]}"
        
        # Create birth data dictionary
        birth_data = {
            'name': name,
            'dob': dob_formatted,
            'tob': tob,
            'lat': latitude,
            'lon': longitude,
            'place': place,
            'tz_offset': timezone
        }
        
        # Create calculator instance with user data
        calculator = TamilAshtakavargaCalculator(birth_data)
        
        # Calculate planetary positions
        calculator.calculate_planetary_positions()
        
        # Calculate Ashtakavarga
        calculator.calculate_all_ashtakavarga_tamil()
        
        # Prepare data for display
        result_data = {
            'birth_info': {
                'name': name,
                'dob': dob,
                'tob': tob,
                'place': place,
                'coordinates': f"{latitude}, {longitude}"
            },
            'planetary_positions': calculator.planet_positions,
            'native_chart': calculator.get_native_chart(),
            'ashtakavarga_charts': {},
            'sarvashtakavarga': calculator.sarvashtakavarga,
            'totals': {}
        }
        
        # Process each planet's chart
        for planet in PLANET_INFO:
            if planet in calculator.binnashtakavarga:
                chart = calculator.binnashtakavarga[planet]
                contributions = calculator.contributions[planet]
                
                # Create chart data with visual indicators
                chart_data = []
                for i, value in enumerate(chart):
                    # Determine color based on value
                    if value >= 6:
                        color = '#FF4757'  # Red for high values
                        strength = 'High'
                    elif value >= 4:
                        color = '#FFA502'  # Orange for medium values
                        strength = 'Medium'
                    else:
                        color = '#2ED573'  # Green for low values
                        strength = 'Low'
                    
                    chart_data.append({
                        'house': i + 1,
                        'rasi': TAMIL_RASIS[i],
                        'value': value,
                        'color': color,
                        'strength': strength,
                        'contributors': contributions[i + 1] if i + 1 in contributions else []
                    })
                
                result_data['ashtakavarga_charts'][planet] = {
                    'chart': chart_data,
                    'total': sum(chart),
                    'contributions': contributions,
                    'planet_matrix': calculator.planet_matrices.get(planet, {})
                }
                
                result_data['totals'][planet] = sum(chart)
        
        # Calculate Sarvashtakavarga analysis
        sarva_analysis = []
        for i, value in enumerate(calculator.sarvashtakavarga):
            if value >= 30:
                color = '#FF4757'
                strength = 'Very Strong'
            elif value >= 25:
                color = '#FFA502'
                strength = 'Strong'
            elif value >= 20:
                color = '#2ED573'
                strength = 'Moderate'
            else:
                color = '#747D8C'
                strength = 'Weak'
            
            sarva_analysis.append({
                'house': i + 1,
                'rasi': TAMIL_RASIS[i],
                'value': value,
                'color': color,
                'strength': strength
            })
        
        result_data['sarva_analysis'] = sarva_analysis
        result_data['sarva_total'] = sum(calculator.sarvashtakavarga)
        
        return jsonify({
            'success': True,
            'data': result_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/results')
def results():
    """Results page with tabs for each planet"""
    return render_template('results.html', 
                         planet_info=PLANET_INFO,
                         tamil_rasis=TAMIL_RASIS)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
