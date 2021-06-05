from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Filters
from config import mongo_client, db_name
import requests, json, hashlib, datetime

ud_collection = mongo_client[db_name]["ud"]


def get_word_definition(query: str) -> tuple:
    queryHash = hashlib.sha1(query.encode("utf-8")).hexdigest()
    query_in_db = ud_collection.find_one({"_id": f"{queryHash}"})
    if query_in_db:
        print("Returning a cached response...")
        return query_in_db["definition"], query_in_db["example"]

    r = requests.get(f"https://api.urbandictionary.com/v0/define?term={query}")
    word_data = json.loads(r.text)
    r.close()
    if word_data["list"] == []:
        return None, None
    definition, example = (
        word_data["list"][0]["definition"],
        word_data["list"][0]["example"],
    )

    time = datetime.datetime.utcnow()
    ud_collection.ensure_index("time", expireAfterSeconds=604800)
    ud_collection.insert_one(
        {
            "_id": f"{queryHash}",
            "definition": f"{definition}",
            "example": f"{example}",
            "time": time,
        }
    )
    return definition, example


def ud_callback(update: Update, context: CallbackContext) -> None:
    userQuery = " ".join(context.args)
    definition, example = get_word_definition(userQuery)
    if definition is None:
        return
    example = example.replace("<", "&lt;").replace(">", "&gt;")
    textMsg = f"<b>{userQuery}</b> \n\n {definition} \n\n <i>{example}</i>"

    context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        text=textMsg,
        parse_mode="HTML",
    )


urbanHandler = CommandHandler(
    ["ud", "urbandictionary"], ud_callback, filters=~Filters.update.edited_message
)
