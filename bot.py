import telebot
import requests

BOT_TOKEN = "9122891436:AAEX2kNVZLR6B3WddVWsz-1v7tI_bNmwhgg"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bhai UID bhejo\nExample: 1234567890")

@bot.message_handler(func=lambda m: True)
def info(m):
    uid = m.text.strip()
    if not uid.isdigit():
        bot.reply_to(m, "Bhai sirf UID bhejo")
        return
    try:
        # Info API
        r = requests.get(f"https://ff-info-api.vercel.app/info?uid={uid}", timeout=20).json()
        msg = f"✅ FOUND\n\nName: {r.get('nickname','N/A')}\nLevel: {r.get('level','N/A')}\nLikes: {r.get('likes','N/A')}\nUID: {uid}"
        bot.reply_to(m, msg)
    except Exception as e:
        bot.reply_to(m, f"UID nahi mila: {e}")

bot.infinity_polling()
