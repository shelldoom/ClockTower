import logging
from telegram import Update
from telegram.ext import Updater, CallbackContext, Dispatcher
from config import botToken
import setup

updater = Updater(token=botToken)
dispatcher = updater.dispatcher

setup.setup(dispatcher)

updater.start_polling()
