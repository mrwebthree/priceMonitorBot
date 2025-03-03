#!/bin/bash

# Load .env to get BOT_TOKEN
export $(grep -v '^#' .env | xargs)

# Kill existing ngrok if already running
pkill -f "ngrok http 5000" > /dev/null 2>&1

# Start ngrok (background mode) and wait a bit
ngrok http 5000 > ngrok.log 2>&1 &
sleep 2

# Extract ngrok URL using Python (cross-platform)
NGROK_URL=$(python -c "import requests, time; time.sleep(1); r = requests.get('http://localhost:4040/api/tunnels'); print(r.json()['tunnels'][0]['public_url'])")

# Check if ngrok URL is valid
if [[ "$NGROK_URL" == "" ]]; then
    echo "❌ Failed to get ngrok URL! Check ngrok status."
    cat ngrok.log
    exit 1
fi

echo "✅ ngrok URL: $NGROK_URL"

# Set Telegram webhook with new ngrok URL
WEBHOOK_URL="$NGROK_URL/$BOT_TOKEN"
curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/setWebhook" -H "Content-Type: application/json" -d "{\"url\": \"$WEBHOOK_URL\"}"

# Rebuild and run Docker
docker build -t price-monitor-bot .
docker run --name price-monitor-container --env-file .env -p 5000:5000 price-monitor-bot
