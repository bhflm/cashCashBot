import logging
import telebot
import time
from handlers import *
from keys import TOKEN
from consts import LINK,BANELCO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def main():

    logger = logging.getLogger(__name__)
    bot = telebot.TeleBot(token=TOKEN)
    set_handlers(bot)

    bot.polling()


main()
