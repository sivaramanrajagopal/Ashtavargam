#!/usr/bin/env python3
"""
Clean Flask App - Version 2
Simple, reliable Ashtakavarga web application
"""

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ashtakavarga_calculator_final import AshtakavargaCalculator
from interpretation_engine import AshtakavargaInterpreter
from tamil_interpretation_engine import TamilAshtakavargaInterpreter

app = Flask(__name__)

# Planet info for display
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

# Tamil Rasi abbreviations
TAMIL_RASI_ABBR = [
    "மே", "ரி", "மி", "க", "சி", "க", "து", "வி", "த", "ம", "கு", "மீ"
]

@app.route('/')
def index():
    """Main page with birth data input form"""
    return render_template('index_v2.html', 
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
        
        # Create calculator instance
        calculator = AshtakavargaCalculator(birth_data)
        
        # Calculate positions and charts
        positions = calculator.calculate_positions()
        charts = calculator.calculate_all_charts()
        
        # Get display data
        display_data = calculator.get_display_data()
        
        # Create interpreter and generate analysis
        interpreter = AshtakavargaInterpreter()
        ascendant_rasi = display_data['planetary_positions'].get('ASCENDANT', 1)
        interpretation = interpreter.generate_comprehensive_analysis(
            display_data['sarvashtakavarga'],
            display_data['totals'],
            display_data['sarva_total'],
            ascendant_rasi
        )
        
        # Create Tamil interpreter and generate Tamil analysis
        tamil_interpreter = TamilAshtakavargaInterpreter()
        tamil_interpretation = tamil_interpreter.generate_comprehensive_tamil_interpretation(
            display_data['sarvashtakavarga'],
            ascendant_rasi
        )
        
        # Prepare result data
        result_data = {
            'birth_info': {
                'name': name,
                'dob': dob,
                'tob': tob,
                'place': place,
                'coordinates': f"{latitude}, {longitude}"
            },
            'planetary_positions': display_data['planetary_positions'],
            'native_chart': display_data['native_chart'],
            'ashtakavarga_charts': {},
            'sarvashtakavarga': display_data['sarvashtakavarga'],
            'totals': display_data['totals'],
            'sarva_total': display_data['sarva_total'],
            'interpretation': interpretation,
            'tamil_interpretation': tamil_interpretation
        }
        
        # Process each planet's chart for display
        for planet in PLANET_INFO:
            if planet in display_data['ashtakavarga_charts']:
                chart = display_data['ashtakavarga_charts'][planet]
                
                # Create chart data with house information
                chart_data = []
                for i, value in enumerate(chart):
                    chart_data.append({
                        'house': i + 1,
                        'rasi': TAMIL_RASIS[i],
                        'value': value
                    })
                
                result_data['ashtakavarga_charts'][planet] = {
                    'chart': chart_data,
                    'total': sum(chart)
                }
        
        return jsonify({
            'success': True,
            'data': result_data
        })
        
    except Exception as e:
        print(f"Error in calculate: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/results')
def results():
    """Results page with tabs for each planet"""
    return render_template('results_v2.html', 
                         planet_info=PLANET_INFO,
                         tamil_rasis=TAMIL_RASIS,
                         tamil_rasi_abbr=TAMIL_RASI_ABBR)

@app.route('/dashboard')
def dashboard():
    """Dashboard page with comprehensive analysis"""
    return render_template('dashboard_v3.html')

@app.route('/tamil-interpretations')
def tamil_interpretations():
    """Tamil interpretations page"""
    return render_template('tamil_interpretations.html')

@app.route('/matrix-view')
def matrix_view():
    """Matrix view page with all 8 Bhinnashtakavarga matrices"""
    return render_template('matrix_view_simple.html')

if __name__ == '__main__':
    print("🏛️ Tamil Ashtakavarga Calculator - Flask Web Application V2")
    print("=" * 60)
    print("🌐 Starting web server...")
    print("📍 Application will be available at: http://localhost:5002")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5002)
