#!/bin/bash

echo "🛑 Stopping Docker containers..."
docker-compose down

# Uncomment the line below to also remove volumes
 #docker-compose down -v

echo "🔒 Optionally closing Docker Desktop (Windows side)..."
powershell.exe -Command "Stop-Process -Name 'Docker Desktop' -Force"

echo "✅ Shutdown complete. Rest mode activated. ✨"