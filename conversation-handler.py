import logging
from typing import Final
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)


BOT_TOKEN: Final = "token"
BOT_USERNAME: Final = "@astrologieMobinaBot"

logging.basicConfig(
    format="%(levelname)s - (%(asctime)s) - %(message)s - (Line: %(lineno)d) - [%(filename)s]",
    datefmt="%H:%M:%S",
    encoding="utf-8",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

TASKS, PHOTO, GIFT, MUSIC = range(4)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("User %s has started the bot ...", update.effective_user.id)
    reply_keyboard = [["Photos", "Music"], ["Gift"]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="سلام مبینا :) تولدت مبارک باشه. چیکار برات انجام بدم؟",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="دوست داری چی برات بفرستم؟",
        ),
        reply_to_message_id=update.effective_message.id,
    )
    return TASKS


# /help handler
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s wants help: /help ...", update.effective_user.id)
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
    logger.info("User %s wants bot to send a dice ...", update.effective_user.id)
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
    logger.info("daily quote has been sent to user")
    job = context.job
    chat_id = job.context["id"]
    quote = choose_quotes()
    await context.bot.send_message(chat_id=chat_id, text=quote)


async def photos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s wants photos and videos ...", update.effective_user.id)
    # Send some photos
    # ...
    document_path = ""
    with open(document_path, "rb") as document_file:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=document_file,
            reply_to_message_id=update.effective_message.id,
        )
    return ConversationHandler.END


async def music_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s wants a music ...", update.effective_user.id)
    audio_path = ""
    with open(audio_path, "rb") as audio_file:
        await context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=audio_file,
            reply_to_message_id=update.effective_message.id,
        )
    return ConversationHandler.END


async def gift_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s wants to see her gift ...", update.effective_user.id)
    text = "Text of the gift"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )
    return ConversationHandler.END


async def task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s has selected she wants ...", update.effective_user.id)
    user_input = update.effective_message.text
    if user_input == "Photos":
        return PHOTO
    elif user_input == "Gift":
        return GIFT
    elif user_input == "Music":
        return MUSIC


async def skip_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s has skipped the photos ...", update.effective_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="می تونی /skip کنی و برگردی مرحله اول",
        reply_to_message_id=update.effective_message.id,
    )
    return ConversationHandler.END


async def skip_gift_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s has skipped the gift part ...", update.effective_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="می تونی کادوت رو ببینی یا روی /skip بزنی و خارج بشی",
        reply_to_message_id=update.effective_message.id,
    )
    return ConversationHandler.END


async def skip_music_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s has skipped the music part ...", update.effective_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="می تونی /skip کنی و برگردی مرحله اول",
        reply_to_message_id=update.effective_message.id,
    )
    return TASKS


if __name__ == "__main__":
    logger.info("Starting bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("start", start_handler)],
            states={
                TASKS: [
                    MessageHandler(
                        filters.Regex(r"^(Music|Photos|Gift)$"),
                        task_handler,
                    )
                ],
                PHOTO: [
                    MessageHandler(
                        filters.Regex(r"^(Photos)$"),
                        photos_handler,
                    ),
                    CommandHandler("skip", skip_photo_handler),
                ],
                GIFT: [
                    MessageHandler(filters.Regex(r"^(Gift)$"), gift_handler),
                    CommandHandler("skip", skip_gift_handler),
                ],
                MUSIC: [
                    MessageHandler(filters.Regex(r"^(Music)$"), music_handler),
                    CommandHandler("skip", skip_music_handler),
                ],
            },
            fallbacks=[CommandHandler("skip", skip_gift_handler)],
        )
    )

    logger.info("Start polling...")
    app.run_polling()
