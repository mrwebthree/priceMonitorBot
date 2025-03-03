import time
import threading
from telegram_bot import send_telegram_menu, send_telegram_message
from monitor import monitor_price
from config import CHAT_ID, BOT_TOKEN
from flask import Flask, request

app = Flask(__name__)
monitor_thread = None
stop_flag = False

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    global monitor_thread, stop_flag
    data = request.json

    if "callback_query" in data:
        callback_data = data['callback_query']['data']
        chat_id = data['callback_query']['message']['chat']['id']

        if chat_id != int(CHAT_ID):
            return "Unauthorized", 403

        if callback_data == "start":
            if monitor_thread and monitor_thread.is_alive():
                send_telegram_message("⚠️ Monitoring already running.")
            else:
                stop_flag = False
                monitor_thread = threading.Thread(target=monitor_price, args=("bitcoin",))
                monitor_thread.start()
                send_telegram_message("✅ Monitoring started.")

        elif callback_data == "stop":
            stop_flag = True
            send_telegram_message("🛑 Monitoring stopped.")
        
        elif callback_data == "status":
            if monitor_thread and monitor_thread.is_alive():
                send_telegram_message("✅ Monitoring is running.")
            else:
                send_telegram_message("❌ Monitoring is not running.")

    return "OK", 200

def setup_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    webhook_url = f"https://your-server.com/{BOT_TOKEN}"  # <-- Replace with your actual server URL if hosting
    requests.post(url, json={"url": webhook_url})

if __name__ == "__main__":
    setup_webhook()
    send_telegram_menu()
    app.run(host="0.0.0.0", port=5000)
