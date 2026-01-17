#!/usr/bin/env python3
"""
Simplified Ashtakavarga Calculator - Basic and Optimized
"""

from flask import Flask, render_template, request, jsonify, session
import json
from ashtakavarga_calculator_final import AshtakavargaCalculator
from interpretation_engine import AshtakavargaInterpreter
from tamil_interpretation_engine import TamilAshtakavargaInterpreter

app = Flask(__name__)
app.secret_key = 'ashtakavarga_secret_key'

# Planet information
PLANET_INFO = {
    'SUN': {'name': 'Sun', 'tamil': 'சூர்யன்'},
    'MOON': {'name': 'Moon', 'tamil': 'சந்திரன்'},
    'MARS': {'name': 'Mars', 'tamil': 'செவ்வாய்'},
    'MERCURY': {'name': 'Mercury', 'tamil': 'புதன்'},
    'JUPITER': {'name': 'Jupiter', 'tamil': 'குரு'},
    'VENUS': {'name': 'Venus', 'tamil': 'சுக்ரன்'},
    'SATURN': {'name': 'Saturn', 'tamil': 'சனி'},
    'ASCENDANT': {'name': 'Ascendant', 'tamil': 'லக்கினம்'}
}

TAMIL_RASIS = [
    "மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்", "சிம்மம்", "கன்னி",
    "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்", "கும்பம்", "மீனம்"
]

TAMIL_RASI_ABBR = [
    "மே", "ரி", "மி", "க", "சி", "க", "து", "வி", "த", "ம", "கு", "மீ"
]

@app.route('/')
def index():
    """Home page with birth data input form"""
    return render_template('index_simple.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate Ashtakavarga charts"""
    try:
        # Get form data
        name = request.form.get('name', 'Unknown')
        dob = request.form.get('dob')
        tob = request.form.get('tob')
        place = request.form.get('place', 'Unknown')
        latitude = float(request.form.get('latitude', 0))
        longitude = float(request.form.get('longitude', 0))
        tz_offset = float(request.form.get('tz_offset', 0))

        # Prepare birth data
        birth_data = {
            'name': name,
            'dob': dob,
            'tob': tob,
            'place': place,
            'latitude': latitude,
            'longitude': longitude,
            'tz_offset': tz_offset
        }

        # Calculate Ashtakavarga
        calculator = AshtakavargaCalculator(birth_data)
        calculator.calculate_all_charts()
        
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
            'ashtakavarga_charts': display_data['ashtakavarga_charts'],
            'sarvashtakavarga': display_data['sarvashtakavarga'],
            'totals': display_data['totals'],
            'sarva_total': display_data['sarva_total'],
            'interpretation': interpretation,
            'tamil_interpretation': tamil_interpretation
        }
        
        # Store in session
        session['ashtakavargaResult'] = json.dumps(result_data)
        
        return jsonify({
            'success': True,
            'data': result_data
        })
        
    except Exception as e:
        print(f"Error in calculation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/results')
def results():
    """Results page"""
    return render_template('results_simple.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard_simple.html')

@app.route('/tamil-interpretations')
def tamil_interpretations():
    """Tamil interpretations page"""
    return render_template('tamil_interpretations_simple.html')

@app.route('/matrix-view')
def matrix_view():
    """Matrix view page"""
    return render_template('matrix_view_simple.html')

if __name__ == '__main__':
    print("🏛️ Tamil Ashtakavarga Calculator - Simple Version")
    print("=" * 60)
    print("🌐 Starting web server...")
    print("📍 Application will be available at: http://localhost:5003")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5003, debug=True)
