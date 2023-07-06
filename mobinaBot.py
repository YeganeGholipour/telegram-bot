import asyncio
import telegram
from datetime import datetime, time
import random
from telegram.ext import JobQueue
from typing import Final
from telegram import Update
from telegram.ext import (
    filters,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
)

BOT_TOKEN: Final = "6397308023:AAF86R8vR5zvke7kOjhi8S2_HCI3q6OuNVU"

#### command handlers ####
# /start
# /help
# /dice


# /start handler
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Bonjour Mobina!! \n que puis-je faire pour vous?",
        reply_to_message_id=update.effective_message.id,
    )


# /help handler
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""You can use the bot in the following manner mobina \n:
     /start -> start
     /dice -> bot sends you a text based on the number of the dice
     /help -> This text""",
        reply_to_message_id=update.effective_message.id,
    )


# /dice handler
async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texts = {
        0: "مبینا گور بابای بقیه. امروز خوشحالی مگه نه؟",
        1: "امروز ناراحت نیستی مگه نه؟ اگر ناراحتی می تونی یکی از ویدیو هامون رو ببینی تا دلت باز بشه :)",
        2: "اگر امروز حالت خوب نیست یادت بیاد ریحانه چطوری بطری های عرق نعنا رو خورد :)",
        3: "چه خبرا؟ امروز به خودت رسیدی مگه نه؟",
        4: "اگر حالت خوب نیست بیا به من پیام بده تا منم یکم غر بزنم. تو خودت نریزی یه وقت !!!",
        5: "خوشگله اگه حالت خوب نیست برو یه آهنگ بذار و بدون من خلی دوستت دارم",
        6: "باورت میشه ما هنوز هم باهم دوستیم؟ من که باورم نمیشه و واقعا نمی دونم چطوری اخلافت رو تحمل می کنم قشنگه :)",
    }
    my_dice = await context.bot.send_dice(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"شماره تاس شما: {my_dice.dice.value} \n {texts[my_dice.dice.value]}",
        reply_to_message_id=update.effective_message.id,
    )


# choose daily quotes
def choose_quotes():
    quote_file_path = "~/Document"
    with open(quote_file_path, "r") as quotes:
        pass


# Daily quotes job
async def daily_quotes_job(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.context["id"]
    quote = choose_quotes()
    await context.bot.send_message(chat_id=chat_id, text=quote)


# Message Handler
async def music_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    parsed_message = message.strip()
    if "آهنگ" in parsed_message:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="لطفا انتخاب کن مودت چطوره تا برات یه آهنگ بفرستم ...",
            reply_to_message_id=update.effective_message.id,
        )


# based on inline keyboard output
async def music_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio_path = "~/Documnets"
    with open(audio_path, "rb") as audio_file:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=audio_file,
            reply_to_message_id=update.effective_message.id,
        )


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    # Add command handlers
    bot.add_handler(CommandHandler("start", start_handler))
    bot.add_handler(CommandHandler("dice", dice_handler))
    bot.add_handler(CommandHandler("help", help_handler))

    # Add message handlers
    bot.add_handler(MessageHandler(filters.TEXT, music_message_handler))

    # Add job queue
    job_queue = bot.job_queue
    job_queue.run_daily(daily_quotes_job, time(hour=8, minute=0, second=0))

    # Start bot
    bot.run_polling()
