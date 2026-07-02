from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- Bot Configuration ---
TELEGRAM_TOKEN = "8904786325:AAGi9BEdKX7r4g1BAuwoyrKPlChwhlMQpTA"
TELEGRAM_CHAT_ID = "8709813670"

def send_telegram_alert(message):
    """Send live trading alerts and notifications to your Telegram channel/chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

@app.route('/')
def home():
    return "🚀 Exness Cloud Bot is Running 24/7 Successfully!"

# --- 📈 Webhook to Receive Trading Signals ---
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
        
    # Send instant notification to your phone via Telegram
    alert_msg = f"🔔 *New Trading Signal Received In Cloud*:\n{data}"
    send_telegram_alert(alert_msg)
    
    # TODO: Integrate your Exness execution logic here later
    
    return jsonify({"status": "success", "message": "Signal processed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)