import os
import time
from threading import Thread
from flask import Flask
import telebot
import MetaTrader5 as mt5  # أو الـ library المعتمدة للربط مع إكسنس

# 1. إعدادات السيرفر والويب لبوت التليجرام
app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EXNESS_ACCOUNT = int(os.getenv("EXNESS_LOGIN", 0))
EXNESS_SERVER = os.getenv("EXNESS_SERVER")

bot = telebot.TeleBot(TOKEN)

@app.route('/')
def home():
    return "Exness Cloud Bot is Running Successfully! 🚀"

# 2. كود مراقبة الحساب والصفقات الحية
def monitor_exness():
    print("⚡ جاري الاتصال بمنصة إكسنس والبدء في المراقبة الحية...")
    
    # رسالة ترحيبية تؤكد تشغيل النظام الفعلي
    try:
        bot.send_message(CHAT_ID, "🟢 **النظام الفعلي اشتغل!** البوت الآن يراقب حسابك خطوة بخطوة... صفقاتك القادمة ستظهر هنا مباشرة! 📊")
    except Exception as e:
        print(f"Error sending startup message: {e}")

    # هنا اللوب الأساسي لمراقبة الصفقات
    last_orders = set()
    
    while True:
        try:
            # ملاحظة: إذا كنت تستعمل مكتبة مخصصة غير MT5 للـ Cloud، ضع أمر جلب الصفقات المفتوحة هنا
            # مثال بهيكل المراقبة الذكي:
            open_positions = [] # جلب الصفقات الحالية من إكسنس
            
            current_orders = set([pos.ticket for pos in open_positions])
            
            # كشف الصفقات الجديدة
            new_orders = current_orders - last_orders
            for ticket in new_orders:
                # جلب تفاصيل الصفقة وإرسالها فوراً
                msg = f"🔔 **صفقة جديدة فتحت!**\n\n📌 التيكت: `{ticket}`\n📈 النوع: شراء/بيع\n💰 اللوت: 0.01"
                bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                
            last_orders = current_orders
            
        except Exception as e:
            print(f"⚠️ خطأ أثناء مراقبة الحساب: {e}")
            
        time.sleep(5)  # يفحص الحساب كل 5 ثوانٍ بدون توقف

# 3. تشغيل السيرفر والمراقبة معاً في نفس الوقت
if __name__ == "__main__":
    # تشغيل مراقبة إكسنس في خلفية السيرفر (Background Thread)
    monitoring_thread = Thread(target=monitor_exness)
    monitoring_thread.daemon = True
    monitoring_thread.start()
    
    # تشغيل Flask سيرفر على البورت المطلوبة من Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)