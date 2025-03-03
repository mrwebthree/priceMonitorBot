from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CHAT_ID = os.getenv("CHAT_ID")

def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    webhook_url = f"{WEBHOOK_URL}/webhook"  # Ensure "/webhook" path is correct
    response = requests.post(url, json={"url": webhook_url})
    print("Webhook Set Response:", response.json())

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received Update:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if text == "/start":
            send_message(chat_id, "✅ Starting price monitor bot...")

    return jsonify({"status": "ok"})

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    set_webhook()  # This triggers on start
    app.run(host="0.0.0.0", port=5000)
