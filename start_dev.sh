#!/bin/bash

# Expected project folder name
EXPECTED_DIR="microblog"

echo "🔍 Verifying project directory..."
CURRENT_DIR=$(basename "$PWD")

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
  echo "⚠️ You're in '$CURRENT_DIR' but expected '$EXPECTED_DIR'. Please cd into the correct directory."
  exit 1
fi

echo "✅ Directory check passed."

# Check if Docker is running
echo "🔧 Checking Docker Desktop status..."
if ! docker info > /dev/null 2>&1; then
  echo "🛑 Docker doesn't appear to be running. Trying to start it now..."
  powershell.exe -Command "Start-Process -FilePath 'C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe'" 
  echo "⏳ Waiting for Docker to start..."
  sleep 10

  # Re-check after waiting
  if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker still isn't responding. Please start Docker Desktop manually and try again."
    exit 1
  fi
fi

echo "🐳 Docker is running!"

# Boost mmap for Elasticsearch
echo "📈 Tuning virtual memory map count..."
sudo sysctl -w vm.max_map_count=262144

# Launch containers
echo "🚀 Starting Docker containers..."
docker-compose up --build -d

# Confirm Elasticsearch is alive
echo "🔍 Checking Elasticsearch health..."
curl -s http://localhost:9200 | jq

echo "🎉 All systems go! You're ready to dive into Flask."