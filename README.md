# Tamil Ashtakavarga Calculator

A comprehensive South Indian/Tamil Ashtakavarga calculator with both command-line and web interface implementations.

## 🌟 Features

### Command Line Version
- ✅ **Authentic Tamil Method**: Implements traditional South Indian Ashtakavarga calculations
- ✅ **Enhanced Display**: Beautiful table formatting with Tamil script and emojis
- ✅ **Comprehensive Analysis**: Individual planet charts + Sarvashtakavarga
- ✅ **Verification System**: Validates against traditional Tamil values
- ✅ **Error Handling**: Robust validation and error management

### Web Application (NEW!)
- 🌐 **Beautiful Web Interface**: Modern, responsive design with Bootstrap
- 📱 **Mobile Friendly**: Works perfectly on all devices
- 🎨 **Interactive Tabs**: Each planet in a separate tab for easy navigation
- 📊 **Visual Indicators**: Color-coded strength levels and quantification
- 🖥️ **User Input Form**: Easy birth data entry with quick-fill options
- 🖨️ **Print Support**: Print results for offline reference
- 🌍 **Multi-language**: Tamil and English support

## 🚀 Quick Start

### Web Application (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the web application
python3 run_app.py
```

Then open your browser and go to: **http://localhost:5000**

### Command Line Version
```bash
# Install dependencies
pip install -r requirements.txt

# Run the calculator
python3 ashtavargam_calculator.py
```

## 📱 Web Application Features

### Input Form
- **Name**: Full name input
- **Date of Birth**: Date picker (YYYY-MM-DD format)
- **Time of Birth**: Time picker (HH:MM format)
- **Place**: Birth place with quick-fill options for major Indian cities
- **Coordinates**: Latitude, Longitude, and Timezone inputs
- **Quick Fill**: One-click buttons for Chennai, Mumbai, Delhi, Bangalore

### Results Display
- **Birth Info Summary**: Displays all entered birth details
- **Planet Tabs**: Individual tabs for each planet (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Ascendant)
- **Sarvashtakavarga Tab**: Combined analysis of all planets
- **Visual Indicators**: 
  - 🔴 High values (6+ points)
  - 🟡 Medium values (4-5 points)  
  - 🟢 Low values (0-3 points)
- **Strength Analysis**: Detailed interpretation for each house
- **Contributors**: Shows which planets contribute to each house

### Interactive Features
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Print Support**: Clean print layout for offline reference
- **Error Handling**: User-friendly error messages
- **Loading Indicators**: Visual feedback during calculations

## 🧮 Tamil Methodology

This calculator follows authentic South Indian/Tamil principles:
- **Parasara Method**: Implements traditional Parasara Ashtakavarga rules
- **Fixed Sign Calculation**: Moving house calculation method
- **Lagna Inclusion**: Ascendant included in individual calculations
- **Regional Variations**: Tamil traditional variations incorporated
- **Bindu Distribution**: Per Tamil traditional rules
- **Perfect Accuracy**: Matches traditional Tamil Ashtakavarga exactly (337 total)

## 📊 Sample Output

### Web Application
- Interactive tabs for each planet
- Color-coded strength indicators
- Detailed house-by-house analysis
- Sarvashtakavarga summary
- Print-friendly layout

### Command Line
- Individual Ashtakavarga charts for all 7 planets + Ascendant
- Comprehensive Sarvashtakavarga analysis
- Tamil verification against traditional values
- Detailed interpretations with strength analysis

## 🔧 Technical Requirements

- **Python**: 3.7 or higher
- **Dependencies**:
  - `pyswisseph` (Swiss Ephemeris for astronomical calculations)
  - `tabulate` (for command-line table formatting)
  - `flask` (for web application)
- **Browser**: Modern web browser with JavaScript enabled (for web app)

## 📁 Project Structure

```
Ashtavargam/
├── app.py                          # Flask web application
├── ashtavargam_calculator.py       # Core calculation engine
├── run_app.py                      # Web app startup script
├── requirements.txt                # Python dependencies
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── index.html                  # Input form page
│   └── results.html                # Results display page
├── static/css/                     # Custom CSS styles
│   └── style.css                   # Additional styling
└── README.md                       # This file
```

## 🌐 Web Application Usage

1. **Start the server**: `python3 run_app.py`
2. **Open browser**: Go to `http://localhost:5000`
3. **Enter birth details**: Fill in the form with your birth information
4. **Quick fill options**: Use city buttons for major Indian locations
5. **Calculate**: Click "Calculate Ashtakavarga" button
6. **View results**: Navigate through planet tabs to see individual charts
7. **Print/Save**: Use print button for offline reference

## 🎯 Verification

The calculator has been thoroughly verified against:
- ✅ **Parasara Principles**: All rules match authentic Parasara methodology
- ✅ **Traditional Values**: Perfect match with classical Tamil values
- ✅ **Trusted Sources**: Verified against production astrological websites
- ✅ **Mathematical Accuracy**: All totals match expected values exactly

## 📞 Support

For issues or questions:
- Check the verification scripts in the repository
- Ensure all dependencies are properly installed
- Verify birth data format and coordinates

---

**🏛️ Tamil Ashtakavarga Calculator - Authentic Parasara Method Implementation**
