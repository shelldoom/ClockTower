from telegram.ext import Updater, Dispatcher
from config import botToken
import setup

updater: Updater = Updater(token=botToken)
dispatcher: Dispatcher = updater.dispatcher

setup.setup(dispatcher)

updater.start_polling()
