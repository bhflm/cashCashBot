import logging
import telebot
import time
from keys import TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(token=TOKEN)

def valid_atm(msg):
    return msg == 'link' or msg == 'banelco'

@bot.message_handler(commands=['start'])

@bot.message_handler(func = lambda msg: msg.text is not None)
def at_answer(message):
    user_input = message.text.lower()
    if (valid_atm(user_input)):
        bot.reply_to(message, 'Great! Gonna look for the nearests {} around'.format(user_input))
    else:
        bot.reply_to(message, 'Sorry, i could not understand "{}", try either asking for a Link or Banelco ATM.'.format(user_input))


bot.polling()
