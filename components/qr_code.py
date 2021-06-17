from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Filters
from config import qr_collection, imgbb_api_key
import qrcode
from PIL import Image
import io, hashlib, base64, requests, json, datetime

# Set expiration for the api and the db
# db expiration time 2592000
# api expiration time 2592500

QR_MSG = '''
Input: Reply /qr to the message containing the text
Output: Converts and returns in its QR image form

Example:
<code>msg 1:  This is a sample text </code>
<code>msg 2: /qr </code>
Here <code>msg 2</code> is a reply to <code>msg 1</code>.

You can also use <code>/qr</code> instead of <code>/qrcode</code>.
'''

def getImageBytes(img:Image):
    byteIO = io.BytesIO()
    img.save(byteIO, format='PNG')
    byteArr = byteIO.getvalue()
    return byteArr

def getQR(query:str) -> str:
    queryHash = hashlib.sha1(query.encode('utf-8')).hexdigest()
    
    query_in_db = qr_collection.find_one({'_id':f'{queryHash}'}) 
    if query_in_db != None:
        print("Returning a cached response...")
        return query_in_db['url']
        
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(query)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    api_url = "https://api.imgbb.com/1/upload"
    payload = {
            "key": imgbb_api_key,
            "image": base64.b64encode(getImageBytes(img)),
            "name": queryHash,
            "expiration": 2592500,
    }
        
    r = requests.post(api_url, payload)
    qr_url = json.loads(r.text)['data']['url']

    time = datetime.datetime.utcnow()
    qr_collection.ensure_index("time", expireAfterSeconds= 1296000)
    qr_collection.insert_one({'_id':f'{queryHash}', 'url':f'{qr_url}', 'time':time})
    return qr_url


def qr_callback(update:Update, context:CallbackContext):
    userQuery = ' '.join(context.args)
    parentMsg = update.effective_message.reply_to_message
    if userQuery in ['', ' ']:
        if parentMsg == None:
            context.bot.send_message(chat_id=update.effective_chat.id, text=QR_MSG, parse_mode="HTML")
            return
        userQuery = parentMsg.text
        
    qr = getQR(userQuery)
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=qr
    )
qr_handler = CommandHandler(["qrcode", "qr"], qr_callback, filters=~Filters.update.edited_message, run_async=True)

