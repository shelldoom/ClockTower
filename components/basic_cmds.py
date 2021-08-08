from telegram.ext import CallbackContext, Filters, CommandHandler, MessageHandler
from telegram import Update
from random import choice
from .messages import HELP_MSG, DONATE_MSG, START_STICKER, GRP_START_MSG


# /start
def start_callback(update: Update, context: CallbackContext):
    if update.effective_chat.type == "group":
        context.bot.send_message(chat_id= update.effective_chat.id, text=GRP_START_MSG, parse_mode="HTML")
        return
    start_msg = f"Hello @{update.effective_user.username}, use /help to get started"
    temp_msg = context.bot.sendSticker(chat_id = update.effective_chat.id, sticker=choice(START_STICKER))
    context.bot.send_message(chat_id= update.effective_chat.id, text=start_msg)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=temp_msg.message_id, timeout=3)
start_handler = CommandHandler(["start"], start_callback, filters=~Filters.update.edited_message)


# /help
def help_callback(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        reply_to_message_id = update.effective_message.message_id,
        text = HELP_MSG,
        parse_mode = "HTML"
    )
help_handler = CommandHandler(["help"], help_callback, filters=~Filters.update.edited_message)


# /donate
def donate_callback(update: Update, context: CallbackContext) -> None:
    context.bot.sendMessage(
        chat_id = update.effective_chat.id,
        text = DONATE_MSG,
        disable_web_page_preview=True
    )
donate_handler = CommandHandler(["donate"], donate_callback)


# /ob
def ob_callback(update: Update, context: CallbackContext) -> None:
    parentMsg = update.effective_message.reply_to_message
    # if parentMsg == None:
        # return

    if not context.bot.can_read_all_group_messages and parentMsg == None:
        context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text="For this feature to work, please grant me the access to messages!"
        )
        return
    
    if parentMsg != None:
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            reply_to_message_id = parentMsg.message_id,
            text = "Ob"
        )
ob_handler = CommandHandler("ob", ob_callback, filters=Filters.chat_type.group & ~Filters.update.edited_message)

def echo_callback(update: Update, context: CallbackContext) -> None:
    userQuery = ' '.join(context.args)
    parentMsg = update.effective_message.reply_to_message
    if userQuery in {"", " "}:
        return
    if parentMsg is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=parentMsg.message_id, text=userQuery)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=userQuery)
echo_handler = CommandHandler("echo", echo_callback, filters=~Filters.update.edited_message)

def new_mem_callback(update: Update, context: CallbackContext) -> None:
    members = update.message.new_chat_members
    members = ['@'+m.username for m in members]
    update.message.reply_text(f"Welcome {','.join(members)}!")

new_mem_handler = MessageHandler(Filters.status_update.new_chat_members, new_mem_callback)

def bad_cmd(update: Update, context: CallbackContext) -> None:
    raise ValueError("This is a sample test error!")

badCmd_Handler = CommandHandler(
    "error_test_test", bad_cmd, filters=~Filters.update.edited_message
)

