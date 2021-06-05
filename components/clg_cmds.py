from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram import Update
from config import calendar_url, bulletin_url
from components.messages import LOADING_STICKER, AR_MSG, DC_MSG
import random

# /cal
def cal_callback(update: Update, context: CallbackContext):
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=calendar_url,
    )


cal_handler = CommandHandler(
    ["cal", "calendar", "holiday", "holidays"],
    cal_callback,
    filters=~Filters.update.edited_message,
)

# /bulletin
def bulletin_callback(update: Update, context: CallbackContext):
    tmp_msg = context.bot.sendSticker(chat_id=update.effective_chat.id, sticker=random.choice(LOADING_STICKER))
    context.bot.sendDocument(chat_id=update.effective_chat.id, document=bulletin_url)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=tmp_msg.message_id)


bulletin_handler = CommandHandler(
    ["bulletin"], bulletin_callback, filters=~Filters.update.edited_message
)


# /dc
def hub_callback(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        text=DC_MSG,
    )


hub_handler = CommandHandler(
    ["hub", "hubs", "dezire", "dc"],
    hub_callback,
    filters=~Filters.update.edited_message,
)


# /ar
def ar_callback(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        text=AR_MSG,
    )


ar_handler = CommandHandler(
    ["ar", "acadresources", "academicresources", "res", "resources", "acads"],
    ar_callback,
    filters=~Filters.update.edited_message,
)
