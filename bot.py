from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from proxy_scraper import get_indian_proxies
from checker import check_all
import os

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8530402543  # apna telegram id daalo

users = set()

keyboard = [
    ["🌐 Get Proxy", "⚡ Fast Proxy"],
    ["🔄 Refresh", "🔍 Check Proxy"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    await update.message.reply_text("Bot Ready 🚀", reply_markup=reply_markup)


async def getproxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching proxies...")

    proxies = get_indian_proxies()
    result = await check_all(proxies[:50])

    if not result:
        await update.message.reply_text("No working proxy 😢")
        return

    msg = "\n\n".join([
        f"🌐 {p}\n⚡ Speed: {s}s"
        for p, s in result[:10]
    ])

    await update.message.reply_text(msg)


async def fast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Finding fast proxies ⚡...")

    proxies = get_indian_proxies()
    result = await check_all(proxies[:50])

    fast_proxies = [r for r in result if r[1] < 1]

    if not fast_proxies:
        await update.message.reply_text("No fast proxy 😢")
        return

    msg = "\n\n".join([
        f"🌐 {p}\n⚡ Speed: {s}s"
        for p, s in fast_proxies[:10]
    ])

    await update.message.reply_text(msg)


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /check ip:port")
        return

    proxy = context.args[0]
    result = await check_all([proxy])

    if not result:
        await update.message.reply_text("Dead proxy ❌")
        return

    p, s = result[0]
    await update.message.reply_text(f"Alive ✅ {p} ⚡ {s}s")


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Not allowed ❌")
        return

    await update.message.reply_text(
        "👑 Admin Panel\n\n"
        "/stats - bot stats"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(f"Total Users: {len(users)}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🌐 Get Proxy":
        await getproxy(update, context)

    elif text == "⚡ Fast Proxy":
        await fast(update, context)

    elif text == "🔄 Refresh":
        await getproxy(update, context)

    elif text == "🔍 Check Proxy":
        await update.message.reply_text("Send like: /check 1.1.1.1:80")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getproxy", getproxy))
app.add_handler(CommandHandler("fast", fast))
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("stats", stats))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
