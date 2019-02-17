import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from keys import TOKEN
from consts import BANELCO,LINK


#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class ATMSearcher():
    def __init__(self):
        self.updater = Updater(token=TOKEN)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.location, self.get_user_location))

    def start(self, bot, update):
        logging.info('started bot')
        welcome_message = "Welcome to cashCash! in order to work properly, i'd need to ask you for permissions over your location."
        bot.send_message(chat_id=update.message.chat_id, text=welcome_message)

        keyboard = telegram.KeyboardButton("Confirm", request_contact=None, request_location=True)
        reply_markup = telegram.ReplyKeyboardMarkup([[keyboard]])
        bot.send_message(chat_id=update.message.chat_id,
                         text = 'Would like to search for Link or Banelco closest ATMs?',
                         reply_markup=reply_markup)

    def get_user_location(self, bot, update):
        user_coords = { 'lat' : update.message.location.latitude, 'long' : update.message.location.longitude }
        print(user_coords['lat'],user_coords['long'])

    def read_csv(self):
        pass

    def load_KDTree(self):
        pass

    def load_dictionary(self):
        pass

    def query_nearest_atms(self, location, query_number, offset):
        hits = self.trees[link].query(query_number)[1][:offset]
        return hits

    def is_a_valid_atm(self, id):
        pass

    def get_nearest_atms(self, location, number=3, query_number=10):

        nearest_valid_atms = []
        offset = 0

        atms = self.query_nearest_atms(location)

        while len(nearest_valid_atms) < 3:
            atms = self.query_nearest_atms(location, number, offset)
            for atm in atms:
                if self.is_a_valid_atm(atm):
                    nearest_valid_atms.append(atm)
            offset = query_number
            query_number *= 2

        return nearest_valid_atms[:3]



    def start(self):
        self.updater.start_polling()
