from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Filters
from PIL import Image
import base64, json, random, requests
from config import imgbb_api_key
from logs import logger
from components.messages import LOADING_STICKER

def uploadImg(img: Image, img_name=None):
    if not img_name:
        img_name = "RAND" + str(random.getrandbits(18))
    api_url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": imgbb_api_key,
        "image": base64.b64encode(img),
        "name": img_name,
        "expiration": 259250,
    }
    r = requests.post(api_url, payload)
    img_url = json.loads(r.text)["data"]["url"]
    return img_url


def imgup_callback(update: Update, context: CallbackContext):
    img_name = " ".join(context.args)
    img_msg = update.effective_message.reply_to_message
    imgs = img_msg.photo
    img_bytes = None
    print(imgs)
    if imgs or len(imgs) > 0:
        img_file = context.bot.get_file(imgs[-1].file_id)
    else:
        try:
            img_file = context.bot.get_file(img_msg.effective_attachment.file_id)
        except AttributeError:
            return
    temp_msg = context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=random.choice(LOADING_STICKER))
    img_bytes = img_file.download_as_bytearray()
    try:
        img_url = uploadImg(img_bytes, img_name)
    except requests.exceptions.ConnectionError:
        logger.info(
            f"Invalid Image: User {update.effective_user.username} tried uploading an invalid img."
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Invalid image format! If not, please send the problem via <code>/feedback</code> command",
            parsemode="HTML",
        
        )
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=temp_msg.message_id)
    del img_bytes
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=temp_msg.message_id)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=img_msg.message_id,
        text=img_url,
    )


imgup_handler = CommandHandler(
    ["imgup", "upimg", "uploadimg", "img"],
    imgup_callback,
    filters=~Filters.update.edited_message,
)