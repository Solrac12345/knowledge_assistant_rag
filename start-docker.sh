#!/bin/bash
# start.sh - Robust startup script for Windows/Git Bash

echo "🔍 Step 1: Ensuring Docker Context is correct..."
# Force Docker to use the default Windows pipe context
docker context use default 2>/dev/null

echo "🔍 Step 2: Checking Docker connectivity..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not responding."
    echo "💡 Solution: Please open 'Docker Desktop' app and wait for it to say 'Docker Desktop is running'."
    exit 1
fi
echo "✅ Docker is connected."

echo "🔍 Step 3: Checking for port 8000 conflicts..."
# Find if any process is listening on port 8000
PID=$(netstat -ano | findstr :8000 | findstr LISTENING | awk '{print $NF}' | head -1)

if [ -n "$PID" ]; then
    echo "⚠️  Warning: Port 8000 is occupied by PID $PID."
    echo "🔨 Attempting to free port..."
    # Kill the process (using // syntax for Git Bash compatibility)
    taskkill //F //PID "$PID" 2>/dev/null
    sleep 2
fi

echo "🚀 Step 4: Starting containers..."
docker compose up -d --build

echo "✅ Done! Checking status..."
sleep 3
docker compose ps

#Make the script executable
#chmod +x start.sh
#./start.sh