#!/bin/bash
# Start All Servers Script

cd "$(dirname "$0")"

echo "🚀 Starting All Vedic Astrology Servers..."
echo ""

# Set Python path
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Stop existing servers
echo "🛑 Stopping existing servers..."
pkill -f "uvicorn.*8000" 2>/dev/null
pkill -f "uvicorn.*8001" 2>/dev/null
pkill -f "uvicorn.*8080" 2>/dev/null
pkill -f "python.*app_complete" 2>/dev/null
sleep 2

# Start BAV/SAV API (Port 8000)
echo "1️⃣  Starting BAV/SAV API on port 8000..."
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8000 > /tmp/bav_sav_api.log 2>&1 &
BAV_SAV_PID=$!
sleep 2

# Start Dasha/Gochara API (Port 8001)
echo "2️⃣  Starting Dasha/Gochara API on port 8001..."
python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8001 > /tmp/dasha_gochara_api.log 2>&1 &
DASHA_GOCHARA_PID=$!
sleep 2

# Start Agent Server (Port 8080)
echo "3️⃣  Starting Agent Server on port 8080..."
python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload > /tmp/agent_server.log 2>&1 &
AGENT_PID=$!
sleep 3

# Start Flask App (Port 5004)
echo "4️⃣  Starting Flask App on port 5004..."
python3 app_complete.py > /tmp/flask_app.log 2>&1 &
FLASK_PID=$!
sleep 3

echo ""
echo "✅ All servers started!"
echo ""
echo "📋 Server URLs:"
echo "  • Flask App:        http://localhost:5004"
echo "  • BAV/SAV API:      http://localhost:8000 (Docs: http://localhost:8000/docs)"
echo "  • Dasha/Gochara API: http://localhost:8001 (Docs: http://localhost:8001/docs)"
echo "  • Agent Server:     http://localhost:8080 (Docs: http://localhost:8080/docs)"
echo ""
echo "📝 Log Files:"
echo "  • Flask: /tmp/flask_app.log"
echo "  • BAV/SAV API: /tmp/bav_sav_api.log"
echo "  • Dasha/Gochara API: /tmp/dasha_gochara_api.log"
echo "  • Agent Server: /tmp/agent_server.log"
echo ""
echo "🛑 To stop all servers, run: pkill -f 'uvicorn|python.*app_complete'"
echo ""
echo "⏳ Waiting for servers to fully start..."
sleep 5

# Verify servers
echo ""
echo "🔍 Verifying servers..."
python3 << 'PYEOF'
import requests
import time

servers = [
    ("BAV/SAV API", "http://localhost:8000/health"),
    ("Dasha/Gochara API", "http://localhost:8001/health"),
    ("Agent Server", "http://localhost:8080/health"),
    ("Flask App", "http://localhost:5004/")
]

print("=" * 60)
all_running = True
for name, url in servers:
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print(f"✅ {name:25} - Running")
        else:
            print(f"⚠️  {name:25} - Status {response.status_code}")
            all_running = False
    except:
        print(f"❌ {name:25} - Not responding yet")
        all_running = False

print("=" * 60)
if all_running:
    print("✅ All servers are running!")
else:
    print("⚠️  Some servers may still be starting. Check logs if needed.")
PYEOF

echo ""
echo "✨ Done! All servers should be running now."

