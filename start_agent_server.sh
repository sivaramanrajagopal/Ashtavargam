#!/bin/bash
# Start Agent Server Script

cd "$(dirname "$0")"

echo "🚀 Starting Vedic Astrology AI Agent Server..."
echo ""

# Set Python path
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Check if port 8080 is already in use
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 8080 is already in use. Stopping existing process..."
    pkill -f "uvicorn.*8080"
    sleep 2
fi

# Start the server
echo "📍 Starting server on http://localhost:8080"
echo "📚 API Docs: http://localhost:8080/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload

