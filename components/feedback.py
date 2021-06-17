from telegram import Update
from telegram.ext import CallbackContext, Filters, CommandHandler
from config import channel_token
import random

THUMBS_UP_STICKERS = ["CAACAgUAAxkBAAIBMGAzoREUmZ-8mqi2CYkzAWrJImU_AAJjAQACNtOwVUwhyujUPAHEHgQ", "CAACAgEAAxkBAAIBMmAzoUHXhGvHjDHHZTeV3A4Lo7_LAAIcAQACuvzyGZHHSbG28gr9HgQ", "CAACAgIAAxkBAAIBM2AzoUQFHIH_6I59LNRn6gLtcrwlAAJ1AAMFzsItu-myAAHWdIpLHgQ"]

feedback_default_txt = '''
Type the feedback after /feedback command.
Example:
<code>/feedback this is an example feedback</code>
'''

# /feedback
def feedback_callback(update: Update, context: CallbackContext):
    feedback_text = ' '.join(context.args)
    
    if feedback_text in [" ", ""]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=feedback_default_txt, parse_mode="HTML")
        return
    
    if len(feedback_text) < 20:
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            reply_to_message_id = update.effective_message.message_id,
            text = "Feedback can't be less than 20 characters. Please enter the feedback just after the /feedback command."
        )
        return
    user_feedback = f"<code>Name = {update.effective_user.full_name}\nUsername = @{update.effective_user.username} \nuser_id = {update.effective_user.id} \nMessage: {feedback_text}</code>"
    context.bot.send_message(
        chat_id=channel_token,
        text=user_feedback,
        parse_mode="HTML"
    )
    tmp_msg = context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=random.choice(THUMBS_UP_STICKERS))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Feedback sended successfully. Thank you for the feedback ^_^")
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=tmp_msg.message_id)
feedback_handler = CommandHandler("feedback", feedback_callback, filters=Filters.chat_type.private)

