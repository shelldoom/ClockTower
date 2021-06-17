import json
from telegram import Update
from telegram.ext import CallbackContext, Filters, CommandHandler
import requests

# QUOTES = [
#     '<i>What is better - to be born good, or to overcome your evil nature through great effort?</i> --<b>Paarthurnax</b>',
#     ''
# ]


def get_quote() -> str:
    r = requests.get('https://api.quotable.io/random')
    r = json.loads(r.text)
    return f"<i>{r['content']}</i> --<b>{r['author']}</b>"

def quote_callback(update:Update, context:CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_quote(),
        parse_mode='HTML'
    )
quote_handler = CommandHandler(["quote", "quotes"], quote_callback, filters=~Filters.update.edited_message)

