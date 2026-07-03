import os
import sys

# تفعيل التثبيت التلقائي للمكتبات الناقصة في السيرفر فوراً
try:
    import telebot
except ImportError:
    os.system(f"{sys.executable} -m pip install pyTelegramBotAPI")
    import telebot

try:
    from flask import Flask
except ImportError:
    os.system(f"{sys.executable} -m pip install flask")
    from flask import Flask

# إعداد السيرفر والويب هوك للبقاء حياً 24/7
app = Flask(__name__)

@app.route('/')
def home():
    return "🟢 Exness Cloud Bot is Running Live!"

# ضع هنا توكن البوت الخاص بك (تأكد من وضعه بين علامتي التنصيص)
BOT_TOKEN = "ضع_التوكن_الخاص_بك_هنا"
bot = telebot.TeleBot(BOT_TOKEN)

# الأوامر الأساسية للبوت
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🦅 أهلاً بك في بوت إكسنس السحابي! أنا أعمل الآن من السحاب 24/7 بدون انقطاع! 🚀")

@bot.message_handler(commands=['status'])
def send_status(message):
    bot.reply_to(message, "🟢 السيرفر شغال في السحاب ومستعد 100% يا مهندس!")

# تشغيل البوت بأمان
if __name__ == "__main__":
    print("🚀 Starting Bot...")
    # تشغيل البوت في الخلفية بدون حجز السيرفر بالكامل لضمان عمل الـ Web
    import threading
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    
    # تشغيل Flask على البورت الذي يطلبه Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)