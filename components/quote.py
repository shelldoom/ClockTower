from random import choice
from telegram import Update
from telegram.ext import CallbackContext, Filters, CommandHandler

QUOTES = [
    '<i>What is better - to be born good, or to overcome your evil nature through great effort?</i> --<b>Paarthurnax</b>',   
]

def get_quote() -> str:
    return choice(QUOTES)

def quote_callback(update:Update, context:CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=choice(QUOTES),
        parse_mode='HTML'
    )
quote_handler = CommandHandler(["quote", "quotes"], quote_callback, filters=~Filters.update.edited_message)

