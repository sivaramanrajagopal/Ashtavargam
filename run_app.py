#!/usr/bin/env python3
"""
Startup script for Tamil Ashtakavarga Flask Application
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'pyswisseph', 'tabulate']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
    
    return True

def main():
    """Main startup function"""
    print("🏛️ Tamil Ashtakavarga Calculator - Flask Web Application")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Import and run the Flask app
    try:
        from app import app
        print("✅ Flask application loaded successfully!")
        print("\n🌐 Starting web server...")
        print("📍 Application will be available at: http://localhost:5001")
        print("📍 Or access from other devices: http://0.0.0.0:5001")
        print("\n💡 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5001)
        
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("Make sure all files are in the correct directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
