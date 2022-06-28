import dotenv
from telegram.ext import *
from telegram import *

FIRST,SECOND = map(chr,range(2))

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام به تو")
    return FIRST

async def first(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("first message")
    return SECOND

async def second(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("second message")

async def back_first(update:Update,context:ContextTypes.DEFAULT_TYPE):
    return FIRST



import dotenv;dotenv.load_dotenv()
import os
application = Application.builder().token(os.getenv("TOKEN")).build()

application.add_handler(ConversationHandler(
    entry_points=[CommandHandler("start",start)],
    states={
        FIRST:[MessageHandler(filters.Text(["f"]),first)],
        SECOND:[MessageHandler(filters.Text(["s"]),second),MessageHandler(filters.Text("b"),back_first)],
    },
    fallbacks=[]
))
application.run_polling()
