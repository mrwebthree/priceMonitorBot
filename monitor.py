import time
import requests
from telegram_bot import send_telegram_message
from config import CHECK_INTERVAL

def get_price_and_change(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_change=true"
    response = requests.get(url).json()

    if symbol not in response:
        raise Exception(f"Failed to fetch price for {symbol}. Response: {response}")

    price = response[symbol]['usd']
    change_24hr = response[symbol]['usd_24h_change']
    return price, change_24hr

def monitor_price(symbol):
    last_reported_change = None
    send_telegram_message(f"✅ Monitoring started for {symbol.upper()}. Checking every {CHECK_INTERVAL} seconds.")

    while True:
        try:
            _, change_24hr = get_price_and_change(symbol)

            if last_reported_change is None:
                last_reported_change = change_24hr

            else:
                change_diff = abs(change_24hr - last_reported_change)
                if change_diff >= 5:
                    direction = "📈 UP" if change_24hr > last_reported_change else "📉 DOWN"
                    message = (
                        f"🚨 {symbol.upper()} 24h Change Alert!\n\n"
                        f"New 24h Change: {round(change_24hr, 2)}%\n"
                        f"Direction: {direction}"
                    )
                    send_telegram_message(message)
                    last_reported_change = change_24hr

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            send_telegram_message(f"⚠️ Error: {e}")
            time.sleep(30)
