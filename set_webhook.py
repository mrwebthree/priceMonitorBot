import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
webhook_url = "https://a3d7-84-54-70-248.ngrok-free.app/{BOT_TOKEN}"  # Replace with actual ngrok URL

response = requests.post(url, json={"url": webhook_url})
print(response.json())
