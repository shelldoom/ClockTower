import configparser
import pymongo

botConfig = configparser.ConfigParser()
botConfig.read("./config/config.ini")
botToken = botConfig["BOT"]["TOKEN"]
feedbackToken = botConfig["FEEDBACK"]["TOKEN"]

pwd = botConfig["MONGO"]["PWD"]
user = botConfig["MONGO"]["USER"]
db_name = botConfig["MONGO"]["DB_NAME"]
imgbb_api_key = botConfig["IMGBB_API"]["TOKEN"]
mongo_url = botConfig["MONGO"]["URL"]

mongo_client = pymongo.MongoClient(
    mongo_url.format(user=user, db_name=db_name, pwd=pwd)
)

qr_collection = mongo_client[db_name]["qr_collection"]

calendar_url = botConfig["COLLEGE"]["CAL_URL"]
bulletin_url = botConfig["COLLEGE"]["BULLETIN_URL"]
