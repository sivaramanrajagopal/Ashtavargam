#!/bin/bash
# Start the Agent Server
# Make sure BAV/SAV API (port 8000) and Dasha/Gochara API (port 8001) are running first

cd /Users/sivaramanrajagopal/Ashtavargam
export PYTHONPATH=/Users/sivaramanrajagopal/Ashtavargam:$PYTHONPATH

echo "🚀 Starting Vedic Astrology AI Agent Server..."
echo "📍 Server will run on http://localhost:8080"
echo ""
echo "Make sure these APIs are running:"
echo "  - BAV/SAV API: http://localhost:8000"
echo "  - Dasha/Gochara API: http://localhost:8001"
echo ""

uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload

