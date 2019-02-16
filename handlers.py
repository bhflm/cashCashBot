from consts import *

def valid_atm(msg):
    atm = msg.capitalize()
    return atm == LINK or atm == BANELCO


def set_handlers(bot):

    @bot.message_handler(commands=['start'])

    @bot.message_handler(func = lambda msg: msg.text is not None)
    def at_answer(message):
        if (valid_atm(message.text)):
            bot.reply_to(message, 'Great! Gonna look for the three nearest {} ATMs around.'.format(message.text.capitalize()))
        else:
            bot.reply_to(message, 'Sorry, i could not understand "{}". Try either asking for a Link or Banelco ATM.'.format(message.text))
