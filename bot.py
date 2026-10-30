import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

YOUTUBE_LINK = "https://www.youtube.com/@NXLIVE3"
GROUP_LINK = "https://t.me/"

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 SUBSCRIBE MY YOUTUBE CHANNEL", url=YOUTUBE_LINK)],
        [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP", url=GROUP_LINK)],
        [InlineKeyboardButton("FULL ACCOUNT INFO", callback_data="full"), InlineKeyboardButton("LEVEL & EXP", callback_data="level")],
        [InlineKeyboardButton("PLAYER BIO", callback_data="bio"), InlineKeyboardButton("REGION", callback_data="region")],
        [InlineKeyboardButton("PRIME LEVEL", callback_data="prime"), InlineKeyboardButton("GUILD INFO", callback_data="guild")],
        [InlineKeyboardButton("BANNER IMAGE", callback_data="banner"), InlineKeyboardButton("OUTFIT IMAGE", callback_data="outfit")],
        [InlineKeyboardButton("HOW TO USE", callback_data="how"), InlineKeyboardButton("BAN CHECK", callback_data="ban")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 **NXLIVE3 BOT**\n\n"
        "Welcome to Free Fire Info Bot\n\n"
        "👇 **Niche se option choose karo**\n"
        "Fir apna UID bhejo"
    )
    await update.message.reply_text(text, reply_markup=menu(), parse_mode="Markdown")

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "how":
        await q.message.reply_text("📖 **HOW TO USE:**\n1. Koi bhi button dabao\n2. Apna FF UID bhejo")
    else:
        context.user_data['mode'] = q.data
        await q.message.reply_text(f"✅ **{q.data.upper()}** selected\nAb apna Free Fire UID bhejo 👇")

async def uid_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    if not uid.isdigit():
        await update.message.reply_text("❌ Sahi UID bhejo bhai")
        return
    mode = context.user_data.get('mode','full')
    reply = f"✅ UID Received: `{uid}`\nMode: {mode.upper()}\n\nReal FF API jodne par yaha real data ayega."
    await update.message.reply_text(reply, reply_markup=menu(), parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, uid_handle))
    app.run_polling()

if __name__ == "__main__":
    main()
