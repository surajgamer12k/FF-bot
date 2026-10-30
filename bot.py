import telebot, threading
from flask import Flask
import requests

TOKEN = "9122891436:AAEX2kNVZLR6B3WddVWsz-1v7tI_bNmwhgg"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bhai UID bhejo\nExample: 3334527536")

@bot.message_handler(func=lambda m: True)
def info(m):
    uid = m.text.strip()
    if not uid.isdigit():
        bot.reply_to(m, "Bhai sirf number wala UID bhejo")
        return
    try:
        r = requests.get(f"https://api-info-ff.vercel.app/info?uid={uid}", timeout=15).json()
        text = f"UID: {uid}\nName: {r.get('name','N/A')}\nLevel: {r.get('level','N/A')}\nLikes: {r.get('likes','N/A')}"
        bot.reply_to(m, text)
    except:
        bot.reply_to(m, "UID nahi mila bhai")

@app.route('/')
def home():
    return "Bot Running 24/7"

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
