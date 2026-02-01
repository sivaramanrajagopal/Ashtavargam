#!/bin/bash
# Start server with performance log filtering

echo "🚀 Starting Agent App with Performance Monitoring..."
echo "📊 Logs will show timing information (⏱️)"
echo "🛑 Press Ctrl+C to stop"
echo ""
echo "=========================================="
echo ""

# Start server and filter for performance-related logs
python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload 2>&1 | \
  grep --line-buffered -E '(⏱️|took|ERROR|WARNING|INFO.*API|INFO.*retrieve|INFO.*LLM|INFO.*Total)' || \
  python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 --reload
