import logging
import telebot
import time
from keys import TOKEN
from consts import LINK,BANELCO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
def valid_atm(msg):
    atm = msg.capitalize()
    return atm == LINK or atm == BANELCO

def main():

    logger = logging.getLogger(__name__)
    bot = telebot.TeleBot(token=TOKEN)

    @bot.message_handler(commands=['start'])

    @bot.message_handler(func = lambda msg: msg.text is not None)
    def at_answer(message):
        if (valid_atm(message.text)):
            bot.reply_to(message, 'Great! Gonna look for the three nearest {} ATMs around.'.format(message.text.capitalize()))
        else:
            bot.reply_to(message, 'Sorry, i could not understand "{}". Try either asking for a Link or Banelco ATM.'.format(message.text))


    bot.polling()


main()
