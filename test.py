import dotenv
from telegram.ext import *
from telegram import *

FIRST,SECOND,THIRD,FORTH = map(chr,range(4))

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام به تو")
    return FIRST

def third():
    pass

async def first(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("first message")
    return SECOND

async def second(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("second message")

async def back_first(update:Update,context:ContextTypes.DEFAULT_TYPE):
    return FIRST
def forth():
    pass



import dotenv;dotenv.load_dotenv()
import os
application = Application.builder().token(os.getenv("TOKEN")).build()

application.add_handler(ConversationHandler(
    entry_points=[CommandHandler("start",start)],
    states={
        FIRST:[CommandHandler("first",first)],
        SECOND:[CommandHandler("second",second)],
        THIRD:[ConversationHandler(
            entry_points=[CommandHandler("third",third)],
            states={
                FORTH:[CommandHandler("forth",forth)]
            },
            fallbacks=[] # first fallback
        )]
    },
    fallbacks=[] # second fallback
))
application.run_polling()
