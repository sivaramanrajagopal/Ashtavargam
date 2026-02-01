#!/bin/bash
# Kill existing processes on port 8080 and restart agent server

echo "🛑 Killing existing processes on port 8080..."
kill -9 38466 39677 2>/dev/null
sleep 2

echo "🚀 Starting Agent App server..."
cd /Users/sivaramanrajagopal/Ashtavargam
export PYTHONPATH=/Users/sivaramanrajagopal/Ashtavargam:$PYTHONPATH

# Start with logs saved to file
python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload 2>&1 | tee agent_logs.txt
