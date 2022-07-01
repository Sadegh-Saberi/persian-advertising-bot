import asyncio
import aiofiles
import logging
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    filters,
    CallbackQueryHandler,
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ReplyKeyboardMarkup,
)
from telegram.constants import ChatAction
# import asyncio
from utils import DataBase
import os
import dotenv
dotenv.load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

### base keyboard buttons' text ###
back_text = "🔙 برگشت"
skip_text = "◀️ رد شدن"
cancel_text = "💢 کنسل"

### db settings ####
temp_adv = DataBase('DataBase.db', "adv", [back_text, skip_text, cancel_text])
final_adv = DataBase("DataBase.db", "final_adv", [back_text, skip_text])

service = DataBase("DataBase.db", "service",  [
                   back_text, skip_text, cancel_text])
final_service = DataBase("DataBase.db", "final_service",  [
                         back_text, skip_text, cancel_text])

project = DataBase("DataBase.db", "project",  [
                   back_text, skip_text, cancel_text])
final_project = DataBase("DataBase.db", "final_project",  [
                         back_text, skip_text, cancel_text])

### setting variables ###
(
    ### COMMON VARIABLES ###
    ANNOUNCEMENT,
    CHOOSE_ANN_TYPE,
    ### ADV VARIABLES ###
    ADV_TITLE,
    ADV_GENDER,
    ADV_TERM,
    ADV_EDUCATION,
    ADV_EXPERIENCE,
    ADV_TIME,
    ADV_AGE,
    ADV_ADVANTAGES,
    ADV_CONTACT,
    ADV_PHOTO,
    ADV_PREVIEW,
    ADV_SEND_TO_ADMIN,
    ### SERVICE VARIABLES ###
    SERVICE_TITLE,
    SERVICE_SKILLS,
    SERVICE_EXPLANATION,
    SERVICE_PHOTO,
    SERVICE_CONTACT,
    SERVICE_PREVIEW,
    SERVICE_SEND_TO_ADMIN,
    ### PROJECT VARIABLES ###
    PROJECT_TITLE,
    PROJECT_EXPLANATION,
    PROJECT_BUDGET,
    PROJECT_CONTACT,
    PROJECT_PREVIEW,
    PROJECT_SEND_TO_ADMIN,
) = map(chr, range(27))

### starting handlers ###


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    keyboard = [
        ["ثبت آگهی", "جست و جو (به زودی...)"],
        ["افزودن اشتراک (به زودی...)"],
        ["درباره‌ی ما (به زودی...)", "⚖️ قوانین"]
    ]
    await temp_adv.delete_data("user_id", user_id)
    await final_adv.delete_data("user_id", user_id)
    await service.delete_data("user_id", user_id)
    await final_service.delete_data("user_id", user_id)
    await project.delete_data("user_id", user_id)
    await final_project.delete_data("user_id", user_id)
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(

        text="جهت ایجاد یک آگهی جدید، از دکمه‌ی «ثبت آگهی» استفاده کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True)
    )

    return CHOOSE_ANN_TYPE


async def choose_announce_type(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_chat.id
    keyboard = [
        ["استخدام", "انجام دهنده", "پروژه"],
        [cancel_text, back_text]
    ]
    await temp_adv.delete_data("user_id", user_id)
    await final_adv.delete_data("user_id", user_id)
    await service.delete_data("user_id", user_id)
    await final_service.delete_data("user_id", user_id)
    await project.delete_data("user_id", user_id)
    await final_project.delete_data("user_id", user_id)
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="قالب آگهی خود را انتخاب کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True))
    return ANNOUNCEMENT


async def announcement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    await temp_adv.delete_data("user_id", user_id)
    await final_adv.delete_data("user_id", user_id)
    await service.delete_data("user_id", user_id)
    await final_service.delete_data("user_id", user_id)
    await project.delete_data("user_id", user_id)
    await final_project.delete_data("user_id", user_id)

    message = update.message.text
    context.user_data["message"] = message
    keyboard = [
        [cancel_text, back_text],
    ]
    if message == "استخدام":
        await temp_adv.insert_data({"user_id": user_id})
        await update.message.reply_chat_action(action=ChatAction.TYPING)

        await update.message.reply_text(
            text="لطفا یک تیتر برای آگهی استخدام خود انتخاب کنید.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                one_time_keyboard=True,
            )
        )
        return ADV_TITLE

    elif message == "انجام دهنده":
        await service.insert_data({"user_id": user_id})
        await update.message.reply_chat_action(action=ChatAction.TYPING)

        await update.message.reply_text(
            text="لطفا یک تیتر برای آگهی خود به عنوان انجام دهنده انتخاب کنید.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard, resize_keyboard=True,),

        )
        return SERVICE_TITLE

    elif message == "پروژه":
        await project.insert_data({"user_id": user_id})
        await update.message.reply_chat_action(action=ChatAction.TYPING)
        await update.message.reply_text(
            text="لطفا یک تیتر برای پروژه‌ی خود انتخاب کنید.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard, resize_keyboard=True,)

        )
        return PROJECT_TITLE


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiofiles.open("rules.txt", "r", encoding="utf8") as file:
        rules_txt = await file.read()
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text=rules_txt,
    )


### ADVERTISEMENT HANDLERS ###
async def adv_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    message = update.message.text
    await temp_adv.update_data(user_id, key="title", value=message)
    keyboard = [
        ["آقا", "خانم"],
        ["خانم یا آقا"],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text="لطفا جنسیت مورد نظر را انتخاب کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return ADV_GENDER


async def adv_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    gender_number = await temp_adv.get_data("user_id", user_id)
    if gender_number == None:
        gender_text = update.message.text
        if gender_text == 'آقا':
            gender_number = 0
        elif gender_text == 'خانم':
            gender_number = 1
        elif gender_text == 'خانم یا آقا':
            gender_number = 2
        await temp_adv.update_data(
            update.effective_chat.id,
            key='gender',
            value=gender_number)

    keyboard = [
        ["پاره وقت", "تمام وقت"],
        [cancel_text, back_text],

    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text="لطفا نوبت کاری را وارد کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return ADV_TERM


# شیوه‌ی همکاری
async def adv_term(update: Update, context: ContextTypes.DEFAULT_TYPE):
    term_text = update.message.text
    id = update.effective_chat.id
    keyboard = [
        [skip_text],
        [cancel_text, back_text],

    ]
    if term_text == 'پاره وقت':
        term_number = 0
    elif term_text == 'تمام وقت':
        term_number = 1
    try:
        await temp_adv.update_data(id, 'term', term_number)
    except UnboundLocalError:  # if the user enter the back key, this error occurs
        pass
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text="لطفا تحصیلات مورد نیاز را وارد کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            # one_time_keyboard=True
        )
    )
    return ADV_EDUCATION


# رد شدن از شیوه‌ی همکاری
async def adv_skip_term(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text="لطفا تحصیلات مورد نیاز را وارد کنید.",
    )

    return ADV_EDUCATION

# تحصیلات


async def adv_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    education_text = update.message.text
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await temp_adv.update_data(id, 'education', education_text)
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text="لطفا سابقه‌ی کاری مورد نیاز را وارد کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            # one_time_keyboard=True,
        ))

    return ADV_EXPERIENCE


# ٰرد شدن از تحصیلات
async def adv_skip_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text="از وارد کردن تحصیلات گذر کردید.\n"
        "لطفا سابقه‌ی کار مورد نیاز را وارد کنید."
    )
    return ADV_EXPERIENCE

# سابقه‌ی کاری


async def adv_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    exp_text = update.message.text
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await temp_adv.update_data(user_id=user_id, key='experience', value=exp_text)
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text="لطفا ساعت کاری مورد نظر را وارد کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            # one_time_keyboard=True
        ))
    return ADV_TIME


# رد شدن از سابقه‌ی کاری
async def adv_skip_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text="از وارد کردن سابقه‌ی کاری گذر کردید."
        "لطفا ساعت کاری مورد نظر را وارد کنید."
    )
    return ADV_TIME


async def adv_time(update: Update, context: ContextTypes.DEFAULT_TYPE):  # ساعت کاری
    user_id = update.effective_chat.id
    work_time_text = update.message.text
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await temp_adv.update_data(user_id=user_id, key='time', value=work_time_text)
    await update.message.reply_chat_action(action=ChatAction.TYPING)

    await update.message.reply_text(
        text="لطفا سن مورد نیاز را وارد کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            # one_time_keyboard=True,
        ))
    return ADV_AGE


async def adv_age(update: Update, context: ContextTypes.DEFAULT_TYPE):  # سن
    user_id = update.effective_chat.id
    age_text = update.message.text
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await temp_adv.update_data(user_id, key='age', value=age_text)
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا مزایای کاری را به صورت یک لیست (مانند لیست نمونه) وارد کنید.\n"
        "مزینت ۱\n"
        "مزینت ۲\n"
        "مزینت ۳",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            # one_time_keyboard=True,
        )
    )
    return ADV_ADVANTAGES


async def adv_skip_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="از وارد کردن سن مورد نیاز گذر کردید.\n"
        "لطفا مزایای کاری را به صورت یک لیست (مانند لیست نمونه) وارد کنید.\n"
        "مزینت ۱\n"
        "مزینت ۲\n"
        "مزینت ۳\n"

    )
    return ADV_ADVANTAGES


async def adv_advantages(update: Update, context: ContextTypes.DEFAULT_TYPE):  # مزایای کاری
    user_id = update.effective_chat.id
    adv_text = update.message.text
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await temp_adv.update_data(user_id=user_id, key='advantages', value=adv_text)
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا جهت ارتباط نیرو با شما، یک یا چند راه ارتباطی وارد کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            # one_time_keyboard=True
        )
    )
    return ADV_CONTACT


# رد شدن از مزایای کاری
async def adv_skip_advantages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="از وارد کردن مزایای کاری گذر کردید."
        "لطفا جهت ارتباط نیرو با شما، یک یا چند راه ارتباطی وارد کنید."
    )
    return ADV_CONTACT


async def adv_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):  # راه ارتباطی
    user_id = update.effective_chat.id
    contact_text = update.message.text
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await temp_adv.update_data(user_id=user_id, key='contact', value=contact_text)
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا عکس را ارسال کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        ))
    return ADV_PHOTO


async def adv_skip_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    contact_text = "@"+update.effective_chat.username
    await temp_adv.update_data(user_id=user_id, key='contact', value=contact_text)
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="از وارد کردن راه ارتباطی گذر کردید.\n"
        "لطفا تصویر بنر را ارسال کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return ADV_PHOTO


async def adv_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    photo_file = await update.message.photo[-1].get_file()
    binary_photo = await photo_file.download_as_bytearray()
    await temp_adv.update_data(user_id=user_id, key='photo', value=binary_photo)
    keyboard = [
        ["پیش‌نمایش"],
        [skip_text],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="اگر از اطلاعات وارد شده اطمینان دارید. روی گزینه‌ی 'پیش‌نمایش' جهت مشاهده‌ی آگهی، قبل از ارسال شدن جهت بازبیی، کلیک کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,)
    )
    return ADV_PREVIEW


async def adv_skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["پیش‌نمایش"],
        [skip_text],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="از ارسال عکس گذر کردید.\n"
        "اگر از اطلاعات وارد شده اطمینان دارید. روی گزینه‌ی 'پیش‌نمایش' جهت مشاهده‌ی آگهی، قبل از ارسال شدن جهت بازبینی، کلیک کنید.",
        reply_markup=ReplyKeyboardMarkup(keyboard=keyboard),
    )
    return ADV_PREVIEW


async def adv_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    data = await temp_adv.get_data("user_id", user_id)
    title, gender_number, term_number, education, experience, time, age, advantages, contact, binary_photo = data[
        1:]
    if advantages is not None:
        adv_list = str()
        for adv in advantages.split("\n"):
            adv_list += f"    🔹 {adv}\n"
    else:
        adv_list = None

    contact_list = str()
    for cnt in contact.split("\n"):
        contact_list += f"    🔹 {cnt}\n"

    caption = f"✅ {title}\n"
    if age is not None:
        caption += f"🟠 سن:\t{age}\n"
    if gender_number is not None:
        caption += f"🟠 جنسیت:\n    🔹 {DataBase.number_to_gender(gender_number)}\n"
    if term_number is not None:
        caption += f"🟠 نوع قرارداد:\n    🔹 {DataBase.number_to_term(term_number)}\n"
    if education is not None:
        caption += f"🟠 تحصیلات:\n    🔹 {education}\n"
    if experience is not None:
        caption += f"🟠 سابقه‌ی همکاری:\n    🔹 {experience}\n"
    if time is not None:
        caption += f"🟠 ساعت کاری:\n    🔹 {time}\n"
    if adv_list is not None:
        caption += f"🟠 مزایای کاری:\n{adv_list}\n"
    caption += f"☎️ راه ارتباطی:\n{contact_list}"

    inline_keyboard = [[
        InlineKeyboardButton("ارسال", callback_data='adv_send_to_check'),
    ]]
    if binary_photo is not None:
        await update.message.reply_chat_action(action=ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(
            photo=binary_photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=inline_keyboard,
            )
        )
    else:
        await update.message.reply_chat_action(action=ChatAction.TYPING)
        await update.message.reply_text(
            text=caption,
            reply_markup=InlineKeyboardMarkup(inline_keyboard)
        )

    await final_adv.insert_data({"user_id": user_id, "caption": caption, "photo": binary_photo})

    return ADV_SEND_TO_ADMIN


async def adv_send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await temp_adv.delete_data("user_id", query.from_user.id)
    await query.answer()
    if query.data == "adv_send_to_check":
        inline_keyboard = [[InlineKeyboardButton(
            "🟦 جهت بازبینی ارسال شد 🟦 ", callback_data="sent_to_check")]]
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
        user_id = query.from_user.id
        final_data = await final_adv.get_data("user_id", user_id)
        inline_keyboard = [
            [InlineKeyboardButton('لغو', callback_data="reject"), InlineKeyboardButton(
                'ارسال به کانال', callback_data="send_to_channel")]
        ]
        caption, photo = final_data[1:]
        admin_id = os.getenv("ADMIN_CHAT_ID")
        if photo is not None:
            await context.bot.send_photo(
                chat_id=admin_id,
                caption=caption,
                photo=photo,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
        else:
            await context.bot.send_message(
                chat_id=admin_id,
                text=caption,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=inline_keyboard)
            )
        return await start(update,context)


### SERVICE HANDLERS ###
async def service_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    message = update.message.text
    await service.update_data(user_id, "title", message)
    keyboard = [
        [cancel_text, back_text]
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا مهارت های خود را (طبق نمونه) ارسال کنید.\n"
        "مهارت ۱\nمهارت ۲\nمهارت ۳\n...",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True)
    )
    return SERVICE_SKILLS


async def service_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    message = update.message.text
    await service.update_data(user_id, "skills", message)
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا توضیحاتی در مورد پروژه‌ی خود ارايه دهید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True)
    )
    return SERVICE_EXPLANATION


async def service_skip_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="از وارد کردن کردن مهارت ها عبور کردید.\n"
        "لطفا توضیحاتی در مورد پروژه‌ی خود ارایه دهید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True)
    )
    return SERVICE_EXPLANATION


async def service_explanation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    message = update.message.text
    await service.update_data(user_id, "explanation", message)
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا تصویر را ارسال کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True)
    )
    return SERVICE_PHOTO


async def service_skip_explanation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="از وارد کردن توضیحات بیشتر گذر کردید.\n"
        "لطفا تصویر بنر خود را ارسال کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True)
    )
    return SERVICE_PHOTO


async def service_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    photo_file = await update.message.photo[-1].get_file()
    binary_photo = await photo_file.download_as_bytearray()
    await service.update_data(user_id=user_id, key="photo", value=binary_photo)
    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا جهت ارتباط کارفرما با شما، یک یا چند راه ارتباطی وارد کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True),
    )
    return SERVICE_CONTACT


async def service_skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [skip_text],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="از ارسال کردن تصویر بنر عبور کردید.\n"
        "لطفا جهت ارتباط کارفرما با شما، یک یا چند راه ارتباطی وارد کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True),
    )
    return SERVICE_CONTACT


async def service_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    message = update.message.text
    await service.update_data(user_id, key="contact", value=message)
    keyboard = [
        ["پیش‌نمایش"],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="جهت مشاهده‌ی پیش‌نمایش آگهی قبل از ارسال، روی کلید پیش‌نمایش کلیک کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return SERVICE_PREVIEW


async def service_skip_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    contact_text = update.effective_chat
    if contact_text == skip_text:
        contact_text = "@"+update.effective_chat.username
    await temp_adv.update_data(user_id=user_id, key='contact', value=contact_text)
    keyboard = [
        ["پیش‌نمایش"],
        [cancel_text, back_text],
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="از وارد کردن راه ارتباطی گذر کردید.(نام کاربری شما به عنوان راه ارتباطی انتخاب می‌شود.)"
        "جهت مشاهده‌ی پیش‌نمایش آگهی قبل از ارسال، روی کلید پیش‌نمایش کلیک کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return SERVICE_PREVIEW


async def service_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    data = await service.get_data("user_id", user_id)
    title, skills, explanation, contact, binary_photo = data[1:]
    skills_list = str()
    for skill in skills.split("\n"):
        skills_list += f"    🔹 {skill}\n"

    caption = f"✅ {title}\n"
    caption += f"🟠 مهارت ها:\n{skills_list}"
    if explanation is not None:
        caption += f"🟠 توضیحات:\n{explanation}"
    if contact is not None:
        contact_list = f"☎️ راه ارتباطی:\n"
        for cnt in contact.split("\n"):
            contact_list += f"    🔹 {cnt}\n"
        caption += contact_list

    await final_service.insert_data({"user_id": user_id, "caption": caption, "photo": binary_photo})
    inline_keyboard = [[InlineKeyboardButton(
        "ارسال", callback_data="service_send_to_check")]]
    if binary_photo is not None:
        await update.message.reply_chat_action(action=ChatAction.UPLOAD_PHOTO)
        await update.message.reply_photo(
            photo=binary_photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        )
    else:
        await update.message.reply_chat_action(action=ChatAction.TYPING)
        await update.message.reply_text(
            text=caption,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard),
        )
    return SERVICE_SEND_TO_ADMIN


async def service_send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await service.delete_data("user_id", query.from_user.id)
    await query.answer()
    if query.data == "service_send_to_check":
        inline_keyboard = [[InlineKeyboardButton(
            "🟦 جهت بازبینی ارسال شد 🟦 ", callback_data="sent_to_check")]]
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
        user_id = query.from_user.id
        final_data = await final_service.get_data("user_id", user_id)
        inline_keyboard = [
            [InlineKeyboardButton('لغو', callback_data="reject"), InlineKeyboardButton(
                'ارسال به کانال', callback_data="send_to_channel")]
        ]
        caption, photo = final_data[1:]
        admin_id = os.getenv("ADMIN_CHAT_ID")
        if photo is not None:
            await context.bot.send_photo(
                chat_id=admin_id,
                caption=caption,
                photo=photo,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
        else:
            await context.bot.send_message(
                chat_id=admin_id,
                text=caption,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
    return await start(update,context)



### PROJECT HANDLERS ###


async def project_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    message = update.message.text
    await project.update_data(user_id=user_id, key="title", value=message)
    keyboard = [
        [cancel_text, back_text]

    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا توضیحاتی در مورد پروژه ارائه دهید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True,),
    )
    return PROJECT_EXPLANATION


async def project_explanation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    message = update.message.text
    await project.update_data(user_id, "explanation", message)
    keyboard = [
        [cancel_text, back_text]

    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا بودجه‌ی خود را وارد کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True),
    )
    return PROJECT_BUDGET


async def project_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    message = update.message.text
    await project.update_data(user_id=user_id, key="budget", value=message)
    keyboard = [
        [skip_text],
        [cancel_text, back_text]
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="جهت ارتباط افراد با شما، لطفا یک یا چند راه ارتباطی وارد کنید.\n"
        "در صورت گذر کردن از این قسمت، «نام کاربری» شما جهت ارتباط با شما در آگهی قرار می‌گیرد.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True)
    )
    return PROJECT_CONTACT


async def project_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    message = update.message.text
    await project.update_data(user_id=user_id, key="contact", value=message)
    keyboard = [
        ["پیش‌نمایش"],
        [cancel_text, back_text]
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="لطفا جهت مشاهده‌ی پیش‌نمایش آگهی، قبل از ارسال، روی کلید «پیش‌نمایش» کلیک کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True)
    )
    return PROJECT_PREVIEW


async def project_skip_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    contact_text = update.effective_chat
    if contact_text == skip_text:
        contact_text = "@"+update.effective_chat.username
    await temp_adv.update_data(user_id=user_id, key='contact', value=contact_text)
    keyboard = [
        ["پیش‌نمایش"],
        [cancel_text, back_text]
    ]
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="از وارد کردن راه ارتباطی عبور کردید.\n"
        "لطفا جهت مشاهده‌ی پیش‌نمایش آگهی، قبل از ارسال، روی کلید «پیش‌نمایش» کلیک کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard, resize_keyboard=True),
    )
    return PROJECT_PREVIEW


async def project_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    data = await project.get_data("user_id", user_id)
    title, explanation, budget, contact = data[1:]

    if contact is not None:
        contact_list = str()
        for cnt in contact.split("\n"):
            contact_list += f"    🔹 {cnt}\n"
    else:
        contact_list = None

    text = f"✅ {title}\n"
    if explanation is not None:
        text += f"🟠 توضیحات:\n\t{explanation}\n"
    if budget is not None:
        text += f"🟠 بودجه:\n    🔹 {budget}\n"
    if contact_list is not None:
        text += f"☎️ راه ارتباطی:\n{contact_list}\n"

    inline_keyboard = [[InlineKeyboardButton(
        "ارسال", callback_data="project_send_to_check")]]

    await final_project.insert_data({"user_id": user_id, "text": text})
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard),
    )

    
    # did not work ...

    # keyboard = [
    #     [cancel_text, back_text]
    # ]
    # await update.message.edit_reply_markup(
        
    #     reply_markup=ReplyKeyboardMarkup(keyboard=keyboard)
    # )
    return PROJECT_SEND_TO_ADMIN


async def project_send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await project.delete_data("user_id", query.from_user.id)
    await query.answer()
    if query.data == "project_send_to_check":
        inline_keyboard = [[InlineKeyboardButton(
            "🟦 جهت بازبینی ارسال شد 🟦 ", callback_data="sent_to_check")]]
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
        user_id = query.from_user.id
        final_data = await final_project.get_data("user_id", user_id)
        inline_keyboard = [
            [InlineKeyboardButton('لغو', callback_data="reject"), InlineKeyboardButton(
                'ارسال به کانال', callback_data="send_to_channel")]
        ]
        caption = final_data[1]
        admin_id = os.getenv("ADMIN_CHAT_ID")
        await context.bot.send_message(
            chat_id=admin_id,
            text=caption,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=inline_keyboard)
        )
    return await start(update,context)


### COMMON HANDLERS ###

# this is a hard coding ...
async def admin_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        final_data = await final_project.get_data("user_id", query.from_user.id)
        caption = final_data[1]
        photo = None
        await final_project.delete_data("user_id", query.from_user.id)

    except:
        try:
            final_data = await final_service.get_data("user_id", query.from_user.id)
            caption, photo = final_data[1:]
            await final_service.delete_data("user_id", query.from_user.id)

        except:
            final_data = await final_adv.get_data("user_id", query.from_user.id)
            caption, photo = final_data[1:]
            await final_adv.delete_data("user_id", query.from_user.id)

    channel_id = os.getenv('CHANNEL_ID')
    if query.data == "send_to_channel":
        bot_url = os.getenv("BOT_URL")
        inline_keyboard = [[InlineKeyboardButton(
            "برای ساخت آگهیت کلیک کن", url=bot_url)]]
        if photo is not None:
            await context.bot.send_photo(
                chat_id=channel_id,
                photo=photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
        else:
            await context.bot.send_message(
                chat_id=channel_id,
                text=caption,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard))
        inline_keyboard = [[InlineKeyboardButton(
            "🟢 ارسال شد. 🟢", callback_data="sent_to_channel")]]
        await query.edit_message_reply_markup(InlineKeyboardMarkup(inline_keyboard))
    elif query.data == "reject":
        inline_keyboard = [
            [InlineKeyboardButton("🔴 لغو شد. 🔴", callback_data="rejected")]
        ]
        await query.edit_message_reply_markup(InlineKeyboardMarkup(inline_keyboard))


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="فرایند متوقف شد.")
    return await start(update, context)


async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="متن وارد شده پذیرفته نیست. لطفا مجددا تلاش کنید."
    )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="دستور وارد شده پذیرفته نیست. لطفا مجددا تلاش کنید."
    )


async def unknown_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_chat_action(action=ChatAction.TYPING)
    await update.message.reply_text(
        text="فایل ارسال شده پذیرفته نیست. لطفا مجددا تلاش کنید."
    )


async def back_swicher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.text = context.user_data["message"]
    return await announcement(update, context)


TOKEN = os.getenv("TOKEN")


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
        ],
        states={
            CHOOSE_ANN_TYPE: [
                MessageHandler(filters.Text(
                    ["ثبت آگهی"]), choose_announce_type),
            ],
            ANNOUNCEMENT: [
                MessageHandler(filters.Text([back_text]), start),
                MessageHandler(filters.Text(
                    ["استخدام", "انجام دهنده", "پروژه"]), announcement),
            ],
            ADV_TITLE: [ConversationHandler(
                entry_points=[
                    MessageHandler(filters.TEXT & (~filters.Text(
                        [cancel_text, back_text])), adv_title),
                ],
                states={
                    ADV_GENDER: [
                        MessageHandler(filters.Text(
                            [back_text]), back_swicher),
                        MessageHandler(filters.Text(
                            ["آقا", "خانم", "خانم یا آقا"]), adv_gender),
                    ],
                    ADV_TERM: [
                        MessageHandler(filters.Text([back_text]), adv_title),
                        MessageHandler(filters.Text(
                            [skip_text]), adv_skip_term),
                        MessageHandler(filters.Text(
                            ['پاره وقت', 'تمام وقت']), adv_term),
                    ],
                    ADV_EDUCATION: [
                        MessageHandler(filters.Text(
                            [skip_text]), adv_skip_education),
                        MessageHandler(filters.Text([back_text]), adv_gender),
                        MessageHandler(filters.TEXT, adv_education),
                    ],
                    ADV_EXPERIENCE: [
                        MessageHandler(filters.Text(
                            [skip_text]), adv_skip_experience),
                        MessageHandler(filters.Text([back_text]), adv_term), MessageHandler(
                            filters.TEXT, adv_experience),
                    ],
                    ADV_TIME: [
                        MessageHandler(filters.Text(
                            [back_text]), adv_education),
                        MessageHandler(filters.TEXT & (
                            ~filters.Text([cancel_text, back_text])), adv_time)
                    ],
                    ADV_AGE: [
                        MessageHandler(filters.Text(
                            [skip_text]), adv_skip_age),
                        MessageHandler(filters.Text(
                            [back_text]), adv_experience),
                        MessageHandler(filters.TEXT, adv_age), MessageHandler(
                            filters.Text(skip_text), adv_skip_age)
                    ],
                    ADV_ADVANTAGES: [
                        MessageHandler(filters.Text(skip_text),
                                       adv_skip_advantages),
                        MessageHandler(filters.Text([back_text]), adv_time),
                        MessageHandler(filters.TEXT & (~filters.Text(
                            [cancel_text, back_text])), adv_advantages)
                    ],
                    ADV_CONTACT: [
                        MessageHandler(filters.Text([back_text]), adv_age),
                        MessageHandler(filters.Text(
                            [skip_text]), adv_skip_contact),
                        MessageHandler(filters.TEXT & (~filters.Text(
                            [cancel_text, back_text])), adv_contact)
                    ],
                    ADV_PHOTO: [
                        MessageHandler(filters.Text(
                            [skip_text]), adv_skip_photo),
                        MessageHandler(filters.Text([back_text]), adv_advantages), MessageHandler(
                            filters.PHOTO, adv_photo),
                    ],
                    ADV_PREVIEW: [
                        MessageHandler(filters.Text(back_text), adv_contact),
                        MessageHandler(filters.Text(
                            ["پیش‌نمایش"]), adv_preview)
                    ],
                    ADV_SEND_TO_ADMIN: [
                        MessageHandler(filters.Text([back_text]), adv_photo),
                        CallbackQueryHandler(adv_send_to_admin),
                    ],
                },
                fallbacks=[
                    MessageHandler(filters.Text([cancel_text]), start), ],
                map_to_parent={
                    ADV_TITLE: ADV_TITLE,
                    CHOOSE_ANN_TYPE: CHOOSE_ANN_TYPE,
                },

            )],
            SERVICE_TITLE: [ConversationHandler(
                entry_points=[
                    MessageHandler(filters.TEXT & (
                        ~filters.Text([cancel_text, back_text])), service_title),
                ],
                states={
                    SERVICE_SKILLS: [
                        MessageHandler(filters.Text(
                            [skip_text]), service_skip_skills),
                        MessageHandler(filters.Text(
                            [back_text]), back_swicher),
                        MessageHandler(filters.TEXT & (
                            ~filters.Text([cancel_text])), service_skills),
                    ],
                    SERVICE_EXPLANATION: [
                        MessageHandler(filters.Text(
                            [skip_text]), service_skip_explanation),
                        MessageHandler(filters.Text(
                            [back_text]), service_title),
                        MessageHandler(filters.TEXT & (~filters.Text(
                            [cancel_text])), service_explanation),
                    ],
                    SERVICE_CONTACT: [
                        MessageHandler(filters.Text(
                            [skip_text]), service_skip_contact),
                        MessageHandler(filters.Text(
                            [back_text]), service_skills),
                        MessageHandler(filters.TEXT & (
                            ~filters.Text([cancel_text])), service_contact),
                    ],
                    SERVICE_PHOTO: [
                        MessageHandler(filters.Text(
                            [skip_text]), service_skip_photo),
                        MessageHandler(filters.Text(
                            [back_text]), service_explanation),
                        MessageHandler(filters.PHOTO & (
                            ~filters.Text([cancel_text])), service_photo),
                    ],
                    SERVICE_PREVIEW: [
                        MessageHandler(filters.Text(
                            [back_text]), service_contact),
                        MessageHandler(filters.Text(
                            ["پیش‌نمایش"]), service_preview),
                    ],
                    SERVICE_SEND_TO_ADMIN: [
                        MessageHandler(filters.Text(
                            [back_text]), service_photo),
                        CallbackQueryHandler(service_send_to_admin),
                    ],
                },
                fallbacks=[
                    MessageHandler(filters.Text([cancel_text]), start),
                ],
                map_to_parent={
                    SERVICE_TITLE: SERVICE_TITLE,
                    CHOOSE_ANN_TYPE: CHOOSE_ANN_TYPE,
                },
            )],
            PROJECT_TITLE: [ConversationHandler(
                entry_points=[
                    MessageHandler(filters.TEXT & (~filters.Text(
                        [cancel_text, back_text])), project_title),
                ],
                states={
                    PROJECT_EXPLANATION: [
                        MessageHandler(filters.TEXT & (~filters.Text(
                            [cancel_text, back_text])), project_explanation),
                        MessageHandler(filters.Text([back_text]), announcement)
                    ],
                    PROJECT_BUDGET: [
                        MessageHandler(filters.TEXT & (
                            ~filters.Text([cancel_text])), project_budget),
                    ],
                    PROJECT_CONTACT: [
                        MessageHandler(filters.TEXT & (
                            ~filters.Text([cancel_text])), project_contact),
                        MessageHandler(filters.Text(
                            [skip_text]), project_skip_contact)
                    ],
                    PROJECT_PREVIEW: [
                        MessageHandler(filters.TEXT & (
                            ~filters.Text([cancel_text])), project_preview),
                    ],
                    PROJECT_SEND_TO_ADMIN: [
                        CallbackQueryHandler(project_send_to_admin),
                    ],
                },
                fallbacks=[
                    MessageHandler(filters.Text([cancel_text]), start),
                ],
                map_to_parent={
                    PROJECT_TITLE: PROJECT_TITLE,
                    CHOOSE_ANN_TYPE: CHOOSE_ANN_TYPE,
                }
            )]
        },
        fallbacks=[
            MessageHandler(filters.Text([back_text]), choose_announce_type),
            MessageHandler(filters.Text([cancel_text]), cancel),
            CommandHandler("start", start),
        ],
    ))
    application.add_handler(CallbackQueryHandler(admin_answer))
    application.add_handler(CommandHandler("rules", rules))
    application.add_handler(MessageHandler(filters.Text(["⚖️ قوانین"]), rules))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    application.add_handler(MessageHandler(filters.TEXT, unknown_text))
    application.add_handler(MessageHandler(filters.ALL, unknown_file))
    application.run_polling()


if __name__ == "__main__":
    main()
