# priceMonitorBot

This bot tracks price changes for crypto coins and alerts on Telegram if the 24-hour change crosses ±5%.

## 📦 Files
- `monitor.py` - The main bot logic.
- `.env` - Your bot config (tokens, coins, interval).
- `Dockerfile` - To run the bot in Docker.
- `requirements.txt` - Python dependencies.
- `start.sh` - Easy script to build & run in Docker.

## 🚀 Quick Start

1. Fill `.env` with your bot token, chat ID, etc.
2. Run the bot locally (no Docker):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python monitor.py
    ```
3. Run in Docker (recommended):
    ```bash
    ./start.sh
    ```
