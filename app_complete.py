#!/usr/bin/env python3
"""
Complete Ashtakavarga Calculator - Flask Web Application
Fully functional with traditional chart layout and all features
"""

from flask import Flask, render_template, request, jsonify, session
from ashtakavarga_calculator_final import AshtakavargaCalculatorFinal
from interpretation_engine import AshtakavargaInterpreter
import json

app = Flask(__name__)
app.secret_key = 'ashtakavarga_secret_key_2024'

# Planet information
PLANET_INFO = {
    'SUN': {'name': 'சூர்யன்', 'color': '#FFD700'},
    'MOON': {'name': 'சந்திரன்', 'color': '#C0C0C0'},
    'MARS': {'name': 'செவ்வாய்', 'color': '#FF4500'},
    'MERCURY': {'name': 'புதன்', 'color': '#32CD32'},
    'JUPITER': {'name': 'குரு', 'color': '#4169E1'},
    'VENUS': {'name': 'சுக்ரன்', 'color': '#FF69B4'},
    'SATURN': {'name': 'சனி', 'color': '#2F4F4F'},
    'ASCENDANT': {'name': 'லக்கினம்', 'color': '#FF6347'}
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
    """Home page with birth data input form - redirects to Prokerala style after calculation"""
    return render_template('index_complete.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate Ashtakavarga"""
    try:
        # Get form data
        name = request.form.get('name', '')
        dob = request.form.get('dob', '')
        tob = request.form.get('tob', '')
        place = request.form.get('place', '')
        
        # Validate required fields
        if not dob or not tob:
            return jsonify({
                'success': False,
                'error': 'Date of birth and time of birth are required'
            })
        
        try:
            latitude = float(request.form.get('latitude', 0))
            longitude = float(request.form.get('longitude', 0))
            tz_offset = float(request.form.get('tz_offset', 0))
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid latitude, longitude, or timezone offset'
            })
        
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
        
        # Calculate Ashtakavarga using correct Tamil rules - All 8 planets including Ascendant
        calculator = AshtakavargaCalculatorFinal(birth_data)
        calculator.calculate_all_charts()
        
        # Get display data
        display_data = calculator.get_display_data()
        
        # Generate interpretations with Vedic rules
        interpreter = AshtakavargaInterpreter()
        ascendant_rasi = display_data['planetary_positions'].get('ASCENDANT', 1)
        interpretation = interpreter.generate_comprehensive_analysis(
            display_data['sarvashtakavarga'],
            display_data['totals'],
            display_data['sarva_total'],
            ascendant_rasi,
            display_data['ashtakavarga_charts'],
            display_data['planetary_positions']
        )
        
        # Add interpretation to display data
        display_data['interpretation'] = interpretation
        
        # Add birth info to display data
        display_data['birth_info'] = {
            'name': name,
            'dob': dob,
            'tob': tob,
            'place': place,
            'coordinates': f"{latitude}, {longitude}"
        }
        
        # Store in session
        session['calculation_data'] = display_data
        session['birth_info'] = birth_data
        
        return jsonify({
            'success': True,
            'data': display_data
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in calculation: {e}")
        print(f"Traceback: {error_trace}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': error_trace if app.debug else None
        }), 500

@app.route('/results')
def results():
    """Results page with traditional chart layout"""
    # Try to get data from session as fallback
    calculation_data = session.get('calculation_data')
    return render_template('results_complete.html', calculation_data=calculation_data)

@app.route('/dashboard')
def dashboard():
    """Dashboard page with interpretations"""
    # Try to get data from session as fallback
    calculation_data = session.get('calculation_data')
    return render_template('dashboard_complete.html', calculation_data=calculation_data)

@app.route('/matrix-view')
def matrix_view():
    """Matrix view page with all 8 Bhinnashtakavarga matrices"""
    # Try to get data from session as fallback
    calculation_data = session.get('calculation_data')
    return render_template('matrix_view_complete.html', calculation_data=calculation_data)

@app.route('/tamil-interpretations')
def tamil_interpretations():
    """Tamil interpretations page"""
    # Try to get data from session as fallback
    calculation_data = session.get('calculation_data')
    return render_template('tamil_interpretations_complete.html', calculation_data=calculation_data)

@app.route('/ashtakavarga-prokerala')
def ashtakavarga_prokerala():
    """Prokerala-style Ashtakavarga display"""
    # Try to get data from session as fallback
    calculation_data = session.get('calculation_data')
    return render_template('ashtakavarga_prokerala.html', calculation_data=calculation_data)

@app.route('/interpretations')
def interpretations():
    """Interpretations page"""
    # Try to get data from session as fallback
    calculation_data = session.get('calculation_data')
    return render_template('ashtakavarga_prokerala.html', calculation_data=calculation_data)

if __name__ == '__main__':
    import os
    
    # Get port from environment variable (Railway) or use default
    port = int(os.environ.get('PORT', 5004))
    # Disable debug mode in production (Railway sets NODE_ENV or similar)
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print("🏛️ Complete Ashtakavarga Calculator - Flask Web Application")
    print("=" * 60)
    print("🌐 Starting web server...")
    print(f"📍 Application will be available at: http://0.0.0.0:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
