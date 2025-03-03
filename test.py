import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
webhook_url = "https://abc123.ngrok.io/" + BOT_TOKEN  # Replace with your ngrok URL

response = requests.post(url, json={"url": webhook_url})
print(response.json())
