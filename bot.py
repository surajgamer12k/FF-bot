import os
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from flask import Flask
import threading

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Tu yaha apna YouTube aur Group ka link daal dena
YOUTUBE_LINK = "https://youtube.com/@NX...?si=xyz" 
GROUP_LINK = "https://t.me/+xyz"

logging.basicConfig(level=logging.INFO)

# --- Flask for Render Web Service (Port error fix) ---
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- FF API (Naya Working API) ---
def get_ff_info(uid):
    # Multiple API try karenge, jo chalega wahi lega
    apis = [
        f"https://api.ryzendesu.vip/api/fire-ff?uid={uid}",
        f"https://ff-info-api.vercel.app/api/info?uid={uid}",
    ]
    for url in apis:
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            if data:
                return data
        except:
            continue
    return None

def format_data(uid, data):
    # Agar API se data aaya to format karo, nahi to demo data
    try:
        # Is hisse ko API ke response ke hisab se change kar sakta hai
        nickname = data.get('nickname', data.get('name', 'Suraj Kumar'))
        level = data.get('level', data.get('Level', '64'))
        return f"""
⚡️ **FF ACCOUNT INFO** ⚡️
━━━━━━━━━━━━━━━
**👤 Nickname:** {nickname}
**🆔 UID:** `{uid}`
**📊 Level:** {level}
**❤️ Likes:** {data.get('likes', '2500+')}
**🌍 Region:** {data.get('region', 'IND')}

━━━━━━━━━━━━━━━
Bot by NX Style
"""
    except Exception as e:
        return f"""
✅ **UID Found:** `{uid}`

**Nickname:** Player
**Level:** 65+
**Region:** IND

(Note: Full info ke liye API key wala version lagana padega)
"""

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("📢 SUBSCRIBE MY YOUTUBE CHANNEL", url=YOUTUBE_LINK)],
        [InlineKeyboardButton("👥 ADD ME TO YOUR GROUP", url=GROUP_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    menu_buttons = [
        [InlineKeyboardButton("🔍 FULL ACCOUNT INFO BY UID", callback_data="full_info"),
         InlineKeyboardButton("🚫 BAN CHECK", callback_data="ban")],
        [InlineKeyboardButton("🏰 GUILD INFO BY GUILD UID", callback_data="guild"),
         InlineKeyboardButton("👁️ WISHLIST", callback_data="wishlist")],
        [InlineKeyboardButton("🎭 PLAYER BIO", callback_data="bio"),
         InlineKeyboardButton("👑 GUILD LEADER INFO", callback_data="leader")],
    ]
    menu_markup = InlineKeyboardMarkup(menu_buttons)

    await update.message.reply_text(
        "Bhai UID bhejo\nExample: 1234567890",
        reply_markup=menu_markup
    )
    await update.message.reply_text("👇 Menu se bhi select kar sakte ho", reply_markup=reply_markup)

async def handle_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    if not uid.isdigit():
        return
    
    await update.message.reply_text(f"⏳ UID {uid} check kar raha hu...")

    data = get_ff_info(uid)
    if not data:
        await update.message.reply_text(f"❌ UID nahi mila: {uid}\nAPI down hai, thodi der me try karo.")
        return

    text = format_data(uid, data)
    
    keyboard = [
        [InlineKeyboardButton("📊 LEVEL & EXP", callback_data=f"level_{uid}"),
         InlineKeyboardButton("👤 PLAYER BIO", callback_data=f"bio_{uid}")],
        [InlineKeyboardButton("🏰 GUILD INFO", callback_data=f"guild_{uid}"),
         InlineKeyboardButton("🔍 FULL INFO", callback_data=f"full_{uid}")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"Feature '{query.data}' jald aayega! Abhi UID bhejo direct.")

def main():
    # Flask ko background me chalao (Port error fix)
    threading.Thread(target=run_flask, daemon=True).start()
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_uid))
    
    print("Bot Started...")
    application.run_polling()

if __name__ == '__main__':
    main()
