from telegram import Update
from telegram.ext import CallbackContext
from logs import logger
import traceback, html, json
from config import channel_token
import os

def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception occurred while handling an update:", exc_info=context.error)
    tb_str = ''.join(traceback.format_exception(None, context.error, context.error.__traceback__))
    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    msg = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_str)}</pre>'
    )
    # os.getenv('username') # Windows
    msg = msg.replace(os.getlogin(), "USERNAME")
    msg = msg.replace(os.getcwd(), ".")
    if len(msg) > 4000:
        print('Sending Error!')
        piece_len = len(msg)//4000
        msgs = [msg[4000*i:4000*(i + 1)] for i in range(0, piece_len)] + [msg[piece_len*4000:]]
        for index, i_msg in enumerate(msgs):
            context.bot.send_message(
                chat_id=channel_token,
                text=f'Page {index}/{len(msgs) - 1}\n\n' + i_msg,
                parse_mode='HTML'
            )
    else:
        context.bot.send_message(
            chat_id=channel_token,
            text=msg,
            parse_mode='HTML'
        )