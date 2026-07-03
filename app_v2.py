# -*- coding: utf-8 -*-
import os
import sys

# 1. التثبيت التلقائي للمكتبات لضمان عمل السيرفر بدون مشاكل
try:
    import telebot
except ImportError:
    os.system(f"{sys.executable} -m pip install pyTelegramBotAPI")
    import telebot

try:
    from flask import Flask, request, jsonify
except ImportError:
    os.system(f"{sys.executable} -m pip install flask")
    from flask import Flask, request, jsonify

# 2. إعدادات البوت والسيرفر
BOT_TOKEN = "8904786325:AAGi9BEdKX7r4g1BAuwoyrKPlChwhlMQpTA"
ALLOWED_CHAT_ID = 8709813670

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

RISK_SETTINGS = {
    "demo_days": 21,
    "start_balance": 100.0,
}

@app.route('/')
def home():
    return "🚀 Exness Bot Server is Active!"

# 3. استقبال تحديثات التليجرام عبر الـ Webhook
@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return jsonify({"status": "error"}), 403

# 4. الأوامر المسموحة فقط لحسابك أنت
@bot.message_handler(commands=['status'])
def send_status(message):
    if message.chat.id != ALLOWED_CHAT_ID: 
        return
    bot.reply_to(message, "🟢 السيرفر شغال في السحاب ومستعد 100% يا مهندس!")

@bot.message_handler(commands=['balance'])
def send_balance(message):
    if message.chat.id != ALLOWED_CHAT_ID: 
        return
    bot.reply_to(message, f"💰 الرصيد الحالي: ${RISK_SETTINGS['start_balance']} USD")

# 5. تشغيل السيرفر بالبورت المتوافق مع Render بالسيف عليه
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)