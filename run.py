from uuid import uuid4
from telegram.ext import(
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    filters,
)
from telegram import(
    InputTextMessageContent,
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InputMediaPhoto,
    InlineQueryResultArticle,
    Animation,
)
from telegram.constants import ChatAction

import os
from dotenv import load_dotenv

import httpx


import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton('/start'), KeyboardButton('/word')],
        [KeyboardButton('Random')],
    ]
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name if not None else ""
    name = f'{first_name}'
    if last_name is not None:
        name += f' {last_name}'
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    await update.effective_message.reply_text(
        f'سلام {name} عزیز. لیست دستورات:\n'
        '/start                          شروع\n'
        '/word <word> <number>     تکثیر کلمه\n', quote=True,
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))


def duplicate_word(word: str, number: int):
    return (word+' ')*number


async def word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # It's a default number. When the user doesn't enter the number, the word duplicates 100 numbers.
    number = 100
    if len(context.args) == 0:

        await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        await update.message.reply_text(
            'نحوه‌ی استفاده:\n'
            '/word <word> <number>\n'
        )

    else:
        word = context.args[0]
        if len(context.args) == 2:
            number = int(context.args[1])
            while (len(word)+1) * number > 4096:
                edited_number = 4096 // (len(word)+1)  # sus +1
                number -= edited_number
                await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
                await update.message.reply_text(duplicate_word(word, edited_number))

        await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        await update.message.reply_text(duplicate_word(word, number))

        await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        await update.message.reply_text(f'کلمه‌ی {word} به تعداد {number} تا با موفقیت تکثیر شد.')


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton('Random Person'), KeyboardButton('Random Image')],
    ]
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING

    )
    await update.message.reply_text(
        text='لطفا گزینه‌ی مورد نظر راانتخاب کنید.',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
        )
    )


async def random_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    RandomImageText = 'Random Image'
    RandomImageUrl = 'https://picsum.photos/1200/'
    RandomPeopleText = 'Random Person'
    RandomPeopleUrl = 'https://thispersondoesnotexist.com/image'
    # import pdb;pdb.set_trace()
    client = httpx.Client(follow_redirects=True)
    if RandomImageText in update.message.text:
        image = client.get(RandomImageUrl).content
    elif RandomPeopleText in update.message.text:
        image = client.get(RandomPeopleUrl).content
    if image:
        print(type(image))
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
        await update.message.reply_media_group(media=[InputMediaPhoto(image)], read_timeout=600)


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if query == '':
        return
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Lower Case',
            input_message_content=InputTextMessageContent(query.lower()),

        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Upper Case',
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Bold',
            input_message_content=InputTextMessageContent(
                message_text=f'<b>{query}</b>',
                parse_mode='HTML',
            ),
        ),
            InlineQueryResultArticle(
                id =str(uuid4()),
                title  = "Italic",
                input_message_content=InputTextMessageContent(
                    message_text=f'<i>{query}</i>',
                    parse_mode='HTML'
                ),

            ),
            
    ]
    await update.inline_query.answer(results)

async def send_animation(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_animation(animation=Animation(
        file_id='BAACAgQAAxkBAAIFbWKq4c9FWTSfHqurYWc--kmEP9zoAAKiDgACgI1YUfGqHByywIlcJAQ',
        file_unique_id=None,
        width=None,
        height=None,
        duration=None,
        ))

async def unknown_type(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(update)
    await update.message.reply_text('got it')

load_dotenv()
TOKEN = os.getenv('TOKEN')
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler(['start', 'keyboard'], start))
application.add_handler(CommandHandler('word', word))
application.add_handler(MessageHandler(filters.Text('Random'), random))
application.add_handler(MessageHandler(filters.Text(
    ['Random Person', 'Random Image']), random_picture))
application.add_handler(InlineQueryHandler(inline_query))
application.add_handler(CommandHandler('l',send_animation))
application.add_handler(MessageHandler(filters.ALL,unknown_type))

application.run_polling(pool_timeout=600) #  the telegram.TimeOut error was fixed by setting pool_time variable to 600



