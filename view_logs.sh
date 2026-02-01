#!/bin/bash
# Quick log viewer script

echo "📋 Vedic Astrology App - Log Viewer"
echo "===================================="
echo ""
echo "Select which logs to view:"
echo "1) Agent Server (Port 8080)"
echo "2) BAV/SAV API (Port 8000)"
echo "3) Dasha/Gochara API (Port 8001)"
echo "4) All logs (last 20 lines each)"
echo "5) Follow all logs (real-time)"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "📊 Agent Server Logs (Press Ctrl+C to exit):"
        tail -f /tmp/agent_server.log
        ;;
    2)
        echo "📊 BAV/SAV API Logs (Press Ctrl+C to exit):"
        tail -f /tmp/bav_sav_api.log
        ;;
    3)
        echo "📊 Dasha/Gochara API Logs (Press Ctrl+C to exit):"
        tail -f /tmp/dasha_gochara_api.log
        ;;
    4)
        echo "📊 All Logs (Last 20 lines each):"
        echo ""
        echo "=== Agent Server ==="
        tail -n 20 /tmp/agent_server.log
        echo ""
        echo "=== BAV/SAV API ==="
        tail -n 20 /tmp/bav_sav_api.log
        echo ""
        echo "=== Dasha/Gochara API ==="
        tail -n 20 /tmp/dasha_gochara_api.log
        ;;
    5)
        echo "📊 Following all logs (Press Ctrl+C to exit):"
        echo "Opening in separate windows..."
        # Try to open in separate terminal windows if possible
        if command -v osascript &> /dev/null; then
            osascript -e "tell application \"Terminal\" to do script \"tail -f /tmp/agent_server.log\""
            osascript -e "tell application \"Terminal\" to do script \"tail -f /tmp/bav_sav_api.log\""
            osascript -e "tell application \"Terminal\" to do script \"tail -f /tmp/dasha_gochara_api.log\""
        else
            echo "Running all in one window (use Ctrl+C to exit):"
            tail -f /tmp/agent_server.log /tmp/bav_sav_api.log /tmp/dasha_gochara_api.log
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
