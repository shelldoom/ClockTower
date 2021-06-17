from telegram.ext import Updater, Dispatcher
from config import botToken
import setup

def main():
    updater: Updater = Updater(token=botToken)
    dispatcher: Dispatcher = updater.dispatcher

    setup.setup(dispatcher)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()