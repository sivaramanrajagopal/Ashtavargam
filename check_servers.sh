#!/bin/bash
# Quick script to check server status

echo "🔍 Server Status Check"
echo "===================="
echo ""

echo "1. BAV/SAV API (Port 8000):"
curl -s http://localhost:8000/health 2>&1 | head -1 || echo "   ❌ Not running"
echo ""

echo "2. Dasha/Gochara API (Port 8001):"
curl -s http://localhost:8001/health 2>&1 | head -1 || echo "   ❌ Not running"
echo ""

echo "3. Agent Server (Port 8080):"
curl -s http://localhost:8080/health 2>&1 | python3 -m json.tool 2>/dev/null || echo "   ❌ Not running"
echo ""

echo "📊 Running Processes:"
ps aux | grep -E "uvicorn.*(8000|8001|8080)" | grep -v grep || echo "   No uvicorn processes found"
echo ""

echo "🌐 Access URLs:"
echo "   - Agent Dashboard: http://localhost:8080"
echo "   - API Docs: http://localhost:8080/docs"
echo "   - Health Check: http://localhost:8080/health"

