import requests
from config import BOT_TOKEN, CHAT_ID

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_telegram_message(message):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def send_telegram_menu():
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "📊 Bot Menu - Choose Action:",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "Start Monitoring", "callback_data": "start"}],
                [{"text": "Stop Monitoring", "callback_data": "stop"}],
                [{"text": "Check Status", "callback_data": "status"}]
            ]
        }
    }
    requests.post(url, json=payload)
