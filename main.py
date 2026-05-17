from flask import Flask, request
import requests
import threading
import time

app = Flask(__name__)

TELEGRAM_TOKEN = "8929739297:AAEGbaI3Ihk3jqpJ1dSVNOajt8a6gAS9RZ8"
TELEGRAM_CHAT_ID = "8971168812"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def keep_alive():
    while True:
        try:
            requests.get("https://smc-webhook.onrender.com/ping")
        except:
            pass
        time.sleep(240)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    if data and "message" in data:
        send_telegram(data["message"])
    elif request.data:
        send_telegram(request.data.decode("utf-8"))
    return "OK", 200

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

@app.route("/", methods=["GET"])
def index():
    return "SMC Webhook activ!", 200

t = threading.Thread(target=keep_alive)
t.daemon = True
t.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
