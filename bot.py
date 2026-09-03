import os
import requests

TOKEN = os.environ["BOT_TOKEN"]

url = f"https://api.telegram.org/bot{TOKEN}/getMe"

response = requests.get(url, timeout=20)

if response.ok:
    bot = response.json()["result"]
    print("Bot connected successfully:")
    print(bot["username"])
else:
    print("Telegram connection failed")
    print(response.text)
