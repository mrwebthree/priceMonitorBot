import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
SYMBOLS = os.getenv("SYMBOLS", "bitcoin").split(",")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN and CHAT_ID must be set in .env file!")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload).raise_for_status()
    except requests.exceptions.RequestException as e:
        log_error(f"Telegram Error: {e}")

def log_error(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("monitor_errors.log", "a") as file:
        file.write(f"[{timestamp}] {message}\n")

class PriceMonitor:
    def __init__(self, symbol):
        self.symbol = symbol.lower().strip()
        self.last_reported_change = None

    def fetch_price_and_change(self):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={self.symbol}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10).json()
        price = response[self.symbol]['usd']
        change_24h = response[self.symbol]['usd_24h_change']
        return price, change_24h

    def check_price(self):
        try:
            price, change_24h = self.fetch_price_and_change()
            if self.last_reported_change is None:
                self.last_reported_change = change_24h
            else:
                if abs(change_24h - self.last_reported_change) >= 5:
                    direction = "📈 UP" if change_24h > self.last_reported_change else "📉 DOWN"
                    send_telegram_message(
                        f"🚨 {self.symbol.upper()} Alert!\nPrice: ${price:.2f}\n24h Change: {change_24h:.2f}%\nDirection: {direction}"
                    )
                    self.last_reported_change = change_24h
        except Exception as e:
            log_error(f"{self.symbol.upper()} Error: {e}")

def run_monitor():
    send_telegram_message(f"✅ Monitoring started for: {', '.join(SYMBOLS)}")
    monitors = [PriceMonitor(symbol) for symbol in SYMBOLS]
    while True:
        for monitor in monitors:
            monitor.check_price()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_monitor()
