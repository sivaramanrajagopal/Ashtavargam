#!/bin/bash
# Start script for Railway deployment
# This script ensures PORT is properly set

# Railway sets PORT automatically, but we ensure it's available
export PORT=${PORT:-8080}

# Start uvicorn
exec python -m uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT

