from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from proxy_scraper import get_indian_proxies
from checker import check_all

TOKEN = "YOUR_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Ready 🚀")

async def getproxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching proxies...")

    proxies = get_indian_proxies()
    result = await check_all(proxies[:50])

    if not result:
        await update.message.reply_text("No working proxy 😢")
        return

    msg = "\n".join([f"{p} ⚡ {s}s" for p, s in result[:10]])
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getproxy", getproxy))

app.run_polling()
