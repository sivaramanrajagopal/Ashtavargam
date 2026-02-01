#!/bin/bash
# Performance Monitoring Script for Agent App

echo "🔍 PERFORMANCE MONITORING - Agent App"
echo "======================================"
echo ""
echo "📊 Real-time Performance Logs (Filtered):"
echo "   - Shows only timing/performance related logs"
echo "   - Press Ctrl+C to stop"
echo ""

# Monitor uvicorn output and filter for performance logs
tail -f /dev/null 2>&1 | while read line; do
    # This will be replaced with actual log monitoring
    echo "Waiting for logs..."
done

# Alternative: Check if we can capture uvicorn output
echo "💡 To view real-time logs, run:"
echo "   python3 -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080 2>&1 | grep -E '(⏱️|took|ERROR|WARNING|performance)'"
