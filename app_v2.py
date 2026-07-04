import os
import time
from threading import Thread
from flask import Flask
import telebot

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TOKEN)

@app.route('/')
def home():
    return "Exness Direct Bot is Live! 🚀"

def send_startup_msg():
    time.sleep(3)
    try:
        bot.send_message(CHAT_ID, "🟢 **البوت السحابي شغال ومستقر 100%!**\nجاهز الآن لاستقبال الأوامر وتتبع حسابك بأقصى قوة.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    Thread(target=send_startup_msg, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)