#!/bin/bash

# Stop Docker container
docker stop price-monitor-container
docker rm price-monitor-container

# Kill ngrok
pkill -f "ngrok http 5000"

echo "✅ Stopped bot and ngrok."
